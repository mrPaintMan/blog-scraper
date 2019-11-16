from bs4 import BeautifulSoup
import urllib
import urllib.request


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
    thepage = urllib.request.urlopen(req)
    thesoup = BeautifulSoup(thepage, "html.parser")
    return thesoup


def write_datafile(data, file_name):
    f = open(file_name, "w")
    f.write("id,title,link\n")
    for element in data:
        f.write("{},{},{}\n".format(element["id"], element["title"], element["link"]))
    f.close()
    return len(data)
