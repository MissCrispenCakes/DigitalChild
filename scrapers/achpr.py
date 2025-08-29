"""
ACHPR Scraper
-------------
Scrapes African Commission on Human and Peoples' Rights (ACHPR) reports (placeholder).
"""

import os
from processors.logger import get_logger
from scrapers.utils import download_file

RAW_DIR = "data/raw/achpr"
logger = get_logger("achpr")

# Placeholder: fill with actual URLs later
URLS = {
    # "ACHPR_Report_2021": "https://example.org/achpr_report_2021.pdf"
}


def scrape():
    os.makedirs(RAW_DIR, exist_ok=True)
    if not URLS:
        logger.warning("No URLs defined for ACHPR scraper. Place documents manually in data/raw/achpr/")
        return []

    downloaded = []
    for name, url in URLS.items():
        dest_path = os.path.join(RAW_DIR, f"{name}.pdf")
        if download_file(url, dest_path):
            downloaded.append(dest_path)

    return downloaded
