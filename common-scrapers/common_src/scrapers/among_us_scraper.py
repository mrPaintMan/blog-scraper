from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup, now, remove_dups

SOURCE_CODE = "among_us"
WEBSITE = "https://innersloth.itch.io/among-us/devlog"
ALT_IMAGE = 'https://img.itch.zone/aW1nLzE3MzAzNTQucG5n/original/6ZlfCk.png'
FILENAME = "../resources/data/among_us.txt"


def get_source():
    name = "Among Us"
    description = 'The booming murder multiplayer game everyone is talking about!'
    profile_image = 'https://img.itch.zone/aW1hZ2UyL3VzZXIvMTg5NzU5LzE3MzAzNTcucG5n/original/7quYQx.png'
    return Source(SOURCE_CODE, name, description, profile_image, ALT_IMAGE, None)


def scrape():
    soup = make_soup(WEBSITE)
    data = []

    for post in soup.find("ul", {"class": "blog_post_list_widget"}):

        date = post.find("abbr").get("title").replace("-", "").replace(" ", "").replace(":", "")[0:-2]
        title = post.find("a", {"class": "title"}).text.strip()
        link = post.find("a", {"class": "title"}).get("href")
        alt_image = ALT_IMAGE
        image_element = post.find("img", {"class": "post_image"})
        image = image_element.get("src").replace(" ", "%20") if image_element else ALT_IMAGE

        data.append(Post(None, date, title, link, image, alt_image, SOURCE_CODE, None))

        if len(data) % 25 == 0:
            print(now() + f"Processed {len(data)} posts")

    return data
