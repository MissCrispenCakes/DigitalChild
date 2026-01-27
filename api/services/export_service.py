# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Export service layer

Generates CSV exports for datasets (scorecard, tags, documents).
"""

import csv
import io
import json
from typing import Dict

from flask import current_app

from api.services.scorecard_service import get_scorecard_summary
from api.services.tags_service import get_tag_frequency


def load_metadata() -> Dict:
    """Load metadata from JSON file"""
    metadata_file = current_app.config["METADATA_FILE"]
    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        current_app.logger.error(f"Metadata file not found: {metadata_file}")
        return {"documents": []}


def generate_scorecard_summary_csv() -> str:
    """
    Generate scorecard summary CSV

    Returns:
        CSV string with country, region, and indicator counts
    """
    # Get all scorecard data (no pagination)
    result = get_scorecard_summary(region=None, page=1, per_page=1000)
    countries = result["countries"]

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["Country", "Region", "Region_Specific", "Indicator_Count"])

    # Write rows
    for country in countries:
        writer.writerow(
            [
                country["country"],
                country.get("region", ""),
                country.get("region_specific", ""),
                country["indicator_count"],
            ]
        )

    # Footer
    # REUSE-IgnoreStart
    output.write("\n")
    output.write("# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights\n")
    output.write("# SPDX-License-Identifier: CC-BY-4.0\n")
    output.write("\n")
    # REUSE-IgnoreEnd
    output.write("# Project: GRIMdata / LittleRainbowRights\n")
    output.write("# Domains: https://GRIMdata.org | https://LittleRainbowRights.com\n")
    output.write(f"# Dataset: Scorecard Summary ({len(countries)} countries)\n")

    return output.getvalue()


def generate_tags_summary_csv(version: str = None) -> str:
    """
    Generate tags summary CSV

    Args:
        version: Tag version to export (e.g., 'tags_v3')

    Returns:
        CSV string with tag, count, and percentage
    """
    # Get tag frequency data
    result = get_tag_frequency(version=version)
    tags = result["tags"]
    total_docs = result["total_documents"]

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["Tag", "Count", "Percentage"])

    # Write rows
    for tag_data in tags:
        writer.writerow([tag_data["tag"], tag_data["count"], tag_data["percentage"]])

    # Footer
    # REUSE-IgnoreStart
    output.write("\n")
    output.write("# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights\n")
    output.write("# SPDX-License-Identifier: CC-BY-4.0\n")
    output.write("\n")
    # REUSE-IgnoreEnd
    output.write("# Project: GRIMdata / LittleRainbowRights\n")
    output.write("# Domains: https://GRIMdata.org | https://LittleRainbowRights.com\n")
    output.write(f"# Dataset: Tags Summary ({total_docs} documents analyzed)\n")

    if version:
        output.write(f"# Version: {version}\n")

    return output.getvalue()


def generate_documents_list_csv() -> str:
    """
    Generate documents list CSV

    Returns:
        CSV string with document metadata
    """
    metadata = load_metadata()
    documents = metadata.get("documents", [])

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(
        [
            "ID",
            "Country",
            "Region",
            "Year",
            "Source",
            "Doc_Type",
            "File_Type",
            "Last_Processed",
        ]
    )

    # Write rows
    for doc in documents:
        writer.writerow(
            [
                doc.get("id", ""),
                doc.get("country", ""),
                doc.get("region", ""),
                doc.get("year", ""),
                doc.get("source", ""),
                doc.get("doc_type", ""),
                doc.get("file_type", ""),
                doc.get("last_processed", ""),
            ]
        )

    # Footer
    # REUSE-IgnoreStart
    output.write("\n")
    output.write("# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights\n")
    output.write("# SPDX-License-Identifier: CC-BY-4.0\n")
    output.write("\n")
    # REUSE-IgnoreEnd
    output.write("# Project: GRIMdata / LittleRainbowRights\n")
    output.write("# Domains: https://GRIMdata.org | https://LittleRainbowRights.com\n")
    output.write(f"# Dataset: Documents List ({len(documents)} documents)\n")

    return output.getvalue()


# Export format registry
EXPORT_FORMATS = {
    "scorecard_summary": {
        "generator": generate_scorecard_summary_csv,
        "filename": "scorecard_summary.csv",
        "content_type": "text/csv",
        "description": "Scorecard summary (all countries)",
    },
    "tags_summary": {
        "generator": generate_tags_summary_csv,
        "filename": "tags_summary.csv",
        "content_type": "text/csv",
        "description": "Tag frequency summary",
    },
    "documents_list": {
        "generator": generate_documents_list_csv,
        "filename": "documents_list.csv",
        "content_type": "text/csv",
        "description": "Complete documents list",
    },
}


def get_available_formats() -> Dict:
    """Get list of available export formats"""
    formats = []
    for format_id, format_info in EXPORT_FORMATS.items():
        formats.append(
            {
                "format": format_id,
                "filename": format_info["filename"],
                "description": format_info["description"],
            }
        )
    return {"formats": formats, "count": len(formats)}


def generate_export(format_id: str, **kwargs) -> tuple:
    """
    Generate export file

    Args:
        format_id: Export format identifier
        **kwargs: Additional parameters (e.g., version for tags)

    Returns:
        Tuple of (csv_content, filename, content_type)

    Raises:
        ValueError: If format_id is invalid
    """
    if format_id not in EXPORT_FORMATS:
        available = ", ".join(EXPORT_FORMATS.keys())
        raise ValueError(
            f"Invalid export format: {format_id}. Available formats: {available}"
        )

    format_info = EXPORT_FORMATS[format_id]
    generator = format_info["generator"]

    # Call generator with kwargs if it accepts them
    try:
        csv_content = generator(**kwargs)
    except TypeError:
        # Generator doesn't accept kwargs
        csv_content = generator()

    return csv_content, format_info["filename"], format_info["content_type"]
