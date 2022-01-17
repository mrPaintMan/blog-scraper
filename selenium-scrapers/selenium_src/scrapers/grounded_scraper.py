from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium_src.lib.model.post import Post
from selenium_src.lib.model.source import Source

from selenium_src.scrapers.abstract_scraper import get_driver, long_months, get_page, remove_dups, now

SOURCE_CODE = "grounded"
WEBSITE = "https://grounded.obsidian.net/"
PROFILE_IMAGE = "https://pbs.twimg.com/profile_images/1228034225896488960/nLHFQkdS_400x400.jpg"
AlT_IMAGE = "https://pbs.twimg.com/profile_banners/1198662953467174912/1605057069/1500x500"
FILENAME = "../resources/data/grounded.txt"


def get_source():
    name = "Grounded"
    description = "Grounded the game by Obsidian Entertainment"
    return Source(SOURCE_CODE, name, description, PROFILE_IMAGE, AlT_IMAGE, None)


def conform_date(date):
    refined_date = date.split("• ")[1]
    words = refined_date.replace(",", "").split(" ")
    if len(words) >= 3:
        if len(words[1]) == 1:
            words[1] = "0" + words[1]
        new_date = words[2] + long_months[words[0].lower()] + words[1] + "0000"
    else:
        new_date = "N/A"

    return new_date


def scrape():
    driver = get_driver()
    driver = get_page(driver, WEBSITE)
    data = []

    xpath_to_pag = "/html/body/div/main/div/section[2]/div/div[1]/div[2][@class='pagination']/button"

    # Wait for page to load
    WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, xpath_to_pag)))

    # Click the "load more" button until it disappears
    while True:
        pagination = driver.find_element_by_xpath(xpath_to_pag)

        pagination.click()
        try:
            WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, xpath_to_pag)))

        except BaseException:
            break

    for article in driver.find_elements_by_class_name("news-card--home"):
        link = article.find_element_by_class_name("news-card__body").get_attribute("data-href")
        image = article.find_element_by_class_name("news-card__image").get_attribute("src")
        date = article.find_element_by_class_name("news-card__date").text.strip()
        title = article.find_element(By.TAG_NAME, "h2").text.strip()

        if len(title) > 64:
            title = title[0:60] + "..."

        data.append(Post(None, conform_date(date), title, link, image, AlT_IMAGE, SOURCE_CODE, None))

        if len(data) % 25 == 0:
            print(now() + f"Processed {len(data)} posts")

    return remove_dups(data)
