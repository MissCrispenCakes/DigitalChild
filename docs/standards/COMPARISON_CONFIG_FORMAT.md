# Comparison Config Format

This document defines how comparison configurations are structured.

---

## Purpose

Comparison configs define how two or more runs of the pipeline should
be compared, especially across different tagging or recommendation versions.

---

## Fields

- `versions`: list of versions to compare
- `order`: which order to show results (`tags_first`, `recs_first`)
- `output`: filename of CSV export
- `filters`: optional filter settings (region, country, tags)

---

## Example

```json
{
  "versions": ["v1", "v3"],
  "order": "tags_first",
  "output": "data/exports/comparison_export.csv",
  "filters": {
    "region": "Africa",
    "tags": ["ChildRights", "LGBTQ"]
  }
}
```
