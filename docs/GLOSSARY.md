# Glossary

This glossary defines key terms used throughout the DigitalChild project documentation.

## Human Rights Organizations & Bodies

### ACERWC

**African Committee of Experts on the Rights and Welfare of the Child**

- Treaty body monitoring implementation of the African Charter on the Rights and Welfare of the Child
- Established by the African Union
- Reviews state reports and issues recommendations

### ACHPR

**African Commission on Human and Peoples' Rights**

- Quasi-judicial body under the African Union
- Promotes and protects human rights in Africa
- Examines state reports and individual complaints

### AU (African Union)

Pan-African organization of 55 member states

- Successor to the Organization of African Unity (OAU)
- Focuses on continental integration, peace, security, and development
- Issues policies, charters, and protocols on human rights

### OHCHR

**Office of the High Commissioner for Human Rights**

- United Nations entity for human rights
- Coordinates UN human rights activities
- Provides technical assistance and monitors human rights situations

### UNICEF

**United Nations Children's Fund**

- UN agency responsible for humanitarian and developmental aid to children
- Advocates for child protection, survival, and development
- Publishes reports on child rights globally

### UPR (Universal Periodic Review)

UN Human Rights Council mechanism reviewing human rights records of all UN member states

- Occurs every 4-5 years per country
- State-driven process with stakeholder input
- Results in recommendations for improvement

## Human Rights Terms

### Child Rights

Rights specific to persons under 18 years old, including:

- Protection from exploitation, abuse, and violence
- Right to education, health care, and family life
- Special protections for digital spaces

### Data Protection

Legal and technical measures safeguarding personal information, including:

- Right to privacy
- Control over personal data
- Consent requirements for data collection and processing

### Digital Rights

Human rights in the context of digital technology and internet access:

- Freedom of expression online
- Privacy in digital communications
- Access to information
- Protection from surveillance

### LGBTQ+ Rights

Rights of lesbian, gay, bisexual, transgender, queer/questioning individuals, including:

- Protection from discrimination
- Legal recognition
- Freedom from criminalization
- Access to services without prejudice

### Treaty Body

Committee of independent experts monitoring implementation of international human rights treaties

- Reviews state reports
- Issues concluding observations and recommendations
- May handle individual complaints

## Technical Terms

### API (Application Programming Interface)

Set of protocols allowing software applications to communicate

- In this project: Future feature for accessing data programmatically
- Currently: CLI-based (no API yet)

### BeautifulSoup4

Python library for parsing HTML and XML documents

- Used by scrapers to extract data from web pages
- Enables navigation and search of parse trees

### CLI (Command-Line Interface)

Text-based interface for interacting with software

- Primary mode of operation for DigitalChild pipeline
- Commands run via terminal/command prompt

### CSV (Comma-Separated Values)

Plain text format for tabular data

- Used for exports (scorecard summaries, tags analysis)
- Easily imported into Excel, R, Python, etc.

### Fallback Handler

Module that tries multiple processors in sequence until one succeeds

- Used when file type is uncertain
- Ensures maximum document processing success

### GitHub Pages

Static site hosting service by GitHub

- Hosts websites directly from GitHub repositories
- Free for public repositories
- Used for GRIMdata.org website

### MkDocs

Static site generator for project documentation

- Converts Markdown files to HTML website
- Material theme provides modern, responsive design
- Used to build DigitalChild documentation site

### Pandas

Python library for data analysis and manipulation

- Used for scorecard data processing
- Provides DataFrame structures for tabular data

### PDF (Portable Document Format)

File format for presenting documents independent of software/hardware

- Most common format for human rights documents
- Processed using PyPDF2 in this pipeline

### PyPDF2

Python library for reading and manipulating PDF files

- Extracts text from PDFs for analysis
- Handles multi-page documents

### Pytest

Python testing framework

- Used to run 124 tests in DigitalChild
- Supports fixtures, parameterization, coverage reporting

### Regex (Regular Expression)

Pattern-matching syntax for text

