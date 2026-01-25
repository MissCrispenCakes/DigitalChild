"""
Scorecard Diff/Update Checker
------------------------------
Monitors key live data sources and detects when scorecard entries may be stale.
Compares current scorecard values against live source pages.
"""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from processors.logger import get_logger
from processors.scorecard import extract_all_source_urls, load_scorecard
from processors.validators import URLValidationError, validate_url

# Output files
DIFF_REPORT_FILE = "data/exports/scorecard_diff_report.json"
CACHE_DIR = "data/cache/scorecard_sources"

# Key sources to monitor (subset for automated checking)
MONITORED_SOURCES = {
    "unesco_ai": {
        "name": "UNESCO AI Policy Observatory",
        "base_url": "https://en.unesco.org/artificial-intelligence/observatory",
        "pattern": r"AI_Policy_Status",
    },
    "unctad_dp": {
        "name": "UNCTAD Data Protection Tracker",
        "base_url": "https://unctad.org/page/data-protection-and-privacy-legislation-worldwide",
        "pattern": r"Data_Protection_Law",
    },
    "ilga_maps": {
        "name": "ILGA World Maps",
        "base_url": "https://ilga.org/maps-sexual-orientation-laws",
        "pattern": r"LGBTQ_Legal_Status|Promotion_Propaganda",
    },
    # REMOVED: human_dignity_trust (site unreachable)
    # Replaced by: ilga_maps (already monitored above)
    # See: docs/maintenance/SCORECARD_MAINTENANCE_REPORT.md for details
    "privacy_intl_sim": {
        "name": "Privacy International - SIM Registration",
        "base_url": "https://privacyinternational.org/learn/biometric-id-databases",
        "pattern": r"SIM_Biometric",
    },
    # NOTE: gsma_sim removed (site unreachable)
    # Replaced by: privacy_intl_sim (above)
    # See: docs/maintenance/SCORECARD_MAINTENANCE_REPORT.md for details
}

REQUEST_TIMEOUT = 20
USER_AGENT = "Mozilla/5.0 (compatible; DigitalChild-DiffChecker/1.0)"


def hash_content(content: str) -> str:
    """Generate hash of content for change detection."""
    # Normalize whitespace and lowercase
    normalized = re.sub(r"\s+", "", content.lower())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def fetch_page_content(url: str) -> Optional[str]:
    """
    Fetch a page and return its text content.

    Args:
        url: URL to fetch

    Returns:
        Page text content or None on error
    """
    logger = get_logger("scorecard_diff")

    # Validate URL format before making request
    try:
        url = validate_url(url, allow_http=True)
    except URLValidationError as e:
        logger.warning(f"Invalid URL format: {url} - {e}")
        return None

    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None


def compute_content_hash(content: str) -> str:
    """Compute MD5 hash of content for change detection."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def load_cached_hash(source_key: str) -> Optional[str]:
    """Load previously cached content hash."""
    cache_file = os.path.join(CACHE_DIR, f"{source_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            data = json.load(f)
            return data.get("hash")
    return None


def save_cached_hash(source_key: str, content_hash: str, url: str) -> None:
    """Save content hash to cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{source_key}.json")
    with open(cache_file, "w") as f:
        json.dump(
            {
                "hash": content_hash,
                "url": url,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            },
            f,
            indent=2,
        )


def check_source_for_changes(source_key: str, source_info: Dict) -> Dict[str, Any]:
    """
    Check a monitored source for changes.

    Args:
        source_key: Key from MONITORED_SOURCES
        source_info: Source config dict

    Returns:
        Dict with check results
    """
    logger = get_logger("scorecard_diff")
    url = source_info["base_url"]

    result = {
        "source": source_key,
        "name": source_info["name"],
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": "unknown",
        "changed": False,
        "error": None,
    }

    content = fetch_page_content(url)
    if not content:
        result["status"] = "error"
        result["error"] = "Failed to fetch page"
        return result

    current_hash = compute_content_hash(content)
    cached_hash = load_cached_hash(source_key)

    if cached_hash is None:
        result["status"] = "new"
        result["changed"] = False  # First check, no comparison
        logger.info(f"First check for {source_key}, caching hash")
    elif cached_hash != current_hash:
        result["status"] = "changed"
        result["changed"] = True
        logger.warning(f"Source {source_key} has changed!")
    else:
        result["status"] = "unchanged"
        result["changed"] = False

    # Update cache
    save_cached_hash(source_key, current_hash, url)

    return result


