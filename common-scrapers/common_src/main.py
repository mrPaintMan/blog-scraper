import os
import sys

from common_src.lib import db
from common_src.lib.model.notification import Notification, push_notifications
from common_src.scrapers import *
from common_src.scrapers.abstract_scraper import remove_dups

SCRAPERS = {
    "gen_zero": gen_zero_scraper,
    "no_mans_sky": no_mans_sky_scraper,
    "windbound": windbound_scraper,
    "second_extinction": second_extinction_scraper,
    "among_us": among_us_scraper,
    "zomboid": zomboid_scraper
}

if "ENV" in os.environ:
    ENV = os.environ["ENV"]
    scraper_name = os.environ["SCRAPER"]
    host = "host.docker.internal" if "HOST" not in os.environ else os.environ["HOST"]

elif len(sys.argv) >= 3:
    ENV = sys.argv[1]
    scraper_name = sys.argv[2]
    host = sys.argv[3]

else:
    raise Exception("No environment variables found.")

print(f"Using {host} as host.")
db = db.Db(host, scraper_name)
scraper = SCRAPERS[scraper_name]

source = scraper.get_source()
print(f"Using {source.source_code} scraper.")
source.save(db)
db.commit()


def main():
    unfiltered_posts = scraper.scrape()
    posts = remove_dups(unfiltered_posts)
    posts.reverse()  # To make the oldest post iterated first
    new_posts = []

    print(f"Scraped {len(posts)} entries.")
    for post in posts:
        post.match(db)

        if post.post_id == 0 or post.post_id is None:
            post.post_id = post.save(db)
            new_posts.append(post)

        else:
            post.save(db)

        db.commit()

    print(f"{len(new_posts)} new additions")
    if len(new_posts) > 0:
        for post in new_posts:
            notification = Notification(None, post.post_id)
            notification.save(db)

        db.commit()
        push_notifications(ENV, host)


try:
    main()

finally:
    db.close()
