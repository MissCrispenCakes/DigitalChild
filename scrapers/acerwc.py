"""
ACERWC Scraper
--------------
Scrapes African Committee of Experts on the Rights and Welfare of the Child (ACERWC) reports (placeholder).
"""

import os
from processors.logger import get_logger
from scrapers.utils import download_file

RAW_DIR = "data/raw/acerwc"
logger = get_logger("acerwc")

# Placeholder: fill with actual URLs later
URLS = {
    # "ACERWC_Report_2022": "https://example.org/acerwc_report_2022.pdf"
}


def scrape():
    os.makedirs(RAW_DIR, exist_ok=True)
    if not URLS:
        logger.warning("No URLs defined for ACERWC scraper. Place documents manually in data/raw/acerwc/")
        return []

    downloaded = []
    for name, url in URLS.items():
        dest_path = os.path.join(RAW_DIR, f"{name}.pdf")
        if download_file(url, dest_path):
            downloaded.append(dest_path)

    return downloaded
