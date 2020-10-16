import os
import sys

from selenium_src.lib import db
from selenium_src.lib.model.notification import Notification, push_notifications
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

print(f"Using {postgres_host} as db host.")
db = db.Db(postgres_host)

source = scraper.get_source()
print(f"Using {source.source_code} scraper.")
source.save(db)
db.commit()

posts = scraper.scrape()
posts.reverse()  # To make the oldest post iterated first
newPosts = []

print(f"Scraped {len(posts)} entries.")
for post in posts:
    post.match(db)

    if post.post_id == 0 or post.post_id is None:
        post.post_id = post.save(db)
        newPosts.append(post)

    else:
        post.save(db)

    db.commit()

print(f"{len(newPosts)} new additions")
for post in newPosts:
    notification = Notification(None, post.post_id)
    notification.save(db)

db.commit()

if len(newPosts) > 0:
    push_notifications(ENV)

db.close()
