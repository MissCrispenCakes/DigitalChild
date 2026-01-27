# Website & Documentation Restructure Plan

**Date:** 2026-01-26
**Status:** Proposed
**Goal:** Create logical, consistent structure with proper landing pages and clear navigation

---

## Current Problems Identified

### 1. Navigation Inconsistencies

❌ **Issue:** Top navigation has both "Scorecard" and "Data Explorer" as separate top-level items, but both point to `docs/scorecard/` directory
- Line 145: `- Scorecard: scorecard/index.md`
- Line 146: `- Data Explorer: scorecard/explorer.md`

❌ **Issue:** API section uses emojis in navigation (🆕 NEW - REST API) - unprofessional for production
- Line 139: `- 🆕 NEW - REST API:`

❌ **Issue:** Inconsistent naming between navigation labels and actual page titles
- Nav says "Scorecard Visualization" (line 161) but links to `scorecard/index.md`
- Nav has redundant entries (scorecard appears twice in the Projects > LittleRainbowRights section)

### 2. File Organization Issues

❌ **Issue:** Scorecard files scattered across multiple locations:
- `docs/scorecard/index.md` (main visualization page)
- `docs/scorecard/explorer.md` (future interactive explorer)
- `docs/website/scorecard/` (empty directory)
- `docs/guides/SCORECARD_WORKFLOW.md` (technical guide)
- `docs/maintenance/SCORECARD_*.md` (maintenance docs)

❌ **Issue:** API documentation duplicated:
- `docs/api/README.md` (full documentation)
- `docs/api/QUICK_START.md` (quick start guide)
- `docs/website/api-reference.md` (duplicate quick reference)

❌ **Issue:** No clear separation between:
- User-facing website content (`docs/website/`)
- Technical documentation (`docs/`)
- Developer guides (`docs/guides/`)

### 3. Missing Landing Pages

❌ **Missing:** Scorecard landing page explaining:
- What the scorecard is
- Why it exists
- What problems it solves
- How to use it (overview, then links to sub-sections)

❌ **Missing:** API landing page explaining:
- What the API provides
- Use cases
- Quick comparison: API vs CSV exports vs direct file access
- Links to Quick Start, Full Docs, Reference

❌ **Missing:** Clear section organization for scorecard subsections:
- Design & Methodology
- Data Access (API)
- Visualization (current + future)
- Data Explorer (interactive tool)

---

## Proposed New Structure

### Directory Organization

```
docs/
├── website/                          # User-facing website content
│   ├── index.md                      # GRIMdata home page ✅ (exists)
│   ├── getting-started/              # Getting started guides ✅
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── projects/                     # Projects section ✅
│   │   ├── index.md                  # Projects landing page
│   │   ├── littlerainbowrights/
│   │   │   └── index.md
│   │   └── sgbv/
│   │       └── index.md
│   ├── api/                          # API section (NEW organization)
│   │   ├── index.md                  # 🆕 API landing page (to create)
│   │   ├── quickstart.md             # Quick start guide (move from docs/api/)
│   │   ├── reference.md              # Full API reference (move from docs/api/README.md)
│   │   └── quick-reference.md        # Quick reference table (current api-reference.md)
│   ├── scorecard/                    # Scorecard section (NEW organization)
│   │   ├── index.md                  # 🆕 Scorecard landing page (to create)
│   │   ├── design.md                 # 🆕 Design & methodology (to create)
│   │   ├── data-access.md            # 🆕 How to access scorecard data via API (to create)
│   │   ├── visualization.md          # Current scorecard/index.md (renamed)
│   │   └── explorer.md               # Interactive data explorer (current explorer.md)
│   └── about/                        # About section
│       └── research-context.md
├── api/                              # API technical docs (keep for legacy, deprecate over time)
│   ├── QUICK_START.md                # ⚠️  Move to website/api/quickstart.md
│   ├── README.md                     # ⚠️  Move to website/api/reference.md
│   └── SYNC_NOTE.md                  # ⚠️  Internal note, move to docs/notes/
├── guides/                           # User guides for running the pipeline
│   ├── RUNBOOK.md
│   ├── SCORECARD_WORKFLOW.md         # Technical workflow for developers
│   ├── FIRST_RUN_ERRORS.md
│   ├── VALIDATORS_USAGE.md
│   └── PRODUCTION_DEPLOYMENT.md
├── standards/                        # Technical standards for developers
│   ├── METADATA_SCHEMA.md
│   ├── FILE_NAMING_STANDARDS.md
│   └── ...
├── notes/                            # Internal development notes
├── planning/                         # Planning documents
├── maintenance/                      # Maintenance logs and reports
└── reviews/                          # Review summaries
```

### Navigation Structure (mkdocs.yml)

