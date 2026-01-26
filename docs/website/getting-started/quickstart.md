# Quick Start

Get started with DigitalChild in 5 minutes.

!!! tip "🚀 Fastest Way: Use the API"
    **Don't want to run the pipeline?** Access data directly via REST API:

    ```bash
    pip install -r api_requirements.txt
    python run_api.py
    ```

    Then query data:
    ```bash
    curl http://localhost:5000/api/documents
    curl http://localhost:5000/api/scorecard/Kenya
    ```

    [:octicons-rocket-24: Full API Guide](../../api/README/){ .md-button .md-button--primary }

---

## Prerequisites

Ensure you've [installed](installation.md) DigitalChild and activated your virtual environment.

## Your First Pipeline Run

### Step 1: Basic Run

Run the pipeline on African Union policy documents:

```bash
python pipeline_runner.py --source au_policy
```

This will:

1. ✅ Scrape AU policy documents (or skip if already downloaded)
1. ✅ Process PDFs to extract text
1. ✅ Apply tags using default tag configuration
1. ✅ Generate exports in `data/exports/`

Expected output:

```terminal
[INFO] Starting pipeline for source: au_policy
[INFO] Scraping documents...
[INFO] Found 12 documents
[INFO] Processing documents...
[INFO] Tagging documents...
[INFO] Generating exports...
[INFO] Pipeline complete!
```

### Step 2: View Results

Check the exports:

```bash
ls data/exports/
```

You'll find:

- `tags_summary.csv` - Tag frequencies and document counts
- `metadata_export.csv` - All document metadata

Open in Excel, Google Sheets, or analyze with pandas:

```python
import pandas as pd

df = pd.read_csv('data/exports/tags_summary.csv')
print(df.head())
```

### Step 3: Explore Metadata

View processed documents:

```bash
# See metadata
cat data/metadata/metadata.json | python -m json.tool | head -50

# See processed text
ls data/processed/Africa/AU/text/
```

## Access Data via API (Alternative)

**NEW:** Instead of running the pipeline, you can access the data programmatically via the REST API:

```bash
# Start the API server
python run_api.py
```

Then access data via HTTP requests:

```bash
# Health check
curl http://localhost:5000/api/health

# List all documents
curl http://localhost:5000/api/documents

# Filter documents by country
curl "http://localhost:5000/api/documents?country=Kenya"

# Get scorecard summary
curl http://localhost:5000/api/scorecard

# Get country scorecard
curl http://localhost:5000/api/scorecard/Kenya
```

Or use Python:

```python
import requests

# Get documents filtered by country
response = requests.get("http://localhost:5000/api/documents?country=Kenya")
documents = response.json()["data"]["items"]

# Get scorecard for Kenya
response = requests.get("http://localhost:5000/api/scorecard/Kenya")
scorecard = response.json()["data"]
print(scorecard["indicators"])
```

See [API Documentation](../../../api/README/) for all 14 endpoints and features.

## Common Use Cases

### Process Specific Country (UPR)

```bash
python pipeline_runner.py --source upr --country kenya
```

This scrapes and processes UPR (Universal Periodic Review) documents for Kenya specifically.

### Use Latest Tags

```bash
python pipeline_runner.py --source au_policy --tags-version latest
```

The `latest` version points to the most recent tag configuration (currently `tags_v3`). Other versions available: `v1`, `v2`, `v3`, `digital`, `queerai`.

### Run Scorecard Workflow

```bash
python pipeline_runner.py --mode scorecard --scorecard-action all
```

This:

1. Enriches metadata with country-level indicators
1. Exports scorecard summaries
1. Validates all 2,543 source URLs

Results appear in `data/exports/scorecard_*.csv`.

### Process Multiple Sources

```bash
# AU Policy
python pipeline_runner.py --source au_policy

# OHCHR
python pipeline_runner.py --source ohchr

# UNICEF
python pipeline_runner.py --source unicef
```

Each source has unique scraping logic for that organization's website.

## Understanding the Pipeline

### Data Flow

```txt
┌─────────────────┐
│   WEB SOURCES   │ (AU, OHCHR, UPR, UNICEF)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    SCRAPERS     │ Download PDFs/DOCX/HTML
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   data/raw/     │ Store downloaded files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PROCESSORS    │ Extract text
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ data/processed/ │ Store text files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     TAGGER      │ Apply regex rules
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    METADATA     │ metadata.json with tags history
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    EXPORTS      │ CSV files for analysis
└─────────────────┘
```

### File Locations

After running the pipeline:

