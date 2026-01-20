# System Architecture

This document provides a high-level overview of the DigitalChild pipeline architecture.

## 🎯 Purpose

DigitalChild is a data pipeline that:

1. **Scrapes** human rights documents from international organizations
2. **Processes** documents into structured, analyzable text
3. **Analyzes** content using regex-based tagging and enrichment
4. **Enriches** with country-level indicators via scorecard system
5. **Exports** analysis results for research use

**Focus:** Child and LGBTQ+ digital rights, with particular emphasis on AI policy, data protection, and online safety.

## 🏗️ High-Level Architecture

```
┌─────────────┐
│   SOURCES   │  (Web: AU, OHCHR, UPR, UNICEF, etc.)
└──────┬──────┘
       │ HTTP/Selenium
       ▼
┌─────────────┐
│  SCRAPERS   │  (Download PDFs, DOCX, HTML)
└──────┬──────┘
       │ Files
       ▼
┌─────────────┐
│  data/raw/  │  (Raw documents by source)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PROCESSORS  │  (PDF→text, DOCX→text, HTML→text)
└──────┬──────┘
       │ Text files
       ▼
┌─────────────┐
│data/process │  (Extracted text by region/org)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   TAGGER    │  (Apply regex rules from configs)
└──────┬──────┘
       │ Tags
       ▼
┌─────────────┐
│ METADATA    │  (metadata.json with tags_history)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ENRICHER   │  (Add scorecard indicators)
└──────┬──────┘
       │ Enriched metadata
       ▼
┌─────────────┐
│  EXPORTERS  │  (Generate CSV summaries)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│data/exports │  (CSV files for analysis)
└─────────────┘
```

## 📦 Core Components

### 1. Pipeline Runner

**File:** `pipeline_runner.py`

**Responsibilities:**

- Orchestrates entire workflow
- Handles CLI arguments
- Manages logging
- Supports 3 modes:
  - `scraper` - Run scrapers, process, tag, export
  - `urls` - Process from static URL dictionaries
  - `scorecard` - Enrich/export/validate scorecard data

**Entry Point:**

```bash
python pipeline_runner.py --source au_policy --tags-version latest
```

### 2. Scrapers (`scrapers/`)

**Purpose:** Fetch documents from web sources

**Structure:**

- Each source has its own module (e.g., `au_policy.py`)
- Two variants: requests-based and Selenium (`_sel` suffix)
- Implements standard `scrape()` function
- Outputs to `data/raw/<source>/`

**Example Sources:**

- `au_policy` - African Union policy documents
- `ohchr` - OHCHR Treaty Body database
- `upr` - Universal Periodic Review documents
- `unicef` - UNICEF reports
- `acerwc` - African Committee on Child Rights
- `achpr` - African Commission on Human Rights

**Key Features:**

- Skip existing files (idempotent)
- Configurable timeouts and retry logic
- Logging for all operations
- Error handling and graceful failures

### 3. Processors (`processors/`)

**Purpose:** Convert documents to analyzable text

**Modules:**

- `pdf_to_text.py` - Extract text from PDFs (PyPDF2)
- `docx_to_text.py` - Extract text from Word docs (python-docx)
- `html_to_text.py` - Extract text from HTML (BeautifulSoup4)
- `fallback_handler.py` - Try processors until one succeeds

**Output:** Text files in `data/processed/<region>/<org>/text/`

### 4. Tagger (`processors/tagger.py`)

**Purpose:** Apply regex-based tags to documents

**How it works:**

1. Load tag config (e.g., `configs/tags_v3.json`)
2. Apply regex patterns to text
3. Record matched tags
4. Store in `metadata.json` with version and timestamp

**Tags include:**

- ChildRights, LGBTQ, AI, Privacy
- DigitalPolicy, OnlineRights, DataProtection
- And more (expandable via configs)

**Versioning:**

- Multiple tag versions (v1, v2, v3, digital)
- `tags_main.json` maps version aliases
- Tags history preserves all versions for comparison

### 5. Scorecard System

**Purpose:** Enrich documents with country-level indicators

**Components:**

#### A. **Data Loader** (`processors/scorecard.py`)

- Loads `scorecard_main.xlsx` (194 countries, 10 indicators)
- Provides query functions
- Caches data in memory

#### B. **Enricher** (`processors/scorecard_enricher.py`)

- Matches documents to countries
- Adds indicator data to metadata
- Tracks enrichment timestamp

#### C. **Exporter** (`processors/scorecard_export.py`)

- Exports to CSV formats:
  - Summary (countries × indicators)
  - Sources (all source URLs)
  - By indicator
  - By region

#### D. **Validator** (`processors/scorecard_validator.py`)

- Validates 2,543 source URLs
- Parallel workers for performance
- Retry logic for transient failures
- Generates broken links report