```yaml
nav:
  - GRIMdata Home: website/index.md

  - Getting Started:
      - Installation: website/getting-started/installation.md
      - Quick Start: website/getting-started/quickstart.md
      - First Run Errors: guides/FIRST_RUN_ERRORS.md
      - FAQ: FAQ.md

  - API:
      - Overview: website/api/index.md                      # 🆕 NEW landing page
      - Quick Start: website/api/quickstart.md              # Moved from docs/api/
      - Full Documentation: website/api/reference.md        # Moved from docs/api/README.md
      - Quick Reference: website/api/quick-reference.md     # Current api-reference.md

  - Scorecard:
      - Overview: website/scorecard/index.md                # 🆕 NEW landing page
      - Design & Methodology: website/scorecard/design.md   # 🆕 NEW
      - Data Access (API): website/scorecard/data-access.md # 🆕 NEW
      - Visualization: website/scorecard/visualization.md   # Current scorecard/index.md
      - Data Explorer: website/scorecard/explorer.md        # Current scorecard/explorer.md

  - Projects:
      - Overview: website/projects/index.md
      - LittleRainbowRights:
          - Project Overview: website/projects/littlerainbowrights/index.md
          - User Guides:
              - Runbook: guides/RUNBOOK.md
              - Scorecard Workflow: guides/SCORECARD_WORKFLOW.md
              - Validators Usage: guides/VALIDATORS_USAGE.md
              - Production Deployment: guides/PRODUCTION_DEPLOYMENT.md
          - Documentation:
              - Architecture: ARCHITECTURE.md
              - Glossary: GLOSSARY.md
              - Data Governance: DATA_GOVERNANCE.md
              - Docs Index: DOCS_INDEX.md
          - Development:
              - Roadmap: ROADMAP.md
              - Standards:
                  - Metadata Schema: standards/METADATA_SCHEMA.md
                  - File Naming: standards/FILE_NAMING_STANDARDS.md
                  - Document Types: standards/DOC_TYPE_STANDARDS.md
                  - Scraper Structure: standards/SCRAPER_STRUCTURE.md
                  - Tags Config: standards/TAGS_CONFIG_FORMAT.md
                  - Recommendations Config: standards/RECOMMENDATIONS_CONFIG_FORMAT.md
                  - Comparison Config: standards/COMPARISON_CONFIG_FORMAT.md
                  - Filters Config: standards/FILTERS_CONFIG_FORMAT.md
                  - ISO Mapping: standards/ISO_MAPPING.md
              - Notes:
                  - Directory Structure: notes/DIRECTORY_STRUCTURE.md
                  - Pipeline Flow: notes/PIPELINE_FLOW.md
                  - Pipeline Logging: notes/PIPELINE_LOGGING.md
                  - Tags Main Notes: notes/TAGS_MAIN_NOTES.md
                  - Tags Export Notes: notes/TAGS_EXPORT_NOTES.md
                  - Comparison Export Notes: notes/COMPARISON_EXPORT_NOTES.md
              - Planning:
                  - Source Feasibility: planning/SOURCE_FEASIBILITY_CHECKLIST.md
                  - Tags Visualization: planning/TAGS_VISUALIZATION_PLAN.md
              - Reviews:
                  - Scorecard Review: reviews/SCORECARD_REVIEW_SUMMARY.md
                  - Processor Tests: reviews/PROCESSOR_TEST_RUN.md
      - SGBV-UPR:
          - Project Overview: website/projects/sgbv/index.md

  - About:
      - Research Context: RESEARCH_CONTEXT.md
      - Contributing: CONTRIBUTING.md
```

---

## New Pages to Create

### 1. API Landing Page (`docs/website/api/index.md`)

**Purpose:** Explain what the API is, why use it, and guide users to appropriate sub-sections

**Content outline:**
```markdown
# GRIMdata REST API

## Overview
Brief explanation of what the API provides (access to 78+ documents, 194-country scorecard, tags analysis, timeline data)

## Why Use the API?
- Programmatic access to data
- Real-time queries
- Integration with other tools
- Better than manual CSV downloads for automated workflows

## Quick Comparison

| Access Method | Best For | Setup Time |
|---------------|----------|------------|
| REST API | Programmatic access, integrations | 5 minutes |
| CSV Export | One-time analysis, Excel/R | 2 minutes |
| Direct Files | Deep exploration, custom processing | Immediate |

## Get Started

Quick links:
- [🚀 Quick Start Guide](quickstart.md) - Get running in 5 minutes
- [📖 Full Documentation](reference.md) - Complete API reference
- [⚡ Quick Reference](quick-reference.md) - Endpoint cheat sheet

## Features
- 14 production-ready endpoints
- Advanced filtering and pagination
- Rate limiting and caching
- Docker deployment ready
- 100% test coverage

## Example Use Cases
- Fetch all documents about AI policy in Africa
- Get LGBTQ+ legal status for specific countries
- Download scorecard data as CSV
- Track tags over time (2018-2024)

[Continue with examples and links to sub-pages]
```

