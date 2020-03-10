# blog-scraper
Python scraping repo

This repo consist of 3 docker applications written in Python 3.8 with PyCharm IDE. 
The folders `common-scraper`, `selenium-scraper` and `server` represent the applications and are to be treated as completely separated.

The applications:

- common-scraper, scraping application using beautiful soup 4
- selenium-scraper, scraping application using selenium
- server, a flask REST api server 
 
Scraped data is stored in a postgres db, using pg8000 package.

### Installation

prerequisites:
- [python 3.8](https://www.python.org/downloads/release/python-380/)
- a local [postgres db](https://wiki.postgresql.org/wiki/Homebrew)
- [docker](https://www.docker.com/)

to develop using venv, run from blog-scraper folder:
```
$ python3 -m venv ./
$ source ./venv/bin/activate
$ pip3 install -r ./{application}/requirments.txt
$ deactivate
``` 

to run: 
```
$ docker build -t {image-name} ./{application}/Dockerfile
$ docker run {see individual application readme}
```

### Database

Each application requires a local postgresql database, with the following config:
- port = `5432`
- database = `blogscraper`
- user = `postgres`
- password `postgres`