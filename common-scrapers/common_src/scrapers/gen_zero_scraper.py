import re
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


def get_better_image(original, date):
    base_link = "https://generationzero.com/content/2-blog/" + date + "-"
    name_arr = original.split("/")
    name_arr.reverse()
    file_name = name_arr[0]
    resource = name_arr[1] + "/"

    if file_name.__contains__("-"):
        return base_link + resource + re.sub(r"-.*\.", ".", file_name)

    else:
        return base_link + resource + file_name


def scrape():
    soup = make_soup(WEBSITE)
    data = []
    for post in soup.find_all("div", {"class": "post-content"}):
        date = post.find("p").text.strip().replace('-', '')
        title = post.find("h4").text.strip()
        link = post.find("a").get("href")
        original_image = post.findAll("img")[0].get("src")

        image = None if not original_image else get_better_image(original_image, date)

        data.append(Post(None, date + "0000", title, link, image, None, SOURCE_CODE, None))

    return data
