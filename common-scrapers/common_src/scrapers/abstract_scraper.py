from bs4 import BeautifulSoup
import urllib
import urllib.request
import os

from common_src.lib.model.post import Post

STATIC_FILE = "not-implemented"

MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}


def make_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.157 Safari/537.36',
        'Accept': '*/*',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive'
    }
    req = urllib.request.Request(url=url, headers=headers)
    the_page = urllib.request.urlopen(req, timeout=120)

    return BeautifulSoup(the_page, "html.parser")


def make_local_soup():
    if os.stat(STATIC_FILE).st_size > 0:
        the_page = open(STATIC_FILE, "r")

    else:
        raise ValueError("static_page.html is empty! Fill it with HTML and try again.")

    return BeautifulSoup(the_page, "html.parser")


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


def match_data(data):
    for post in data:
        if type(post) == Post:
            post.match()

    return data
