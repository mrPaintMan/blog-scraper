from src.scrapers.abstract_scraper import make_soup, make_local_soup, write_datafile

WEBSITE = "https://generationzero.com/en/blog"
FILENAME = "../resources/data/gen_zero.txt"
INPUT_FILE = "../resources/input_files/gen_zero.html"


def scrape(use_web):

    soup = make_soup(WEBSITE) if use_web else make_local_soup()
    data = []
    for post in soup.find_all("div", {"class": "post-content"}):

        link = post.find("a").get("href")
        date = post.find("p").text.strip().replace('-', '') + "0000"
        title = post.find("h4").text.strip()

        data.append({"id": date, "title": title, "link": link})

    return write_datafile(data, FILENAME)
