# Recommendations extraction test
import json
import os

from processors import recommendations


def test_recommendations_regex(tmp_path):
    # Create a temporary recommendations config
    recs_config = tmp_path / "recs_v1.json"
    config = {
        "version": "recs_v1",
        "strategy": "regex",
        "rules": ["The Committee recommends", "should adopt", "urges the State Party"],
    }
    with open(recs_config, "w", encoding="utf-8") as f:
        json.dump(config, f)

    # Sample text with recommendations
    text = """
    The Committee recommends that the State Party should adopt stronger protections.
    It also urges the State Party to provide resources.
    """

    matches = recommendations.apply_recommendations(text, str(recs_config))

    assert "The Committee recommends" in matches
    assert "should adopt" in matches
    assert "urges the State Party" in matches
    assert len(matches) >= 3
