# Tagger placeholder
"""
Tagger
------
Simple regex-based tagging using external config.
"""

import json
import re
from processors.logger import get_logger

logger = get_logger("tagger")


def load_tags(config_file="../configs/tags_v1.json"):
    """
    Load tag rules from a JSON config file.
    Returns dict with { "rules": {tag: [patterns...] } }
    """
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load tag config {config_file}: {e}")
        return {"rules": {}}


def apply_tags(text, config_file="../configs/tags_v1.json"):
    """
    Apply regex-based tag rules to text.
    Returns a list of tags matched.
    """
    tags = []
    config = load_tags(config_file)
    for tag, patterns in config.get("rules", {}).items():
        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                tags.append(tag)
                break
    if tags:
        logger.info(f"Matched tags: {tags}")
    else:
        logger.warning("No tags matched")
    return tags