### 2. Scorecard Landing Page (`docs/website/scorecard/index.md`)

**Purpose:** Explain what the scorecard is, its purpose, and guide users to detailed sections

**Content outline:**
```markdown
# Digital Rights Scorecard

## What is the Scorecard?

The Digital Rights Scorecard tracks **10 key indicators** across **194 countries** to assess digital rights protections for vulnerable populations, particularly LGBTQ+ individuals and children.

## Why It Exists

[Brief explanation of the research context and goals]

## What It Tracks

**10 Indicators:**
1. Data Protection Law
2. DPA Independence
3. Children's Data Safeguards
4. Child Online Protection Strategy
5. SOGI Sensitive Data Protections
6. LGBTQ+ Legal Status
7. LGBTQ+ Promotion/Propaganda Offences
8. AI Policy Status
9. DPIA Required for High-Risk AI
10. SIM Card Biometric ID Linkage

**194 Countries:** Comprehensive global coverage

**2,543 Source URLs:** Validated authoritative sources

## Explore the Scorecard

Choose your path:

### Learn About the Design
[Design & Methodology →](design.md)
- Indicator definitions
- Scoring system (0-1-2 scale)
- Data sources and validation
- Composite metrics

### Access the Data
[Data Access (API) →](data-access.md)
- REST API endpoints
- CSV exports
- Python examples
- Direct file access

### Visualize the Data
[Visualization →](visualization.md)
- Current: CSV exports, API queries
- Future: Interactive heatmaps, country cards, regional comparisons

### Interactive Explorer
[Data Explorer →](explorer.md)
- Coming soon: Filter, search, compare countries
- Current: Use API or CSV exports

## Quick Stats

📊 **194 Countries** | 🔍 **10 Indicators** | 🔗 **2,543 Sources** | 📅 **Updated Jan 2026**

## Use Cases

- Research: Identify patterns in digital rights protections
- Advocacy: Compare countries and track policy changes
- Risk Assessment: Evaluate digital safety for vulnerable groups
- Policy Analysis: Understand global trends in digital governance

## Citation

[Include citation format]
```

### 3. Scorecard Design & Methodology (`docs/website/scorecard/design.md`)

**Purpose:** Detailed explanation of the scorecard's design, indicators, scoring system

**Content:** Move the detailed indicator definitions from current `docs/scorecard/index.md` here

### 4. Scorecard Data Access (`docs/website/scorecard/data-access.md`)

**Purpose:** Central page explaining all ways to access scorecard data

**Content outline:**
```markdown
# Accessing Scorecard Data

## Overview

Multiple ways to access the scorecard data depending on your needs.

## Option 1: REST API (Recommended for Programmatic Access)

### Endpoints
- `GET /api/scorecard` - All countries summary
- `GET /api/scorecard/:country` - Specific country details
- `GET /api/scorecard/indicators/statistics` - Indicator statistics

### Quick Example
```bash
# Get Kenya's scorecard
curl http://localhost:5000/api/scorecard/Kenya
```

### Python Example
```python
import requests
response = requests.get("http://localhost:5000/api/scorecard/Kenya")
scorecard = response.json()["data"]
print(scorecard["indicators"])
```

[Link to full API documentation]

## Option 2: CSV Export

[Instructions for CSV export via pipeline]

## Option 3: Direct File Access

[Instructions for accessing scorecard_main.xlsx directly]

## Option 4: Pipeline Integration

[Instructions for using scorecard in pipeline]

## Comparison Table

| Method | Best For | Setup |
|--------|----------|-------|
| REST API | Automation, integration | `python run_api.py` |
| CSV Export | Excel analysis | `pipeline_runner.py --mode scorecard --scorecard-action export` |
| Direct File | Manual exploration | Open `scorecard_main.xlsx` |
| Pipeline | Document enrichment | Used automatically in pipeline |
```

---

## Implementation Steps

### Phase 1: Create New Landing Pages (Priority: HIGH)

1. **Create `docs/website/api/index.md`**
   - API overview and landing page
   - Links to Quick Start, Full Docs, Quick Reference

2. **Create `docs/website/scorecard/index.md`**
   - Scorecard landing page
   - Explain what it is, why it exists, how to use it
   - Links to Design, Data Access, Visualization, Explorer

3. **Create `docs/website/scorecard/design.md`**
   - Move detailed indicator definitions from current scorecard/index.md
   - Add methodology explanation
   - Include scoring system details

4. **Create `docs/website/scorecard/data-access.md`**
   - Central page for all data access methods
   - API endpoints specific to scorecard
   - CSV export instructions
   - Direct file access
   - Python examples

