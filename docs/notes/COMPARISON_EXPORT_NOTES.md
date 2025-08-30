# Comparison Export Notes

This document explains how to interpret CSV files produced by `comparison.py`.

---

## File Format

- Exported as CSV.
- Rows = documents.
- Columns = tags or recommendations under different versions.

---

## Conventions

- **Empty cell** → no match for that version.
- **Semicolon-separated values** → multiple tags or recommendations matched.

---

## Example

```csv
id,source,v1_tags,v3_tags
AU_AI_Strategy_2024.pdf,au_policy,"ChildRights;AI","ChildRights;AI;DigitalPolicy"
AU_Digital_Compact.pdf,au_policy,,"AI;DigitalPolicy;OnlineRights"
```

---

## Notes

- Always check `tags_master.json` or `recs_v1.json` to confirm which version sets were compared.
- `comparison.py` will also print a header note into the CSV with version info.
