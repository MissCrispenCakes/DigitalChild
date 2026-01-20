# Source Feasibility Checklist

This checklist helps determine whether a source can be scraped or must be ingested manually.

______________________________________________________________________

## Questions to Ask

1. **Is there a public URL or portal for the documents?**

   - Yes → proceed to scrape.
   - No → manual ingestion required.

1. **Does the site allow automated scraping?**

   - Check robots.txt and terms of service.
   - If blocked, use manual ingestion.

1. **Is there an API or bulk download option?**

   - If yes → preferred over scraping.

1. **Are documents PDFs, DOCX, HTML, or mixed?**

   - PDFs → use `pdf_to_text.py`.
   - DOCX → use `docx_to_text.py`.
   - HTML → use `html_to_text.py`.
   - Mixed → use `fallback_handler.py`.

1. **Do file names include year/country?**

   - Yes → easier metadata extraction.
   - No → rely on text scanning.

1. **Are there metadata pages (HTML tables, JSON endpoints)?**

   - Yes → scrape for structured metadata.
   - No → metadata must be inferred.

______________________________________________________________________

## Output of Feasibility Review

- `scrapable`: true/false
- `api_available`: true/false
- `file_formats`: list
- `obstacles`: notes
- `priority`: high/medium/low

______________________________________________________________________

## Example

- Source: OHCHR Treaty Body Database
- scrapable: true
- api_available: false
- file_formats: [pdf, docx]
- obstacles: pagination, session cookies
- priority: high
