from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from common_src.lib.model.post import Post
from common_src.lib.model.source import Source

SOURCE_CODE = "dayz"
WEBSITE = "https://dayz.com/search?rowsPerPage=5"
BASESITE = "https://dayz.com"
FILENAME = "../resources/data/dayz.txt"
XPATH_TO_FIRST_POST = "//div[1][@class='content']//a[@class='link']"
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


def get_source():
    description = 'Dayz blog'
    profile_image = 'https://dayz.com/90ee40a3203a24fee8ffa8d42cc6ab5a-180.png'
    alt_image = 'https://dayz.com/b53749822130d9ff884b711e0d721ed7-1920.jpg'
    return Source(SOURCE_CODE, description, profile_image, alt_image, None)


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
        old_name = driver.find_element_by_xpath(XPATH_TO_FIRST_POST).text

        for post in soup.find_all("div", {"class": "content"}):
            articles.append(post)

        if "paginate__item--arrow-disabled" not in pagination.get_attribute("class"):

            pagination.find_element_by_class_name("butn").click()
            WebDriverWait(driver, 5).until_not(
                ec.text_to_be_present_in_element(
                    (By.XPATH, XPATH_TO_FIRST_POST),
                    old_name
                )
            )

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
        link = BASESITE + article.find(lambda tag: tag.name == 'a' and tag.get('class') == ['link']).get("href")
        date = article.find("time").text.strip().replace('-', '') + "0000"
        title = article.find("h1").text.strip()

        data.append(Post(None, conform_date(date), title, link, None, None, SOURCE_CODE, None))

    return data
