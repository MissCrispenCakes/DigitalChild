"""
Universal Periodic Review Scraper - Selenium Version
---------------------------------
Fetches UPR documents from OHCHR with country-aware folders.
Logs all discovered document links into a separate file.
"""

import os
import logging
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapers.utils import download_file
from scrapers.selenium_setup import init_driver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upr_selenium")

RAW_DIR = "data/raw/upr"
LINK_DIR = "data/try_sel/upr"
BASE_URL = "https://www.ohchr.org/en/hr-bodies/upr/documentation"
LINKS_LOG = os.path.join(LINK_DIR, "upr_links_found.txt")


def scrape(base_url=BASE_URL, countries=None):
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(LINK_DIR, exist_ok=True)

    driver = init_driver(headless=True)
    driver.get(base_url)

    try:
        # Wait for country links to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        links = driver.find_elements(By.TAG_NAME, "a")

        # Step 1: Build country link list
        country_links = []
        for link in links:
            href = link.get_attribute("href")
            text = link.text.strip()
            if href and "/hr-bodies/upr/" in href and href.endswith("-index"):
                country_links.append((text, href))

        logger.info(f"Found {len(country_links)} country pages")

        # Optional filter
        if countries:
            wanted = [c.lower() for c in countries]
            country_links = [c for c in country_links if c[0].lower() in wanted]

        all_downloaded = []

        # Prepare log file
        with open(LINKS_LOG, "w", encoding="utf-8") as logf:

            # Step 2: Visit each country page
            for country_name, country_url in country_links:
                safe_name = country_name.replace(" ", "_")
                country_dir = os.path.join(RAW_DIR, safe_name)
                os.makedirs(country_dir, exist_ok=True)

                logger.info(f"Fetching docs for {country_name} → {country_url}")
                driver.get(country_url)

                try:
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
                    )
                except Exception:
                    logger.warning(f"No links loaded for {country_name}")
                    continue

                doc_links = driver.find_elements(By.TAG_NAME, "a")
                for dl in doc_links:
                    href = dl.get_attribute("href")
                    if href and href.lower().endswith((".pdf", ".doc", ".docx")):
                        file_url = urljoin(country_url, href)
                        filename = os.path.basename(href.split("?")[0])
                        dest_path = os.path.join(country_dir, f"{safe_name}_{filename}")

                        # Always log the link
                        logf.write(f"{country_name} → {file_url}\n")

                        if download_file(file_url, dest_path):
                            all_downloaded.append(dest_path)

        if not all_downloaded:
            logger.warning("No UPR documents downloaded.")
        else:
            logger.info(f"Downloaded {len(all_downloaded)} documents total.")

        return all_downloaded

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape()
