# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for ACHPR Scraper

Verifies that achpr scraper:
1. Accepts optional base_url parameter
2. Returns a list of file paths
3. Handles errors gracefully
"""

import os
import tempfile
from unittest import mock

import scrapers.achpr as achpr


class TestACHPRScraper:
    """Test suite for achpr scraper."""

    def test_scrape_accepts_base_url(self):
        """Test that scrape() accepts base_url parameter."""
        with mock.patch("scrapers.achpr.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html><body></body></html>"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = achpr.RAW_DIR
                achpr.RAW_DIR = tmpdir
                try:
                    result = achpr.scrape(base_url="https://example.com")
                    assert isinstance(result, list)
                finally:
                    achpr.RAW_DIR = original_raw_dir

    def test_scrape_returns_list(self):
        """Test that scrape() returns a list."""
        with mock.patch("scrapers.achpr.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html><body></body></html>"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = achpr.RAW_DIR
                achpr.RAW_DIR = tmpdir
                try:
                    result = achpr.scrape()
                    assert isinstance(result, list)
                    assert result is not None
                finally:
                    achpr.RAW_DIR = original_raw_dir

    def test_scrape_handles_network_error(self):
        """Test that scrape() handles network errors gracefully."""
        with mock.patch("scrapers.achpr.requests.get") as mock_get:
            mock_get.side_effect = Exception("Network error")
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = achpr.RAW_DIR
                achpr.RAW_DIR = tmpdir
                try:
                    result = achpr.scrape()
                    assert isinstance(result, list)
                    assert len(result) == 0
                finally:
                    achpr.RAW_DIR = original_raw_dir

    def test_scrape_handles_http_error(self):
        """Test that scrape() handles HTTP errors gracefully."""
        with mock.patch("scrapers.achpr.requests.get") as mock_get:
            mock_get.return_value.raise_for_status.side_effect = Exception("404")
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = achpr.RAW_DIR
                achpr.RAW_DIR = tmpdir
                try:
                    result = achpr.scrape()
                    assert isinstance(result, list)
                    assert len(result) == 0
                finally:
                    achpr.RAW_DIR = original_raw_dir


class TestACHPRReturnValue:
    """Test return value consistency."""

    def test_return_type_consistency(self):
        """Verify that achpr returns list consistently."""
        with mock.patch("scrapers.achpr.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html><body></body></html>"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = achpr.RAW_DIR
                achpr.RAW_DIR = tmpdir
                try:
                    result = achpr.scrape()
                    assert isinstance(result, list)
                    assert result is not None
                finally:
                    achpr.RAW_DIR = original_raw_dir
