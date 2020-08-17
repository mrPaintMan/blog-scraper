import os
import sys

from common_src.lib import db
from common_src.scrapers import *

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

print("Using {} as db host.".format(postgres_host))
db = db.Db(postgres_host)

scraper_source = scraper.get_source()
db_source = scraper_source.get_by_source_code(db)

print("Using {} scraper.".format(scraper_source.source_code))
if db_source is None or len(db_source) == 0:
    scraper_source.insert(db)

posts = scraper.scrape()
newPosts = 0

print("Scraped {} entries.".format(len(posts)))
for post in posts:
    post.match(db)

    if post.post_id == 0 or post.post_id is None:
        newPosts += 1

    post.save(db)
    db.commit()

print("{} new additions".format(newPosts))
db.close()
