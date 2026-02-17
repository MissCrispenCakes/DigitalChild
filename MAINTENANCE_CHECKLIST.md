# Maintenance Checklist

**Purpose:** Track files requiring updates during releases, version changes, and regular maintenance.

**Last Updated:** February 2026 (v2.0.1)

---

## 🔴 CRITICAL - Update on Every Release

These files MUST be updated with every version release:

### 1. CITATION.cff
**Location:** `/CITATION.cff`

**Update:**
- [ ] `version:` field (e.g., "2.0.1")
- [ ] `date-released:` field (YYYY-MM-DD)
- [ ] Verify author ORCIDs are current
- [ ] Check all DOI references
- [ ] Review keywords for accuracy

**Last Updated:** v2.0.1 (2026-02-16)

---

### 2. SECURITY.md
**Location:** `/SECURITY.md`

**Update:**
- [ ] Supported Versions table
- [ ] "Last updated" date at bottom
- [ ] Any version-specific security notes

**Last Updated:** v2.0.1 (2026-02-17)

---

### 3. README.md
**Location:** `/README.md`

**Update:**
- [ ] Version badges (if present)
- [ ] Quick Start version references
- [ ] Installation instructions
- [ ] API version references
- [ ] Documentation links

**Last Updated:** v2.0.0

---

## 🟡 IMPORTANT - Update When Significant Changes

### 4. CHANGELOG.md
**Location:** `/CHANGELOG.md` (if exists)

**Update:**
- [ ] Add new version section
- [ ] Document breaking changes
- [ ] List new features
- [ ] Note bug fixes
- [ ] Migration instructions

---

### 5. docs/ROADMAP.md
**Location:** `/docs/ROADMAP.md`

**Update:**
- [ ] Mark completed features
- [ ] Update phase statuses
- [ ] Add new planned features
- [ ] Update timelines

**Last Updated:** v2.0.0

---

### 6. Package Configuration
**Locations:** `setup.py`, `pyproject.toml` (if they exist)

**Update:**
- [ ] Version numbers
- [ ] Dependencies
- [ ] Python version requirements
- [ ] Entry points

---

### 7. Dependencies
**Locations:**
- `/requirements.txt`
- `/api_requirements.txt`

**Update:**
- [ ] Pin dependency versions
- [ ] Check for security updates
- [ ] Test compatibility
- [ ] Update Python version requirement

**Last Updated:** v2.0.0

---

### 8. API Documentation
**Location:** `/api/` and `/docs/api/`

**Update:**
- [ ] Endpoint changes
- [ ] New routes
- [ ] Deprecated endpoints
- [ ] Version compatibility notes
- [ ] Example requests/responses

**Last Updated:** v2.0.0

---

### 9. GitHub Release Notes
**Location:** GitHub Releases page

**Create:**
- [ ] Feature descriptions
- [ ] Breaking changes
- [ ] Migration guides
- [ ] Full changelog link
- [ ] Zenodo DOI reference

**Last Release:** v2.0.1

---

### 10. paper.md (JOSS)
**Location:** `/paper.md`

**Update (if resubmitting):**
- [ ] Author affiliations
- [ ] New citations
- [ ] Software version references
- [ ] Impact statement updates

**Last Updated:** v2.0.1 (JOSS submission ready)

---

## 🟢 REVIEW - Check Quarterly or When Relevant

### 11. LICENSE Files
**Locations:** `/LICENSE`, `/LICENSE-DATA`

**Review:**
- [ ] Copyright year
- [ ] Licensing terms
- [ ] Third-party attributions

**Last Updated:** 2025

---

### 12. CONTRIBUTING.md
**Location:** `/CONTRIBUTING.md` (if exists)

**Review:**
- [ ] Setup instructions
- [ ] Version requirements
- [ ] Development workflow
- [ ] Testing procedures

---

### 13. CODE_OF_CONDUCT.md
**Location:** `/CODE_OF_CONDUCT.md` (if exists)

**Review:**
- [ ] Contact information
- [ ] Enforcement procedures
- [ ] Community guidelines

---

### 14. Documentation Guides
**Location:** `/docs/guides/`

