import json
import os

from pipeline_runner import load_metadata, save_metadata, update_metadata

METADATA_FILE = "data/metadata/metadata.json"


def test_metadata_updates(tmp_path):
    test_id = "TestDoc.pdf"
    tags = ["AI", "Privacy"]

    # Backup original metadata.json
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            original = json.load(f)
    else:
        original = {"documents": []}

    # Run update
    update_metadata(
        doc_id=test_id,
        source="test_source",
        country="Kenya",
        region="Africa",
        year=2025,
        tags=tags,
        tag_version="tags_v1",
    )

    metadata = load_metadata()
    doc = next((d for d in metadata["documents"] if d["id"] == test_id), None)
    assert doc is not None
    assert "tags_history" in doc
    assert tags == doc["tags_history"][-1]["tags"]

    # ✅ new assertions
    assert doc["country_iso"] == "KE"
    assert doc["country_display"] == "Kenya"
    assert "AFU" in doc["regions_memberships"]

    # Restore metadata.json
    save_metadata(original)
