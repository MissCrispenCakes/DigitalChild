# Frequently Asked Questions (FAQ)

## General Questions

### What is DigitalChild / GRIMdata / LittleRainbowRights?

DigitalChild (also known as GRIMdata or LittleRainbowRights) is an open-source data pipeline for analyzing human rights documents, with a specific focus on child and LGBTQ+ digital rights. It scrapes documents from international organizations, processes them into structured data, applies automated tagging, and enriches them with country-level indicators.

### Who is this for?

- **Researchers:** Human rights academics studying digital rights trends
- **NGOs:** Organizations tracking child/LGBTQ+ protections globally
- **Policy Analysts:** Those comparing policies across countries
- **Journalists:** Investigating digital rights stories
- **Students:** Learning about data analysis and human rights

### Is this free to use?

Yes! The code is licensed under MIT (permissive, free for any use including commercial). The data and documentation are licensed under CC BY 4.0 (free to use with attribution).

### Can I use this for my research?

Absolutely! That's the intended purpose. Please cite the project using the format in [CITATION.cff](../CITATION.cff).

______________________________________________________________________

## Getting Started

### What do I need to run this?

**Minimum requirements:**

- Python 3.12
- 1GB disk space (for code + small dataset)
- Internet connection (for scraping)

**Recommended:**

- 10GB+ disk space (for large document collections)
- Good internet connection (faster scraping)

### How do I install it?

```bash
# 1. Clone the repository
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild

# 2. Set up virtual environment
python3 -m venv .LittleRainbow
source .LittleRainbow/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize project structure
python init_project.py

# 5. Run the pipeline
python pipeline_runner.py --source au_policy
```

See [docs/guides/FIRST_RUN_ERRORS.md](guides/FIRST_RUN_ERRORS.md) for troubleshooting.

### How long does it take to scrape documents?

Depends on the source and number of documents:

- **AU Policy:** ~5-10 minutes (small collection)
- **UPR (single country):** ~2-5 minutes
- **OHCHR:** ~15-30 minutes (larger collection)

The pipeline skips already-downloaded files, so subsequent runs are faster.

### Where do the downloaded files go?

- **Raw documents:** `data/raw/<source>/`
- **Processed text:** `data/processed/<region>/<org>/text/`
- **Metadata:** `data/metadata/metadata.json`
- **Exports:** `data/exports/`
- **Logs:** `logs/`

______________________________________________________________________

## Features & Capabilities

### What sources does it support?

Currently supports 7 sources:

1. **AU Policy** - African Union policy documents
1. **OHCHR** - Office of the High Commissioner for Human Rights
1. **UPR** - Universal Periodic Review documents
1. **UNICEF** - UNICEF reports and publications
1. **ACERWC** - African Committee on Child Rights
1. **ACHPR** - African Commission on Human Rights
1. **Manual** - Upload your own documents to `data/raw/manual/`

### What file formats can it process?

- PDF (most common)
- DOCX (Microsoft Word)
- HTML (web pages)

The `fallback_handler` automatically tries different processors until one succeeds.

### What is the scorecard system?

The scorecard tracks **10 human rights indicators** across **194 countries**:

1. AI Policy Status
1. Data Protection Law
1. LGBTQ+ Legal Status
1. Child Online Protection
1. SIM Card Biometric Requirements
1. Encryption Backdoors
1. LGBTQ+ Promotion/Propaganda Laws
1. Data Protection Authority Independence
1. Content Moderation Regulations
1. Age Verification Requirements

Each indicator includes the current status and source URL for verification.

### How does tagging work?

The tagger applies regex-based rules to identify mentions of:

- Child rights
- LGBTQ+ rights
- AI and automation
- Privacy and data protection
- Digital policy
- Online rights
- And more...

Tags are versioned (v1, v2, v3, digital) allowing comparison across rule sets.

### Can I add my own tags?

Yes! Edit `configs/tags_v3.json` (or create a new version) and add your regex patterns:

```json
{
  "rules": {
    "YourNewTag": [
      "keyword1",
      "keyword2",
      "regex.*pattern"
    ]
  }
}
```

Then run: `python pipeline_runner.py --tags-version v3`

______________________________________________________________________

## Technical Questions

### Why Python 3.12 specifically?

The project uses modern Python features available in 3.12. While it may work with 3.10+, we only test and support 3.12.

### Can I run this on Windows?

Yes! The code works on Windows, Mac, and Linux. Paths are handled with `os.path` for cross-platform compatibility.

### Do I need Selenium/ChromeDriver?

No, unless you want to use Selenium scrapers (`_sel` variants). The standard scrapers use `requests` and work without browser drivers.

### How much bandwidth does scraping use?

Varies by source:

- **Small collection:** 10-50 MB
- **Large collection:** 100-500 MB
- **Full multi-source scrape:** 1-5 GB

The pipeline skips existing files, so re-runs use minimal bandwidth.

### Can I run this in the cloud?

Yes! Works on:

- AWS EC2
- Google Cloud Compute
- Azure VMs
- DigitalOcean Droplets
- Any Linux server

Just ensure Python 3.12 is installed and you have sufficient disk space.

### Does it use a database?

Currently uses JSON files (`metadata.json`) for simplicity. A future version may migrate to PostgreSQL for better performance at scale.

______________________________________________________________________

## Data & Privacy

### What data does this collect?

