# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

# utils/selenium_setup.py
"""
Initialize a Selenium Chrome/Chromium driver that works in WSL Ubuntu.
Auto-detects binary and chromedriver paths.
"""

import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def init_driver(headless=True):
    # Try to detect Chrome/Chromium binary
    chrome_binary = (
        shutil.which("google-chrome")
        or shutil.which("chromium-browser")
        or shutil.which("chromium")
    )
    if not chrome_binary:
        raise RuntimeError(
            "No Chrome/Chromium binary found. Install with `sudo apt install chromium-browser`"
        )

    # Try to detect chromedriver
    chromedriver_path = shutil.which("chromedriver")
    if not chromedriver_path:
        raise RuntimeError(
            "No chromedriver found. Install with `sudo apt install chromium-chromedriver` "
            "or download matching version manually."
        )

    options = Options()
    options.binary_location = chrome_binary

    if headless:
        # new headless mode (Chrome 109+)
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    )

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
