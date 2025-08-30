"""
Tags Timeline Export (by Country)
---------------------------------
Aggregates tags per year grouped by country.
Outputs CSV with counts per year per country.
"""

import csv
import json
import os

from processors.logger import get_logger

logger = get_logger("tags_timeline_country")


def load_metadata(metadata_file="data/metadata/metadata.json"):
    with open(metadata_file, "r", encoding="utf-8") as f:
        return json.load(f)


def export(
    metadata_file="data/metadata/metadata.json",
    output_file="data/exports/tags_timeline_country.csv",
):
    metadata = load_metadata(metadata_file)
    docs = metadata.get("documents", [])

    timeline = {}  # {(country, year): {tag: count}}

    for doc in docs:
        year = doc.get("year")
        country = doc.get("country")
        if not year or not country:
            continue
        tags_entries = doc.get("tags_history", [])
        if not tags_entries:
            continue
        latest_tags = tags_entries[-1]["tags"]

        key = (country, year)
        if key not in timeline:
            timeline[key] = {}
        for tag in latest_tags:
            timeline[key][tag] = timeline[key].get(tag, 0) + 1

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    all_tags = sorted({tag for counts in timeline.values() for tag in counts.keys()})
    countries = sorted({c for (c, y) in timeline.keys()})
    years = sorted({y for (c, y) in timeline.keys()})

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        header = ["country", "year"] + all_tags
        writer.writerow(header)

        for country in countries:
            for year in years:
                row = [country, year]
                counts = timeline.get((country, year), {})
                for tag in all_tags:
                    row.append(counts.get(tag, 0))
                writer.writerow(row)

    logger.info(f"Country-level tags timeline exported → {output_file}")
