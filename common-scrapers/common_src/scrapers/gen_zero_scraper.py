from datetime import datetime

from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup, now, remove_dups

SOURCE_CODE = "gen_zero"
WEBSITE = "https://generationzero.com/en/blog"
ALT_IMAGE = 'https://generationzero.com/content/1-home/hunter-version2.jpg'
FILENAME = "../resources/data/gen_zero.txt"


def get_source():
    name = "Generation Zero"
    description = 'Official Generation Zero blog'
    profile_image = 'https://generationzero.com/content/leftlogo.png'
    return Source(SOURCE_CODE, name, description, profile_image, ALT_IMAGE, None)


def get_image(link):
    soup = make_soup(link)
    content = soup.find("div", {"class": "post-content"})
    image = content.find("img")

    if image:
        return image.get("src")

    else:
        return ALT_IMAGE


def scrape():
    soup = make_soup(WEBSITE)
    data = []

    for post in soup.find_all("div", {"class": "post-content"}):
        date = post.find("p").text.strip().replace('-', '')
        title = post.find("h4").text.strip()
        link = post.find("a").get("href")
        alt_image = post.findAll("img")[0].get("src")
        image = get_image(link)

        data.append(Post(None, date + "0000", title, link, image, alt_image, SOURCE_CODE, None))

        if len(data) % 25 == 0:
            print(now() + f"Processed {len(data)} posts")

    return remove_dups(data)
