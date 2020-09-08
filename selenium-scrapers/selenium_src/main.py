import os
import sys

from selenium_src.lib import db
from selenium_src.scrapers import *

SCRAPERS = {
    "dayz": dayz_scraper
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

source = scraper.get_source()
print("Using {} scraper.".format(source.source_code))
source.save(db)

posts = scraper.scrape()
posts.reverse()  # To make the oldest post iterated first
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
