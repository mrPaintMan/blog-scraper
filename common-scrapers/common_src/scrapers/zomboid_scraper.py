from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup, MONTHS, remove_dups, now

SOURCE_CODE = "zomboid"
WEBSITE = "https://projectzomboid.com/blog/news/"
ALT_IMAGE = 'https://projectzomboid.com/blog/content/uploads/2020/02/z-crojpg.jpg'
FILENAME = "../resources/data/zomboid.txt"


def get_source():
    name = "Project Zomboid"
    description = 'An indie zombie 2D survival game'
    profile_image = 'https://projectzomboid.com/blog/content/themes/rw-project-zomboid/assets/images/logo.png'
    return Source(SOURCE_CODE, name, description, profile_image, ALT_IMAGE, None)


def conform_date(string):
    words = string.split(' ')
    year = words[2]
    month = MONTHS[words[0].lower()]
    day = words[1].replace(',', '')

    if len(day) == 1:
        day = "0" + day

    return year + month + day + "0000"


def get_image(post):
    text_with_image = post.find("div", {"class": "mb-3"}).get("style")
    return text_with_image[text_with_image.index('(') + 1: -2]


def scrape():
    data = []
    current_site = WEBSITE

    while current_site is not None:
        soup = make_soup(current_site)
        container_div = soup.find("div", {"class": "c-latest-news"})

        for post in container_div.find_all("div", {"class": "col-12 mb-5 col-lg-4"}):
            date_string = post.find("span", {"class": "published-date"}).text.strip().replace(',', '')
            date = conform_date(date_string)
            title = post.find("h3").text.strip()
            link = post.find("a").get("href")
            alt_image = ALT_IMAGE
            image = get_image(post)

            data.append(Post(None, date, title, link, image, alt_image, SOURCE_CODE, None))

            if len(data) % 50 == 0:
                print(now() + f"Processed {len(data)} posts")

        next_site_div = soup.find("a", {"class": "next"})

        if next_site_div is not None:
            current_site = next_site_div.get("href")

        else:
            current_site = None

    return remove_dups(data)
