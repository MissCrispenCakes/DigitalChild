"""
ACHPR Scraper
-------------
African Commission on Human and Peoples' Rights (ACHPR).
Fetches communications, reports, and policy docs from ACHPR AU site.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from processors.logger import get_logger
from scrapers.utils import download_file

DEFAULT_URL = "https://www.achpr.org/"
RAW_DIR = "data/raw/achpr"

logger = get_logger("achpr")


def scrape(base_url=DEFAULT_URL):
    os.makedirs(RAW_DIR, exist_ok=True)

    try:
        resp = requests.get(base_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch ACHPR page: {e}")
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
        logger.warning("No PDFs found for ACHPR scrape.")
    return downloaded