def check_all_monitored_sources() -> Dict[str, Any]:
    """
    Check all monitored sources for changes.

    Returns:
        Report with all source check results
    """
    logger = get_logger("scorecard_diff")
    logger.info(f"Checking {len(MONITORED_SOURCES)} monitored sources...")

    results = []
    changed_count = 0

    for source_key, source_info in MONITORED_SOURCES.items():
        result = check_source_for_changes(source_key, source_info)
        results.append(result)
        if result.get("changed"):
            changed_count += 1

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_sources": len(MONITORED_SOURCES),
        "changed": changed_count,
        "results": results,
    }

    if changed_count > 0:
        logger.warning(f"{changed_count} sources have changed - review scorecard!")
    else:
        logger.info("No changes detected in monitored sources")

    return report


def check_country_sources(country: str) -> List[Dict[str, Any]]:
    """
    Check all source URLs for a specific country.

    Args:
        country: Country name

    Returns:
        List of check results for each source URL
    """
    all_urls = extract_all_source_urls()
    country_urls = [u for u in all_urls if u["country"].lower() == country.lower()]

    results = []
    for url_info in country_urls:
        content = fetch_page_content(url_info["url"])
        results.append(
            {
                **url_info,
                "reachable": content is not None,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    return results


def find_stale_entries(max_age_days: int = 365) -> List[Dict[str, Any]]:
    """
    Find scorecard entries that may be stale based on source URL dates.

    This is a heuristic check - looks for year patterns in URLs/values
    and flags entries where the cited year is old.

    Args:
        max_age_days: Days after which an entry is considered stale

    Returns:
        List of potentially stale entries
    """
    df = load_scorecard()
    current_year = datetime.now().year
    stale = []

    year_pattern = re.compile(r"\b(20[0-2][0-9])\b")

    for _, row in df.iterrows():
        country = row.get("Country")

        for col in df.columns:
            if "_Source" in col or col in ["Country", "RowNumber"]:
                continue

            value = str(row.get(col, ""))
            matches = year_pattern.findall(value)

            if matches:
                cited_year = max(int(y) for y in matches)
                if current_year - cited_year >= 2:  # 2+ years old
                    stale.append(
                        {
                            "country": country,
                            "indicator": col,
                            "value": value[:200],  # Truncate
                            "cited_year": cited_year,
                            "age_years": current_year - cited_year,
                        }
                    )

    return stale


def save_diff_report(report: Dict[str, Any], filepath: str = None) -> str:
    """Save diff report to JSON file."""
    logger = get_logger("scorecard_diff")
    filepath = filepath or DIFF_REPORT_FILE

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved diff report to {filepath}")
    return filepath


def run_diff_check(save_report: bool = True) -> Dict[str, Any]:
    """
    Run full diff check on monitored sources and stale entries.

    Args:
        save_report: Whether to save report to disk

    Returns:
        Combined diff report
    """
    logger = get_logger("scorecard_diff")

    # Check monitored sources
    source_report = check_all_monitored_sources()

    # Find stale entries
    stale_entries = find_stale_entries()

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_changes": source_report,
        "stale_entries": {
            "count": len(stale_entries),
            "entries": stale_entries[:50],  # Limit output size
        },
    }

    if save_report:
        save_diff_report(report)

    logger.info(
        f"Diff check complete: {source_report['changed']} sources changed, "
        f"{len(stale_entries)} potentially stale entries"
    )

    return report


# CLI entry point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Check scorecard sources for changes and stale data"
    )
    parser.add_argument(
        "--country",
        type=str,
        help="Check sources for a specific country",
    )
    parser.add_argument(
        "--sources-only",
        action="store_true",
        help="Only check monitored sources, skip stale entry detection",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save report to disk",
    )
    args = parser.parse_args()

    from processors.logger import set_run_logfile

    set_run_logfile("scorecard_diff_check")

    if args.country:
        results = check_country_sources(args.country)
        print(json.dumps(results, indent=2))
    elif args.sources_only:
        report = check_all_monitored_sources()
        if not args.no_save:
            save_diff_report(report)
        print(json.dumps(report, indent=2))
    else:
        report = run_diff_check(save_report=not args.no_save)
        print(
            f"\nSummary: {report['source_changes']['changed']} sources changed, "
            f"{report['stale_entries']['count']} potentially stale entries"
        )
