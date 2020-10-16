from common_src.lib.model.post import Post
from common_src.lib.model.source import Source
from common_src.scrapers.abstract_scraper import make_soup, MONTHS

SOURCE_CODE = "no_mans_sky"
WEBSITE = "https://www.nomanssky.com/news/"
ALT_IMAGE = 'https://www.nomanssky.com/wp-content/uploads/2017/02/logo.png'
FILENAME = "../resources/data/no_mans_sky.txt"


def get_source():
    name = "No Man's Sky"
    description = 'Official No Mans Sky blog'
    profile_image = 'https://www.nomanssky.com/wp-content/uploads/2017/02/icon.png'
    return Source(SOURCE_CODE, name, description, profile_image, ALT_IMAGE, None)


def conform_date(string):
    words = string.split(' ')
    year = words[2]
    month = MONTHS[words[0].lower()]
    day = words[1].replace(',', '')

    if len(day) == 1:
        day = "0" + day

    return year + month + day + "0000"


def remove_date_dups(data):
    temp_list = []
    for post in data:
        if post.ext_id not in temp_list:
            temp_list.append(post.ext_id)

        else:
            int_date = int(post.ext_id)
            int_date = int_date + 1
            post.ext_id = str(int_date)

    return data


def get_image(text_with_image):
    result = text_with_image[text_with_image.index('(') + 1: -2]
    return result.replace('\'', '')


def scrape():
    data = []
    current_site = WEBSITE

    while current_site is not None:
        soup = make_soup(current_site)

        for post in soup.find_all("article", {"class": "post"}):
            date_string = post.find("span", {"class": "date"}).text.strip().replace('-', '')
            date = conform_date(date_string)
            title = post.find("h3").text.strip()
            link = post.find("a").get("href")
            alt_image = ALT_IMAGE
            text_with_image = post.find("div", {"class": "background--cover"}).get("style")
            image = get_image(text_with_image)

            data.append(Post(None, date, title, link, image, alt_image, SOURCE_CODE, None))

        print(f"Processed {len(data)} posts")
        next_site_div = soup.find("a", {"class": "next"})

        if next_site_div is not None:
            current_site = next_site_div.get("href")

        else:
            current_site = None

    data = remove_date_dups(data)

    return data
