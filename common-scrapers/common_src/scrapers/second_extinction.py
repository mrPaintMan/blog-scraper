from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup, remove_date_dups, now

SOURCE_CODE = "second_extinction"
WEBSITE = "https://www.secondextinctiongame.com/news"
ALT_IMAGE = 'https://www.secondextinctiongame.com/static/242486b363d867dc483deb6d7038dde1/d8255/se_screenshot_5.jpg'
FILENAME = "../resources/data/second_extinction.txt"


def get_source():
    name = "Second Extinction"
    description = 'Second Extinction is a first person shooter game where earth has been invaded by mutated dinosaurs.'
    profile_image = 'https://www.secondextinctiongame.com/static/logo-0d52f8575a251eff8ebd6e2d6bd6c51b.png'
    return Source(SOURCE_CODE, name, description, profile_image, ALT_IMAGE, None)


def scrape():
    soup = make_soup(WEBSITE)
    base_site = "https://www.secondextinctiongame.com"
    data = []

    for post in soup.findAll("article", {"class": "cgYILD"}):

        date = post.find("time").text.replace("-", "") + "0000"
        title = post.find("h3").text.strip()
        link = base_site + post.find("a").get("href")
        alt_image = ALT_IMAGE
        image = base_site + post.find("picture").find("img").get("src").replace(" ", "%20")

        data.append(Post(None, date, title, link, image, alt_image, SOURCE_CODE, None))

        if len(data) % 25 == 0:
            print(now() + f"Processed {len(data)} posts")

    return remove_date_dups(data)
