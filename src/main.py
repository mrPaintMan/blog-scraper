import os
from src.scrapers import *

SCRAPERS = {
    "gen_zero": gen_zero_scraper,
    "minecraft_snapshot": minecraft_snapshot_scraper
}

scraper = SCRAPERS[os.environ["SCRAPER"]]
use_web = os.getenv("USEWEB", False)

entries_scraped = scraper.scrape(use_web)

print("Scraped {} entries".format(entries_scraped))
