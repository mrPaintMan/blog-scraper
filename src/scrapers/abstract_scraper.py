from bs4 import BeautifulSoup
import urllib
import urllib.request
import os

STATIC_FILE = "not-implemented"


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


def write_datafile(data, file_name):
    f = open(file_name, "w")
    f.write("id,title,link\n")
    for element in data:
        f.write("{},{},{}\n".format(element["id"], element["title"], element["link"]))
    f.close()
    return len(data)
