from src.scrapers.abstract_scraper import make_soup, write_datafile
from selenium import webdriver

WEBSITE = "https://dayz.com/search"
FILENAME = "../resources/data/dayz.txt"
MONTHS = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12"
}


def conform_date(date):
    words = date.replace(",", "").replace(":","").split(" ")
    if len(words) > 3:
        if len(words[1]) == 1:
            words[1] = "0" + words[1]
        new_date = words[2] + MONTHS[words[0]] + words[1] + words[3]
    else:
        new_date = "N/A"

    return new_date


def get_articles(articles, soup):
    # Setup selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
    driver.get(WEBSITE)

    while True:
        pagination = soup.find(lambda tag: tag.name == "i" and tag["class"] == ["iconmoon-pagination-right"])
        posts = soup.find("div", {"class": "vfg-grid-item"})
        for post in posts.find_all("div", {"class": "content"}):
            articles.append(post)

        driver.execute_script("arguments[0].click();", pagination)
        if pagination is not None:
            soup = make_soup(pagination.find("a").get("href"))
        else:
            break

    return articles


def scrape():
    soup = make_soup(WEBSITE)
    articles = []
    data = []

    # Get each individual entry
    articles = get_articles(articles, soup)
    for article in articles:
        link = article.find("a").get("href")
        date = article.find("time").text.strip().replace('-', '') + "0000"
        title = article.find("h1").text.strip()

        data.append({"id": conform_date(date), "title": title, "link": link})

    return write_datafile(data, FILENAME)
