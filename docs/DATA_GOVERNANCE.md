# Data Governance

This document outlines the data governance policies, ethical considerations, and responsible research practices for the DigitalChild project.

## 🎯 Purpose

DigitalChild collects, processes, and analyzes human rights documents to support research on child and LGBTQ+ digital protection. This governance framework ensures:

1. **Ethical data collection** - Respecting source terms and permissions
1. **Privacy protection** - Safeguarding any personal information
1. **Transparency** - Clear documentation of data sources and methods
1. **Reproducibility** - Enabling verification and replication of findings
1. **Responsible use** - Supporting human rights research without causing harm

## 📜 Data Collection Principles

### 1. Public Domain Documents Only

**What we collect:**

- Publicly available human rights documents
- Policy statements from governments and international organizations
- Reports published by UN bodies, regional organizations, and NGOs

**What we DO NOT collect:**

- Personal data from individuals
- Leaked or confidential documents
- Data obtained without permission
- Information behind paywalls or authentication

### 2. Source Attribution

Every document includes:

- Original source URL
- Publishing organization
- Date of collection
- Verification of public availability

See `metadata.json` schema for attribution fields.

### 3. Respect for Terms of Service

Scrapers designed to:

- ✅ Respect robots.txt directives
- ✅ Implement rate limiting and timeouts
- ✅ Identify as research tool (User-Agent headers)
- ✅ Minimize server load
- ❌ Never bypass authentication
- ❌ Never ignore explicit blocking

## 🔒 Privacy & Data Protection

### Personal Information

**DigitalChild does NOT:**

- Collect user data from website visitors (future website will be static)
- Track individual researchers using the tool
- Store login credentials or authentication tokens
- Share data with third parties

**If documents contain personal information:**

