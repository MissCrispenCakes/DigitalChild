# Tags summary exporter placeholder
"""
Tags Summary Export
-------------------
Counts tagged documents and outputs summary CSV.
"""

import csv
import os

from processors.logger import get_logger

logger = get_logger("tags_summary")


def export(docs, output_file="data/exports/tags_summary.csv"):
    """
    Takes a list of docs like:
    [
      {"id": "file1.pdf", "tags": ["AI", "Privacy"]},
      {"id": "file2.pdf", "tags": ["ChildRights"]}
    ]
    Writes a CSV summary with tag counts and percentages.
    """
    counts = {}
    total_docs = len(docs)

    for doc in docs:
        for tag in doc.get("tags", []):
            counts[tag] = counts.get(tag, 0) + 1

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["tag", "count", "percentage_of_documents"])
        for tag, count in counts.items():
            pct = round((count / total_docs) * 100, 2) if total_docs else 0
            writer.writerow([tag, count, pct])

        # Branding footer
        csvfile.write("\n# Project: GRIMdata / LittleRainbowRights\n")
        csvfile.write(
            "# Domains: https://GRIMdata.org | https://LittleRainbowRights.com\n"
        )
        csvfile.write(
            "# Note: This dataset is part of the pipeline for analyzing child & LGBTQ+ digital protections.\n"
        )
        csvfile.write("# ----------------------------------------\n")

    logger.info(f"Exported summary → {output_file}")
