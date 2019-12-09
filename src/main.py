import os
from src.scrapers import *

SCRAPERS = {
    "gen_zero": gen_zero_scraper,
    "minecraft_snapshot": minecraft_snapshot_scraper
}

scraper = SCRAPERS[os.environ["SCRAPER"]]

entries_scraped = scraper.scrape()

print("Scraped {} entries".format(entries_scraped))