The pipeline downloads **publicly available documents** from government and UN websites. No personal data is collected from users.

### Is the scraped data private?

The documents are already public (published by governments/UN). However, be mindful of:

- Where you store the data
- Who has access to your machine
- Data retention policies

See [DATA_GOVERNANCE.md](DATA_GOVERNANCE.md) for details.

### Can I share the scraped documents?

The documents themselves are typically public domain (government/UN publications). However:

- Check the original source's terms
- Respect copyright if applicable
- Attribute the original publishers

Your **compiled dataset** (scorecard, tags, analysis) is licensed CC BY 4.0 (requires attribution).

### How often is the scorecard data updated?

Manually updated as new information becomes available. The `scorecard_diff.py` module monitors sources for changes and alerts when updates are needed.

### Are the scorecard sources reliable?

We aim to use authoritative sources (UNESCO, UNCTAD, ILGA, UNICEF, etc.). Each indicator includes the source URL for verification. If you find an error, please [report it](https://github.com/MissCrispenCakes/DigitalChild/issues).

______________________________________________________________________

## Contributing & Development

### Can I contribute?

Yes! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines. Contributions welcome:

- Bug reports
- New scrapers
- Documentation improvements
- Test coverage
- Visualization ideas

### I found a bug. What should I do?

1. Check if it's already reported: [Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
1. Review [FIRST_RUN_ERRORS.md](guides/FIRST_RUN_ERRORS.md)
1. If not resolved, open a new issue with details

### How do I add a new scraper?

See [SCRAPER_STRUCTURE.md](standards/SCRAPER_STRUCTURE.md) for a template and guide.

Basic steps:

1. Create `scrapers/new_source.py`
1. Implement `scrape()` function
1. Add to `SCRAPER_MAP` in `pipeline_runner.py`
1. Add tests
1. Submit pull request

### How can I test my changes?

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_validators.py -v

# With coverage
pytest tests/ --cov
```

______________________________________________________________________

## Troubleshooting

### The scraper isn't downloading anything. Why?

Common causes:

1. **Already downloaded:** Pipeline skips existing files (check `data/raw/<source>/`)
1. **Network issues:** Firewall, proxy, or connection problems
1. **Source changed:** Website structure may have changed
1. **Robots.txt blocking:** Some sites block automated access

Check logs in `logs/` for error messages.

### Processing fails with "File not found" error

Run `python init_project.py` to ensure all directories exist.

### Tests are failing

Common reasons:

1. **Pre-commit not installed:** Run `pip install pre-commit && pre-commit install`
1. **Dependencies outdated:** Run `pip install --upgrade -r requirements.txt`
1. **Python version:** Ensure Python 3.12 is active
1. **Working directory:** Run from project root, not subdirectory

### I'm getting import errors

Ensure you're running commands from the **project root** directory (where `pipeline_runner.py` is located), not from subdirectories.

### The website/visualization isn't working

The website is static and generated from docs. If it's not working:

1. Ensure MkDocs is installed: `pip install mkdocs mkdocs-material`
1. Build locally: `mkdocs serve`
1. Check `mkdocs.yml` configuration

______________________________________________________________________

## Research & Citations

### How should I cite this project?

Use the format in [CITATION.cff](../CITATION.cff):

```
GRIMdata / LittleRainbowRights. (2025). DigitalChild: Human Rights Data
Pipeline for Child and LGBTQ+ Digital Protection.
Available at: https://github.com/MissCrispenCakes/DigitalChild
```

### Are there published papers using this?

Check the project website at [grimdata.org](https://grimdata.org) for latest publications.

### Can I use this for my thesis/dissertation?

Absolutely! That's an intended use case. Please cite the project and consider contributing back improvements.

### How can I get involved in research collaborations?

Open a [discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions) or reach out via the website contact form.

______________________________________________________________________

## Future Development

### What features are planned?

See [ROADMAP.md](ROADMAP.md) for the full roadmap. Highlights:

- Recommendations extraction (NLP-based)
- Timeline visualizations
- Comparison analytics
- Interactive research dashboard
- Global expansion (Europe, Asia, Americas)

### When will the research dashboard be ready?

Target: Late 2026. It's in Phase 4 of the roadmap. Focus right now is on completing Phase 3 (advanced processing).

### Can I request a feature?

Yes! Open a [feature request issue](https://github.com/MissCrispenCakes/DigitalChild/issues/new) or discussion. No guarantees, but we're open to suggestions that align with the project mission.

______________________________________________________________________

## Contact & Support

### How do I get help?

1. **Documentation:** Check [docs/](.)
1. **FAQ:** This page
1. **Issues:** Search [existing issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
1. **Discussions:** Ask in [discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)

### Is there a mailing list or community forum?

Not yet. Use GitHub Discussions for now. A community forum may be added in the future.

### Who maintains this project?

This is a PhD research project maintained part-time by one person. Please be patient with response times!

### How can I support the project?

- ⭐ Star the repo on GitHub
- 📢 Share it with researchers in your network
- 🐛 Report bugs and issues
- 💻 Contribute code or documentation
- 📝 Cite it in your publications
- 💰 Consider sponsoring (if/when GitHub Sponsors is enabled)

______________________________________________________________________

**Didn't find your answer?** Open a [discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions) or [issue](https://github.com/MissCrispenCakes/DigitalChild/issues).

**Last updated:** January 2026
