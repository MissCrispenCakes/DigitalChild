"""
UNICEF Scraper
--------------
Fetches UNICEF policy and research reports.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from processors.logger import get_logger
from scrapers.utils import download_file

DEFAULT_URL = "https://www.unicef.org/reports"
RAW_DIR = "data/raw/unicef"

logger = get_logger("unicef")


def scrape(base_url=DEFAULT_URL):
    os.makedirs(RAW_DIR, exist_ok=True)

    try:
        resp = requests.get(base_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch UNICEF reports page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a", href=True)

    downloaded = []
    for link in links:
        href = link["href"]
        if href.lower().endswith(".pdf"):
            file_url = urljoin(BASE_URL, href)
            name = os.path.basename(href)
            dest_path = os.path.join(RAW_DIR, name)
            if download_file(file_url, dest_path):
                downloaded.append(dest_path)

    if not downloaded:
        logger.warning("No PDFs found for UNICEF scrape.")
    return downloaded
