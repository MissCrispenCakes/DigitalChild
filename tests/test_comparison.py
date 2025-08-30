# Comparison export test
import csv  # noqa: F401
import json
import os  # noqa: F401

from processors import comparison


def test_comparison_export(tmp_path):
    # Create dummy metadata
    metadata_file = tmp_path / "metadata.json"
    metadata = {
        "documents": [
            {
                "id": "doc1.pdf",
                "source": "au_policy",
                "tags_history": [
                    {
                        "tags": ["AI", "ChildRights"],
                        "version": "v1",
                        "timestamp": "2025-08-28T00:00:00Z",
                    },
                    {
                        "tags": ["AI", "ChildRights", "DigitalPolicy"],
                        "version": "v3",
                        "timestamp": "2025-08-28T01:00:00Z",
                    },
                ],
                "recommendations_history": [
                    {
                        "recommendations": ["The Committee recommends"],
                        "version": "recs_v1",
                        "timestamp": "2025-08-28T00:30:00Z",
                    }
                ],
            }
        ]
    }
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Create comparison config
    config_file = tmp_path / "comparison.json"
    config = {
        "versions": ["v1", "v3"],
        "order": "tags_first",
        "output": str(tmp_path / "comparison_export.csv"),
        "filters": {"region": "Africa"},
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Run comparison
    comparison.run_comparison(str(config_file), str(metadata_file))

    # Verify CSV export created
    output_file = tmp_path / "comparison_export.csv"
    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Header note with versions
    assert "# Comparison of versions:" in content

    # Expected columns
    assert "v1_tags" in content
    assert "v3_tags" in content

    # Expected data row
    assert "doc1.pdf" in content
    assert "DigitalPolicy" in content
