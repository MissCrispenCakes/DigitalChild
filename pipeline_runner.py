"""
Pipeline Runner
---------------
Scrapes, processes, tags, and updates metadata for human rights + digital child docs.
Supports both live scrapers and static url_dict JSONs.
"""

import argparse
import json
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

from processors import (
    json_normalizer,
    pdf_to_text,
    recommendations,
    tagger,
    tags_summary,
    tags_timeline,
    tags_timeline_country,
    tags_timeline_region,
)
from processors.logger import get_logger, set_run_logfile
from processors.scorecard_enricher import enrich_document
from processors.scorecard_export import export_scorecard
from scrapers import (
    acerwc,
    acerwc_sel,
    achpr,
    achpr_sel,
    au_policy,
    au_policy_sel,
    ohchr,
    ohchr_sel,
    unicef,
    unicef_sel,
    upr,
    upr_sel,
)
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
URL_DICT_DIR = os.path.join("configs", "url_dict")

# Doc type mapping
DOC_TYPES = {
    "au_policy": "Policy",
    "ohchr": "TreatyBodyReport",
    "upr": "UPR",
    "unicef": "Report",
    "acerwc": "TreatyBodyReport",
    "achpr": "TreatyBodyReport",
}


# -------------------------
# Shared Helper: Conversion
# -------------------------
def convert_to_text(raw_path, proc_dir, logger):
    """
    Convert a document (PDF, DOCX, HTML, etc.) to text using the right processor.
    Returns (txt_path, file_type) or (None, None) if failed.
    """
    from processors import fallback_handler

    ext = os.path.splitext(raw_path)[1].lower()
    txt_path, file_type = None, None

    try:
        if ext == ".pdf":
            txt_path = pdf_to_text.convert(raw_path, proc_dir)
            file_type = "PDF"
        elif ext in (".doc", ".docx"):
            from processors import docx_to_text

            txt_path = docx_to_text.convert(raw_path, proc_dir)
            file_type = "Word"
        elif ext in (".htm", ".html"):
            from processors import html_to_text

            txt_path = html_to_text.convert(raw_path, proc_dir)
            file_type = "HTML"
        else:
            txt_path = fallback_handler.convert(raw_path, proc_dir)
            file_type = "Other"
    except Exception as e:
        logger.error(f"Failed to convert {raw_path}: {e}")
        return None, None

    if not txt_path:
        logger.warning(f"No text extracted from {raw_path}")
        return None, None

    return txt_path, file_type


# -------------------------
# Metadata Helpers
# -------------------------
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
    file_type=None,
):
    """Update metadata.json with normalized fields."""
    if country and not country_raw:
        country_raw = country
    if region and not region_raw:
        region_raw = region

    metadata = load_metadata()
    now = datetime.now(timezone.utc).isoformat()

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
            "file_type": file_type,
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
    existing["file_type"] = file_type
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

    # Ensure json_normalizer sees normalized fields
    if country_raw:
        existing["country"] = country_raw
    if region_raw:
        existing["region"] = region_raw

    existing = json_normalizer.normalize_document(existing)
    save_metadata(metadata)


# -------------------------
# Year Extraction
# -------------------------
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


# -------------------------
# Tags Config
# -------------------------
def resolve_tags_config(version):
    with open(MAIN_TAGS_FILE, "r", encoding="utf-8") as f:
        main = json.load(f)
    versions = main.get("versions", {})
    if version in versions:
        return os.path.join("configs", versions[version])
    elif os.path.exists(version):  # direct file path
        return version
    else:
        # Try treating it as a filename in configs/
        config_path = os.path.join("configs", f"{version}.json")
        if os.path.exists(config_path):
            return config_path
        # Provide helpful error with available versions
        available = ", ".join(sorted(versions.keys())) if versions else "none found"
        raise ValueError(
            f"Unknown tags version: '{version}'. Available versions: {available}"
        )


def run_pipeline(
    source="au_policy", tags_version="latest", no_module_logs=False, args=None
):
    set_run_logfile(f"{source}_run", module_logs=not no_module_logs)
    logger = get_logger("pipeline_runner")

    if source not in SCRAPER_MAP:
        logger.error(f"Unknown source: {source}")
        return

    scraper, proc_subdir, doc_type = SCRAPER_MAP[source]
    base_source = source.replace("_sel", "")
    raw_dir = os.path.join("data", "raw", base_source)
    proc_dir = os.path.join("data", "processed", proc_subdir)

    scrape_kwargs = {}
    if args and args.base_url:
        scrape_kwargs["base_url"] = args.base_url
    if args and args.countries_file:
        with open(args.countries_file, "r", encoding="utf-8") as f:
            scrape_kwargs["countries"] = [line.strip() for line in f if line.strip()]
    elif args and args.country:
        scrape_kwargs["countries"] = [args.country]

    scraper.scrape(**scrape_kwargs)
    tags_config = resolve_tags_config(tags_version)
    logger.info(f"Using tags config: {tags_config}")

    docs = []
    for filename in os.listdir(raw_dir):
        raw_path = os.path.join(raw_dir, filename)
        txt_path, file_type = convert_to_text(raw_path, proc_dir, logger)
        if not txt_path:
            continue

        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        tags = tagger.apply_tags(text, tags_config)
        recs = recommendations.apply_recommendations(text, "configs/recs_v1.json")
        docs.append({"id": filename, "tags": tags, "recs": recs})

        year, year_src = extract_year(filename, txt_path, logger)

        country_name, country_iso, regions_list = detect_country_region(
            filename=filename, text=text[:2000]
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
            file_type=file_type,
            recommendations_list=recs,
            recs_version="recs_v1",
        )

    # Enrich metadata with scorecard indicators
    logger.info("Enriching documents with scorecard data...")
    metadata = load_metadata()
    for doc in metadata.get("documents", []):
        enrich_document(doc)
    save_metadata(metadata)

    tags_summary.export(docs)
    tags_timeline.export()
    tags_timeline_region.export()
    tags_timeline_country.export()

    # Export scorecard summary
    try:
        export_scorecard()
        logger.info("Scorecard exports complete.")
    except Exception as e:
        logger.warning(f"Scorecard export failed: {e}")

    logger.info(f"Pipeline complete for {source}. Exports in data/exports/.")


