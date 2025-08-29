"""
OHCHR Treaty Body Scraper
-------------------------
Fetches documents from the OHCHR Treaty Body Database.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from processors.logger import get_logger
from scrapers.utils import download_file

RAW_DIR = "data/raw/ohchr"
BASE_URL = "https://tbinternet.ohchr.org/"

logger = get_logger("ohchr")


def scrape():
    os.makedirs(RAW_DIR, exist_ok=True)

    start_url = urljoin(BASE_URL, "Treaties/CRC/Shared%20Documents/")
    try:
        resp = requests.get(start_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch OHCHR TB start page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a", href=True)

    downloaded = []
    for link in links:
        href = link["href"]
        if href.lower().endswith(".pdf"):
            url = urljoin(BASE_URL, href)
            name = os.path.basename(href)
            dest_path = os.path.join(RAW_DIR, name)
            if download_file(url, dest_path):
                downloaded.append(dest_path)

    if not downloaded:
        logger.warning("No PDFs found for OHCHR TB scrape.")
    return downloaded
