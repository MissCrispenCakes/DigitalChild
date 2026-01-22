# Installation

This guide walks you through installing DigitalChild on your system.

## Prerequisites

### Required

- **Python 3.12** - Modern Python features required
- **pip** - Python package installer
- **Git** - Version control (for cloning repository)
- **1GB+ disk space** - For code and small dataset
- **Internet connection** - For scraping documents

### Optional

- **10GB+ disk space** - For large document collections
- **Virtual environment tool** - venv, virtualenv, or conda

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild
```

### 2. Set Up Virtual Environment

=== "Linux / macOS"

````
```bash
python3 -m venv .LittleRainbow
source .LittleRainbow/bin/activate
```
````

=== "Windows"

````
```cmd
python -m venv .LittleRainbow
.LittleRainbow\Scripts\activate
```
````

=== "conda"

````
```bash
conda create -n digitalchild python=3.12
conda activate digitalchild
```
````

!!! tip "Why virtual environment?"
    Virtual environments isolate project dependencies, preventing conflicts with other Python projects on your system.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `beautifulsoup4` - HTML parsing
- `selenium` - Browser automation (optional)
- `pandas` - Data manipulation
- `PyPDF2` - PDF processing
- `python-docx` - Word document processing
- `openpyxl` - Excel file handling
- `requests` - HTTP requests

### 4. Initialize Project Structure

```bash
python init_project.py
```

This creates:

- `data/raw/` - Downloaded documents
- `data/processed/` - Extracted text
- `data/metadata/` - Metadata JSON files
- `data/exports/` - CSV export outputs
- `logs/` - Run logs

!!! success "Ready to Go!"
    Your installation is complete. Proceed to [Quick Start](quickstart.md) to run your first pipeline.

## Development Installation

For contributors and developers:

```bash
# Install development tools
pip install pre-commit pytest pytest-cov

# Set up pre-commit hooks
pre-commit install

# Verify installation
pytest tests/ -v
pre-commit run --all-files
```

## Verifying Installation

Test your setup:

```bash
# Check Python version
python --version  # Should be 3.12.x

# Test imports
python -c "import pandas; import bs4; print('Success!')"

# Run demo (no internet needed)
python utils/pipeline_runner_DEMO.py
```

## Optional: Selenium Setup

Only needed for `_sel` variant scrapers (browser automation):

### 1. Install ChromeDriver

=== "Linux"

````
```bash
sudo apt-get install chromium-chromedriver
```
````

=== "macOS"

````
```bash
brew install chromedriver
```
````

=== "Windows"

```
Download from [ChromeDriver](https://chromedriver.chromium.org/) and add to PATH.
```

### 2. Verify Selenium

```bash
python -c "from selenium import webdriver; print('Selenium ready!')"
```

## Troubleshooting

### Python Version Issues

!!! failure "Error: Python 3.12 required"
    The project uses modern Python features from 3.12. Install Python 3.12 from [python.org](https://www.python.org/downloads/).

### Virtual Environment Not Activating

=== "Linux / macOS"

````
Check file permissions:
```bash
chmod +x .LittleRainbow/bin/activate
```
````

=== "Windows"

````
Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
````

### Dependency Installation Failures

Try upgrading pip first:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Import Errors

Ensure you're running from project root:

```bash
# Wrong
cd processors
python pipeline_runner.py  # Error!

# Right
cd /path/to/DigitalChild
python pipeline_runner.py  # Success
```

### More Help

See [First Run Errors](../guides/FIRST_RUN_ERRORS.md) for comprehensive troubleshooting.

## Next Steps

- [Quick Start Guide](quickstart.md) - Run your first pipeline
- [Runbook](../guides/RUNBOOK.md) - Complete command reference
- [FAQ](../FAQ.md) - Common questions answered

## System Requirements

### Minimum

- Python 3.12
- 1GB RAM
- 1GB disk space
- Broadband internet

### Recommended

- Python 3.12
- 4GB+ RAM
- 10GB+ disk space
- Fast internet connection
- SSD for faster processing

## Platform Support

DigitalChild runs on:

- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ✅ macOS (10.15+)
- ✅ Windows 10/11
- ✅ WSL2 (Windows Subsystem for Linux)
- ✅ Cloud VMs (AWS EC2, Google Cloud, Azure, DigitalOcean)

## Need Help?

- Check [FAQ](../FAQ.md)
- Review [First Run Errors](../guides/FIRST_RUN_ERRORS.md)
- Open [GitHub Issue](https://github.com/MissCrispenCakes/DigitalChild/issues)
- Start [Discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions)
