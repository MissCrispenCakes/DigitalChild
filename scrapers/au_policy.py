# AU policy scraper placeholder
"""
AU Policy Scraper
-----------------
Fetches AU policy PDFs from predefined URLs and saves to /data/raw/au_policy/.
"""

import os
import requests
from processors.logger import get_logger

RAW_DIR = "data/raw/au_policy"
logger = get_logger("au_policy")

URLS = {
    "AU_Child_Online_Safety_2024": "https://au.int/sites/default/files/documents/43798-doc-African_Union_Child_Online_Safety_and_Empowerment_Policy_Feb_2024.pdf",
    "AU_AI_Strategy_2024": "https://au.int/sites/default/files/documents/44004-doc-EN-_Continental_AI_Strategy_July_2024.pdf",
    "AU_Digital_Compact": "https://au.int/sites/default/files/documents/44005-doc-AU_Digital_Compact_V4.pdf"
}


def scrape():
    os.makedirs(RAW_DIR, exist_ok=True)
    for name, url in URLS.items():
        filename = os.path.join(RAW_DIR, f"{name}.pdf")
        if os.path.exists(filename):
            logger.info(f"Skipping (already exists): {filename}")
            continue
        try:
            logger.info(f"Downloading {url}")
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            with open(filename, "wb") as f:
                f.write(resp.content)
            logger.info(f"Saved → {filename}")
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")


if __name__ == "__main__":
    scrape()
