# Release & Zenodo Corrections Needed

**Date:** 2026-01-26
**Priority:** CRITICAL - Must fix before next release/Zenodo publication

---

## Critical Issues Found

### 1. INCORRECT Indicators in v1.0.0 Release Notes

**File:** `RELEASE_NOTES_v1.0.0.md` (lines 34-44)

**Problem:** Lists WRONG indicators that were NEVER part of LittleRainbowRights scorecard

**Current (WRONG) indicators listed:**
```markdown
- AI Policy Status ✅ (correct)
- Data Protection Law ✅ (correct)
- LGBTQ Legal Status ✅ (correct)
- Child Online Protection ✅ (correct)
- Biometric SIM Registration ✅ (correct)
- Digital Services Taxation ❌ (WRONG - never existed)
- Internet Penetration ❌ (WRONG - never existed)
- Mobile Coverage ❌ (WRONG - never existed)
- Digital Skills Investment ❌ (WRONG - never existed)
- Online Content Regulation ❌ (WRONG - never existed)
```

**Correct indicators should be:**
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

**Impact:**
- This incorrect information is on the public GitHub releases page
- Misleads anyone citing the v1.0.0 release
- Damages credibility of the research
- Could be indexed by Zenodo with wrong metadata

**Action Required:**
- ✅ RELEASE_NOTES_DRAFT.md already has the correction (lines 123-131)
- ❌ Need to publish corrected release notes as v1.0.2 or v2.0.0
- ❌ Need to add correction notice to v1.0.0 release (can't edit, must add comment or deprecation note)

---

### 2. Outdated Version in CITATION.cff

**File:** `CITATION.cff` (line 27)

**Current:**
```yaml
version: "0.9.0"
date-released: "2026-01-19"
```

**Problem:**
- Version is 0.9.0 but v1.0.0 and v1.0.1 have already been released
- This file feeds Zenodo metadata
- Incorrect version will be cited in academic publications

**Should be:**
```yaml
version: "1.0.1"  # Or "2.0.0" if preparing for next major release
date-released: "2026-01-20"  # Match actual release date
```

---

### 3. Placeholder DOI in CITATION.cff

**File:** `CITATION.cff` (line 29)

**Current:**
```yaml
doi: "[YOUR-DOI-IF-PUBLISHED]"
# Uncomment and fill when you have a DOI (e.g., from Zenodo)
```

**Problem:**
- DOI is a placeholder
- The draft release notes reference DOI: 10.5281/zenodo.18318099
- Need to confirm if this DOI is real and active

**Action Required:**
- Verify Zenodo DOI: https://doi.org/10.5281/zenodo.18318099
- If confirmed, update CITATION.cff with:
  ```yaml
  doi: "10.5281/zenodo.18318099"
  ```
- If not confirmed, keep commented out until DOI is issued

---

### 4. Version Mismatch Across Files

**Current state:**
- `CITATION.cff`: version "0.9.0"
- `CHANGELOG.md`: Has [1.0.1] and [1.0.0] sections, but [Unreleased] is draft v2.0.0 content
- `RELEASE_NOTES_v1.0.0.md`: References v1.0.1 in citation (line 63)
- `RELEASE_NOTES_DRAFT.md`: Preparing v2.0.0
- Git tags: v1.0.0, v1.0.1 exist (from git log)

**Recommended Version Strategy:**

**Option A - Immediate Patch Release v1.0.2:**
```
Purpose: Correct v1.0.0 release notes errors
Changes:
- Update CITATION.cff to v1.0.2
- Add RELEASE_NOTES_v1.0.2.md with correction notice
- Update CHANGELOG.md
Timeline: Now (before Zenodo publication)
```

**Option B - Wait for v2.0.0:**
```
Purpose: Include API release + corrections
Changes:
- Update CITATION.cff to v2.0.0
- Publish RELEASE_NOTES_DRAFT.md as v2.0.0
- Note v1.0.0 errors in release notes
Timeline: When Phase 4 API work is complete
```

**Recommendation:** Do Option A now to fix critical errors, then do Option B when API is stable.

---

## Zenodo Publication Checklist

Before publishing to Zenodo:

### Metadata Verification
- [ ] Confirm correct version number in CITATION.cff
- [ ] Verify all 10 indicators are correctly listed
- [ ] Confirm DOI or mark as placeholder
- [ ] Check author names and ORCID match publication records
- [ ] Verify license (MIT for code, CC BY 4.0 for data)
- [ ] Confirm repository URL (https://github.com/MissCrispenCakes/DigitalChild)
- [ ] Confirm website URL (https://grimdata.org)

### Release Notes Verification
- [ ] Release notes have correct indicator list
- [ ] Statistics are up-to-date (194 countries, 2,543 sources, etc.)
- [ ] Citation format is correct
- [ ] Links to documentation work
- [ ] Changelog is complete

### Code Quality Verification
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Pre-commit hooks pass (`pre-commit run --all-files`)
- [ ] No sensitive data in repository
- [ ] No API keys or credentials committed
- [ ] README.md is up-to-date

### Documentation Verification
- [ ] Website builds correctly (`mkdocs build`)
- [ ] All internal links work
- [ ] API documentation is complete
- [ ] Installation instructions are accurate
- [ ] Citation examples are correct

---

## Immediate Actions Required

### Priority 1 (CRITICAL - Before any Zenodo publication)
1. **Fix CITATION.cff version and DOI**
   - Update version to current (1.0.1 or prepare 2.0.0)
   - Add confirmed Zenodo DOI or remove placeholder

2. **Address v1.0.0 release notes error**
   - Option A: Create v1.0.2 patch with correction
   - Option B: Add prominent correction notice to v1.0.0 GitHub release

3. **Verify Zenodo DOI**
   - Check if 10.5281/zenodo.18318099 is active
   - If not, generate new DOI via Zenodo integration

### Priority 2 (HIGH - Before v2.0.0 release)
4. **Complete RELEASE_NOTES_DRAFT.md**
   - Finalize v2.0.0 content
   - Update statistics if needed
   - Verify all links work

5. **Update CHANGELOG.md**
   - Move [Unreleased] content to [2.0.0] section when ready
   - Ensure consistency with release notes

### Priority 3 (MEDIUM - Documentation improvements)
6. **Implement website restructure** (see WEBSITE_RESTRUCTURE_PLAN.md)
   - Create landing pages
   - Fix navigation
   - Organize scorecard and API sections

---

## Files That Need Updates

### Must Update Now (Before Zenodo)
- `CITATION.cff` - version and DOI
- `RELEASE_NOTES_v1.0.0.md` - add correction notice OR
- Create `RELEASE_NOTES_v1.0.2.md` with corrections

### Should Update Soon (Before v2.0.0)
- `CHANGELOG.md` - move unreleased to v2.0.0 when ready
- `RELEASE_NOTES_DRAFT.md` - finalize and publish as v2.0.0
- `mkdocs.yml` - implement navigation fixes

### Nice to Have
- All docs/ files affected by website restructure

---

## Verification Commands

Before releasing:

```bash
# 1. Check version consistency
grep -r "version" CITATION.cff CHANGELOG.md RELEASE_NOTES*.md

# 2. Verify tests pass
pytest tests/ -v

# 3. Verify pre-commit passes
pre-commit run --all-files

# 4. Build documentation
mkdocs build

# 5. Verify no sensitive data
git log --all --full-history --source --pretty=format: --name-only | sort -u | grep -i "secret\|key\|password\|token"

# 6. Check for correct indicators in all docs
grep -r "Digital Services Taxation\|Internet Penetration\|Mobile Coverage" docs/

# Should return ONLY matches from this file and RELEASE_NOTES_v1.0.0.md
# If found elsewhere, those need correction too
```

---

## Questions to Answer

1. **Is Zenodo DOI 10.5281/zenodo.18318099 real and active?**
   - If yes: Update CITATION.cff
   - If no: Get new DOI before publishing

2. **What version should be the next release?**
   - v1.0.2 (patch to fix errors) OR
   - v2.0.0 (major release with API)

3. **Is v1.0.0 release already on Zenodo?**
   - If yes: Cannot change, must release correction
   - If no: Can update before publishing

4. **When is API (Phase 4) complete enough for v2.0.0?**
   - If soon: Wait and do v2.0.0
   - If not soon: Do v1.0.2 now, v2.0.0 later

---

## Recommended Workflow

**Scenario: Need to publish to Zenodo NOW**

1. Check Zenodo DOI status
2. Update CITATION.cff:
   ```yaml
   version: "1.0.1"
   date-released: "2026-01-20"
   doi: "10.5281/zenodo.XXXXX"  # or comment out if not available
   ```
3. Create v1.0.2 release with corrected notes:
   ```bash
   # Tag the release
   git tag -a v1.0.2 -m "Corrected indicator list in documentation"

   # Create RELEASE_NOTES_v1.0.2.md
   # Copy RELEASE_NOTES_v1.0.0.md but fix indicators section

   # Push
   git push origin v1.0.2
   ```
4. Add correction notice to v1.0.0 GitHub release page
5. Publish v1.0.2 to Zenodo

**Scenario: Can wait for v2.0.0**

1. Complete Phase 4 API work
2. Update CITATION.cff to v2.0.0
3. Finalize RELEASE_NOTES_DRAFT.md
4. Update CHANGELOG.md
5. Tag and release v2.0.0
6. Publish to Zenodo with correct metadata

---

## Contact

For questions about this correction:
- See: docs/CONTRIBUTING.md
- GitHub: https://github.com/MissCrispenCakes/DigitalChild/issues

---

**Last Updated:** 2026-01-26
**Status:** Awaiting decision on release strategy
