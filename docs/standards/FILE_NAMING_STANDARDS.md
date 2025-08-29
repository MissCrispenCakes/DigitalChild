# File Naming Standards

Consistent file naming helps downstream processing and filtering.

---

## General Rules

- Use underscores `_` not spaces.
- Include year when available: `AU_AI_Strategy_2024.pdf`.
- Use PascalCase or underscores for multi-word titles.
- Avoid ambiguous suffixes like `final2`.

---

## Examples

✅ Good:

- `AU_Digital_Compact_2024.pdf`
- `Kenya_UPR_Report_2020.pdf`
- `Nigeria_CRC_Observation_2019.docx`

❌ Bad:

- `digital compact final.pdf`
- `Kenya report.doc`
- `doc1.pdf`

---

## Processing Notes

- Year extraction depends on `\d{4}` patterns.
- If no year in filename, pipeline scans document text.
- `_raw` field in metadata preserves original names.
