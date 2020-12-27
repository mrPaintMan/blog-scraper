from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup

SOURCE_CODE = "windbound"
WEBSITE = "https://windboundgame.com/news"
ALT_IMAGE = 'https://2ffad809f2275eb5.azureedge.net/media/Windbound/Gallery/windbound-screenshot-3-1024w.jpg'
FILENAME = "../resources/data/windbound.txt"


def get_source():
    name = "Windbound"
    description = 'The Windbound development blog'
    profile_image = 'https://pbs.twimg.com/profile_images/1244576569881960453/LtsDRVRs_reasonably_small.png'
    return Source(SOURCE_CODE, name, description, profile_image, ALT_IMAGE, None)


def get_date(date_string):
    date_parts = date_string.split('/')
    return date_parts[2] + date_parts[1] + date_parts[0] + "0000"


def scrape():
    soup = make_soup(WEBSITE)
    base_site = "https://windboundgame.com"
    data = []

    for post in soup.find_all("div", {"class": "card--news"}):
        date = get_date(post.find("p").text.strip())
        title = post.find("h3").text.strip()
        link = base_site + post.find("a").get("href")
        alt_image = ALT_IMAGE
        image = base_site + post.findAll("img")[0].get("src").replace(" ", "%20")

        data.append(Post(None, date, title, link, image, alt_image, SOURCE_CODE, None))

    return data
