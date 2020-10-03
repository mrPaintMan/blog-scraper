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
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.11 (KHTML, like Gecko) '
                             'Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
    req = urllib.request.Request(url=url, headers=headers)
    the_page = urllib.request.urlopen(req)
    the_soup = BeautifulSoup(the_page, "html.parser")

    return the_soup


def make_local_soup():
    if os.stat(STATIC_FILE).st_size > 0:
        the_page = open(STATIC_FILE, "r")

    else:
        raise ValueError("static_page.html is empty! Fill it with html and try again.")

    the_soup = BeautifulSoup(the_page, "html.parser")

    return the_soup


def match_data(data):
    for post in data:
        if type(post) == Post:
            post.match()

    return data