### Phase 2: Move and Rename Files (Priority: MEDIUM)

5. **Rename `docs/scorecard/index.md` → `docs/website/scorecard/visualization.md`**
   - This is the visualization page, not the landing page
   - Keep all visualization content

6. **Move `docs/scorecard/explorer.md` → `docs/website/scorecard/explorer.md`**
   - Keep as-is, just move to website directory

7. **Move `docs/api/QUICK_START.md` → `docs/website/api/quickstart.md`**
   - Rename to use lowercase for consistency
   - Update internal links

8. **Move `docs/api/README.md` → `docs/website/api/reference.md`**
   - This is the full reference documentation
   - Update internal links

9. **Rename `docs/website/api-reference.md` → `docs/website/api/quick-reference.md`**
   - This is the quick reference table
   - Move into api/ subdirectory

### Phase 3: Update Navigation (Priority: HIGH)

10. **Update `mkdocs.yml` with new navigation structure**
    - Remove emojis from navigation labels
    - Fix "Scorecard" and "Data Explorer" to be nested under Scorecard section
    - Add new API section with landing page
    - Add new Scorecard section with landing page and subsections
    - Remove redundant entries

### Phase 4: Update Cross-References (Priority: MEDIUM)

11. **Update all internal links**
    - Search for links to old paths
    - Update to new paths
    - Test all links work

12. **Update README.md and main documentation**
    - Update links to new structure
    - Update references in CLAUDE.md if needed

### Phase 5: Clean Up (Priority: LOW)

13. **Archive old files**
    - Move old docs/api/ files to docs/website/archive/ after confirming new structure works
    - Add deprecation notices if needed

14. **Update .gitignore if needed**
    - Ensure archived files are handled correctly

---

## Link Consistency Rules

### URL Patterns

**External links (absolute URLs):**
- Use full URLs: `https://github.com/...`
- Always use HTTPS

**Internal links (relative paths):**
- From any page in `docs/website/`: Use relative paths
  - Same directory: `[link](other-page.md)`
  - Parent directory: `[link](../index.md)`
  - Sibling directory: `[link](../api/index.md)`
- From any page in `docs/` root: Use relative paths from root
  - `[link](guides/RUNBOOK.md)`

### Anchor Links

- Use kebab-case: `#overview-section`
- MkDocs auto-generates anchors from headers
- Test anchor links work after restructure

### Navigation Label Consistency

| Section | Navigation Label | File Path |
|---------|-----------------|-----------|
| API Landing | "Overview" | website/api/index.md |
| API Quick Start | "Quick Start" | website/api/quickstart.md |
| API Full Docs | "Full Documentation" | website/api/reference.md |
| API Quick Ref | "Quick Reference" | website/api/quick-reference.md |
| Scorecard Landing | "Overview" | website/scorecard/index.md |
| Scorecard Design | "Design & Methodology" | website/scorecard/design.md |
| Scorecard Data | "Data Access (API)" | website/scorecard/data-access.md |
| Scorecard Viz | "Visualization" | website/scorecard/visualization.md |
| Scorecard Explorer | "Data Explorer" | website/scorecard/explorer.md |

---

## Testing Checklist

After implementation:

- [ ] All navigation links work
- [ ] All internal cross-references work
- [ ] No broken links reported by `mkdocs build`
- [ ] All pages render correctly
- [ ] Left sidebar TOC appears correctly on all pages
- [ ] Top navigation tabs work
- [ ] Breadcrumb navigation is logical
- [ ] Search functionality works
- [ ] Mobile view works correctly
- [ ] All code examples are properly formatted
- [ ] All admonitions (info, warning, etc.) render correctly

---

## Timeline Estimate

**Total: 4-6 hours**

- Phase 1 (Create landing pages): 2-3 hours
- Phase 2 (Move/rename files): 30 minutes
- Phase 3 (Update navigation): 30 minutes
- Phase 4 (Update cross-references): 1 hour
- Phase 5 (Clean up): 30 minutes
- Testing: 30 minutes

---

## Benefits of New Structure

✅ **Clear hierarchy:** Landing pages explain each section before diving into details

✅ **Consistent naming:** No more confusion between "Scorecard Visualization" and "Scorecard"

✅ **Logical nesting:** Data Explorer is under Scorecard, not a top-level item

✅ **Professional navigation:** No emojis in navigation labels

✅ **Centralized API docs:** All API content in one section

✅ **Better discoverability:** Users can easily find what they need

✅ **Future-proof:** Easy to add new scorecard features (heatmaps, country cards) under appropriate sections

---

## Notes

- Keep `docs/scorecard/` directory for now (symlinks or redirects later)
- Keep `docs/api/` directory for now with deprecation notices
- Archive old files in `docs/website/archive/` with date stamps
- Update CHANGELOG.md when restructure is complete
