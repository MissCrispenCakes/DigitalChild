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

from processors import (json_normalizer, pdf_to_text, recommendations, tagger,
                        tags_summary, tags_timeline, tags_timeline_country,
                        tags_timeline_region)
from processors.logger import get_logger, set_run_logfile
from scrapers import (acerwc, acerwc_sel, achpr, achpr_sel, au_policy,
                      au_policy_sel, ohchr, ohchr_sel, unicef, unicef_sel,
                      upr, upr_sel)
from utils.detectors import detect_country_region

SCRAPER_MAP = {
    "au_policy": (au_policy, "Africa/African_Union/text", "Policy"),
    "ohchr": (ohchr, "Global/OHCHR/text", "TreatyBodyReport"),
    "upr": (upr, "Global/UPR/text", "UPR"),
    "unicef": (unicef, "Global/UNICEF/text", "Report"),
    "acerwc": (acerwc, "Africa/ACERWC/text", "TreatyBodyReport"),
    "achpr": (achpr, "Africa/ACHPR/text", "TreatyBodyReport"),
    # Selenium variants point to selenium scrapers directly
    "au_policy_sel": (au_policy_sel, "Africa/African_Union/text", "Policy"),
    "ohchr_sel": (ohchr_sel, "Global/OHCHR/text", "TreatyBodyReport"),
    "upr_sel": (upr_sel, "Global/UPR/text", "UPR"),
    "unicef_sel": (unicef_sel, "Global/UNICEF/text", "Report"),
    "acerwc_sel": (acerwc_sel, "Africa/ACERWC/text", "TreatyBodyReport"),
    "achpr_sel": (achpr_sel, "Africa/ACHPR/text", "TreatyBodyReport"),
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
):
    """Update metadata.json with normalized fields."""
    if country and not country_raw:
        country_raw = country
    if region and not region_raw:
        region_raw = region

    metadata = load_metadata()
    now = datetime.utcnow().isoformat() + "Z"

    existing = next((d for d in metadata["documents"] if d["id"] == doc_id), None)
    if not existing:
        existing = {
            "id": doc_id,
            "source": source,
            "country_raw": country_raw,
            "region_raw": region_raw,
            "year": year,
            "year_extracted_from": year_extracted_from,
            "doc_type": doc_type,
            "ingestion_method": "scraper",
            "tags_history": [],
            "recommendations_history": [],
            "last_processed": now,
        }
        metadata["documents"].append(existing)

    # Always update values
    existing["last_processed"] = now
    existing["year"] = year
    existing["year_extracted_from"] = year_extracted_from
    existing["doc_type"] = doc_type
    existing["country_raw"] = country_raw
    existing["region_raw"] = region_raw

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

    # Normalize consistently
    existing = json_normalizer.normalize_document(existing)

    save_metadata(metadata)


def extract_year(filename, txt_path=None, logger=None):
    YEAR_PATTERN = r"(19|20)\d{2}"

    # 1. From filename
    matches = re.finditer(YEAR_PATTERN, filename)
    for m in matches:
        year_str = m.group(0)
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


def run_pipeline(
    source="au_policy", tags_version="latest", no_module_logs=False, args=None
):
    set_run_logfile(f"{source}_run", module_logs=not no_module_logs)
    logger = get_logger("pipeline_runner")

    if source not in SCRAPER_MAP:
        logger.error(f"Unknown source: {source}")
        return

    scraper, proc_subdir, doc_type = SCRAPER_MAP[source]

    # Normalize raw_dir for _sel sources
    base_source = source.replace("_sel", "")
    raw_dir = f"data/raw/{base_source}"
    proc_dir = f"data/processed/{proc_subdir}"

    # Scrape
    scrape_kwargs = {}
    if args and args.base_url:
        scrape_kwargs["base_url"] = args.base_url
    if args and args.countries_file:
        with open(args.countries_file, "r", encoding="utf-8") as f:
            scrape_kwargs["countries"] = [line.strip() for line in f if line.strip()]
    elif args and args.country:
        scrape_kwargs["countries"] = [args.country]

    scraper.scrape(**scrape_kwargs)

    # Resolve tags config
    tags_config = resolve_tags_config(tags_version)
    logger.info(f"Using tags config: {tags_config}")

    docs = []
    for filename in os.listdir(raw_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(raw_dir, filename)
            txt_path = pdf_to_text.convert(pdf_path, proc_dir)
            if txt_path:
                with open(txt_path, "r", encoding="utf-8") as f:
                    text = f.read()

                # Apply tags & recs
                tags = tagger.apply_tags(text, tags_config)
                recs = recommendations.apply_recommendations(
                    text, "configs/recs_v1.json"
                )
                docs.append({"id": filename, "tags": tags, "recs": recs})

                # Year
                year, year_src = extract_year(filename, txt_path, logger)

                # Detect country/region
                country_name, country_iso, regions_list = detect_country_region(
                    filename=filename,
                    text=text[:2000],
                )

                update_metadata(
                    doc_id=filename,
                    source=source,
                    country_raw=country_name,
                    region_raw=None,
                    year=year,
                    year_extracted_from=year_src,
                    tags=tags,
                    tag_version=tags_version,
                    doc_type=doc_type,
                    recommendations_list=recs,
                    recs_version="recs_v1",
                )

    tags_summary.export(docs)
    tags_timeline.export()
    tags_timeline_region.export()
    tags_timeline_country.export()

    logger.info(f"Pipeline complete for {source}. Exports generated in data/exports/.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")
    parser.add_argument("--source", default="au_policy", help="Source scraper to run")
    parser.add_argument("--tags-version", default="latest", help="Tags config version")
    parser.add_argument(
        "--no-module-logs", action="store_true", help="Disable module logs"
    )
    parser.add_argument("--base-url", default=None, help="Optional base URL override")
    parser.add_argument("--country", default=None, help="Single country (legacy)")
    parser.add_argument(
        "--countries-file", default=None, help="File with countries list (UPR only)"
    )

    args = parser.parse_args()
    run_pipeline(
        source=args.source,
        tags_version=args.tags_version,
        no_module_logs=args.no_module_logs,
        args=args,
    )
