# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Integration tests for Export API routes

Tests CSV export endpoints for various data formats.
"""

import json


class TestExportRoutes:
    """Tests for export API routes"""

    def test_list_export_formats(self, client):
        """Test GET /api/export - list available formats"""
        response = client.get("/api/export")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "formats" in data["data"]
        assert "count" in data["data"]
        assert isinstance(data["data"]["formats"], list)
        assert data["data"]["count"] > 0

    def test_export_formats_structure(self, client):
        """Test structure of export formats list"""
        response = client.get("/api/export")
        data = json.loads(response.data)

        assert len(data["data"]["formats"]) > 0

        # Check structure of each format
        for fmt in data["data"]["formats"]:
            assert "format" in fmt
            assert "filename" in fmt
            assert "description" in fmt
            assert isinstance(fmt["format"], str)
            assert isinstance(fmt["filename"], str)
            assert isinstance(fmt["description"], str)

    def test_download_scorecard_summary(self, client):
        """Test downloading scorecard summary CSV"""
        response = client.get("/api/export/scorecard_summary")

        assert response.status_code == 200
        assert response.mimetype == "text/csv"
        assert "Content-Disposition" in response.headers
        assert "attachment" in response.headers["Content-Disposition"]
        assert "scorecard_summary.csv" in response.headers["Content-Disposition"]

        # Check CSV content has headers
        csv_content = response.data.decode("utf-8")
        assert len(csv_content) > 0
        # Should have SPDX license header
        assert "SPDX-FileCopyrightText" in csv_content or "Country" in csv_content

    def test_download_tags_summary(self, client):
        """Test downloading tags summary CSV"""
        response = client.get("/api/export/tags_summary")

        assert response.status_code == 200
        assert response.mimetype == "text/csv"
        assert "Content-Disposition" in response.headers
        assert "tags_summary.csv" in response.headers["Content-Disposition"]

        # Check CSV content
        csv_content = response.data.decode("utf-8")
        assert len(csv_content) > 0

    def test_download_tags_summary_with_version(self, client):
        """Test downloading tags summary with version parameter"""
        response = client.get("/api/export/tags_summary?version=tags_v3")

        assert response.status_code == 200
        assert response.mimetype == "text/csv"

        # Check CSV content
        csv_content = response.data.decode("utf-8")
        assert len(csv_content) > 0

    def test_download_documents_list(self, client):
        """Test downloading documents list CSV"""
        response = client.get("/api/export/documents_list")

        assert response.status_code == 200
        assert response.mimetype == "text/csv"
        assert "Content-Disposition" in response.headers
        assert "documents_list.csv" in response.headers["Content-Disposition"]

        # Check CSV content
        csv_content = response.data.decode("utf-8")
        assert len(csv_content) > 0

    def test_download_invalid_format(self, client):
        """Test downloading with invalid format ID"""
        response = client.get("/api/export/invalid_format_12345")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["error"]["code"] == "INVALID_FORMAT"

    def test_export_csv_license_headers(self, client):
        """Test that exported CSVs contain SPDX license headers"""
        response = client.get("/api/export/scorecard_summary")

        assert response.status_code == 200
        csv_content = response.data.decode("utf-8")

        # Check for SPDX license information in CSV footer
        assert (
            "SPDX-FileCopyrightText" in csv_content
            or "GRIMdata" in csv_content
            or "LittleRainbowRights" in csv_content
        )


class TestExportResponseFormat:
    """Tests for export API response structure"""

    def test_export_list_response_structure(self, client):
        """Test structure of export formats list response"""
        response = client.get("/api/export")
        data = json.loads(response.data)

        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"
        assert "formats" in data["data"]
        assert "count" in data["data"]
        assert data["data"]["count"] == len(data["data"]["formats"])

    def test_export_csv_content_type(self, client):
        """Test that CSV exports have correct content type"""
        formats_response = client.get("/api/export")
        formats_data = json.loads(formats_response.data)

        # Test first available format
        if formats_data["data"]["formats"]:
            format_id = formats_data["data"]["formats"][0]["format"]
            response = client.get(f"/api/export/{format_id}")

            assert response.status_code == 200
            assert response.mimetype == "text/csv"
            assert "Content-Disposition" in response.headers
