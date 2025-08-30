"""
Pipeline Runner (Full Version with Metadata + Logging)
------------------------------------------------------
End-to-end run: scrape → process → tag → export summary → metadata update.
Supports multiple sources and tag versions.
"""

import argparse
import json
import os
import re
from datetime import datetime

from processors import (pdf_to_text, recommendations, tagger, tags_summary,
                        tags_timeline, tags_timeline_country,
                        tags_timeline_region)
from processors.logger import get_logger, set_run_logfile
from scrapers import (acerwc, achpr, au_policy, country_utils, ohchr,
                      region_utils, unicef, upr)

SCRAPER_MAP = {
    "au_policy": (
        au_policy,
        "Africa/African_Union/text",
        "African_Union",
        "Africa",
        "Policy",
    ),
    "ohchr": (
        ohchr,
        "Africa/OHCHR/text",
        "African_Union",
        "Africa",
        "TreatyBodyReport",
    ),
    "upr": (upr, "Africa/UPR/text", "African_Union", "Africa", "UPR"),
    "unicef": (unicef, "Global/UNICEF/text", "Global", "Global", "Report"),
    "acerwc": (
        acerwc,
        "Africa/ACERWC/text",
        "African_Union",
        "Africa",
        "TreatyBodyReport",
    ),
    "achpr": (
        achpr,
        "Africa/ACHPR/text",
        "African_Union",
        "Africa",
        "TreatyBodyReport",
    ),
}


METADATA_FILE = "data/metadata/metadata.json"
MAIN_TAGS_FILE = "configs/tags_main.json"


def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return {"documents": []}
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(metadata):
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def update_metadata(
    doc_id,
    source,
    country_raw=None,
    region_raw=None,
    year=None,
    year_extracted_from="unknown",
    tags=None,
    tag_version="tags_v1",
    doc_type="Unknown",
    recommendations_list=None,
    recs_version="recs_v1",
    country=None,
    region=None,
):  # legacy args supported
    """
    Update metadata.json with normalized fields.
    Accepts both new (country_raw, region_raw) and legacy (country, region).
    """

    # Handle legacy args for backward compatibility
    if country and not country_raw:
        country_raw = country
    if region and not region_raw:
        region_raw = region

    metadata = load_metadata()
    now = datetime.utcnow().isoformat() + "Z"

    # Normalize country + region
    c_raw, country_norm, country_iso = country_utils.normalize_country(country_raw)
    r_raw, region_norm = region_utils.normalize_region(region_raw)

    existing = next((d for d in metadata["documents"] if d["id"] == doc_id), None)

    if not existing:
        existing = {
            "id": doc_id,
            "source": source,
            "country": country_norm,
            "country_raw": c_raw,
            "country_iso": country_iso,
            "region": region_norm,
            "region_raw": r_raw,
            "year": year,
            "year_extracted_from": year_extracted_from,
            "doc_type": doc_type,
            "ingestion_method": "scraper",
            "tags_history": [],
            "recommendations_history": [],
            "last_processed": now,
        }
        metadata["documents"].append(existing)

    existing["last_processed"] = now
    existing["year"] = year
    existing["year_extracted_from"] = year_extracted_from
    existing["doc_type"] = doc_type
    existing["country"] = country_norm
    existing["country_raw"] = c_raw
    existing["country_iso"] = country_iso
    existing["region"] = region_norm
    existing["region_raw"] = r_raw

    if tags is not None:
        existing["tags_history"].append(
            {"tags": tags, "version": tag_version, "timestamp": now}
        )

    if recommendations_list is not None:
        existing["recommendations_history"].append(
            {
                "recommendations": recommendations_list,
                "version": recs_version,
                "timestamp": now,
            }
        )

    save_metadata(metadata)


def extract_year(filename, txt_path=None, logger=None):
    """
    Extract year from filename and/or text file.
    Always returns (year or None, source).
    """

    YEAR_PATTERN = r"(19|20)\d{2}"

    # 1. From filename
    matches = re.finditer(YEAR_PATTERN, filename)
    for m in matches:
        year_str = m.group(0)
        # Reject if part of a longer number (look before and after)
        start, end = m.span()
        if (start > 0 and filename[start - 1].isdigit()) or (
            end < len(filename) and filename[end].isdigit()
        ):
            continue
        return int(year_str), "filename"

    # 2. From text
    if txt_path:
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read(1000)
                matches = re.finditer(YEAR_PATTERN, text)
                for m in matches:
                    year_str = m.group(0)
                    start, end = m.span()
                    if (start > 0 and text[start - 1].isdigit()) or (
                        end < len(text) and text[end].isdigit()
                    ):
                        continue
                    return int(year_str), "first_page"
        except Exception as e:
            if logger:
                logger.warning(f"Error scanning text for year in {filename}: {e}")

    return None, "unknown"


