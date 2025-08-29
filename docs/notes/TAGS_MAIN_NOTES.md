# Tags Main Notes

This document explains how `tags_main.json` manages multiple versions of tag configs.

---

## Purpose

- Central mapping of version labels to config files.
- Ensures reproducibility: old runs can be compared even after new configs are added.
- Provides a `latest` alias so the pipeline can always grab the newest version.

---

## Example

```json
{
  "versions": {
    "v1": "tags_v1.json",
    "v2": "tags_v2.json",
    "v3": "tags_v3.json",
    "digital": "tags_digital.json",
    "latest": "tags_v3.json"
  },
  "notes": "tags_main.json tracks multiple tag sets. Update 'latest' when adding new versions."
}
```

---

## Notes

- Do not remove older versions.
- Add new versions sequentially (`v4`, etc.).
- Update the `latest` pointer.
