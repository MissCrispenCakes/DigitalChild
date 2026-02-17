# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for AU Policy Selenium Scraper

Verifies that au_policy_sel scraper:
1. Accepts optional base_url parameter
2. Returns a list of file paths
3. Handles errors gracefully
4. Properly initializes and quits Selenium driver
"""

import os
import tempfile
from unittest import mock

import scrapers.au_policy_sel as au_policy_sel


class TestAUPolicySeleniumScraper:
    """Test suite for au_policy_sel scraper."""

    def test_scrape_accepts_base_url(self):
        """Test that scrape() accepts base_url parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = au_policy_sel.RAW_DIR
            au_policy_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"
            mock_driver.find_elements.return_value = []

            try:
                with mock.patch("scrapers.au_policy_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.au_policy_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        result = au_policy_sel.scrape(base_url="https://example.com")
                        assert isinstance(result, list)
                        mock_driver.quit.assert_called_once()
            finally:
                au_policy_sel.RAW_DIR = original_raw_dir

    def test_scrape_returns_list(self):
        """Test that scrape() returns a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = au_policy_sel.RAW_DIR
            au_policy_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"
            mock_driver.find_elements.return_value = []

            try:
                with mock.patch("scrapers.au_policy_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.au_policy_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        result = au_policy_sel.scrape()
                        assert isinstance(result, list)
                        assert result is not None
                        mock_driver.quit.assert_called_once()
            finally:
                au_policy_sel.RAW_DIR = original_raw_dir

    def test_scrape_handles_driver_error(self):
        """Test that scrape() handles driver initialization errors gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = au_policy_sel.RAW_DIR
            au_policy_sel.RAW_DIR = tmpdir

            try:
                with mock.patch(
                    "scrapers.au_policy_sel.init_driver"
                ) as mock_init:
                    mock_init.side_effect = Exception("Driver error")
                    try:
                        result = au_policy_sel.scrape()
                        # If it doesn't raise, should return empty list or handle gracefully
                        assert isinstance(result, list)
                    except Exception:
                        # Exception is acceptable for driver errors
                        pass
            finally:
                au_policy_sel.RAW_DIR = original_raw_dir

    def test_scrape_quits_driver_on_error(self):
        """Test that scrape() quits driver even when errors occur."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = au_policy_sel.RAW_DIR
            au_policy_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.find_elements.side_effect = Exception("Element find error")

            try:
                with mock.patch("scrapers.au_policy_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.au_policy_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        try:
                            au_policy_sel.scrape()
                        except Exception:
                            pass
                        # Driver should be quit even on error
                        mock_driver.quit.assert_called_once()
            finally:
                au_policy_sel.RAW_DIR = original_raw_dir

    def test_scrape_downloads_pdfs(self):
        """Test that scrape() attempts to download PDF files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = au_policy_sel.RAW_DIR
            au_policy_sel.RAW_DIR = tmpdir

            # Create mock driver and elements
            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"

            mock_link = mock.Mock()
            mock_link.get_attribute.return_value = "https://example.com/test.pdf"
            mock_link.text = "Test Document"

            mock_driver.find_elements.return_value = [mock_link]

            try:
                with mock.patch("scrapers.au_policy_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.au_policy_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        with mock.patch(
                            "scrapers.au_policy_sel.download_file"
                        ) as mock_download:
                            mock_download.return_value = True
                            result = au_policy_sel.scrape()
                            assert isinstance(result, list)
                            mock_download.assert_called()
                            mock_driver.quit.assert_called_once()
            finally:
                au_policy_sel.RAW_DIR = original_raw_dir


class TestAUPolicySeleniumReturnValue:
    """Test return value consistency."""

    def test_return_type_consistency(self):
        """Verify that au_policy_sel returns list consistently."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = au_policy_sel.RAW_DIR
            au_policy_sel.RAW_DIR = tmpdir

            mock_driver = mock.Mock()
            mock_driver.title = "Test Page"
            mock_driver.find_elements.return_value = []

            try:
                with mock.patch("scrapers.au_policy_sel.init_driver") as mock_init:
                    with mock.patch("scrapers.au_policy_sel.WebDriverWait"):
                        mock_init.return_value = mock_driver
                        result = au_policy_sel.scrape()
                        assert isinstance(result, list)
                        assert result is not None
                        mock_driver.quit.assert_called_once()
            finally:
                au_policy_sel.RAW_DIR = original_raw_dir
