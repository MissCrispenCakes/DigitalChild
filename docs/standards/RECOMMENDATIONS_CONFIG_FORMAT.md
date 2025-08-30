# Recommendations Config Format

This document explains the format for configuration files that drive
recommendations extraction from documents.

---

## Purpose

Recommendations may be extracted using multiple strategies:

- Regex rules
- NLP keyword spotting
- ML models (future extension)

Configs define which strategy to use and how to apply it.

---

## Fields

- `version`: version name of the config
- `rules`: list of rules (regex patterns, keywords, or other strategies)
- `strategy`: method used (`regex`, `keywords`, `nlp`)
- `notes`: optional description

---

## Example (Regex Strategy)

```json
{
  "version": "recs_v1",
  "strategy": "regex",
  "rules": [
    "The Committee recommends",
    "should adopt",
    "urges the State Party",
    "calls upon the Government"
  ],
  "notes": "Regex strategy for treaty body concluding observations."
}
```
