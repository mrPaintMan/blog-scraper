import os

from src.lib.db import Db
from src.scrapers import *

DEV_POSTGRES_STRING = "YOUR LOCAL POSTGRES CONNSTRING HERE"  # e.g filippalmqvist;filippalmqvist;/tmp/.s.PGSQL.5432
SCRAPERS = {
    "gen_zero": gen_zero_scraper,
    "minecraft_snapshot": minecraft_snapshot_scraper,
    "dayz": dayz_scraper
}

scraper = SCRAPERS[os.environ["SCRAPER"]]
db = Db(DEV_POSTGRES_STRING)

posts = scraper.scrape()

for post in posts:
    post.match(db)
    post.save(db)
    db.commit()

db.close()

print("Scraped {} entries".format(len(posts)))