**Review:**
- [ ] Installation steps
- [ ] Version-specific instructions
- [ ] Screenshots (if outdated)
- [ ] Command examples
- [ ] API examples

---

### 15. Standards Documentation
**Location:** `/docs/standards/`

**Review:**
- [ ] API standards
- [ ] Coding standards
- [ ] Data schemas
- [ ] File naming conventions

---

### 16. CI/CD Workflows
**Location:** `.github/workflows/`

**Review:**
- [ ] Python version in CI
- [ ] Dependency versions
- [ ] GitHub Action versions
- [ ] Test commands
- [ ] Deployment scripts

**Last Updated:** v2.0.1 (draft-pdf.yml added)

---

### 17. Docker Configuration
**Location:** Docker files (if exist)

**Review:**
- [ ] Base image versions
- [ ] Python versions
- [ ] Dependency installations
- [ ] Environment variables

---

### 18. Scorecard Data
**Location:** `/data/scorecard/scorecard_main.xlsx`

**Maintain:**
- [ ] Validate source URLs
- [ ] Update indicators
- [ ] Check for broken links
- [ ] Add new countries/data

**Frequency:** Quarterly or as sources update

---

## 🔵 MAINTENANCE - Annual Review

### 19. AUTHORS File
**Location:** `/AUTHORS` (if exists)

**Review:**
- [ ] Contributor list
- [ ] ORCIDs
- [ ] Affiliations
- [ ] Contact information

---

### 20. ACKNOWLEDGEMENTS
**Location:** `/ACKNOWLEDGEMENTS` or in README

**Review:**
- [ ] Funding sources
- [ ] Institutional support
- [ ] Contributors
- [ ] Conference presentations

---

### 21. DATA_GOVERNANCE.md
**Location:** `/docs/DATA_GOVERNANCE.md`

**Review:**
- [ ] Data policies
- [ ] Privacy guidelines
- [ ] Contact information
- [ ] Compliance requirements

---

### 22. RESEARCH_CONTEXT.md
**Location:** `/docs/RESEARCH_CONTEXT.md`

**Review:**
- [ ] Citations
- [ ] Conference presentations
- [ ] Publications
- [ ] Impact metrics

---

## 📋 Version Release Checklist

Use this when preparing a new release:

### Pre-Release:
- [ ] Update CITATION.cff (version + date)
- [ ] Update SECURITY.md (supported versions)
- [ ] Update README.md (if needed)
- [ ] Review CHANGELOG.md
- [ ] Check dependencies for updates
- [ ] Run full test suite
- [ ] Verify CI/CD passes
- [ ] Update API documentation (if changed)

### Release:
- [ ] Create git tag (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`)
- [ ] Push tag (`git push origin vX.Y.Z`)
- [ ] Create GitHub Release
- [ ] Verify Zenodo archive created
- [ ] Check Zenodo metadata

### Post-Release:
- [ ] Announce on GitHub Discussions
- [ ] Update project website (if applicable)
- [ ] Notify major users (if applicable)
- [ ] Plan next release cycle

---

## 🔍 File Status Quick Reference

| File | Last Updated | Version | Status |
|------|--------------|---------|--------|
| CITATION.cff | 2026-02-16 | 2.0.1 | ✅ Current |
| SECURITY.md | 2026-02-17 | 2.0.1 | ✅ Current |
| README.md | 2026-01-27 | 2.0.0 | ⚠️ Check |
| paper.md | 2026-02-16 | 2.0.1 | ✅ Current |
| requirements.txt | 2026-01-26 | 2.0.0 | ⚠️ Check deps |
| .github/workflows/ | 2026-02-16 | 2.0.1 | ✅ Current |

---

## 📝 Notes

**Automation Opportunities:**
- Version bumping could be scripted
- Dependency checking via Dependabot (already enabled)
- Automated changelog generation

**Best Practices:**
- Always update CITATION.cff first (single source of truth for version)
- Test locally before release
- Never skip CI/CD checks
- Document breaking changes prominently

---

**Maintained by:** Project maintainers
**Next Review:** Before v2.1.0 or March 2026 (whichever comes first)