# -------------------------
# URL Dict Mode
# -------------------------
def download_file(url, dest_path, logger):
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(r.content)
        logger.info(f"Downloaded {url} -> {dest_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False


def run_from_url_dicts(tags_version="latest", no_module_logs=False):
    set_run_logfile("url_dicts_run", module_logs=not no_module_logs)
    logger = get_logger("pipeline_runner")

    for fname in os.listdir(URL_DICT_DIR):
        if not (fname.startswith("urls_dict_") and fname.endswith(".json")):
            continue
        source = fname.replace("urls_dict_", "").replace(".json", "")
        url_dict_file = os.path.join(URL_DICT_DIR, fname)
        doc_type = DOC_TYPES.get(source, "Report")

        logger.info(f"=== Processing {fname} ({source}) ===")
        with open(url_dict_file, "r", encoding="utf-8") as f:
            urls_dict = json.load(f)

        raw_dir = os.path.join("data", "raw", source)
        proc_dir = os.path.join("data", "processed", source)
        tags_config = resolve_tags_config(tags_version)

        docs = []
        for name, url in urls_dict.items():
            filename = os.path.basename(urlparse(url).path) or f"{name}.pdf"
            raw_path = os.path.join(raw_dir, filename)

            if not os.path.exists(raw_path):
                ok = download_file(url, raw_path, logger)
                if not ok:
                    continue
            else:
                logger.info(f"Skipping (already exists): {raw_path}")

            txt_path, file_type = convert_to_text(raw_path, proc_dir, logger)
            if not txt_path:
                continue

            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()

            tags = tagger.apply_tags(text, tags_config)
            recs = recommendations.apply_recommendations(text, "configs/recs_v1.json")
            docs.append({"id": filename, "tags": tags, "recs": recs})

            year, year_src = extract_year(filename, txt_path, logger)

            country_name, country_iso, regions_list = detect_country_region(
                filename=filename, url_key=name, text=text[:2000]
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
                file_type=file_type,
                recommendations_list=recs,
                recs_version="recs_v1",
            )

        tags_summary.export(docs)
        tags_timeline.export()
        tags_timeline_region.export()
        tags_timeline_country.export()
        logger.info(f"Finished processing {len(docs)} docs from {fname}")

    # Enrich all metadata with scorecard indicators
    logger.info("Enriching documents with scorecard data...")
    metadata = load_metadata()
    for doc in metadata.get("documents", []):
        enrich_document(doc)
    save_metadata(metadata)

    # Export scorecard summary
    try:
        export_scorecard()
        logger.info("Scorecard exports complete.")
    except Exception as e:
        logger.warning(f"Scorecard export failed: {e}")


# -------------------------
# CLI Entrypoint
# -------------------------
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
    parser.add_argument(
        "--mode",
        choices=["scraper", "urls", "scorecard"],
        default="scraper",
        help="Pipeline mode: scraper (default), urls (process url_dicts), or scorecard (enrich/export/validate)",
    )
    parser.add_argument(
        "--scorecard-action",
        choices=["enrich", "export", "validate", "diff", "all"],
        default="all",
        help="Scorecard action (used with --mode scorecard)",
    )
    args = parser.parse_args()

    if args.mode == "scorecard":
        # Scorecard-only mode
        from processors.scorecard_diff import run_diff_check
        from processors.scorecard_enricher import enrich_all_metadata
        from processors.scorecard_validator import validate_all_urls

        set_run_logfile("scorecard_run", module_logs=not args.no_module_logs)
        logger = get_logger("pipeline_runner")

        if args.scorecard_action in ("enrich", "all"):
            logger.info("Enriching metadata with scorecard...")
            stats = enrich_all_metadata(save=True)
            logger.info(f"Enrichment stats: {stats}")

        if args.scorecard_action in ("export", "all"):
            logger.info("Exporting scorecard...")
            exports = export_scorecard()
            logger.info(f"Scorecard exports: {exports}")

        if args.scorecard_action in ("validate", "all"):
            logger.info("Validating scorecard URLs...")
            report = validate_all_urls(save_report=True)
            summary = f"{report['summary']['total_urls']} URLs, {report['summary']['reachable']} reachable"
            logger.info(f"URL validation: {summary}")

        if args.scorecard_action in ("diff", "all"):
            logger.info("Checking for scorecard source updates...")
            report = run_diff_check(save_report=True)
            summary = f"{report['source_changes']['changed']} sources changed, {report['stale_entries']['count']} stale entries"
            logger.info(f"Diff check: {summary}")

        logger.info("Scorecard operations complete.")
    elif args.mode == "urls":
        run_from_url_dicts(
            tags_version=args.tags_version,
            no_module_logs=args.no_module_logs,
        )
    else:
        run_pipeline(
            source=args.source,
            tags_version=args.tags_version,
            no_module_logs=args.no_module_logs,
            args=args,
        )