- We process publicly available documents as-is
- We do not redact names from public reports (they're already public)
- We do not extract personal information as separate data points
- We comply with original publisher's privacy practices

### Data Storage

**Local storage (default):**

- All data stored on user's machine
- User controls access and retention
- Gitignored by default (`data/`, `logs/`)

**Users are responsible for:**

- Securing their own machines
- Controlling access to downloaded documents
- Following their institution's data policies
- Complying with local data protection laws (GDPR, CCPA, etc.)

### Data Sharing

**What can be shared:**

- ✅ Compiled analysis (CSV exports)
- ✅ Tags and metadata (with attribution)
- ✅ Scorecard data (CC BY 4.0 license)
- ✅ Code and documentation (MIT license)

**What requires caution:**

- ⚠️ Raw downloaded documents (check original publisher's terms)
- ⚠️ Bulk document collections (respect copyright)
- ⚠️ Personal identifiers extracted from documents

**Licensing:**

- **Code:** MIT (free use, attribution appreciated)
- **Data/Documentation:** CC BY 4.0 (attribution required)

See [LICENSE](../LICENSE) and [LICENSE-DATA](../LICENSE-DATA) for details.

## 🧭 Ethical Research Practices

### 1. Do No Harm

This project analyzes human rights violations and protections. We must ensure our work does not:

- ❌ Expose vulnerable individuals to retaliation
- ❌ Enable surveillance or targeting of at-risk populations
- ❌ Misrepresent data to support harmful policies
- ❌ Weaponize findings against vulnerable communities

**Best practices:**

- Focus on systemic patterns, not individuals
- Contextualize findings appropriately
- Acknowledge limitations and uncertainties
- Consider potential misuse of research outputs

### 2. Transparency

All aspects of this project are open:

- ✅ Source code publicly available (GitHub)
- ✅ Methodology documented
- ✅ Data sources cited with URLs
- ✅ Limitations acknowledged
- ✅ Changes tracked via version control

### 3. Reproducibility

Researchers can verify and replicate findings:

- Config files define tag rules
- Metadata tracks processing history
- Timestamps record when data was collected
- Version control preserves historical states

### 4. Accountability

**Maintainer responsibilities:**

- Respond to data quality concerns
- Correct errors when identified
- Update sources as information changes
- Credit contributors appropriately

**User responsibilities:**

- Verify findings before publication
- Cite sources appropriately
- Report errors and issues
- Use data ethically and legally

## 📊 Data Quality & Integrity

### Source Validation

Scorecard system includes:

- 2,543 source URLs (as of January 2026)
- Automated validation (`scorecard_validator.py`)
- Broken link detection
- Change monitoring (`scorecard_diff.py`)

### Metadata Integrity

Every document tracked with:

- Unique ID (filename)
- Source organization
- Country/region (normalized)
- Year extracted
- Processing timestamps
- Tags history (versioned)
- Scorecard indicators (with sources)

### Error Handling

When processing fails:

- Errors logged to `logs/`
- Documents marked with processing status
- Fallback handlers attempt alternative methods
- Manual review flagged for complex cases

### Recent Data Quality Verification (January 2026)

A comprehensive verification of scorecard data across 194 countries revealed important insights:

**Key Findings:**

- ✅ **No factual errors** in primary indicators across the dataset
- ✅ **Manual research was superior** to scorecard file maintenance at time of Sept 2025 conference
- ⚠️ **File synchronization workflow issue** identified (not research quality problem)

**What Happened:**

- Conference presentation materials (slides, detailed analysis) demonstrated thorough, accurate legal research
- Example: Botswana's Data Protection Act 2024 correctly identified in presentation slides
- However, scorecard Excel files weren't systematically synchronized with research findings
- Different researchers updated different files without cross-checking

**Resolution:**

- All 9 data conflicts verified and documented in `data/VERIFICATION_RESULTS.md`
- Root cause analysis: File maintenance workflow gap, not research inadequacy
- Complete analysis documented in `data/REVISION_SUMMARY.md`
- Recommendations for workflow improvements in `data/DATA_RECONCILIATION_RECOMMENDATIONS.md`

**Lesson:** Manual research captured accurate, current knowledge. The disconnect was in systematic back-population of findings into data management files. This validates that thorough human rights research requires careful knowledge management systems alongside the research itself.

## 🌍 International Considerations

### Multi-Jurisdictional Data

Documents originate from 194 countries with varying:

- Copyright laws
- Data protection regulations
- Freedom of information standards
- Cultural sensitivities

**Our approach:**

- Respect most restrictive interpretation
- Defer to original publisher's terms
- Acknowledge legal uncertainties
- Seek legal advice for edge cases

### Language & Translation

Current scope: English-language documents primarily

- African Union documents (English, French, Arabic)
- UN documents (multiple languages available)

Future expansion may include:

- Machine translation with disclaimers
- Native language processing
- Cultural context preservation

### Cultural Sensitivity

Human rights standards vary globally. We:

- ✅ Document facts without imposing Western-centric values
- ✅ Acknowledge cultural context in analysis
- ✅ Include diverse sources (UN, AU, regional bodies)
- ✅ Avoid oversimplification of complex issues

## 🔐 Security & Access Control

### Data Access

**Who can access the data:**

- Anyone who downloads and runs this open-source tool
- Static website visitors (scorecard visualizations)
- Researchers citing published findings

**No authentication required:**

- Tool is CLI-based, no login system
- Future website will be static (no user accounts)

### Security Measures

Code includes validators for:

- Path traversal attacks (`validate_path()`)
- URL injection (`validate_url()`)
- File size limits
- Extension whitelisting

See [SECURITY.md](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/SECURITY.md) for vulnerability reporting.

### Secure Deployment

When deploying or using this tool:

1. Keep software updated (`git pull` regularly)
1. Review dependencies for vulnerabilities (`pip install safety && safety check`)
1. Limit access to downloaded documents
1. Use HTTPS for all web requests
1. Follow your institution's security policies

## 📝 Data Retention & Deletion

### Default Retention

Data persists indefinitely on user's machine unless manually deleted.

**Recommended practices:**

- Delete raw documents after processing if storage limited
- Keep metadata.json and exports for reproducibility
- Archive complete datasets before major version changes

### Right to be Forgotten

If a document publisher requests removal:

1. Verify authenticity of request
1. Remove from future scrapes
1. Delete from existing datasets
1. Document removal in changelog
1. Notify users via GitHub issue

**Note:** We cannot control what users have already downloaded.

## 🧪 Research Ethics

### Human Subjects

This project does NOT involve human subjects research:

- No recruitment or consent procedures
- No direct interaction with individuals
- Documents are already public

**However:**

- Documents may contain names of human rights defenders, victims, or officials
- We treat all individuals mentioned with respect and dignity
- We do not extract personal data as separate fields

### Institutional Review Board (IRB)

PhD research using this tool may require IRB approval depending on:

- Your institution's policies
- Your specific research questions
- Whether you're analyzing individuals vs. systemic patterns

**Recommendation:** Consult your IRB if unsure.

### Publication Ethics

When publishing research using DigitalChild:

- ✅ Cite the project (see [CITATION.cff](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/CITATION.cff))
- ✅ Describe methodology clearly
- ✅ Acknowledge limitations
- ✅ Share code and data where possible (within legal constraints)
- ✅ Follow journal data sharing policies

## 🤝 Community Standards

### Contributor Conduct

See [CONTRIBUTING.md](CONTRIBUTING.md) for code of conduct.

**Core values:**

- Respectful, inclusive collaboration
- Constructive feedback
- Focus on human rights mission
- No harassment or discrimination

### Issue Reporting

When reporting data quality issues:

- Provide specific examples (URLs, filenames)
- Distinguish errors from design choices
- Suggest corrections with sources
- Assume good faith

### User Expectations

**What users can expect:**

- Open, documented code
- Best-effort data quality
- Responsive issue handling (within maintainer capacity)
- Academic citation and credit

**What users should NOT expect:**

- 24/7 support (maintained part-time)
- Legal guarantees or warranties (MIT license)
- Custom features on demand
- Validation of all 2,543 source URLs in real-time

## 📚 Compliance & Legal

### Copyright

**Documents:**

- Most are public domain (government/UN publications)
- Some may have copyright restrictions
- Check original source before redistribution

**Code:**

- MIT License (see [LICENSE](../LICENSE))
- Free use including commercial

**Data/Documentation:**

- CC BY 4.0 (see [LICENSE-DATA](../LICENSE-DATA))
- Attribution required

### Data Protection Laws

**GDPR (European Union):**

- No personal data collection from users
- Public documents processed as published
- Users responsible for their own compliance

**CCPA (California):**

- No sale of personal information
- No tracking of website visitors

**Other jurisdictions:**

- Follow local data protection laws
- Seek legal advice if processing sensitive categories

### Freedom of Information

Documents often obtained via:

- Government websites (public records)
- UN databases (publicly accessible)
- NGO publications (openly shared)

This constitutes legitimate research use of public information.

## 🔄 Updates & Versioning

### Data Updates

**Scorecard:**

- Manually updated as new information available
- Change monitoring (`scorecard_diff.py`)
- Version tracked in exports (timestamped)

**Documents:**

- Scrapers can be re-run to fetch updates
- Duplicate detection (skip existing files)
- Metadata tracks last_processed timestamp

### Policy Updates

This governance document reviewed annually or when:

- Major legal/regulatory changes occur
- New data sources added
- User feedback identifies gaps
- Research ethics standards evolve

**Version history:** Tracked via Git commits

## 📞 Contact & Questions

### Data Quality Issues

Report via [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues) with:

- Specific data point or document
- Expected vs. actual value
- Source URL for verification

### Ethical Concerns

For sensitive matters not suitable for public issues:

- Use [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions) (can be private)
- Or report via [Security tab](https://github.com/MissCrispenCakes/DigitalChild/security) for confidential concerns

### Collaboration

Open to partnerships with:

- Human rights organizations
- Academic researchers
- Policy analysts
- Data scientists

Use [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions) for collaboration proposals.

## 🌈 Mission Alignment

All data governance decisions prioritize:

1. **Human Rights First** - Support research that advances protections
1. **Open Science** - Maximize accessibility and reproducibility
1. **Responsible Research** - Do no harm, ensure integrity
1. **Community Benefit** - Serve researchers, advocates, and affected communities

This project exists to shine light on digital rights protections (or lack thereof) for vulnerable populations. Every governance decision should serve that mission.

______________________________________________________________________

**Last updated:** January 2026
