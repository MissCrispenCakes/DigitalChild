______________________________________________________________________

🌍 Project Domains:

- https://GRIMdata.org
- https://LittleRainbowRights.com

______________________________________________________________________

# Pipeline Runbook

This runbook provides common commands for running the DigitalChild pipeline, tests, and maintenance tasks.

______________________________________________________________________

## Prerequisites

### First-Time Setup

```bash
# 1. Clone repository
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild

# 2. Create and activate virtual environment
python3 -m venv .LittleRainbow
source .LittleRainbow/bin/activate  # On Windows: .LittleRainbow\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize project structure
python init_project.py

# 5. Install pre-commit hooks (for development)
pip install pre-commit
pre-commit install
```

______________________________________________________________________

## Running the Pipeline

### Basic Pipeline Execution

```bash
# Run AU Policy scraper and full pipeline
python pipeline_runner.py --source au_policy

# Run with specific tags version (available: v1, v2, v3, digital, queerai)
python pipeline_runner.py --source au_policy --tags-version v3

# Run without module logs
python pipeline_runner.py --source au_policy --no-module-logs

# Process from static URL dictionary
python pipeline_runner.py --mode urls --source upr --country kenya
```

### Scorecard Operations

```bash
# Run all scorecard operations (enrich + export + validate)
python pipeline_runner.py --mode scorecard --scorecard-action all

# Just enrich metadata with scorecard data
python pipeline_runner.py --mode scorecard --scorecard-action enrich

# Just export scorecard CSVs
python pipeline_runner.py --mode scorecard --scorecard-action export

# Just validate scorecard URLs
python pipeline_runner.py --mode scorecard --scorecard-action validate

# Check for stale scorecard data
python pipeline_runner.py --mode scorecard --scorecard-action diff
```

### Direct Processor Calls

```bash
# Enrich metadata with scorecard indicators
python processors/scorecard_enricher.py

# Export scorecard data to CSV
python -c "from processors.scorecard_export import export_scorecard; export_scorecard()"

# Validate all scorecard source URLs
python processors/scorecard_validator.py

# Check for changes in monitored sources
python processors/scorecard_diff.py
```

______________________________________________________________________

## Testing

### Run All Tests

```bash
# Full test suite with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=processors --cov=scrapers --cov-report=term-missing

# Quick run (stop on first failure, quiet output)
pytest tests/ --maxfail=1 -q
```

### Run Specific Test Files

```bash
# Test validators module
pytest tests/test_validators.py -v

# Test scorecard functionality
pytest tests/test_scorecard.py -v

# Test tagging system
pytest tests/test_tagger.py -v

# Test metadata operations
pytest tests/test_metadata.py -v

# Test logging system
pytest tests/test_logging.py -v
```

### Run Specific Test Categories

```bash
# Test all processors
pytest tests/test_fallback_handler.py tests/test_metadata.py -v

# Test year extraction
pytest tests/test_year_extraction.py -v

# Test country/region normalization
pytest tests/test_country_region.py -v
```

______________________________________________________________________

## Code Quality

### Pre-commit Checks

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run specific hooks
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run isort --all-files

# Show diff on failures
pre-commit run --all-files --show-diff-on-failure
```

### Manual Formatting

```bash
# Format with black
black processors/ scrapers/ tests/ --line-length 88

# Sort imports with isort
isort processors/ scrapers/ tests/ --profile black

# Lint with flake8
flake8 processors/ scrapers/ tests/ --max-line-length=88
```

______________________________________________________________________

## Data Exploration

### Inspect Metadata

```bash
# View metadata file (formatted)
python -c "import json; print(json.dumps(json.load(open('data/metadata/metadata.json')), indent=2))"

# Count documents by source
python -c "import json; m=json.load(open('data/metadata/metadata.json')); from collections import Counter; print(Counter(d.get('source') for d in m.get('documents', [])))"

# List documents with scorecard data
python -c "import json; m=json.load(open('data/metadata/metadata.json')); print([d['id'] for d in m.get('documents', []) if 'scorecard' in d])"
```

### Check Exports

```bash
# List all export files
ls -lh data/exports/

# View tags summary
cat data/exports/tags_summary.csv | head -20

# View scorecard summary (first 10 countries)
cat data/exports/scorecard_summary.csv | head -11

# Count source URLs
wc -l data/exports/scorecard_sources.csv
```

### View Logs

```bash
# List recent logs
ls -lt logs/ | head -10

# Tail the most recent log
tail -f logs/*.log

# View specific module logs
cat logs/*scorecard_enricher.log

# Search for errors in logs
grep ERROR logs/*.log
```

______________________________________________________________________

## Scraper Operations

### Run Individual Scrapers

```bash
# AU Policy scraper
python -c "from scrapers.au_policy import scrape; scrape()"

# OHCHR scraper (if implemented)
python -c "from scrapers.ohchr import scrape; scrape()"

# UPR scraper (if implemented)
python -c "from scrapers.upr import scrape; scrape(country='kenya')"
```

### Check Downloaded Files

```bash
# List all raw files by source
ls -lh data/raw/*/

