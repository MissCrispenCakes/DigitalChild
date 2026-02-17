# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for AU Policy Scraper

Verifies that au_policy scraper:
1. Accepts optional kwargs without error (base_url, countries)
2. Returns a list of file paths
3. Handles existing files correctly
"""

import os
import tempfile
from unittest import mock

# Import scraper module directly (no __init__.py in scrapers/)
import scrapers.au_policy as au_policy


class TestAUPolicyScraper:
    """Test suite for au_policy scraper."""

    def test_scrape_accepts_no_arguments(self):
        """Test that scrape() can be called without arguments."""
        with mock.patch("scrapers.au_policy.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"fake pdf content"
            with tempfile.TemporaryDirectory() as tmpdir:
                # Temporarily override RAW_DIR
                original_raw_dir = au_policy.RAW_DIR
                au_policy.RAW_DIR = tmpdir
                try:
                    result = au_policy.scrape()
                    assert isinstance(result, list)
                finally:
                    au_policy.RAW_DIR = original_raw_dir

    def test_scrape_accepts_optional_kwargs(self):
        """Test that scrape() accepts optional base_url and countries kwargs."""
        with mock.patch("scrapers.au_policy.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"fake pdf content"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = au_policy.RAW_DIR
                au_policy.RAW_DIR = tmpdir
                try:
                    # This should not raise TypeError
                    result = au_policy.scrape(
                        base_url="https://example.com", countries=["Kenya"]
                    )
                    assert isinstance(result, list)
                finally:
                    au_policy.RAW_DIR = original_raw_dir

    def test_scrape_returns_list(self):
        """Test that scrape() returns a list."""
        with mock.patch("scrapers.au_policy.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"fake pdf content"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = au_policy.RAW_DIR
                au_policy.RAW_DIR = tmpdir
                try:
                    result = au_policy.scrape()
                    assert isinstance(result, list)
                finally:
                    au_policy.RAW_DIR = original_raw_dir

    def test_scrape_includes_downloaded_files(self):
        """Test that downloaded files are included in returned list."""
        with mock.patch("scrapers.au_policy.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"fake pdf content"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = au_policy.RAW_DIR
                au_policy.RAW_DIR = tmpdir
                try:
                    result = au_policy.scrape()
                    # Should have downloaded files (or at least tried)
                    assert isinstance(result, list)
                    # All returned items should be file paths
                    for filepath in result:
                        assert isinstance(filepath, str)
                        assert os.path.exists(filepath)
                finally:
                    au_policy.RAW_DIR = original_raw_dir

    def test_scrape_handles_existing_files(self):
        """Test that existing files are skipped but included in results."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_raw_dir = au_policy.RAW_DIR
            au_policy.RAW_DIR = tmpdir
            try:
                # Create an existing file
                existing_file = os.path.join(tmpdir, "AU_AI_Strategy_2024.pdf")
                with open(existing_file, "wb") as f:
                    f.write(b"existing content")

                with mock.patch("scrapers.au_policy.requests.get") as mock_get:
                    mock_get.return_value.status_code = 200
                    mock_get.return_value.content = b"fake pdf content"

                    result = au_policy.scrape()

                    # Existing file should be in results
                    assert existing_file in result
                    # Should not have been re-downloaded
                    with open(existing_file, "rb") as f:
                        content = f.read()
                    assert content == b"existing content"
            finally:
                au_policy.RAW_DIR = original_raw_dir

    def test_scrape_handles_download_errors(self):
        """Test that scrape() handles download errors gracefully."""
        with mock.patch("scrapers.au_policy.requests.get") as mock_get:
            # Simulate download failure
            mock_get.side_effect = Exception("Network error")
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = au_policy.RAW_DIR
                au_policy.RAW_DIR = tmpdir
                try:
                    result = au_policy.scrape()
                    # Should return empty list when all downloads fail
                    assert isinstance(result, list)
                    # No files should be downloaded
                    assert len(result) == 0
                finally:
                    au_policy.RAW_DIR = original_raw_dir


class TestAUPolicyReturnValue:
    """Test return value consistency with other scrapers."""

    def test_return_type_consistency(self):
        """Verify that au_policy returns the same type as other scrapers."""
        with mock.patch("scrapers.au_policy.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"fake pdf content"
            with tempfile.TemporaryDirectory() as tmpdir:
                original_raw_dir = au_policy.RAW_DIR
                au_policy.RAW_DIR = tmpdir
                try:
                    result = au_policy.scrape()
                    # Should return list (consistent with unicef, upr, etc.)
                    assert isinstance(result, list)
                    # Should NOT return None
                    assert result is not None
                finally:
                    au_policy.RAW_DIR = original_raw_dir
