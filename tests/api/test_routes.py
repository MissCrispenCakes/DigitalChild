"""
Integration tests for API routes

Tests all API endpoints with Flask test client.
"""

import json


class TestHealthRoutes:
    """Tests for health check routes"""

    def test_health_check(self, client):
        """Test /api/health endpoint"""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["data"]["status"] == "healthy"
        assert "version" in data["data"]

    def test_system_info(self, client):
        """Test /api/info endpoint"""
        response = client.get("/api/info")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "documents" in data["data"]
        assert "scorecard" in data["data"]


class TestDocumentsRoutes:
    """Tests for documents API routes"""

    def test_list_documents_default(self, client):
        """Test GET /api/documents with default parameters"""
        response = client.get("/api/documents")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "items" in data["data"]
        assert "pagination" in data["data"]
        assert data["data"]["pagination"]["page"] == 1
        assert data["data"]["pagination"]["per_page"] == 20

    def test_list_documents_with_pagination(self, client):
        """Test document list pagination"""
        response = client.get("/api/documents?page=1&per_page=5")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["data"]["pagination"]["page"] == 1
        assert data["data"]["pagination"]["per_page"] == 5
        assert len(data["data"]["items"]) <= 5

    def test_list_documents_with_country_filter(self, client):
        """Test filtering by country"""
        response = client.get("/api/documents?country=Kenya")

        assert response.status_code == 200
        data = json.loads(response.data)
        # May have 0 or more results depending on data
        assert "items" in data["data"]

    def test_list_documents_with_region_filter(self, client):
        """Test filtering by region"""
        response = client.get("/api/documents?region=Africa")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "items" in data["data"]

    def test_list_documents_with_source_filter(self, client):
        """Test filtering by source"""
        response = client.get("/api/documents?source=au_policy")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "items" in data["data"]

    def test_list_documents_with_year_filter(self, client):
        """Test filtering by year"""
        response = client.get("/api/documents?year=2024")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "items" in data["data"]

    def test_list_documents_with_year_range(self, client):
        """Test filtering by year range"""
        response = client.get("/api/documents?year_min=2020&year_max=2024")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "items" in data["data"]

    def test_list_documents_with_tags_filter(self, client):
        """Test filtering by tags"""
        response = client.get("/api/documents?tags=AI")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "items" in data["data"]

    def test_list_documents_with_sorting(self, client):
        """Test document sorting"""
        response = client.get("/api/documents?sort_by=year&sort_order=desc")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "items" in data["data"]

    def test_list_documents_invalid_page(self, client):
        """Test invalid page parameter"""
        response = client.get("/api/documents?page=0")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["error"]["code"] == "VALIDATION_ERROR"

    def test_list_documents_invalid_per_page(self, client):
        """Test invalid per_page parameter"""
        response = client.get("/api/documents?per_page=1000")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"

    def test_list_documents_invalid_sort_by(self, client):
        """Test invalid sort_by parameter"""
        response = client.get("/api/documents?sort_by=invalid_field")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"

    def test_get_document_detail(self, client):
        """Test GET /api/documents/<id>"""
        # First get a document ID
        response = client.get("/api/documents?per_page=1")
        data = json.loads(response.data)

        if data["data"]["items"]:
            doc_id = data["data"]["items"][0]["id"]

            # Get document detail
            response = client.get(f"/api/documents/{doc_id}")

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["status"] == "success"
            assert data["data"]["id"] == doc_id

    def test_get_document_not_found(self, client):
        """Test getting non-existent document"""
        response = client.get("/api/documents/nonexistent_document_id")

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["error"]["code"] == "NOT_FOUND"


class TestScorecardRoutes:
    """Tests for scorecard API routes"""

    def test_list_countries_default(self, client):
        """Test GET /api/scorecard with default parameters"""
        response = client.get("/api/scorecard")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "items" in data["data"]
        assert "pagination" in data["data"]

    def test_list_countries_with_pagination(self, client):
        """Test scorecard pagination"""
        response = client.get("/api/scorecard?page=1&per_page=10")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["data"]["pagination"]["page"] == 1
        assert data["data"]["pagination"]["per_page"] == 10
        assert len(data["data"]["items"]) <= 10

    def test_list_countries_with_region_filter(self, client):
        """Test filtering scorecard by region"""
        response = client.get("/api/scorecard?region=Africa")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "items" in data["data"]
        # All items should be from Africa
        for item in data["data"]["items"]:
            assert item["region"] == "Africa"

    def test_get_country_scorecard(self, client):
        """Test GET /api/scorecard/<country>"""
        response = client.get("/api/scorecard/Kenya")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["data"]["country"] == "Kenya"
        assert "region" in data["data"]
        assert "indicators" in data["data"]

    def test_get_country_scorecard_not_found(self, client):
        """Test getting scorecard for non-existent country"""
        response = client.get("/api/scorecard/NonexistentCountry")

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["error"]["code"] == "NOT_FOUND"

    def test_get_indicator_statistics(self, client):
        """Test GET /api/scorecard/indicators/statistics"""
        response = client.get("/api/scorecard/indicators/statistics")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert isinstance(data["data"], dict)
        assert len(data["data"]) > 0


class TestResponseFormat:
    """Tests for standard response format"""

    def test_success_response_format(self, client):
        """Test success response structure"""
        response = client.get("/api/health")
        data = json.loads(response.data)

        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"

    def test_error_response_format(self, client):
        """Test error response structure"""
        response = client.get("/api/documents/nonexistent")
        data = json.loads(response.data)

        assert "status" in data
        assert "error" in data
        assert "timestamp" in data
        assert data["status"] == "error"
        assert "code" in data["error"]
        assert "message" in data["error"]

    def test_paginated_response_format(self, client):
        """Test paginated response structure"""
        response = client.get("/api/documents")
        data = json.loads(response.data)

        assert data["data"]["pagination"]["page"] >= 1
        assert data["data"]["pagination"]["per_page"] >= 1
        assert data["data"]["pagination"]["total"] >= 0
        assert "has_next" in data["data"]["pagination"]
        assert "has_prev" in data["data"]["pagination"]


class TestCaching:
    """Tests for caching behavior"""

    def test_document_detail_caching(self, client):
        """Test that document detail responses are cached"""
        # Get a document ID
        response = client.get("/api/documents?per_page=1")
        data = json.loads(response.data)

        if data["data"]["items"]:
            doc_id = data["data"]["items"][0]["id"]

            # First request
            response1 = client.get(f"/api/documents/{doc_id}")
            assert response1.status_code == 200

            # Second request (should be cached)
            response2 = client.get(f"/api/documents/{doc_id}")
            assert response2.status_code == 200
            assert response1.data == response2.data

    def test_scorecard_country_caching(self, client):
        """Test that scorecard country responses are cached"""
        # First request
        response1 = client.get("/api/scorecard/Kenya")
        assert response1.status_code == 200

        # Second request (should be cached)
        response2 = client.get("/api/scorecard/Kenya")
        assert response2.status_code == 200
        assert response1.data == response2.data
