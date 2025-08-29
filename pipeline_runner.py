"""
Pipeline Runner (Full Version with Metadata + Logging)
------------------------------------------------------
End-to-end run: scrape → process → tag → export summary → metadata update.
Supports multiple sources and tag versions.
"""

import os
import re
import json
import argparse
from datetime import datetime

from scrapers import au_policy  # later add ohchr_tb, upr, etc.
from processors import pdf_to_text, tagger, tags_summary
from processors.logger import set_run_logfile, get_logger

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


def update_metadata(doc_id, source, country, region, year, year_extracted_from, tags, tag_version="tags_v1", doc_type="Unknown"):
    metadata = load_metadata()
    now = datetime.utcnow().isoformat() + "Z"

    existing = next((d for d in metadata["documents"] if d["id"] == doc_id), None)

    if not existing:
        existing = {
            "id": doc_id,
            "source": source,
            "country": country,
            "region": region,
            "year": year,
            "year_extracted_from": year_extracted_from,
            "doc_type": doc_type,
            "ingestion_method": "scraper",
            "tags_history": [],
            "recommendations_history": [],
            "last_processed": now
        }
        metadata["documents"].append(existing)

    existing["last_processed"] = now
    existing["year"] = year
    existing["year_extracted_from"] = year_extracted_from
    existing["doc_type"] = doc_type
    existing["tags_history"].append({
        "tags": tags,
        "version": tag_version,
        "timestamp": now
    })

    save_metadata(metadata)



def extract_year(filename, txt_path, logger):
    # 1. From filename
    match = re.search(r"(19|20)\d{2}", filename)
    if match:
        return int(match.group()), "filename"

    # 2. From first 1000 chars of text
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read(1000)
            match = re.search(r"(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s+(19|20)\d{2}", text, re.IGNORECASE)
            if match:
                return int(match.group(2)), "first_page"
            match = re.search(r"(19|20)\d{2}", text)
            if match:
                return int(match.group()), "first_page"
    except Exception as e:
        logger.warning(f"Error scanning text for year in {filename}: {e}")

    # 3. Unknown
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

    # Choose scraper
    if source == "au_policy":
        scraper = au_policy
        raw_dir = "data/raw/au_policy"
        proc_dir = "data/processed/Africa/African_Union/text"
        country = "African_Union"
        region = "Africa"
        doc_type = "Policy"
    else:
        logger.error(f"Unknown source: {source}")
        return


    # Scrape
    logger.info(f"Starting scrape for {source}...")
    scraper.scrape()

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
                docs.append({"id": filename, "tags": tags})

                # Extract year
                year, year_src = extract_year(filename, txt_path, logger)
                if not year:
                    logger.warning(f"No valid year found in {filename} (source={year_src})")
                else:
                    logger.info(f"Detected year {year} for {filename} (source={year_src})")

                # Update metadata.json
                update_metadata(
                    doc_id=filename,
                    source=source,
                    country=country,
                    region=region,
                    year=year,
                    year_extracted_from=year_src,
                    tags=tags,
                    tag_version=tags_version,
                    doc_type=doc_type
                )


    # Export tags summary
    tags_summary.export(docs)
    logger.info(f"Pipeline complete for {source}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")
    parser.add_argument("--source", default="au_policy", help="Which source scraper to run (e.g., au_policy)")
    parser.add_argument("--tags-version", default="latest", help="Which tags version to use (e.g., v1, v2, v3, digital, latest)")
    parser.add_argument("--no-module-logs", action="store_true",
                        help="Disable per-module logs; use unified run log only")
    args = parser.parse_args()

    run_pipeline(source=args.source, tags_version=args.tags_version, no_module_logs=args.no_module_logs)
