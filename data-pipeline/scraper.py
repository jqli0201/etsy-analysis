import logging
import sys
import time
import requests
import datetime
from bs4 import BeautifulSoup
import numpy as np

WEBSITE = "https://www.etsy.com/search?q="
ITEMS = ["planter", "trash can", "knife holder"]
date = datetime.datetime.now().strftime("%Y%m%d")

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def delay() -> None:
    time.sleep(np.random.uniform(15, 30))
    return None
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
                "li", {"class": "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 wt-grid__item-xl-3 wt-order-xs-0 wt-order-md-0 wt-order-lg-0 wt-order-xl-0 wt-show-xs wt-show-md wt-show-lg wt-show-xl tab-reorder"}
            ):
                print(headline.text)

if __name__ == "__main__":
    logging.info(f"Scraping data...")
    scrape(ITEMS, 1)
