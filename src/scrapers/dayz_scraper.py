from bs4 import BeautifulSoup
from src.scrapers.abstract_scraper import make_soup, write_datafile
from selenium import webdriver

WEBSITE = "https://dayz.com/search?rowsPerPage=5"
BASESITE = "https://dayz.com"
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
    words = date.replace(",", "").replace(":", "").split(" ")
    if len(words) > 3:
        if len(words[1]) == 1:
            words[1] = "0" + words[1]
        new_date = words[2] + MONTHS[words[0].lower()] + words[1] + words[3]
    else:
        new_date = "N/A"

    return new_date


def get_articles(articles, soup, driver):

    while True:
        pagination = driver.find_element_by_class_name("paginate__item--arrow-right")

        for post in soup.find_all("div", {"class": "content"}):
            articles.append(post)

        if "paginate__item--arrow-disabled" not in pagination.get_attribute("class"):
            pagination.find_element_by_class_name("butn").click()
            soup = BeautifulSoup(driver.page_source, "html.parser")
        else:
            break

    return articles


def scrape():

    # Setup selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
    driver.get(WEBSITE)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = []
    data = []

    # Get each individual entry
    articles = get_articles(articles, soup, driver)
    for article in articles:
        link = BASESITE + article.find("a").get("href")
        date = article.find("time").text.strip().replace('-', '') + "0000"
        title = article.find("h1").text.strip()

        data.append({"id": conform_date(date), "title": title, "link": link})

    return write_datafile(data, FILENAME)
