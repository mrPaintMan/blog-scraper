import os
import sys

from common_src.lib import db
from common_src.scrapers import *

SCRAPERS = {
    "gen_zero": gen_zero_scraper,
    "minecraft_snapshot": minecraft_snapshot_scraper,
    "no_mans_sky": no_mans_sky_scraper
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

print(f"Using {postgres_host} as db host.")
db = db.Db(postgres_host)

source = scraper.get_source()
print(f"Using {source.source_code} scraper.")
source.save(db)

posts = scraper.scrape()
posts.reverse()  # To make the oldest post iterated first
newPosts = 0

print(f"Scraped {len(posts)} entries.")
for post in posts:
    post.match(db)

    if post.post_id == 0 or post.post_id is None:
        newPosts += 1

    post.save(db)
    db.commit()

print(f"{newPosts} new additions")
db.close()
