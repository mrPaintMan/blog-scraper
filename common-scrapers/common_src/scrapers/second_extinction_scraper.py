from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup, remove_dups, now

SOURCE_CODE = "second_extinction"
BASESITE = "https://www.secondextinctiongame.com"
WEBSITE = BASESITE + "/news"
MEDIASITE = BASESITE + "/media"
FILENAME = "../resources/data/second_extinction.txt"


def get_source():
    name = "Second Extinction"
    description = 'Second Extinction is a first person shooter game where earth has been invaded by mutated dinosaurs.'
    profile_image = 'https://www.secondextinctiongame.com/static/logo-0d52f8575a251eff8ebd6e2d6bd6c51b.png'
    return Source(SOURCE_CODE, name, description, profile_image, get_alt_image(), None)


def get_alt_image():
    soup = make_soup(MEDIASITE)
    print(BASESITE + soup.findAll("ul")[3].findAll("a", {"title": "Open large image"})[-1].get("href"))
    return BASESITE + soup.findAll("ul")[3].findAll("a", {"title": "Open large image"})[-1].get("href")


def scrape():
    alt_image = get_alt_image()
    soup = make_soup(WEBSITE)

    data = []

    for post in soup.findAll("section")[1].findAll("article"):

        date = post.find("time").text.replace("-", "") + "0000"
        title = post.find("h3").text.strip()
        link = BASESITE + post.find("a").get("href")
        alt_image = alt_image
        image = BASESITE + post.find("picture").find("img").get("src").replace(" ", "%20")

        data.append(Post(None, date, title, link, image, alt_image, SOURCE_CODE, None))

        if len(data) % 25 == 0:
            print(now() + f"Processed {len(data)} posts")

    return remove_dups(data)
