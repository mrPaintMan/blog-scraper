from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium_src.lib.model.post import Post
from selenium_src.lib.model.source import Source

from selenium_src.scrapers.abstract_scraper import get_driver, short_months, get_page, remove_dups, now

SOURCE_CODE = "dayz"
WEBSITE = "https://dayz.com/search?rowsPerPage=5"
BASESITE = "https://dayz.com"
PROFILE_IMAGE = "https://dayz.com/90ee40a3203a24fee8ffa8d42cc6ab5a-180.png"
AlT_IMAGE = "https://dayz.com/b53749822130d9ff884b711e0d721ed7-1920.jpg"
FILENAME = "../resources/data/dayz.txt"
XPATH_TO_FIRST_POST = "//div[1][@class='content']//a[@class='link']"


def get_source():
    name = "Dayz"
    description = "Dayz blog"
    return Source(SOURCE_CODE, name, description, PROFILE_IMAGE, AlT_IMAGE, None)


def conform_date(date):
    words = date.replace(",", "").replace(":", "").split(" ")
    if len(words) > 3:
        if len(words[1]) == 1:
            words[1] = "0" + words[1]
        new_date = words[2] + short_months[words[0].lower()] + words[1] + words[3]
    else:
        new_date = "N/A"

    return new_date


def scrape():
    driver = get_driver()
    driver = get_page(driver, WEBSITE)
    data = []

    # Iterate through the paginated list of articles
    # And get every article link etc
    while True:
        pagination = driver.find_element_by_class_name("paginate__item--arrow-right")
        old_name = driver.find_element_by_xpath(XPATH_TO_FIRST_POST).text

        for article in driver.find_elements_by_class_name("content"):
            link = article.find_element(By.TAG_NAME, "h1").find_element_by_xpath("..").get_attribute("href")
            image = BASESITE + article\
                .find_element_by_xpath("../..")\
                .find_element_by_class_name("thumb")\
                .get_attribute("data-src")
            date = article.find_element(By.TAG_NAME, "time").text.strip().replace('-', '') + "0000"
            title = article.find_element(By.TAG_NAME, "h1").text.strip()

            if image == "https://dayz.com/img/placeholder-300.jpg":
                image = PROFILE_IMAGE

            data.append(Post(None, conform_date(date), title, link, image, AlT_IMAGE, SOURCE_CODE, None))

            if len(data) % 20 == 0:
                print(now() + f"Processed {len(data)} posts")

        if "paginate__item--arrow-disabled" not in pagination.get_attribute("class"):
            pagination.find_element_by_class_name("butn").click()
            WebDriverWait(driver, 5).until_not(
                ec.text_to_be_present_in_element(
                    (By.XPATH, XPATH_TO_FIRST_POST),
                    old_name
                )
            )

        else:
            break

    return data
