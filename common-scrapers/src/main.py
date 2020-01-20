import os
import sys

from src.lib import db
from src.scrapers import *

SCRAPERS = {
    "gen_zero": gen_zero_scraper,
    "minecraft_snapshot": minecraft_snapshot_scraper
}

if "ENV" in os.environ:
    ENV = os.environ["ENV"]
    scraper = SCRAPERS[os.environ["SCRAPER"]]
    postgres_host = "host.docker.internal" if "DB_HOST" not in os.environ else os.environ["DB_HOST"]

elif len(sys.argv) >= 3:
    ENV = sys.argv[1]
    scraper = SCRAPERS[sys.argv[2]]
    postgres_host = sys.argv[3]

else:
    raise Exception("No environment variables found.")


db = db.Db(postgres_host)

posts = scraper.scrape()

for post in posts:
    post.match(db)
    post.save(db)
    db.commit()

db.close()

print("Scraped {} entries".format(len(posts)))
