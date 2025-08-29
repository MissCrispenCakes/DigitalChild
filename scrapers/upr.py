"""
Universal Periodic Review Scraper
---------------------------------
Fetches UPR documents (placeholder demo for one country).
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from processors.logger import get_logger
from scrapers.utils import download_file

RAW_DIR = "data/raw/upr"
BASE_URL = "https://www.ohchr.org/en/hr-bodies/upr"

logger = get_logger("upr")


def scrape(country="kenya"):
    os.makedirs(RAW_DIR, exist_ok=True)

    url = f"{BASE_URL}/{country}"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch UPR page for {country}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a", href=True)

    downloaded = []
    for link in links:
        href = link["href"]
        if href.lower().endswith(".pdf"):
            file_url = urljoin(BASE_URL, href)
            name = os.path.basename(href)
            dest_path = os.path.join(RAW_DIR, f"{country}_{name}")
            if download_file(file_url, dest_path):
                downloaded.append(dest_path)

    if not downloaded:
        logger.warning(f"No PDFs found for UPR scrape ({country}).")
    return downloaded
