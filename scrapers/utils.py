"""
Scraper Utilities
-----------------
Helper functions for all scrapers (HTTP requests, saving files, etc.).
"""

import os

import requests

from processors.logger import get_logger

logger = get_logger("scraper_utils")


def download_file(url, dest_path, overwrite=False, timeout=30):
    """
    Downloads a file from a URL and saves it to dest_path.
    Returns True if successful, False otherwise.
    """
    if os.path.exists(dest_path) and not overwrite:
        logger.info(f"File already exists, skipping: {dest_path}")
        return True

    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(resp.content)
        logger.info(f"Downloaded {url} → {dest_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False
