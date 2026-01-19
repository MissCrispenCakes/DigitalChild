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


def load_tags(config_file=None):
    """
    Load tag rules from a JSON config file.
    Returns dict with { "rules": {tag: [patterns...] } }
    """
    if config_file is None:
        config_file = "configs/tags_v1.json"
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Tag config file not found: {config_file}")
        return {"rules": {}}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in tag config {config_file}: {e}")
        return {"rules": {}}
    except PermissionError:
        logger.error(f"Permission denied reading tag config: {config_file}")
        return {"rules": {}}
    except Exception as e:
        logger.error(
            f"Unexpected error loading tag config {config_file}: {type(e).__name__}: {e}"
        )
        return {"rules": {}}


def apply_tags(text, config_file=None):
    """
    Apply regex-based tag rules to text.
    Returns a list of tags matched.
    """
    if config_file is None:
        config_file = "configs/tags_v1.json"
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
