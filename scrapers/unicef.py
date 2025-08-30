"""
UNICEF Scraper
--------------
Fetches UNICEF policy and research reports.
"""

import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from processors.logger import get_logger
from scrapers.utils import download_file

RAW_DIR = "data/raw/unicef"
BASE_URL = "data.unicef.org/wp-content/uploads/2025/03/ICVAC-Tecnical-Brief-3_17.pdf"
# BASE_URL = "https://www.unicef.org/reports"

logger = get_logger("unicef")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.unicef.org/",
    "Connection": "keep-alive",
}


def scrape(base_url=BASE_URL):
    os.makedirs(RAW_DIR, exist_ok=True)

    try:
        resp = requests.get(base_url, headers=HEADERS, timeout=300)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch UNICEF page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a", href=True)

    downloaded = []
    for link in links:
        href = link["href"]
        if href.lower().endswith(".pdf"):
            file_url = urljoin(base_url, href)
            name = os.path.basename(href)
            dest_path = os.path.join(RAW_DIR, name)
            if download_file(file_url, dest_path):
                downloaded.append(dest_path)

    if not downloaded:
        logger.warning("No PDFs found for UNICEF scrape.")
    return downloaded
