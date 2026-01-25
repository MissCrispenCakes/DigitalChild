"""
Unit tests for API service layer

Tests metadata_service and scorecard_service functions.
"""

import pytest

from api.middleware.error_handlers import NotFoundError
from api.services.metadata_service import (
    get_document,
    get_documents,
    get_metadata_stats,
)


class TestMetadataService:
    """Tests for metadata service"""

    def test_get_documents_no_filters(self, app, sample_metadata, mock_metadata_file):
        """Test getting all documents without filters"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(filters={}, page=1, per_page=10)

            assert "documents" in result
            assert "pagination" in result
            assert result["pagination"]["total"] == 3
            assert len(result["documents"]) == 3

    def test_get_documents_with_country_filter(
        self, app, sample_metadata, mock_metadata_file
    ):
        """Test filtering documents by country"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(filters={"country": "Kenya"}, page=1, per_page=10)

            assert result["pagination"]["total"] == 1
            assert result["documents"][0]["country"] == "Kenya"

    def test_get_documents_with_region_filter(
        self, app, sample_metadata, mock_metadata_file
    ):
        """Test filtering documents by region"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(filters={"region": "Africa"}, page=1, per_page=10)

            assert result["pagination"]["total"] == 2
            for doc in result["documents"]:
                assert doc["region"] == "Africa"

    def test_get_documents_with_tags_filter(
        self, app, sample_metadata, mock_metadata_file
    ):
        """Test filtering documents by tags"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(filters={"tags": "AI"}, page=1, per_page=10)

            assert result["pagination"]["total"] == 2

    def test_get_documents_with_year_filter(
        self, app, sample_metadata, mock_metadata_file
    ):
        """Test filtering documents by year"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(filters={"year": 2024}, page=1, per_page=10)

            assert result["pagination"]["total"] == 1
            assert result["documents"][0]["year"] == 2024

    def test_get_documents_with_year_range(
        self, app, sample_metadata, mock_metadata_file
    ):
        """Test filtering documents by year range"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(
                filters={"year_min": 2023, "year_max": 2024},
                page=1,
                per_page=10,
            )

            assert result["pagination"]["total"] == 2

    def test_get_documents_pagination(self, app, sample_metadata, mock_metadata_file):
        """Test document pagination"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            # Get first page
            result = get_documents(filters={}, page=1, per_page=2)

            assert len(result["documents"]) == 2
            assert result["pagination"]["total"] == 3
            assert result["pagination"]["total_pages"] == 2
            assert result["pagination"]["has_next"] is True
            assert result["pagination"]["has_prev"] is False

            # Get second page
            result = get_documents(filters={}, page=2, per_page=2)

            assert len(result["documents"]) == 1
            assert result["pagination"]["has_next"] is False
            assert result["pagination"]["has_prev"] is True

    def test_get_document_found(self, app, sample_metadata, mock_metadata_file):
        """Test getting a single document that exists"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            doc = get_document("test_doc_1")

            assert doc["id"] == "test_doc_1"
            assert doc["country"] == "Kenya"

    def test_get_document_not_found(self, app, sample_metadata, mock_metadata_file):
        """Test getting a document that doesn't exist"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            with pytest.raises(NotFoundError):
                get_document("nonexistent_doc")

    def test_get_metadata_stats(self, app, sample_metadata, mock_metadata_file):
        """Test getting metadata statistics"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            stats = get_metadata_stats()

            assert stats["total"] == 3
            assert "by_source" in stats
            assert "by_region" in stats
            assert "by_doc_type" in stats
            assert "year_range" in stats
            assert stats["by_source"]["au_policy"] == 2
            assert stats["by_region"]["Africa"] == 2

    def test_documents_sorting_asc(self, app, sample_metadata, mock_metadata_file):
        """Test sorting documents ascending"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(
                filters={},
                page=1,
                per_page=10,
                sort_by="year",
                sort_order="asc",
            )

            years = [doc["year"] for doc in result["documents"]]
            assert years == [2022, 2023, 2024]

    def test_documents_sorting_desc(self, app, sample_metadata, mock_metadata_file):
        """Test sorting documents descending"""
        with app.app_context():
            app.config["METADATA_FILE"] = mock_metadata_file

            result = get_documents(
                filters={},
                page=1,
                per_page=10,
                sort_by="year",
                sort_order="desc",
            )

            years = [doc["year"] for doc in result["documents"]]
            assert years == [2024, 2023, 2022]


class TestScorecardService:
    """Tests for scorecard service"""

    def test_get_scorecard_stats(self, app):
        """Test getting scorecard statistics"""
        with app.app_context():
            from api.services.scorecard_service import get_scorecard_stats

            stats = get_scorecard_stats()

            assert "total_countries" in stats
            assert "by_region" in stats
            assert stats["total_countries"] > 0

    def test_get_country_details_found(self, app):
        """Test getting country details that exists"""
        with app.app_context():
            from api.services.scorecard_service import get_country_details

            # Kenya should exist in the scorecard
            scorecard = get_country_details("Kenya")

            assert scorecard["country"] == "Kenya"
            assert "region" in scorecard
            assert "indicators" in scorecard

    def test_get_country_details_not_found(self, app):
        """Test getting country that doesn't exist"""
        with app.app_context():
            from api.services.scorecard_service import get_country_details

            with pytest.raises(NotFoundError):
                get_country_details("NonexistentCountry")

    def test_get_scorecard_summary(self, app):
        """Test getting scorecard summary"""
        with app.app_context():
            from api.services.scorecard_service import get_scorecard_summary

            result = get_scorecard_summary(region=None, page=1, per_page=10)

            assert "countries" in result
            assert "pagination" in result
            assert len(result["countries"]) <= 10

    def test_get_scorecard_summary_with_region(self, app):
        """Test filtering scorecard by region"""
        with app.app_context():
            from api.services.scorecard_service import get_scorecard_summary

            result = get_scorecard_summary(region="Africa", page=1, per_page=10)

            assert "countries" in result
            for country in result["countries"]:
                assert country["region"] == "Africa"

    def test_get_indicator_statistics(self, app):
        """Test getting indicator statistics"""
        with app.app_context():
            from api.services.scorecard_service import get_indicator_statistics

            stats = get_indicator_statistics()

            assert isinstance(stats, dict)
            assert len(stats) > 0
            # Each indicator should have total_countries and value_distribution
            for _indicator, data in stats.items():
                assert "total_countries" in data
                assert "value_distribution" in data