- Used in tagging system to identify keywords
- Example: `\bAI\b` matches "AI" as whole word

### Scraping (Web Scraping)

Automated extraction of data from websites

- Downloads documents from public sources
- Uses requests library and Selenium

### Selenium

Browser automation tool

- Used for scraping dynamic websites requiring JavaScript
- Requires ChromeDriver for Chrome browser control

## Project-Specific Terms

### Basecamp Branch

Main development branch for DigitalChild project

- Equivalent to "main" or "master" in other repos
- All PRs merge to basecamp

### DigitalChild

Official name of this data pipeline project

- Also known as GRIMdata (research umbrella)
- Also known as LittleRainbowRights (child/LGBTQ+ focus)

### Document Metadata

Structured information about processed documents stored in `metadata.json`:

- Source, country, region, year
- Tags history (versioned)
- Recommendations history
- Scorecard indicators
- Processing timestamps

### Enrichment

Process of adding scorecard indicator data to document metadata

- Matches documents to countries
- Adds 10 indicators per country
- Tracks enrichment timestamp

### GRIMdata

**Global Rights Information Monitoring**

- Umbrella project name
- Website: GRIMdata.org
- Includes DigitalChild and future SGBV-UPR integration

### Indicator

Specific human rights metric tracked in the scorecard system

- 10 indicators total (AI Policy, Data Protection, LGBTQ+ Status, etc.)
- Each includes current status and authoritative source URL
- Covers 194 countries

### LittleRainbowRights

Project name for child and LGBTQ+ digital rights research

- Subset of GRIMdata focusing on vulnerable populations
- Website: LittleRainbowRights.com
- Emphasizes digital protection for children and LGBTQ+ individuals

### Pipeline Runner

Main entry point script (`pipeline_runner.py`)

- Orchestrates entire workflow
- Three modes: scraper, urls, scorecard
- Handles logging, argument parsing, module coordination

### Processor

Module that converts documents to text

- PDF processor (PyPDF2)
- DOCX processor (python-docx)
- HTML processor (BeautifulSoup4)
- Outputs to `data/processed/`

### Scorecard

Comprehensive tracking system for 10 human rights indicators across 194 countries

- Stored in `scorecard_main.xlsx`
- 2,543 source URLs (as of January 2026)
- Separate workflow from main pipeline

### Scraper

Module that downloads documents from web sources

- Each source has dedicated scraper (e.g., `au_policy.py`)
- Returns list of downloaded file paths
- Outputs to `data/raw/<source>/`

### Source

Origin of human rights documents

- Currently supports: AU Policy, OHCHR, UPR, UNICEF, ACERWC, ACHPR, Manual
- Each source has dedicated scraper and processing path

### Tagger

Module that applies regex-based tags to documents

- Uses config files (`tags_v1.json`, `tags_v3.json`, etc.)
- Tracks tags history with versions and timestamps
- Tags include: ChildRights, LGBTQ, AI, Privacy, DigitalPolicy

### Tags History

Versioned record of all tag applications to a document

- Stored in metadata.json
- Includes tags, version, and timestamp
- Allows comparison across different tag rule sets

### Validator

Security module for input validation

- Validates URLs, file paths, configs, schemas
- Prevents path traversal and injection attacks
- 68 tests ensure comprehensive security

## Data Analysis Terms

### Age Verification

Technical or legal requirement to confirm user age before granting access

- Indicator #10 in scorecard
- Increasingly common for social media and adult content
- Privacy concerns around data collection

### AI Policy Status

Whether a country has published policy on artificial intelligence

- Indicator #1 in scorecard
- Includes strategies, frameworks, regulations
- Tracked via UNESCO, UNCTAD, national government sources

### Child Online Protection

Measures to safeguard children in digital environments

- Indicator #4 in scorecard
- Includes laws, policies, filtering, education
- Critical for DigitalChild research focus

### Content Moderation

Rules and systems for removing harmful online content

- Indicator #9 in scorecard
- Includes platform policies, government regulations
- Balance between safety and free expression

