# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Integration tests for Tags API routes

Tests tag frequency and version endpoints.
"""

import json


class TestTagsRoutes:
    """Tests for tags API routes"""

    def test_list_tags_default(self, client):
        """Test GET /api/tags with default parameters"""
        response = client.get("/api/tags")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tags" in data["data"]
        assert "total_documents" in data["data"]
        assert isinstance(data["data"]["tags"], list)

    def test_list_tags_with_version(self, client):
        """Test filtering tags by version"""
        response = client.get("/api/tags?version=tags_v3")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tags" in data["data"]
        assert "filters_applied" in data["data"]
        assert data["data"]["filters_applied"]["version"] == "tags_v3"

    def test_list_tags_with_country_filter(self, client):
        """Test filtering tags by country"""
        response = client.get("/api/tags?country=Kenya")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tags" in data["data"]
        # May have 0 or more results depending on data

    def test_list_tags_with_region_filter(self, client):
        """Test filtering tags by region"""
        response = client.get("/api/tags?region=Africa")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tags" in data["data"]

    def test_list_tags_with_year_filter(self, client):
        """Test filtering tags by specific year"""
        response = client.get("/api/tags?year=2024")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tags" in data["data"]
        if data["data"]["filters_applied"]:
            assert data["data"]["filters_applied"]["year"] == 2024

    def test_list_tags_with_year_range(self, client):
        """Test filtering tags by year range"""
        response = client.get("/api/tags?year_min=2020&year_max=2024")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tags" in data["data"]
        if data["data"]["filters_applied"]:
            assert data["data"]["filters_applied"]["year_min"] == 2020
            assert data["data"]["filters_applied"]["year_max"] == 2024

    def test_list_tags_with_multiple_filters(self, client):
        """Test combining multiple filters"""
        response = client.get("/api/tags?version=tags_v3&region=Africa&year_min=2020")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tags" in data["data"]
        assert "filters_applied" in data["data"]

    def test_list_tags_invalid_version(self, client):
        """Test invalid version parameter"""
        response = client.get("/api/tags?version=invalid_version_12345")

        # Should still work but with warning or empty results
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"

    def test_list_tags_invalid_year(self, client):
        """Test invalid year parameter"""
        response = client.get("/api/tags?year=invalid")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["error"]["code"] == "VALIDATION_ERROR"

    def test_list_versions(self, client):
        """Test GET /api/tags/versions"""
        response = client.get("/api/tags/versions")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "versions" in data["data"]
        assert isinstance(data["data"]["versions"], list)
        assert len(data["data"]["versions"]) > 0


class TestTagsResponseFormat:
    """Tests for tags API response structure"""

    def test_tags_response_structure(self, client):
        """Test structure of tags frequency response"""
        response = client.get("/api/tags")
        data = json.loads(response.data)

        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"

        # Check tags array structure
        if data["data"]["tags"]:
            tag = data["data"]["tags"][0]
            assert "tag" in tag
            assert "count" in tag
            assert "percentage" in tag
            assert isinstance(tag["count"], int)
            assert isinstance(tag["percentage"], (int, float))

    def test_versions_response_structure(self, client):
        """Test structure of versions response"""
        response = client.get("/api/tags/versions")
        data = json.loads(response.data)

        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"
        assert isinstance(data["data"]["versions"], list)
