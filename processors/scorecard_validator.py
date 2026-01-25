# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Scorecard URL Validator
-----------------------
Validates all source URLs in the scorecard by checking HTTP status.
Reports broken, redirected, or unreachable links.
"""

import concurrent.futures
import json
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict

import requests

from processors.logger import get_logger
from processors.scorecard import extract_all_source_urls
from processors.validators import URLValidationError
from processors.validators import validate_url as validate_url_format

# Output files
VALIDATION_REPORT_FILE = "data/exports/scorecard_url_validation.json"
BROKEN_LINKS_FILE = "data/exports/scorecard_broken_links.csv"

# Request settings
REQUEST_TIMEOUT = 15
MAX_WORKERS = 10
RETRY_COUNT = 2
USER_AGENT = "Mozilla/5.0 (compatible; DigitalChild-LinkChecker/1.0)"


def validate_url(url: str, timeout: int = REQUEST_TIMEOUT) -> Dict[str, Any]:
    """
    Check a single URL and return status information.

    Args:
        url: URL to validate
        timeout: Request timeout in seconds

    Returns:
        Dict with url, status_code, ok, redirected, final_url, error
    """
    result = {
        "url": url,
        "status_code": None,
        "ok": False,
        "redirected": False,
        "final_url": url,
        "error": None,
        "response_time_ms": None,
    }

    # Validate URL format before making request
    try:
        url = validate_url_format(url, allow_http=True)
    except URLValidationError as e:
        result["error"] = str(e)
        return result

    headers = {"User-Agent": USER_AGENT}

    for attempt in range(RETRY_COUNT):
        try:
            start = time.time()
            response = requests.head(
                url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True,
            )
            elapsed_ms = int((time.time() - start) * 1000)

            result["status_code"] = response.status_code
            result["response_time_ms"] = elapsed_ms
            result["ok"] = response.status_code < 400
            result["final_url"] = response.url
            result["redirected"] = response.url != url

            # Some servers don't like HEAD, try GET if we got 405
            if response.status_code == 405:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                    allow_redirects=True,
                    stream=True,  # Don't download body
                )
                response.close()
                result["status_code"] = response.status_code
                result["ok"] = response.status_code < 400
                result["final_url"] = response.url
                result["redirected"] = response.url != url

            return result

        except requests.exceptions.Timeout:
            result["error"] = "Timeout"
        except requests.exceptions.SSLError:
            result["error"] = "SSL Error"
        except requests.exceptions.ConnectionError as e:
            result["error"] = f"Connection Error: {str(e)[:100]}"
        except requests.exceptions.RequestException as e:
            result["error"] = f"Request Error: {str(e)[:100]}"

        if attempt < RETRY_COUNT - 1:
            time.sleep(1)  # Brief pause before retry

    return result


def validate_all_urls(
    max_workers: int = MAX_WORKERS,
    progress_callback=None,
) -> Dict[str, Any]:
    """
    Validate all source URLs from the scorecard.

    Args:
        max_workers: Number of parallel workers
        progress_callback: Optional callback(current, total) for progress

    Returns:
        Validation report with summary and per-URL results
    """
    logger = get_logger("scorecard_validator")

    # Extract all URLs
    url_records = extract_all_source_urls()
    total = len(url_records)
    logger.info(f"Validating {total} URLs from scorecard...")

    results = []
    completed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_record = {
            executor.submit(validate_url, rec["url"]): rec for rec in url_records
        }

        for future in concurrent.futures.as_completed(future_to_record):
            record = future_to_record[future]
            completed += 1

            try:
                url_result = future.result()
                results.append(
                    {
                        **record,
                        **url_result,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        **record,
                        "ok": False,
                        "error": str(e),
                    }
                )

            if progress_callback:
                progress_callback(completed, total)

            if completed % 50 == 0:
                logger.info(f"Progress: {completed}/{total} URLs checked")

    # Build summary
    ok_count = sum(1 for r in results if r.get("ok"))
    broken_count = sum(1 for r in results if not r.get("ok"))
    redirected_count = sum(1 for r in results if r.get("redirected"))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_urls": total,
        "ok": ok_count,
        "broken": broken_count,
        "redirected": redirected_count,
        "results": results,
    }

    logger.info(
        f"Validation complete: {ok_count} OK, {broken_count} broken, "
        f"{redirected_count} redirected"
    )

    return report


def save_validation_report(report: Dict[str, Any], filepath: str = None) -> str:
    """
    Save validation report to JSON file.

    Args:
        report: Validation report dict
        filepath: Output path (default: data/exports/scorecard_url_validation.json)

    Returns:
        Path to saved file
    """
    logger = get_logger("scorecard_validator")
    filepath = filepath or VALIDATION_REPORT_FILE

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved validation report to {filepath}")
    return filepath


def save_broken_links_csv(report: Dict[str, Any], filepath: str = None) -> str:
    """
    Export broken links to CSV for easy review.

    Args:
        report: Validation report dict
        filepath: Output path

    Returns:
        Path to saved file
    """
    logger = get_logger("scorecard_validator")
    filepath = filepath or BROKEN_LINKS_FILE

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    broken = [r for r in report.get("results", []) if not r.get("ok")]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("country,indicator,url,status_code,error\n")
        for r in broken:
            country = r.get("country", "").replace(",", ";")
            indicator = r.get("indicator", "")
            url = r.get("url", "")
            status = r.get("status_code", "")
            error = str(r.get("error", "")).replace(",", ";").replace("\n", " ")
            f.write(f'"{country}","{indicator}","{url}","{status}","{error}"\n')

    logger.info(f"Saved {len(broken)} broken links to {filepath}")
    return filepath


def run_validation(save_reports: bool = True) -> Dict[str, Any]:
    """
    Run full URL validation and optionally save reports.

    Args:
        save_reports: Whether to save JSON and CSV reports

    Returns:
        Validation report
    """
    report = validate_all_urls()

    if save_reports:
        save_validation_report(report)
        save_broken_links_csv(report)

    return report


# CLI entry point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate scorecard source URLs")
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_WORKERS,
        help=f"Number of parallel workers (default: {MAX_WORKERS})",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save reports to disk",
    )
    args = parser.parse_args()

    from processors.logger import set_run_logfile

    set_run_logfile("scorecard_url_validation")

    report = validate_all_urls(max_workers=args.workers)

    if not args.no_save:
        save_validation_report(report)
        save_broken_links_csv(report)

    print(
        f"\nSummary: {report['ok']} OK, {report['broken']} broken, "
        f"{report['redirected']} redirected out of {report['total_urls']} URLs"
    )
