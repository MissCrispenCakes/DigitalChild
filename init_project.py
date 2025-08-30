"""
init_project.py
---------------
Bootstraps the GRIMdata / LittleRainbowRights project directory structure.
Creates empty placeholder files where needed.
Safe to re-run (idempotent).
"""

import os

# Base directories
dirs = [
    "scrapers",
    "processors",
    "configs/filters",
    "data/raw/au_policy",
    "data/raw/ohchr",
    "data/raw/upr",
    "data/raw/unicef",
    "data/raw/acerwc",
    "data/raw/achpr",
    "data/raw/manual",
    "data/processed/Africa/African_Union/text",
    "data/processed/Africa/African_Union/json",
    "data/processed/Africa/African_Union/ocr",
    "data/processed/Africa/Kenya/text",
    "data/processed/Africa/Kenya/json",
    "data/processed/Africa/Kenya/ocr",
    "data/processed/Africa/Nigeria/text",
    "data/processed/Africa/Nigeria/json",
    "data/processed/Africa/Nigeria/ocr",
    "data/processed/Africa/South_Africa/text",
    "data/processed/Africa/South_Africa/json",
    "data/processed/Africa/South_Africa/ocr",
    "data/processed/Europe",
    "data/processed/Asia",
    "data/processed/Americas",
    "data/metadata",
    "data/exports",
    "logs",
    "docs",
    "tests",
    ".github/workflows",
]

# Placeholder files
files = {
    "pipeline_runner.py": "",
    "requirements.txt": "# requirements placeholder\n",
    "scrapers/au_policy.py": "# AU policy scraper placeholder\n",
    "processors/pdf_to_text.py": "# PDF processor placeholder\n",
    "processors/tagger.py": "# Tagger placeholder\n",
    "processors/tags_summary.py": "# Tags summary exporter placeholder\n",
    "processors/logger.py": "# Logger placeholder\n",
    "configs/tags_v1.json": '{\n  "rules": {}\n}\n',
    "data/metadata/metadata.json": '{\n  "documents": []\n}\n',
    "docs/README.md": "# Project README\n",
    "docs/FIRST_RUN_ERRORS.md": "# First Run Errors Guide\n",
    "tests/test_year_extraction.py": "# Year extraction test placeholder\n",
    "tests/test_csv_footer.py": "# CSV footer test placeholder\n",
    "tests/test_logging.py": "# Logging test placeholder\n",
    ".github/workflows/ci.yml": "# CI workflow placeholder\n",
}


def ensure_dirs():
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def ensure_files():
    for path, content in files.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    ensure_dirs()
    ensure_files()
    print("✅ Project structure initialized (idempotent).")
