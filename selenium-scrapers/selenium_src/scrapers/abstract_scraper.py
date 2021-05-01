from datetime import datetime

from selenium import webdriver

user_agent_iteration = 1

long_months = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}

short_months = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12"
}


def now():
    return datetime.now().strftime("%X:%f")[:-4] + "\t"


def get_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) " \
        f"Chrome/74.0.3729.{user_agent_iteration} Safari/537.36"

    # Setup selenium
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)

    return driver


def get_page(driver, website):
    global user_agent_iteration
    user_agent_iteration += 1
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) " \
                 f"Chrome/74.0.3729.{user_agent_iteration} Safari/537.36"

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    driver.get(website)

    return driver


def remove_dups(posts):
    link_list = []
    refined_posts = []
    for post in posts:
        if post.link not in link_list:
            link_list.append(post.link)
            refined_posts.append(post)

    return refined_posts
