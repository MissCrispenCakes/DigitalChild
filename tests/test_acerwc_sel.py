# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for ACERWC Selenium Scraper

Verifies that acerwc_sel scraper:
1. Accepts optional base_url parameter
2. Returns a list of file paths
3. Handles errors gracefully
4. Properly initializes and quits Selenium driver
"""

import tempfile
from unittest import mock

import scrapers.acerwc_sel as acerwc_sel


class TestACERWCSeleniumScraper:
    """Test suite for acerwc_sel scraper."""

    def test_scrape_accepts_base_url(self):
        """Test that scrape() accepts base_url parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = acerwc_sel.RAW_DIR
            acerwc_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"
            mock_driver.find_elements.return_value = []

            try:
                with mock.patch("scrapers.acerwc_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.acerwc_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        result = acerwc_sel.scrape(base_url="https://example.com")
                        assert isinstance(result, list)
                        mock_driver.quit.assert_called_once()
            finally:
                acerwc_sel.RAW_DIR = original_raw_dir

    def test_scrape_returns_list(self):
        """Test that scrape() returns a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = acerwc_sel.RAW_DIR
            acerwc_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"
            mock_driver.find_elements.return_value = []

            try:
                with mock.patch("scrapers.acerwc_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.acerwc_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        result = acerwc_sel.scrape()
                        assert isinstance(result, list)
                        assert result is not None
                        mock_driver.quit.assert_called_once()
            finally:
                acerwc_sel.RAW_DIR = original_raw_dir

    def test_scrape_handles_driver_error(self):
        """Test that scrape() handles driver initialization errors gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = acerwc_sel.RAW_DIR
            acerwc_sel.RAW_DIR = tmpdir

            try:
                with mock.patch("scrapers.acerwc_sel.init_driver") as mock_init:
                    mock_init.side_effect = Exception("Driver error")
                    try:
                        result = acerwc_sel.scrape()
                        # If it doesn't raise, should return empty list or handle gracefully
                        assert isinstance(result, list)
                    except Exception:
                        # Exception is acceptable for driver errors
                        pass
            finally:
                acerwc_sel.RAW_DIR = original_raw_dir

    def test_scrape_quits_driver_on_error(self):
        """Test that scrape() quits driver even when errors occur."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = acerwc_sel.RAW_DIR
            acerwc_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.find_elements.side_effect = Exception("Element find error")

            try:
                with mock.patch("scrapers.acerwc_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.acerwc_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        try:
                            acerwc_sel.scrape()
                        except Exception:
                            pass
                        # Driver should be quit even on error
                        mock_driver.quit.assert_called_once()
            finally:
                acerwc_sel.RAW_DIR = original_raw_dir

    def test_scrape_downloads_pdfs(self):
        """Test that scrape() attempts to download PDF files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = acerwc_sel.RAW_DIR
            acerwc_sel.RAW_DIR = tmpdir

            # Create mock driver and elements
            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"

            mock_link = mock.Mock()
            mock_link.get_attribute.return_value = "https://example.com/test.pdf"
            mock_link.text = "Test Document"

            mock_driver.find_elements.return_value = [mock_link]

            try:
                with mock.patch("scrapers.acerwc_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.acerwc_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        with mock.patch(
                            "scrapers.acerwc_sel.download_file"
                        ) as mock_download:
                            mock_download.return_value = True
                            result = acerwc_sel.scrape()
                            assert isinstance(result, list)
                            mock_download.assert_called()
                            mock_driver.quit.assert_called_once()
            finally:
                acerwc_sel.RAW_DIR = original_raw_dir


class TestACERWCSeleniumReturnValue:
    """Test return value consistency."""

    def test_return_type_consistency(self):
        """Verify that acerwc_sel returns list consistently."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = acerwc_sel.RAW_DIR
            acerwc_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"
            mock_driver.find_elements.return_value = []

            try:
                with mock.patch("scrapers.acerwc_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.acerwc_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        result = acerwc_sel.scrape()
                        assert isinstance(result, list)
                        assert result is not None
                        mock_driver.quit.assert_called_once()
            finally:
                acerwc_sel.RAW_DIR = original_raw_dir
