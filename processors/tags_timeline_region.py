"""
Tags Timeline Export (by Region)
--------------------------------
Aggregates tags per year grouped by region.
Outputs CSV with counts per year per region.
"""

import csv
import json
import os

from processors.logger import get_logger

logger = get_logger("tags_timeline_region")


def load_metadata(metadata_file="data/metadata/metadata.json"):
    with open(metadata_file, "r", encoding="utf-8") as f:
        return json.load(f)


def export(
    metadata_file="data/metadata/metadata.json",
    output_file="data/exports/tags_timeline_region.csv",
):
    metadata = load_metadata(metadata_file)
    docs = metadata.get("documents", [])

    timeline = {}  # {(region, year): {tag: count}}

    for doc in docs:
        year = doc.get("year")
        region = doc.get("region")
        if not year or not region:
            continue
        tags_entries = doc.get("tags_history", [])
        if not tags_entries:
            continue
        latest_tags = tags_entries[-1]["tags"]

        key = (region, year)
        if key not in timeline:
            timeline[key] = {}
        for tag in latest_tags:
            timeline[key][tag] = timeline[key].get(tag, 0) + 1

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    all_tags = sorted({tag for counts in timeline.values() for tag in counts.keys()})
    regions = sorted({r for (r, y) in timeline.keys()})
    years = sorted({y for (r, y) in timeline.keys()})

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        header = ["region", "year"] + all_tags
        writer.writerow(header)

        for region in regions:
            for year in years:
                row = [region, year]
                counts = timeline.get((region, year), {})
                for tag in all_tags:
                    row.append(counts.get(tag, 0))
                writer.writerow(row)

    logger.info(f"Regional tags timeline exported → {output_file}")
