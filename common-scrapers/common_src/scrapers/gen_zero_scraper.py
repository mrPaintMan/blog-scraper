from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup

SOURCE_CODE = "gen_zero"
WEBSITE = "https://generationzero.com/en/blog"
FILENAME = "../resources/data/gen_zero.txt"


def get_source():
    description = 'Official Generation Zero blog'
    profile_image = 'https://generationzero.com/thumbs/home/toplogo-300x257.png'
    alt_image = 'https://generationzero.com/content/1-home/hunter-version2.jpg'
    return Source(SOURCE_CODE, description, profile_image, alt_image, None)


def scrape():
    soup = make_soup(WEBSITE)
    data = []
    for post in soup.find_all("div", {"class": "post-content"}):
        link = post.find("a").get("href")
        date = post.find("p").text.strip().replace('-', '') + "0000"
        title = post.find("h4").text.strip()

        data.append(Post(None, date, title, link, None, None, SOURCE_CODE, None))

    return data
