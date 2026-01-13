"""
Scraper Utilities
-----------------
Shared helper functions for scrapers.
"""

import os

import requests

from processors.logger import get_logger

logger = get_logger("scraper_utils")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.ohchr.org/",
    "Connection": "keep-alive",
}


def download_file(url, dest_path, timeout=300):
    """
    Download a file with browser-like headers.
    """
    try:
        resp = requests.get(url, headers=HEADERS, stream=True, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:  # Only create if there's a directory component
        os.makedirs(dest_dir, exist_ok=True)
    try:
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(1024):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        logger.info(f"Downloaded: {dest_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving {dest_path}: {e}")
        return False
