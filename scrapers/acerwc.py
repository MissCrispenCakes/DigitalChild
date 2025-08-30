"""
ACERWC Scraper
--------------
African Committee of Experts on the Rights and Welfare of the Child (ACERWC).
Fetches reports and recommendations from ACERWC AU site.
"""

import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from processors.logger import get_logger
from scrapers.utils import download_file

DEFAULT_URL = "https://au.int/en/acerwc"
RAW_DIR = "data/raw/acerwc"

logger = get_logger("acerwc")


def scrape(base_url=DEFAULT_URL):
    os.makedirs(RAW_DIR, exist_ok=True)

    try:
        resp = requests.get(base_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch ACERWC page: {e}")
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
        logger.warning("No PDFs found for ACERWC scrape.")
    return downloaded