#### E. **Diff Monitor** (`processors/scorecard_diff.py`)

- Monitors sources for changes
- Content hashing for comparison
- Detects stale data

**10 Indicators Tracked:**

1. AI_Policy_Status
2. Data_Protection_Law
3. LGBTQ_Legal_Status
4. Child_Online_Protection
5. SIM_Biometric
6. Encryption_Backdoors
7. Promotion_Propaganda
8. DPA_Independence
9. Content_Moderation
10. Age_Verification

### 6. Validators (`processors/validators.py`)

**Purpose:** Centralized input validation and security

**Functions:**

- URL validation (blocks malicious patterns)
- Path validation (prevents traversal attacks)
- File validation (size, extension checks)
- String validation (length, patterns)
- Config validation (JSON structure)
- Schema validation (metadata documents)

**Security:** Protects against:

- Path traversal (e.g., `../../../etc/passwd`)
- Malicious URLs (e.g., `javascript:`, `file:`)
- File bombs (size limits)
- Invalid configs

### 7. Metadata System

**File:** `data/metadata/metadata.json`

**Structure:**

```json
{
  "project_identity": {...},
  "documents": [
    {
      "id": "doc-123.pdf",
      "source": "au_policy",
      "country": "Kenya",
      "year": 2024,
      "tags_history": [...],
      "recommendations_history": [...],
      "scorecard": {...},
      "last_processed": "2025-01-19T10:00:00Z"
    }
  ]
}
```

**Tracking:**

- Document metadata (source, country, year)
- Tags history (versions, timestamps)
- Recommendations (future)
- Scorecard indicators
- Processing timestamps

### 8. Logging System (`processors/logger.py`)

**Features:**

- Unified run logs
- Per-module logs (optional)
- Timestamped filenames
- Console + file output
- Configurable via `--no-module-logs`

**Levels:**

- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Non-recoverable failures

## 🔄 Data Flow

### Standard Pipeline Execution

```
1. User runs: python pipeline_runner.py --source au_policy

2. Pipeline Runner:
   - Initializes logging
   - Loads SCRAPER_MAP configuration
   - Determines source and output paths

3. Scraper Phase:
   - Downloads documents to data/raw/au_policy/
   - Skips existing files
   - Returns list of file paths

4. Processing Phase:
   For each downloaded file:
   - Detect file type (PDF, DOCX, HTML)
   - Convert to text → data/processed/Africa/AU/text/
   - Extract metadata (year, country from filename/content)

5. Tagging Phase:
   - Load tag config (tags_v3.json)
   - Apply regex rules to each document
   - Store tags in metadata.json

6. Export Phase:
   - Generate tags_summary.csv
   - Count tag frequencies
   - Add project branding footer

7. Logging:
   - Write unified log to logs/<timestamp>_au_policy_run.log
   - Optional per-module logs
```

### Scorecard Workflow

```
1. User runs: python pipeline_runner.py --mode scorecard --scorecard-action all

2. Enrich:
   - Load metadata.json
   - Load scorecard_main.xlsx
   - Match documents to countries
   - Add indicators to metadata
   - Save updated metadata.json

3. Export:
   - Generate scorecard_summary.csv
   - Generate scorecard_sources.csv
   - Generate indicator-specific CSVs

4. Validate:
   - Load all source URLs (2,543)
   - Validate in parallel (10 workers)
   - Generate validation report
   - Create broken links CSV

5. Diff (optional):
   - Fetch monitored sources
   - Compare content hashes
   - Detect changes
   - Generate diff report
```

## 🔌 Extensibility Points

### Adding a New Scraper

1. Create `scrapers/new_source.py`
2. Implement `scrape()` function
3. Add to `SCRAPER_MAP` in `pipeline_runner.py`
4. Add tests in `tests/test_new_source.py`

**Template:**

```python
def scrape(base_url=None, countries=None):
    """Download documents. Returns list of file paths."""
    # Implementation
    return downloaded_files
```

### Adding a New Processor

1. Create `processors/new_processor.py`
2. Implement `convert(input_path, output_dir)` function
3. Update `fallback_handler.py` if needed
4. Add tests

### Adding New Tags

1. Edit `configs/tags_vX.json`
2. Add new tag categories and regex patterns
3. Update version in `configs/tags_main.json`
4. Run tagging: `python pipeline_runner.py --tags-version vX`

### Adding Scorecard Indicators

1. Edit `scorecard_main.xlsx`
2. Add new column for indicator
3. Add source URLs
4. Update `INDICATOR_COLUMNS` in `processors/scorecard.py`
5. Re-run enrichment

## 🧪 Testing Strategy

**Test Suite:** 124 tests covering:

- 68 validator tests (comprehensive security checks)
- 20 scorecard tests (load, enrich, export, validate)
- 36 other tests (tagger, processors, metadata, logging)

