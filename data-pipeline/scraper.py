import logging
import sys
import time
import requests
import datetime
from bs4 import BeautifulSoup

WEBSITE = "https://www.etsy.com/search?q="
ITEMS = ["planter", "trash can", "knife holder"]
date = datetime.datetime.now().strftime("%Y%m%d")

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def preprocess(items: list):
    return [item.replace(" ", "%20") for item in items]


def make_url(items: list, pages: int):
    """Defines url to call Etsy with desired items and pages
    `https://www.etsy.com/search?q=planter&page=2&ref=pagination`
    """
    items = preprocess(items)
    return [
        f"{WEBSITE}={item}&page={page}&ref=pagination"
        for item in items
        for page in range(1, pages + 1)
    ]


def scrape(items, pages):
    urls = make_url(items, pages)
    for url in urls:
        r = requests.get(url)
        if r.status_code == 200:
            logging.info(f"Visiting {url}")
            soup = BeautifulSoup(r.content, "html.parser")
            # work in progress here
            for headline in soup.find_all(
                "a", {"class": "listing-link wt-display-inline-block*"}
            ):
                print(headline.text)

if __name__ == "__main__":
    logging.info(f"Scraping data...")
    scrape(ITEMS, 1)
