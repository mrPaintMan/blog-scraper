import os
import sys

from src.lib.db import Db
from src.scrapers import *

# (user;password;host;port)
DEV_POSTGRES_STRING = "filippalmqvist;filippalmqvist;localhost;5432"  # <- Your local conn string here

if "ENV" in os.environ:
    ENV = os.environ["ENV"]

else:
    ENV = "prod"

SCRAPERS = {
    "gen_zero": gen_zero_scraper,
    "minecraft_snapshot": minecraft_snapshot_scraper,
    "dayz": dayz_scraper
}

if ENV == "prod":
    scraper = SCRAPERS[sys.argv[1]]

else:
    scraper = SCRAPERS[os.environ["SCRAPER"]]

db = Db(DEV_POSTGRES_STRING)

posts = scraper.scrape()

for post in posts:
    post.match(db)
    post.save(db)
    db.commit()

db.close()

print("Scraped {} entries".format(len(posts)))
