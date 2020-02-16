from common_src.lib.model.post import Post
from common_src.scrapers.abstract_scraper import make_soup

SOURCE_CODE = "gen_zero"
WEBSITE = "https://generationzero.com/en/blog"
FILENAME = "../resources/data/gen_zero.txt"


def scrape():

    soup = make_soup(WEBSITE)
    data = []
    for post in soup.find_all("div", {"class": "post-content"}):

        link = post.find("a").get("href")
        date = post.find("p").text.strip().replace('-', '') + "0000"
        title = post.find("h4").text.strip()

        data.append(Post(None, date, title, link, SOURCE_CODE, None))

    return data
