from src.scrapers.abstract_scraper import make_soup, write_datafile, make_local_soup
import re

WEBSITE = "https://feedback.minecraft.net/hc/en-us/sections/360002267532-Snapshot-Information-and-Changelogs"
BASE_SITE = "https://feedback.minecraft.net"
FILENAME = "../resources/data/minecraft_snap.txt"


def scrape(use_web):
    soup = make_soup(WEBSITE) if use_web else make_local_soup()
    articles = []
    data = []

    # Get each individual entry
    while True:
        pagination = soup.find("li", {"class": "pagination-next"})
        posts = soup.find("ul", {"class": "article-list"})
        for post in posts.find_all("li"):
            articles.append(BASE_SITE + post.find("a").get("href"))

        if pagination is not None:
            soup = make_soup(BASE_SITE + pagination.find("a").get("href")) if use_web else make_local_soup()
        else:
            break

    # Get entry data
    for article in articles:
        blog_soup = make_soup(article)

        link = article
        date = blog_soup.find("div", {"class": "article-body"}).findChild().text.strip()
        title = blog_soup.find("h1", {"class": "article-title"}).text.strip()

        if date == "":
            print("date was empty")
            date = blog_soup.find("div", {"class": "article-body"})\
                .findChild()\
                .find_next_sibling()\
                .text\
                .strip()
            print(date + "***")

        print({"id": date, "title": title, "link": link})
        data.append({"id": date, "title": title, "link": link})

    '''
    link = post.find("a").get("href")
    title = post.find("a").text
    date = get_date(title)
    data.append({"id": date, "title": title, "link": link})

    return write_datafile(data, FILENAME)
        
    '''
    return write_datafile(data, FILENAME)
