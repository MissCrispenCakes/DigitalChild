"""
UNICEF Scraper - Selenium Version
--------------
Fetches UNICEF policy and research reports.
Logs all discovered links into a file.
"""

import logging
import os
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from processors.logger import get_logger
from scrapers.selenium_setup import init_driver
from scrapers.utils import download_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("unicef_selenium")

LINK_DIR = "data/try_sel/unicef"
RAW_DIR = "data/raw/unicef"
BASE_URL = "https://www.unicef.org/innocenti/projects/ai-for-children"
LINKS_LOG = os.path.join(LINK_DIR, "unicef_links_found.txt")


def scrape(base_url=BASE_URL):
    os.makedirs(RAW_DIR, exist_ok=True)

    driver = init_driver(headless=True)
    driver.get(base_url)

    try:
        # Wait until at least one <a> link is visible
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        logger.info(f"Page title: {driver.title}")

        links = driver.find_elements(By.TAG_NAME, "a")
        logger.info(f"Found {len(links)} links")

        downloaded = []
        with open(LINKS_LOG, "w", encoding="utf-8") as f:
            for link in links:
                href = link.get_attribute("href")
                text = link.text.strip()
                if not href:
                    continue

                # Log every link to file
                line = f"{text or '[no text]'} → {href}\n"
                f.write(line)

                # Try to normalize & download PDFs
                file_url = urljoin(base_url, href)
                if file_url.lower().endswith(".pdf"):
                    name = os.path.basename(
                        file_url.split("?")[0]
                    )  # strip query params
                    dest_path = os.path.join(RAW_DIR, name)
                    if download_file(file_url, dest_path):
                        downloaded.append(dest_path)

        if not downloaded:
            logger.warning("No PDFs downloaded for unicef scrape.")
        else:
            logger.info(f"Downloaded {len(downloaded)} PDFs")

        return downloaded

    finally:
        driver.quit()