### Data Protection Authority (DPA)

Independent agency overseeing data protection compliance

- Indicator #8 tracks DPA independence
- Key for enforcing privacy rights
- Not all countries have established DPAs

### Data Protection Law

Legislation governing collection, use, and storage of personal data

- Indicator #2 in scorecard
- Examples: GDPR (Europe), POPIA (South Africa), NDPR (Nigeria)
- Foundation for digital privacy rights

### Encryption Backdoor

Intentional weakness in encryption allowing government access

- Indicator #6 in scorecard
- Controversial trade-off between security and surveillance
- Impacts privacy and data protection

### LGBTQ+ Legal Status

Legal recognition and protections for LGBTQ+ individuals

- Indicator #3 in scorecard
- Ranges from criminalization to full equality
- Sourced from ILGA World, State-Sponsored Homophobia report

### Promotion/Propaganda Laws

Legislation restricting discussion or "promotion" of LGBTQ+ topics

- Indicator #7 in scorecard
- Often targets education, media, public discourse
- Human rights concern for freedom of expression

### SIM Card Biometric Registration

Requirement to provide biometric data (fingerprints, facial recognition) to obtain mobile SIM card

- Indicator #5 in scorecard
- Privacy and surveillance implications
- Disproportionately impacts vulnerable populations

## Research Terms

### CC BY 4.0 (Creative Commons Attribution 4.0)

License requiring attribution when using licensed material

- Applied to DigitalChild data and documentation
- Allows sharing, adaptation, even commercial use
- Must credit original creators

### Citation

Formal acknowledgment of sources used in research

- Required when using DigitalChild data (CC BY 4.0)
- Format provided in CITATION.cff
- Critical for academic integrity

### FAIR Data Principles

**Findable, Accessible, Interoperable, Reusable**

- Guidelines for scientific data management
- DigitalChild aims to align with FAIR principles
- Enhances research value and reproducibility

### Metadata Schema

Structured format defining how document information is recorded

- DigitalChild schema documented in `docs/standards/METADATA_SCHEMA.md`
- Ensures consistency across all documents
- Enables systematic analysis

### MIT License

Permissive software license

- Applied to DigitalChild code
- Allows free use, modification, distribution
- Minimal restrictions

### Open Source

Software with source code available for inspection, modification, and enhancement

- DigitalChild is fully open source
- Hosted on GitHub
- Encourages collaboration and transparency

## Acronyms & Abbreviations

- **API**: Application Programming Interface
- **AU**: African Union
- **CLI**: Command-Line Interface
- **CSV**: Comma-Separated Values
- **DPA**: Data Protection Authority
- **GDPR**: General Data Protection Regulation (EU)
- **HTML**: HyperText Markup Language
- **HTTP/HTTPS**: HyperText Transfer Protocol (Secure)
- **JSON**: JavaScript Object Notation
- **LGBTQ+**: Lesbian, Gay, Bisexual, Transgender, Queer/Questioning, and others
- **MIT**: Massachusetts Institute of Technology (license origin)
- **NLP**: Natural Language Processing
- **OHCHR**: Office of the High Commissioner for Human Rights
- **PDF**: Portable Document Format
- **SIM**: Subscriber Identity Module
- **UN**: United Nations
- **UNICEF**: United Nations Children's Fund
- **UPR**: Universal Periodic Review
- **URL**: Uniform Resource Locator
- **XML**: eXtensible Markup Language

## Related Projects

### Beyond the Rainbow

Extended vision encompassing all vulnerable populations

- Future expansion beyond children and LGBTQ+
- Includes elderly, disabled, refugees, indigenous peoples
- Phase 5 roadmap goal

### SGBV-UPR

**Sexual and Gender-Based Violence** analysis using UPR documents

- Separate research project
- Already published in academic journal
- To be integrated into GRIMdata.org website

______________________________________________________________________

**Need a term defined?** Open an [issue](https://github.com/MissCrispenCakes/DigitalChild/issues) or [discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions) requesting the addition.

**Last updated:** January 2026
