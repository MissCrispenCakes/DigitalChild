# Document Type Standards

This file defines how document types are categorized for processing.

______________________________________________________________________

## Major Types

- **Policy** → AU or state-level strategies, compacts, policies.
- **Law / Legislation** → Statutes, reforms, by-laws.
- **Treaty Body Reports** → OHCHR, CRC, CESCR, CCPR, etc.
- **UPR** → Universal Periodic Review documents.
- **Observations** → Concluding observations by treaty bodies.
- **Recommendations** → From committees or commissions.
- **Research / Reports** → UNICEF, ACERWC, ACHPR publications.

______________________________________________________________________

## Processing Implications

- All documents are normalized into text.
- Metadata field `"doc_type"` should capture type (if identified).
- Future processors may add automatic classification rules.

______________________________________________________________________

## File Formats

- `.pdf` → primary format, processed via `pdf_to_text.py`.
- `.docx` → supported, via `docx_to_text.py`.
- `.html` → supported, via `html_to_text.py`.
- `.txt` → may be ingested directly.
