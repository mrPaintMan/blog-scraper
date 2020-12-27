from selenium_src.lib.model.post import Post
from selenium_src.lib.model.source import Source
from selenium_src.scrapers.abstract_scraper import get_driver, get_page

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
            href = re.split(r"\d{12}", link.get_attribute("href"))[1].lower()
            modified_href = href.replace("-minecraft-", "").replace("java-", "").replace("edition-", "")

            if re.search("-pre-", modified_href):
                modified_href = modified_href.replace("snapshot-", "")

                if re.search(r"\d$", modified_href):
                    modified_href = modified_href[0:-1] + "1"

            # Attempt to remove junk chars ('-' for instance)
            if re.search(r"[^a-zA-Z0-9]$", modified_href):
                modified_href = modified_href[0:-1]

            # Replace the last word-char in the link with 'a'
            if re.search(r"\d[a-zA-Z]$", modified_href):
                modified_href = modified_href[0:-1] + "a"

            # These articles contain better images and date information
            articles.append("https://www.minecraft.net/en-us/article/minecraft-" + modified_href)

        if pagination is not None and len(pagination) > 0:
            page = page + 1
            driver = get_page(driver, f"{WEBSITE}?page={page}")

        else:
            break

    return articles


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

        # All links are unfortunately not guaranteed to work...
        if driver.title == "404 | Minecraft":
            continue

        link = article
        date_parts = driver.find_element_by_class_name("pubDate").text.split('/')
        date = date_parts[2] + date_parts[0] + date_parts[1] + "0000"
        title = driver.find_element_by_xpath('//*[@id="main-content"]/div[3]/div[1]/div/div/div/h1').text
        image = driver.find_element_by_class_name("article-head__image").get_attribute("src")
        image = image + ".transform/minecraft-image-large/image.jpg"

        if date is None:
            continue

        data.append(Post(None, date, title, link, image, ALT_IMAGE, SOURCE_CODE, None))

        if len(data) % 10 == 0:
            print(f"Scraped {len(data)} entries.")

    return data
