"""
Tags Timeline Export (Global)
-----------------------------
Aggregates tags per year across all documents.
Outputs CSV with counts per year.
"""

import csv
import json
import os

from processors.logger import get_logger

logger = get_logger("tags_timeline")


def load_metadata(metadata_file="data/metadata/metadata.json"):
    with open(metadata_file, "r", encoding="utf-8") as f:
        return json.load(f)


def export(
    metadata_file="data/metadata/metadata.json",
    output_file="data/exports/tags_timeline.csv",
):
    metadata = load_metadata(metadata_file)
    docs = metadata.get("documents", [])

    timeline = {}  # {year: {tag: count}}

    for doc in docs:
        year = doc.get("year")
        if not year:
            continue
        tags_entries = doc.get("tags_history", [])
        if not tags_entries:
            continue
        latest_tags = tags_entries[-1]["tags"]

        if year not in timeline:
            timeline[year] = {}
        for tag in latest_tags:
            timeline[year][tag] = timeline[year].get(tag, 0) + 1

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    all_tags = sorted({tag for yearly in timeline.values() for tag in yearly.keys()})

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        header = ["year"] + all_tags
        writer.writerow(header)

        for year in sorted(timeline.keys()):
            row = [year]
            for tag in all_tags:
                row.append(timeline[year].get(tag, 0))
            writer.writerow(row)

    logger.info(f"Global tags timeline exported → {output_file}")