def resolve_tags_config(version):
    with open(MAIN_TAGS_FILE, "r", encoding="utf-8") as f:
        main = json.load(f)
    versions = main.get("versions", {})
    if version in versions:
        return os.path.join("configs", versions[version])
    elif os.path.exists(version):  # direct file path
        return version
    else:
        raise ValueError(f"Unknown tags version: {version}")


def run_pipeline(source="au_policy", tags_version="latest", no_module_logs=False):
    # Setup logging
    set_run_logfile(f"{source}_run", module_logs=not no_module_logs)
    logger = get_logger("pipeline_runner")

    if source not in SCRAPER_MAP:
        logger.error(f"Unknown source: {source}")
        return

    scraper, proc_subdir, country, region, doc_type = SCRAPER_MAP[source]
    raw_dir = f"data/raw/{source}"
    proc_dir = f"data/processed/{proc_subdir}"

    # Choose scraper
    if source == "au_policy":
        from scrapers import au_policy as scraper

        raw_dir = "data/raw/au_policy"
        proc_dir = "data/processed/Africa/African_Union/text"
        country = "African_Union"
        region = "Africa"
        doc_type = "Policy"
    elif source == "ohchr":
        from scrapers import ohchr as scraper

        raw_dir = "data/raw/ohchr"
        proc_dir = "data/processed/Africa/OHCHR/text"
        country = "African_Union"
        region = "Africa"
        doc_type = "TreatyBodyReport"
    elif source == "upr":
        from scrapers import upr as scraper

        raw_dir = "data/raw/upr"
        proc_dir = "data/processed/Africa/UPR/text"
        country = "African_Union"
        region = "Africa"
        doc_type = "UPR"
    elif source == "unicef":
        from scrapers import unicef as scraper

        raw_dir = "data/raw/unicef"
        proc_dir = "data/processed/Global/UNICEF/text"
        country = "Global"
        region = "Global"
        doc_type = "Report"
    elif source == "acerwc":
        from scrapers import acerwc as scraper

        raw_dir = "data/raw/acerwc"
        proc_dir = "data/processed/Africa/ACERWC/text"
        country = "African_Union"
        region = "Africa"
        doc_type = "TreatyBodyReport"
    elif source == "achpr":
        from scrapers import achpr as scraper

        raw_dir = "data/raw/achpr"
        proc_dir = "data/processed/Africa/ACHPR/text"
        country = "African_Union"
        region = "Africa"
        doc_type = "TreatyBodyReport"
    else:
        logger.error(f"Unknown source: {source}")
        return

    # Scrape
    logger.info(f"Starting scrape for {source}...")
    scrape_kwargs = {}
    if args.base_url:
        scrape_kwargs["base_url"] = args.base_url
    if args.country:
        scrape_kwargs["country"] = args.country

    scraper.scrape(**scrape_kwargs)

    # Resolve tags config
    tags_config = resolve_tags_config(tags_version)
    logger.info(f"Using tags config: {tags_config}")

    # Process each file
    docs = []
    for filename in os.listdir(raw_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(raw_dir, filename)
            txt_path = pdf_to_text.convert(pdf_path, proc_dir)
            if txt_path:
                with open(txt_path, "r", encoding="utf-8") as f:
                    text = f.read()
                tags = tagger.apply_tags(text, tags_config)
                recs = recommendations.apply_recommendations(
                    text, "configs/recs_v1.json"
                )
                docs.append({"id": filename, "tags": tags, "recs": recs})

                # Extract year
                year, year_src = extract_year(filename, txt_path, logger)
                if not year:
                    logger.warning(
                        f"No valid year found in {filename} (source={year_src})"
                    )
                else:
                    logger.info(
                        f"Detected year {year} for {filename} (source={year_src})"
                    )

                # Update metadata.json
                update_metadata(
                    doc_id=filename,
                    source=source,
                    country_raw=country,
                    region_raw=region,
                    year=year,
                    year_extracted_from=year_src,
                    tags=tags,
                    tag_version=tags_version,
                    doc_type=doc_type,
                    recommendations_list=recs,
                    recs_version="recs_v1",
                )

    # Export tags summary
    tags_summary.export(docs)

    # Export timelines
    tags_timeline.export()
    tags_timeline_region.export()
    tags_timeline_country.export()

    logger.info(f"Pipeline complete for {source}. Exports generated in data/exports/.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")
    parser.add_argument(
        "--source",
        default="au_policy",
        help="Which source scraper to run (e.g., au_policy)",
    )
    parser.add_argument(
        "--tags-version",
        default="latest",
        help="Which tags version to use (e.g., v1, v2, v3, digital, latest)",
    )
    parser.add_argument(
        "--no-module-logs",
        action="store_true",
        help="Disable per-module logs; use unified run log only",
    )
    parser.add_argument(
        "--base-url", default=None, help="Optional base URL override for the scraper"
    )
    parser.add_argument(
        "--country",
        default=None,
        help="Optional optional country parameter for the scraper",
    )
    args = parser.parse_args()

    run_pipeline(
        source=args.source,
        tags_version=args.tags_version,
        no_module_logs=args.no_module_logs,
    )
