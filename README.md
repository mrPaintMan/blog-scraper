# blog-scraper
Python scraping repo

This repo uses Python 3.8 and is written in PyCharm.
 
The scraping is done using Selenium and beautiful soup 4, and the data is then stored in a postgres db (only local at the moment), using pg8000 package

### Installation

prerequisites:
- [python 3.8](https://www.python.org/downloads/release/python-380/)
- a local [postgres db](https://wiki.postgresql.org/wiki/Homebrew)

to install, run
```
pip3 install -r requirments.txt
``` 

to run (from blog-scraper folder): 
```
python3 -m src.main scraper-name-here
```