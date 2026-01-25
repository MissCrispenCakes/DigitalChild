"""
Pytest configuration for API tests

Provides fixtures for Flask app and test client.
"""

import json
import sys
from pathlib import Path

import pytest

# Ensure project root is in path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


@pytest.fixture
def app():
    """Create Flask app for testing"""
    # Import here to avoid issues with path setup
    from api.app import create_app

    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_metadata():
    """Sample metadata for testing"""
    return {
        "documents": [
            {
                "id": "test_doc_1",
                "source": "au_policy",
                "country": "Kenya",
                "country_raw": "Kenya",
                "region": "Africa",
                "region_raw": "Sub-Saharan Africa",
                "year": 2024,
                "doc_type": "Policy",
                "file_type": "PDF",
                "tags_history": [
                    {
                        "tags": ["AI", "DigitalPolicy"],
                        "version": "tags_v3",
                        "timestamp": "2024-01-15T10:00:00Z",
                    }
                ],
                "last_processed": "2024-01-15T10:30:00Z",
            },
            {
                "id": "test_doc_2",
                "source": "upr",
                "country": "Albania",
                "country_raw": "Albania",
                "region": "Europe",
                "region_raw": "Southern Europe",
                "year": 2023,
                "doc_type": "Report",
                "file_type": "PDF",
                "tags_history": [
                    {
                        "tags": ["ChildRights"],
                        "version": "tags_v3",
                        "timestamp": "2024-01-15T11:00:00Z",
                    }
                ],
                "last_processed": "2024-01-15T11:30:00Z",
            },
            {
                "id": "test_doc_3",
                "source": "au_policy",
                "country": "Ghana",
                "country_raw": "Ghana",
                "region": "Africa",
                "region_raw": "Sub-Saharan Africa",
                "year": 2022,
                "doc_type": "Policy",
                "file_type": "PDF",
                "tags_history": [
                    {
                        "tags": ["AI", "ChildRights"],
                        "version": "tags_v3",
                        "timestamp": "2024-01-15T12:00:00Z",
                    }
                ],
                "last_processed": "2024-01-15T12:30:00Z",
            },
        ]
    }


@pytest.fixture
def mock_metadata_file(tmp_path, sample_metadata):
    """Create temporary metadata file for testing"""
    metadata_file = tmp_path / "metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(sample_metadata, f)
    return str(metadata_file)


@pytest.fixture
def auth_headers():
    """Headers for authenticated requests"""
    return {"X-API-Key": "test-key"}
