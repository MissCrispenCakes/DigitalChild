"""
Comparison Processor
--------------------
Compares tagging or recommendations across versions.
Outputs a CSV with per-document differences.
"""

import csv
import json
import os

from processors.logger import get_logger

logger = get_logger("comparison")


def load_metadata(metadata_file="data/metadata/metadata.json"):
    with open(metadata_file, "r", encoding="utf-8") as f:
        return json.load(f)


def run_comparison(
    config_file="configs/comparison.json", metadata_file="data/metadata/metadata.json"
):
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    versions = config.get("versions", [])
    output_file = config.get("output", "data/exports/comparison_export.csv")
    order = config.get("order", "tags_first")  # noqa: F841

    metadata = load_metadata(metadata_file)
    docs = metadata.get("documents", [])

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        header = ["id", "source"]
        for v in versions:
            header.append(f"{v}_tags")
            header.append(f"{v}_recs")
        writer.writerow(header)

        # Insert comment line at top with version info
        csvfile.write(f"# Comparison of versions: {', '.join(versions)}\n")

        for doc in docs:
            row = [doc["id"], doc["source"]]
            for v in versions:
                tags_for_v = [
                    entry["tags"]
                    for entry in doc.get("tags_history", [])
                    if entry["version"] == v
                ]
                recs_for_v = [
                    entry["recommendations"]
                    for entry in doc.get("recommendations_history", [])
                    if entry["version"] == v
                ]
                row.append(";".join(tags_for_v[0]) if tags_for_v else "")
                row.append(";".join(recs_for_v[0]) if recs_for_v else "")
            writer.writerow(row)

    logger.info(f"Comparison export written to {output_file}")
