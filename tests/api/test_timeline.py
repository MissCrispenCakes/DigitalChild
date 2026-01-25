# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Integration tests for Timeline API routes

Tests temporal analysis endpoints for tags over time.
"""

import json


class TestTimelineRoutes:
    """Tests for timeline API routes"""

    def test_tags_timeline_default(self, client):
        """Test GET /api/timeline/tags with default parameters"""
        response = client.get("/api/timeline/tags")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "timeline" in data["data"]
        assert "total_documents" in data["data"]
        assert isinstance(data["data"]["timeline"], list)

    def test_tags_timeline_with_version(self, client):
        """Test timeline with specific tag version"""
        response = client.get("/api/timeline/tags?version=tags_v3")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "timeline" in data["data"]
        assert "filters_applied" in data["data"]
        if data["data"]["filters_applied"]:
            assert data["data"]["filters_applied"]["version"] == "tags_v3"

    def test_tags_timeline_with_year_range(self, client):
        """Test timeline with year range filter"""
        response = client.get("/api/timeline/tags?year_min=2020&year_max=2024")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "timeline" in data["data"]

        # Verify years are within range
        for entry in data["data"]["timeline"]:
            assert 2020 <= entry["year"] <= 2024

    def test_tags_timeline_with_country_filter(self, client):
        """Test timeline filtered by country"""
        response = client.get("/api/timeline/tags?country=Kenya")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "timeline" in data["data"]

    def test_tags_timeline_with_region_filter(self, client):
        """Test timeline filtered by region"""
        response = client.get("/api/timeline/tags?region=Africa")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "timeline" in data["data"]

    def test_tags_timeline_with_multiple_filters(self, client):
        """Test timeline with multiple filters combined"""
        response = client.get(
            "/api/timeline/tags?version=tags_v3&region=Africa&year_min=2020"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "timeline" in data["data"]
        assert "filters_applied" in data["data"]

    def test_tags_timeline_invalid_year_range(self, client):
        """Test timeline with invalid year range"""
        response = client.get("/api/timeline/tags?year_min=invalid")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["error"]["code"] == "VALIDATION_ERROR"


class TestTimelineResponseFormat:
    """Tests for timeline API response structure"""

    def test_timeline_response_structure(self, client):
        """Test structure of timeline response"""
        response = client.get("/api/timeline/tags")
        data = json.loads(response.data)

        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"

        # Check timeline array structure
        if data["data"]["timeline"]:
            entry = data["data"]["timeline"][0]
            assert "year" in entry
            assert "tags" in entry
            assert isinstance(entry["year"], int)
            assert isinstance(entry["tags"], dict)

            # Check that year is reasonable
            assert 1990 <= entry["year"] <= 2030

    def test_timeline_chronological_order(self, client):
        """Test that timeline is in chronological order"""
        response = client.get("/api/timeline/tags")
        data = json.loads(response.data)

        if len(data["data"]["timeline"]) > 1:
            years = [entry["year"] for entry in data["data"]["timeline"]]
            assert years == sorted(years), "Timeline should be in chronological order"