**Test Organization:**

```
tests/
├── test_validators.py      # Input validation
├── test_scorecard.py        # Scorecard system
├── test_tagger.py           # Tagging logic
├── test_metadata.py         # Metadata operations
├── test_logging.py          # Logging system
├── test_fallback_handler.py # Multi-format processing
└── conftest.py              # Pytest configuration
```

**Run tests:**

```bash
pytest tests/ -v                    # All tests
pytest tests/test_validators.py -v # Specific module
pytest tests/ --cov                 # With coverage
```

## 📊 Performance Considerations

### Bottlenecks

1. **Scraping:** Network I/O bound
   - Mitigated by: Timeouts, skip existing files

2. **PDF Processing:** CPU bound
   - Mitigated by: Fallback handler, efficient PyPDF2 usage

3. **URL Validation:** Network I/O bound
   - Mitigated by: Parallel workers (10 concurrent), caching

### Scalability

**Current scale:**

- 194 countries
- 2,543 source URLs
- 7 data sources
- Processing hundreds of documents

**Future scale:** System designed to handle thousands of documents with:

- Incremental processing (skip processed files)
- Efficient caching
- Modular architecture

### Optimization Opportunities

- [ ] Database instead of JSON (PostgreSQL for metadata)
- [ ] Async scrapers (aiohttp)
- [ ] Distributed processing (Celery)
- [ ] Content delivery network (CDN for exports)

## 🔐 Security Architecture

### Input Validation

All external inputs validated through `validators.py`:

- URLs validated before HTTP requests
- File paths validated before file operations
- Configs validated before loading

### Attack Surface

**Minimized by:**

- No user authentication (static site deployment)
- No database (JSON-based metadata)
- No eval/exec of untrusted code
- Sandboxed scraping (timeout limits)

**Protected against:**

- Path traversal attacks
- Malicious URL injection
- File upload vulnerabilities
- XSS (no dynamic web content)

## 🌍 Deployment Architecture

### Development

```
Local Machine
├── Python 3.12 virtual environment
├── Git repository
├── Pre-commit hooks
└── Pytest for testing
```

### Production (Planned)

```
GitHub Repository
├── GitHub Actions (CI/CD)
│   ├── Run tests
│   ├── Check code quality
│   └── Deploy docs
├── GitHub Pages (Static site)
│   ├── MkDocs-generated docs
│   ├── Scorecard visualizations
│   └── Custom domain (GRIMdata.org)
└── Data Files (Gitignored)
    ├── Scraped documents
    ├── Processed text
    └── Export CSVs
```

## 📚 Technology Stack

**Core:**

- Python 3.12
- BeautifulSoup4 (HTML parsing)
- Selenium (dynamic scraping)
- pandas (data manipulation)
- PyPDF2 (PDF processing)

**Testing:**

- pytest
- pytest-cov
- pre-commit hooks

**Code Quality:**

- black (formatting)
- isort (import sorting)
- flake8 (linting)
- mdformat (markdown)

**Documentation:**

- MkDocs (site generation)
- Material theme
- 25 markdown files

**Deployment:**

- GitHub Pages
- Custom domains
- Automatic SSL

## 🔮 Future Architecture

### Phase 3: Advanced Processing

- Recommendations extraction (NLP-based)
- Timeline analysis
- Comparison across versions

### Phase 4: Research Dashboard

- Flask backend (REST API)
- React/Vue frontend
- Interactive visualizations (D3.js, Plotly)
- Database migration (PostgreSQL)

### Phase 5: Global Expansion

- Multi-language support
- Additional regions (Europe, Asia, Americas)
- Machine learning for classification
- Automated report generation

## 🤝 Integration Points

### External Systems

**Currently integrates with:**

- GitHub (version control, CI/CD)
- Public data sources (AU, OHCHR, UPR, etc.)

**Planned integrations:**

- Zotero (citation management)
- SPARQL endpoints (semantic queries)
- Research databases

### APIs

**Current:** None (CLI-based)

**Planned:** REST API for:

- `/api/documents` - Search and filter
- `/api/scorecard` - Query indicators
- `/api/export` - Download datasets

## 📖 Further Reading

- **[PIPELINE_FLOW.md](notes/PIPELINE_FLOW.md)** - Detailed pipeline flow
- **[DIRECTORY_STRUCTURE.md](notes/DIRECTORY_STRUCTURE.md)** - File organization
- **[METADATA_SCHEMA.md](standards/METADATA_SCHEMA.md)** - Metadata structure
- **[SCORECARD_WORKFLOW.md](SCORECARD_WORKFLOW.md)** - Scorecard system details
- **[VALIDATORS_USAGE.md](VALIDATORS_USAGE.md)** - Validation framework

---

**Last updated:** January 2026
