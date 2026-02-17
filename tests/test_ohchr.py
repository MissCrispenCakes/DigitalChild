# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for OHCHR Scraper

Verifies that ohchr scraper:
1. Accepts optional base_url parameter
2. Returns a list of file paths
3. Handles errors gracefully
"""

import os
import tempfile
from unittest import mock

import scrapers.ohchr as ohchr


class TestOHCHRScraper:
    """Test suite for ohchr scraper."""

    def test_scrape_accepts_base_url(self):
        """Test that scrape() accepts base_url parameter."""
        with mock.patch("scrapers.ohchr.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html><body></body></html>"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = ohchr.RAW_DIR
                ohchr.RAW_DIR = tmpdir
                try:
                    result = ohchr.scrape(base_url="https://example.com")
                    assert isinstance(result, list)
                finally:
                    ohchr.RAW_DIR = original_raw_dir

    def test_scrape_returns_list(self):
        """Test that scrape() returns a list."""
        with mock.patch("scrapers.ohchr.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html><body></body></html>"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = ohchr.RAW_DIR
                ohchr.RAW_DIR = tmpdir
                try:
                    result = ohchr.scrape()
                    assert isinstance(result, list)
                    assert result is not None
                finally:
                    ohchr.RAW_DIR = original_raw_dir

    def test_scrape_handles_network_error(self):
        """Test that scrape() handles network errors gracefully."""
        with mock.patch("scrapers.ohchr.requests.get") as mock_get:
            mock_get.side_effect = Exception("Network error")
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = ohchr.RAW_DIR
                ohchr.RAW_DIR = tmpdir
                try:
                    result = ohchr.scrape()
                    assert isinstance(result, list)
                    assert len(result) == 0
                finally:
                    ohchr.RAW_DIR = original_raw_dir

    def test_scrape_handles_http_error(self):
        """Test that scrape() handles HTTP errors gracefully."""
        with mock.patch("scrapers.ohchr.requests.get") as mock_get:
            mock_get.return_value.raise_for_status.side_effect = Exception("404")
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = ohchr.RAW_DIR
                ohchr.RAW_DIR = tmpdir
                try:
                    result = ohchr.scrape()
                    assert isinstance(result, list)
                    assert len(result) == 0
                finally:
                    ohchr.RAW_DIR = original_raw_dir


class TestOHCHRReturnValue:
    """Test return value consistency."""

    def test_return_type_consistency(self):
        """Verify that ohchr returns list consistently."""
        with mock.patch("scrapers.ohchr.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html><body></body></html>"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = ohchr.RAW_DIR
                ohchr.RAW_DIR = tmpdir
                try:
                    result = ohchr.scrape()
                    assert isinstance(result, list)
                    assert result is not None
                finally:
                    ohchr.RAW_DIR = original_raw_dir
