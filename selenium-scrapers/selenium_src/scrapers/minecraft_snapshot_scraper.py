from selenium_src.lib.model.post import Post
from selenium_src.lib.model.source import Source
from selenium_src.scrapers.abstract_scraper import get_driver, long_months, get_page

import re

SOURCE_CODE = "minecraft_snapshot"
WEBSITE = "https://feedback.minecraft.net/hc/en-us/sections/360002267532-Snapshot-Information-and-Changelogs"
PROFILE_IMAGE = 'https://theme.zdassets.com/theme_assets/2155033/e31e57a9e728439e7b4e595ac626e51fdd648f40.png'
ALT_IMAGE = 'https://theme.zdassets.com/theme_assets/2155033/972abdec3b7c5285812aa684bc5b81ca077805ee.png'
BASE_SITE = "https://feedback.minecraft.net"
FILENAME = "../resources/data/minecraft_snap.txt"


def get_source():
    name = "Minecraft Snapshot"
    description = 'Minecraft snapchot blog'
    return Source(SOURCE_CODE, name, description, PROFILE_IMAGE, ALT_IMAGE, None)


def get_articles(articles, driver):
    page = 1

    while True:
        pagination = driver.find_elements_by_class_name("pagination-next")
        links = driver.find_elements_by_class_name("article-list-link")
        for link in links:
            articles.append(link.get_attribute("href"))

        if pagination is not None and len(pagination) > 0:
            page = page + 1
            driver = get_page(driver, f"{WEBSITE}?page={page}")

        else:
            break

    return articles


def get_date(driver):
    date = None
    body = driver.find_element_by_class_name("article-body")
    candidates = body.find_elements_by_xpath(".//*")

    for candidate in candidates[:10]:
        text = candidate.text.strip()
        words = re.split(r"\s+", text)

        if len(words) >= 3 and re.search(r"\d{1,2}", words[0]) and re.search(r"\d{4}", words[2]):
            if len(words[0]) == 1:
                words[0] = "0" + words[0]

            date = words[2] + long_months[words[1].lower()] + words[0]
            date = re.sub(r"\D", "", date) + "0000"
            break

    return date


def scrape():
    driver = get_driver()
    driver = get_page(driver, WEBSITE)
    articles = []
    data = []

    # Get each individual entry
    articles = get_articles(articles, driver)
    print(f"Found {len(articles)} entries")

    for article in articles:
        driver = get_page(driver, article)

        link = article
        date = get_date(driver)
        title = driver.find_element_by_class_name("article-title").text

        if date is None:
            continue

        data.append(Post(None, date, title, link, ALT_IMAGE, PROFILE_IMAGE, SOURCE_CODE, None))

        if len(data) % 10 == 0:
            print(f"Scraped {len(data)} entries.")

    return data