| Path                             | Contents                    |
| -------------------------------- | --------------------------- |
| `data/raw/au_policy/`            | Downloaded PDF files        |
| `data/processed/Africa/AU/text/` | Extracted text files        |
| `data/metadata/metadata.json`    | Document metadata with tags |
| `data/exports/tags_summary.csv`  | Tag analysis                |
| `logs/`                          | Run logs with timestamps    |

## Pipeline Modes

The pipeline has 3 modes:

=== "scraper (default)"

````
**Complete workflow:** Scrape → Process → Tag → Export

```bash
python pipeline_runner.py --source au_policy
```
````

=== "urls"

````
**From static URLs:** Process from `configs/url_dict/*.json`

```bash
python pipeline_runner.py --mode urls --source upr
```
````

=== "scorecard"

````
**Indicator workflow:** Enrich → Export → Validate

```bash
python pipeline_runner.py --mode scorecard --scorecard-action all
```
````

## Command Reference

### Required Arguments

| Argument   | Description      | Example                     |
| ---------- | ---------------- | --------------------------- |
| `--source` | Data source name | `au_policy`, `upr`, `ohchr` |

### Optional Arguments

| Argument             | Description             | Example                               |
| -------------------- | ----------------------- | ------------------------------------- |
| `--tags-version`     | Tag config version      | `latest`, `v3`, `v2`                  |
| `--mode`             | Pipeline mode           | `scraper`, `urls`, `scorecard`        |
| `--country`          | Filter by country       | `kenya`, `south_africa`               |
| `--scorecard-action` | Scorecard action        | `enrich`, `export`, `validate`, `all` |
| `--no-module-logs`   | Disable per-module logs | (flag, no value)                      |

### Examples

```bash
# Minimal
python pipeline_runner.py --source au_policy

# With tags version
python pipeline_runner.py --source upr --tags-version v3

# Country-specific
python pipeline_runner.py --source upr --country kenya

# Scorecard only
python pipeline_runner.py --mode scorecard --scorecard-action enrich

# URLs mode
python pipeline_runner.py --mode urls --source upr
```

## Supported Sources

| Source      | Description                             | Documents       |
| ----------- | --------------------------------------- | --------------- |
| `au_policy` | African Union policy documents          | ~10-15          |
| `ohchr`     | OHCHR Treaty Body database              | Hundreds        |
| `upr`       | Universal Periodic Review (per country) | ~50 per country |
| `unicef`    | UNICEF reports                          | Varies          |
| `acerwc`    | African Committee on Child Rights       | ~20-30          |
| `achpr`     | African Commission on Human Rights      | ~30-40          |
| `manual`    | Manual uploads to `data/raw/manual/`    | User-provided   |

## Next Steps

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } **Learn More**

    ---

    Dive deeper into pipeline operations

    [:octicons-arrow-right-24: Read Runbook](../../guides/RUNBOOK.md)

-   :material-tag-multiple:{ .lg .middle } **Customize Tags**

    ---

    Add your own tag patterns

    [:octicons-arrow-right-24: Tags Config Format](../../standards/TAGS_CONFIG_FORMAT.md)

-   :material-chart-bar:{ .lg .middle } **Explore Scorecard**

    ---

    Understand country indicators

    [:octicons-arrow-right-24: Scorecard Workflow](../../guides/SCORECARD_WORKFLOW.md)

-   :material-cog:{ .lg .middle } **Add Scrapers**

    ---

    Build scrapers for new sources

    [:octicons-arrow-right-24: Scraper Structure](../../standards/SCRAPER_STRUCTURE.md)

</div>

## Troubleshooting

!!! failure "No documents found"
    Check if documents already exist in `data/raw/<source>/`. The pipeline skips existing files. Delete to re-scrape.

!!! failure "Import errors"
    Ensure you're running from project root, not from subdirectories. Use absolute paths if needed.

!!! failure "Processing failed"
    Check `logs/` for error details. Some PDFs may be scanned images (no text layer) and will fail.

!!! failure "Tags summary empty"
    Verify documents have text content. Check `data/processed/` for .txt files.

See [First Run Errors](../../guides/FIRST_RUN_ERRORS.md) for comprehensive troubleshooting.

## Pro Tips

!!! tip "Incremental Processing"
    The pipeline skips already-downloaded files. Run again to only process new documents.

!!! tip "Parallel Analysis"
    Export CSV files can be analyzed in parallel with R, Python, Excel, or Tableau.

!!! tip "Custom Tags"
    Edit `configs/tags_v3.json` to add your own regex patterns. Re-run with `--tags-version v3`.

!!! tip "Version Control"
    Tags history preserves all tagging operations. Compare results across tag versions using metadata.

## Getting Help

- **Documentation:** [Full docs index](../../DOCS_INDEX.md)
- **FAQ:** [Common questions](../../FAQ.md)
- **Issues:** [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)

Happy analyzing! 🌈
