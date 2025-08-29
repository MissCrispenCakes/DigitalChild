"""
Universal Periodic Review Scraper
---------------------------------
Fetches UPR (Universal Periodic Review) documents from OHCHR.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from processors.logger import get_logger
from scrapers.utils import download_file

DEFAULT_URL = "https://www.ohchr.org/en/hr-bodies/upr"
RAW_DIR = "data/raw/upr"

logger = get_logger("upr")


def scrape(base_url=DEFAULT_URL, country=None):
    """
    Scrape UPR documents.
    - base_url: starting URL (default = OHCHR UPR main page)
    - country: if provided, scrape that country's subpage (e.g., 'kenya')
    """

    os.makedirs(RAW_DIR, exist_ok=True)

    target_url = base_url
    if country:
        target_url = f"{base_url}/{country}"

    try:
        resp = requests.get(target_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch UPR page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a", href=True)

    downloaded = []
    for link in links:
        href = link["href"]
        if href.lower().endswith(".pdf"):
            file_url = urljoin(target_url, href)
            name = os.path.basename(href)
            if country:
                name = f"{country}_{name}"
            dest_path = os.path.join(RAW_DIR, name)
            if download_file(file_url, dest_path):
                downloaded.append(dest_path)

    if not downloaded:
        logger.warning(f"No PDFs found for UPR scrape (url={target_url}).")
    return downloaded
