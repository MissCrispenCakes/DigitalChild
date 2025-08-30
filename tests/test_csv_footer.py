# CSV footer test placeholder
import csv
import os

from processors import tags_summary


def test_csv_footer(tmp_path):
    docs = [
        {"id": "file1.pdf", "tags": ["AI", "Privacy"]},
        {"id": "file2.pdf", "tags": ["ChildRights"]},
    ]
    output_file = tmp_path / "tags_summary.csv"

    tags_summary.export(docs, str(output_file))

    with open(output_file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Ensure CSV header present
    assert lines[0].startswith("tag,count,percentage_of_documents")

    # Ensure footer branding present
    assert any("GRIMdata" in line for line in lines), "Footer missing project identity"
    assert any(
        "LittleRainbowRights" in line for line in lines
    ), "Footer missing LittleRainbowRights domain"
