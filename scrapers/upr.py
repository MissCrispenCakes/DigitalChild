# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Universal Periodic Review Scraper
---------------------------------
Fetches UPR documents from OHCHR:
- Main index: https://www.ohchr.org/en/hr-bodies/upr/documentation
- Country pages: e.g. https://www.ohchr.org/en/hr-bodies/upr/af-index
"""

import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from processors.logger import get_logger
from scrapers.utils import download_file

BASE_URL = "https://www.ohchr.org/en/hr-bodies/upr/documentation"
RAW_DIR = "data/raw/upr"

logger = get_logger("upr")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.ohchr.org/en/hr-bodies/upr/upr-home",
    "Connection": "keep-alive",
}


def scrape(base_url=BASE_URL, countries=None):
    """
    Scrape UPR documentation.
    - base_url: UPR index or alternate index page
    - countries: list of country names to scrape (default: all)
    """

    os.makedirs(RAW_DIR, exist_ok=True)

    # 1. Fetch index page
    try:
        resp = requests.get(base_url, headers=HEADERS, timeout=300)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch UPR index page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract all country links from the index page
    country_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/hr-bodies/upr/" in href and href.endswith("-index"):
            country_name = a.get_text(strip=True)
            full_url = urljoin("https://www.ohchr.org", href)
            country_links.append((country_name, full_url))

    if countries:
        wanted = [x.lower() for x in countries]
        country_links = [c for c in country_links if c[0].lower() in wanted]

    if not country_links:
        logger.warning("No country links found on UPR index page")
        return []

    all_downloaded = []

    # 2. Visit each country page
    for country_name, country_url in country_links:
        logger.info(f"Fetching UPR docs for {country_name} → {country_url}")
        country_dir = os.path.join(RAW_DIR, country_name.replace(" ", "_"))
        os.makedirs(country_dir, exist_ok=True)

        try:
            resp = requests.get(country_url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch country page {country_url}: {e}")
            continue

        csoup = BeautifulSoup(resp.text, "html.parser")
        links = csoup.find_all("a", href=True)

        for link in links:
            href = link["href"]
            if href.lower().endswith((".pdf", ".doc", ".docx")):
                file_url = urljoin("https://www.ohchr.org", href)
                filename = os.path.basename(href)
                dest_path = os.path.join(country_dir, f"{country_name}_{filename}")

                if download_file(file_url, dest_path):
                    all_downloaded.append(dest_path)

    if not all_downloaded:
        logger.warning("No UPR documents downloaded")
    return all_downloaded
