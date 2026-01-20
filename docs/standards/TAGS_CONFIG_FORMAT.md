# Tags Config Format

This document explains how tag configuration files (e.g., tags_v1.json, tags_v2.json) are structured.

______________________________________________________________________

## Purpose

- Define regex/keyword rules to identify mentions of children, LGBTQ, AI, privacy, etc.
- Each version expands or refines the rules.
- Allows comparison between versions for research purposes.

______________________________________________________________________

## Fields

- `rules`: dictionary mapping tag name → list of regex/keyword patterns

______________________________________________________________________

## Example

```json
{
  "rules": {
    "ChildRights": [
      "child",
      "children",
      "youth",
      "minor",
      "adolescent"
    ],
    "LGBTQ": [
      "lgbt",
      "lgbti",
      "lgbtq",
      "sexual orientation",
      "gender identity",
      "queer"
    ],
    "AI": [
      "artificial intelligence",
      "\\bAI\\b",
      "machine learning",
      "algorithm"
    ]
  }
}
```