# Count files per source
for dir in data/raw/*/; do echo "$dir: $(ls -1 "$dir" | wc -l) files"; done

# Find largest files
find data/raw -type f -exec ls -lh {} \; | sort -k5 -hr | head -10
```

______________________________________________________________________

## Tagging Operations

### Apply Tags Manually

```bash
# Apply tags to text
python -c "from processors.tagger import apply_tags; text='child rights and AI policy'; print(apply_tags(text, 'configs/tags_v3.json'))"

# Load and view tags config
python -c "import json; print(json.dumps(json.load(open('configs/tags_v3.json')), indent=2))"

# Compare tag versions
python -c "from processors.tagger import apply_tags; text='child rights AI LGBTQ privacy'; print('v1:', apply_tags(text, 'configs/tags_v1.json')); print('v3:', apply_tags(text, 'configs/tags_v3.json'))"
```

______________________________________________________________________

## Validation

### Test URL Validation

```bash
# Test valid URL
python -c "from processors.validators import validate_url; print(validate_url('https://example.com'))"

# Test invalid URL (should raise error)
python -c "from processors.validators import validate_url; validate_url('not-a-url')" || echo "Correctly rejected"

# Test path traversal protection
python -c "from processors.validators import validate_path; validate_path('/tmp/../etc/passwd')" || echo "Correctly blocked"
```

### Run URL Validation on Scorecard

```bash
# Validate all scorecard URLs (parallel workers)
python processors/scorecard_validator.py --workers 10

# Validate without saving report
python processors/scorecard_validator.py --no-save
```

______________________________________________________________________

## Maintenance Tasks

### Clean Generated Files

```bash
# Remove all logs
rm -rf logs/*.log

# Remove all exports
rm -rf data/exports/*

# Remove processed files (keeps raw data)
rm -rf data/processed/*

# Reset metadata to empty state
python init_project.py  # Recreates structure
```

### Update Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade pandas
```

### Git Operations

```bash
# Check status
git status

# Stage all changes
git add .

# Commit with pre-commit hooks
git commit -m "Description of changes"

# Push to remote
git push origin basecamp

# Pull latest changes
git pull origin basecamp
```

______________________________________________________________________

## Troubleshooting

### Common Issues

**Import errors:**

```bash
# Ensure you're in project root
pwd  # Should show .../DigitalChild

# Verify virtual environment is activated
which python  # Should show .LittleRainbow/bin/python
```

**Missing dependencies:**

```bash
# Reinstall all requirements
pip install -r requirements.txt

# Check installed packages
pip list | grep -E "(pandas|requests|beautifulsoup4|PyPDF2|selenium)"
```

**Test failures:**

```bash
# Run specific failing test with verbose output
pytest tests/test_validators.py::TestURLValidation::test_validate_url_valid_https -vv

# Run with full traceback
pytest tests/test_scorecard.py --tb=long
```

**Pre-commit failures:**

```bash
# Let pre-commit auto-fix issues
pre-commit run --all-files

# If still failing, check specific errors
pre-commit run black --all-files --verbose
```

______________________________________________________________________

## Performance Monitoring

### Pipeline Timing

```bash
# Time full pipeline run
time python pipeline_runner.py --source au_policy

# Time just scraping
time python -c "from scrapers.au_policy import scrape; scrape()"

# Time scorecard enrichment
time python processors/scorecard_enricher.py
```

### Resource Usage

```bash
# Monitor during pipeline run
python pipeline_runner.py --source au_policy &
top -p $!

# Check disk usage
du -sh data/*
```

______________________________________________________________________

## Advanced Usage

### Batch Processing

```bash
# Process multiple sources sequentially
for source in au_policy ohchr upr; do
    echo "Processing $source..."
    python pipeline_runner.py --source $source
done

# Run multiple tests in parallel
pytest tests/ -n auto  # Requires pytest-xdist
```

### Custom Workflows

```bash
# 1. Scrape data
python -c "from scrapers.au_policy import scrape; scrape()"

# 2. Process to text
python pipeline_runner.py --source au_policy

# 3. Enrich with scorecard
python processors/scorecard_enricher.py

# 4. Export everything
python -c "from processors.scorecard_export import export_scorecard; export_scorecard()"

# 5. Validate URLs
python processors/scorecard_validator.py
```

______________________________________________________________________

## CI/CD

### Local CI Simulation

```bash
# Run exactly what CI runs
pip install pytest pytest-cov pre-commit
pre-commit run --all-files
pytest tests/ --maxfail=1 --disable-warnings -q --cov=processors --cov=scrapers --cov-report=term-missing
```

### Check Before Push

```bash
# Full validation before pushing
./check_before_push.sh  # If script exists

# Or manually:
pre-commit run --all-files && \
pytest tests/ --maxfail=1 -q && \
echo "✓ Ready to push!"
```

______________________________________________________________________

## Quick Reference

### Most Common Commands

```bash
# Setup (once)
python init_project.py && pip install -r requirements.txt

# Run pipeline
python pipeline_runner.py --source au_policy

# Run tests
pytest tests/ -v

# Run scorecard workflow
python pipeline_runner.py --mode scorecard --scorecard-action all

# Check code quality
pre-commit run --all-files

# View latest logs
tail -f logs/*.log
```

______________________________________________________________________

## Notes

- Always run commands from project root directory
- Virtual environment must be activated for all Python commands
- Pre-commit hooks enforce code quality standards
- Logs are stored in `logs/` (gitignored)
- Exports are stored in `data/exports/` (gitignored)
- Raw data in `data/raw/` should be preserved

______________________________________________________________________

Last updated: January 2026
