"""
Universal Periodic Review Scraper
---------------------------------
Fetches UPR documents from OHCHR:
- Main index: https://www.ohchr.org/en/hr-bodies/upr/documentation
- Country pages: e.g. https://www.ohchr.org/en/hr-bodies/upr/af-index
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from processors.logger import get_logger
from scrapers.utils import download_file

BASE_INDEX = "https://www.ohchr.org/en/hr-bodies/upr/documentation"
RAW_DIR = "data/raw/upr"

logger = get_logger("upr")


def scrape(base_url=BASE_INDEX, countries=None):
    """
    Scrape UPR documentation.
    - base_url: UPR index or alternate index page
    - countries: list of country codes/paths to scrape (default: all)
    """

    os.makedirs(RAW_DIR, exist_ok=True)

    # 1. Fetch index page
    try:
        resp = requests.get(base_url, timeout=30)
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
        # filter to only requested countries
        country_links = [c for c in country_links if c[0].lower() in [x.lower() for x in countries]]

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
            resp = requests.get(country_url, timeout=30)
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
