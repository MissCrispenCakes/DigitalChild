"""
Recommendations Extractor
-------------------------
Extracts recommendations from documents using config-driven rules.
Supports regex or keyword strategies (initially regex/keywords).
"""

import json
import re

from processors.logger import get_logger

logger = get_logger("recommendations")


def load_recs(config_file="configs/recs_v1.json"):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load recommendations config {config_file}: {e}")
        return {"rules": [], "strategy": "regex"}


def apply_recommendations(text, config_file="configs/recs_v1.json"):
    config = load_recs(config_file)
    strategy = config.get("strategy", "regex")
    rules = config.get("rules", [])
    matches = []

    if strategy == "regex":
        for pattern in rules:
            found = re.findall(pattern, text, flags=re.IGNORECASE)
            if found:
                matches.extend(found)
    elif strategy == "keywords":
        for kw in rules:
            if kw.lower() in text.lower():
                matches.append(kw)

    if matches:
        logger.info(f"Extracted {len(matches)} recommendations (strategy={strategy})")
    else:
        logger.warning("No recommendations found")

    return list(set(matches))  # unique
