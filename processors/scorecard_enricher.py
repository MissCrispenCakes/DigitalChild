"""
Scorecard Metadata Enricher
---------------------------
Enriches document metadata with scorecard indicators based on country.
Adds human rights policy/legal context to each document.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from processors.scorecard import (
    get_country_scorecard,
    get_all_indicators,
    load_scorecard,
    INDICATOR_COLUMNS,
)
from processors.logger import get_logger

METADATA_FILE = "data/metadata/metadata.json"


def load_metadata() -> Dict[str, Any]:
    """Load metadata.json."""
    if not os.path.exists(METADATA_FILE):
        return {"documents": []}
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(metadata: Dict[str, Any]) -> None:
    """Save metadata.json."""
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def enrich_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich a single document with scorecard indicators.
    
    Args:
        doc: Document metadata dict (must have 'country' or 'country_raw')
        
    Returns:
        Enriched document with 'scorecard' field
    """
    # Find country from various fields
    country = (
        doc.get("country")
        or doc.get("country_raw")
        or doc.get("Country")
    )
    
    if not country:
        return doc
    
    indicators = get_all_indicators(country)
    if not indicators:
        return doc
    
    # Add scorecard data
    doc["scorecard"] = {
        "country_matched": country,
        "enriched_at": datetime.now(timezone.utc).isoformat(),
        "indicators": indicators,
    }
    
    return doc


def enrich_all_metadata(save: bool = True) -> Dict[str, Any]:
    """
    Enrich all documents in metadata.json with scorecard indicators.
    
    Args:
        save: Whether to save updated metadata
        
    Returns:
        Enrichment statistics
    """
    logger = get_logger("scorecard_enricher")
    
    # Ensure scorecard is loaded
    load_scorecard()
    
    metadata = load_metadata()
    docs = metadata.get("documents", [])
    
    enriched_count = 0
    skipped_count = 0
    
    for doc in docs:
        country = doc.get("country") or doc.get("country_raw")
        if not country:
            skipped_count += 1
            continue
        
        indicators = get_all_indicators(country)
        if indicators:
            doc["scorecard"] = {
                "country_matched": country,
                "enriched_at": datetime.now(timezone.utc).isoformat(),
                "indicators": indicators,
            }
            enriched_count += 1
        else:
            skipped_count += 1
    
    if save:
        save_metadata(metadata)
        logger.info(f"Saved enriched metadata to {METADATA_FILE}")
    
    stats = {
        "total_documents": len(docs),
        "enriched": enriched_count,
        "skipped": skipped_count,
        "enriched_at": datetime.now(timezone.utc).isoformat(),
    }
    
    logger.info(
        f"Enrichment complete: {enriched_count} enriched, "
        f"{skipped_count} skipped out of {len(docs)} documents"
    )
    
    return stats


def get_documents_by_indicator(
    indicator: str,
    value_pattern: str = None,
) -> List[Dict[str, Any]]:
    """
    Find documents matching a scorecard indicator value.
    
    Args:
        indicator: Indicator name (e.g., "LGBTQ_Legal_Status")
        value_pattern: Optional substring to match in value
        
    Returns:
        List of matching documents
    """
    metadata = load_metadata()
    docs = metadata.get("documents", [])
    matches = []
    
    for doc in docs:
        scorecard = doc.get("scorecard", {})
        indicators = scorecard.get("indicators", {})
        
        if indicator in indicators:
            ind_data = indicators[indicator]
            value = ind_data.get("value", "")
            
            if value_pattern is None or value_pattern.lower() in str(value).lower():
                matches.append(doc)
    
    return matches


def generate_enrichment_summary() -> Dict[str, Any]:
    """
    Generate summary of enrichment coverage.
    
    Returns:
        Summary with counts per indicator coverage
    """
    metadata = load_metadata()
    docs = metadata.get("documents", [])
    
    indicator_counts = {col[0]: 0 for col in INDICATOR_COLUMNS}
    enriched_docs = 0
    
    for doc in docs:
        scorecard = doc.get("scorecard", {})
        indicators = scorecard.get("indicators", {})
        
        if indicators:
            enriched_docs += 1
            for ind_name in indicator_counts:
                if ind_name in indicators:
                    indicator_counts[ind_name] += 1
    
    return {
        "total_documents": len(docs),
        "documents_with_scorecard": enriched_docs,
        "indicator_coverage": indicator_counts,
    }


# CLI entry point
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Enrich document metadata with scorecard indicators"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't save changes, just show stats",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show enrichment summary only",
    )
    args = parser.parse_args()
    
    from processors.logger import set_run_logfile
    set_run_logfile("scorecard_enrichment")
    
    if args.summary:
        summary = generate_enrichment_summary()
        print(json.dumps(summary, indent=2))
    else:
        stats = enrich_all_metadata(save=not args.dry_run)
        print(json.dumps(stats, indent=2))
