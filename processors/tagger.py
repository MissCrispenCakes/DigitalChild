# Tagger placeholder
"""
Tagger
------
Simple regex-based tagging using external config.
"""

import re

from processors.logger import get_logger
from processors.validators import (
    ConfigValidationError,
    validate_json_file,
    validate_regex_pattern,
)

logger = get_logger("tagger")


def load_tags(config_file=None):
    """
    Load tag rules from a JSON config file.
    Returns dict with { "rules": {tag: [patterns...] } }
    """
    if config_file is None:
        config_file = "configs/tags_v1.json"
    try:
        config = validate_json_file(config_file)
        # Validate patterns are valid regexes
        for tag_name, patterns in config.get("rules", {}).items():
            for i, pattern in enumerate(patterns):
                try:
                    validate_regex_pattern(pattern, f"tag '{tag_name}' pattern {i}")
                except Exception as e:
                    logger.warning(f"Invalid regex {pattern} for tag {tag_name}: {e}")
        return config
    except ConfigValidationError as e:
        logger.error(f"Config validation error for {config_file}: {e}")
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
