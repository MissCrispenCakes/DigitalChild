"""
Pipeline Runner (Demo Mode with Metadata + Logging)
---------------------------------------------------
End-to-end run for AU policies → PDF → text → tags → export summary.
Now also updates metadata.json with tags and last_processed.
"""

import os
import re
import json
import argparse
from datetime import datetime

from scrapers import au_policy
from processors import pdf_to_text, tagger, tags_summary
from processors.logger import set_run_logfile, get_logger

METADATA_FILE = "data/metadata/metadata.json"


def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return {"documents": []}
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(metadata):
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def update_metadata(doc_id, source, country, region, year, tags, tag_version="tags_v1"):
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
            "ingestion_method": "scraper",
            "tags_history": [],
            "recommendations_history": [],
            "last_processed": now
        }
        metadata["documents"].append(existing)

    existing["last_processed"] = now
    existing["tags_history"].append({
        "tags": tags,
        "version": tag_version,
        "timestamp": now
    })

    save_metadata(metadata)


def run_demo(no_module_logs=False):
    # Setup logging
    set_run_logfile("au_policy_demo", module_logs=not no_module_logs)
    logger = get_logger("pipeline_runner")

    # Step 1: Scrape PDFs
    logger.info("Starting AU Policy scrape...")
    au_policy.scrape()

    # Step 2: Convert to text + tag
    raw_dir = "data/raw/au_policy"
    proc_dir = "data/processed/Africa/African_Union/text"
    docs = []
    for filename in os.listdir(raw_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(raw_dir, filename)
            txt_path = pdf_to_text.convert(pdf_path, proc_dir)
            if txt_path:
                with open(txt_path, "r", encoding="utf-8") as f:
                    text = f.read()
                tags = tagger.apply_tags(text, "configs/tags_v1.json")
                docs.append({"id": filename, "tags": tags})

                # Extract year from filename
                match = re.search(r"(19|20)\d{2}", filename)
                year = int(match.group()) if match else None
                if not year:
                    logger.warning(f"No valid year found in filename: {filename}")
                else:
                    logger.info(f"Detected year {year} for {filename}")

                # Update metadata.json
                update_metadata(
                    doc_id=filename,
                    source="au_policy",
                    country="African_Union",
                    region="Africa",
                    year=year,
                    tags=tags,
                    tag_version="tags_v1"
                )

    # Step 3: Export tags summary
    tags_summary.export(docs)
    logger.info("Demo pipeline complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AU Policy demo pipeline")
    parser.add_argument("--no-module-logs", action="store_true",
                        help="Disable per-module logs; use unified run log only")
    args = parser.parse_args()

    run_demo(no_module_logs=args.no_module_logs)
