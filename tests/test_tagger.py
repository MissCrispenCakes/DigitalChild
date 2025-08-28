import pytest
from processors import tagger

SAMPLE_TEXT = """
This is a policy document mentioning children and youth.
It also discusses LGBT issues, artificial intelligence, and privacy concerns.
"""

def test_apply_tags_default_config(tmp_path):
    # Create a temporary tag config
    config_file = tmp_path / "tags.json"
    config_file.write_text(
        """
        {
          "rules": {
            "ChildRights": ["child", "children", "youth"],
            "LGBTQ": ["lgbt", "lgbti", "lgbtq"],
            "AI": ["artificial intelligence", "\\\\bAI\\\\b"],
            "Privacy": ["privacy", "data protection"]
          }
        }
        """,
        encoding="utf-8"
    )

    tags = tagger.apply_tags(SAMPLE_TEXT, str(config_file))
    assert "ChildRights" in tags
    assert "LGBTQ" in tags
    assert "AI" in tags
    assert "Privacy" in tags

def test_no_tags_match(tmp_path):
    config_file = tmp_path / "tags.json"
    config_file.write_text(
        """
        { "rules": { "Random": ["nonsense"] } }
        """,
        encoding="utf-8"
    )

    tags = tagger.apply_tags("No keywords here.", str(config_file))
    assert tags == []
