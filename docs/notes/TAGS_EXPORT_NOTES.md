# Tags Export Notes

This document explains how to interpret tag summary exports.

---

## File Format

- CSV file with columns:
  - `tag` → the tag label
  - `count` → number of documents matching
  - `percentage_of_documents` → % of documents with this tag

---

## Conventions

- Counts are based on unique documents, not number of mentions.
- Percentages are relative to the number of processed documents.

---

## Example

```csv
tag,count,percentage_of_documents
ChildRights,3,100.0
LGBTQ,2,66.67
AI,2,66.67
Privacy,1,33.33
```

---

## Footer

- Every tags summary CSV ends with a branding footer:

```csv
Project: GRIMdata / LittleRainbowRights / ALLRainbowRights
Domains: https://GRIMdata.org | https://LittleRainbowRights.com | https://ALLRainbowRights.com
Note: This dataset is part of the pipeline for analyzing child & LGBTQ+ digital protections.
```
