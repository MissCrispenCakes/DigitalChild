# Data Verification Checklist

**Created:** 2026-01-20
**Purpose:** Track verification of substantive data conflicts between scorecard files

## Instructions

For each item:
1. Check source URLs in both files
2. Verify current status from official sources
3. Mark correct value
4. Update canonical file
5. Document source in changelog

---

## High Priority Conflicts

### Algeria

#### ✅ AI_Policy_Status
- [ ] **Presentation value:** "None – No formal AI strategy; digital transformation working groups explore AI use (2024)"
- [ ] **MASTER value:** "Adopted (National AI Strategy adopted Dec 2024)"
- [ ] **Verification needed:** Did Algeria adopt National AI Strategy in December 2024?
- [ ] **Source to check:** Presentation file source URL, Algeria government gazette
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

---

### Albania

#### ✅ AI_Policy_Status
- [ ] **Presentation value:** "Partial – Digital Agenda 2022–2026 covers AI, no standalone AI strategy"
- [ ] **MASTER value:** "Draft/Consultation open (National AI Strategy 2025–2030)"
- [ ] **Verification needed:** Is Albania's AI Strategy 2025-2030 in draft/consultation?
- [ ] **Source to check:** Albania Ministry of Digital Transformation
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

#### ✅ Data_Protection_Law
- [ ] **Presentation value:** "In force – Law No. 9887/2008 on Protection of Personal Data (aligned with EU GDPR 2018)"
- [ ] **MASTER value:** "In force (Law 124/2024; GDPR-based)"
- [ ] **Verification needed:** Did Law 124/2024 supersede Law 9887/2008?
- [ ] **Source to check:** Albania Official Gazette, Commissioner for Right to Information
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

#### ✅ Children_Data_Safeguards
- [ ] **Presentation value:** "Partial – General DP law covers children; no child online safety law"
- [ ] **MASTER value:** "Yes"
- [ ] **Verification needed:** Does Albania have dedicated child data safeguards or only general coverage?
- [ ] **Source to check:** Law 124/2024 text, Law 9887/2008 provisions
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

#### ✅ DPIA_Required_High_Risk_AI
- [ ] **Presentation value:** "No legal requirement – DPIA not specifically required for AI/automated systems"
- [ ] **MASTER value:** "Yes"
- [ ] **Verification needed:** Does current law (124/2024?) require DPIA for high-risk AI?
- [ ] **Source to check:** Law 124/2024 provisions, GDPR alignment documentation
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

---

### Botswana

#### ✅ Data_Protection_Law
- [ ] **Presentation value:** "In force — Data Protection Act 2024 (Act 18 of 2024), commenced October 2024"
- [ ] **MASTER value:** "In force (Data Protection Act 2018; DPA launched 2021)"
- [ ] **Verification needed:** Is it Act 18 of 2024 or Act of 2018? When did it commence?
- [ ] **Source to check:** Botswana Government Gazette, IDPC website
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

#### ✅ SOGI_Sensitive_Data
- [ ] **Presentation value:** "Yes — DPA 2024 s.30 prohibits processing data revealing sex or sexual orientation"
- [ ] **MASTER value:** "No"
- [ ] **Verification needed:** Does Botswana DPA include SOGI as sensitive/special category?
- [ ] **Source to check:** Data Protection Act text section 30
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

#### ✅ DPIA_Required_High_Risk_AI
- [ ] **Presentation value:** "Yes — DPA 2024 Part XII requires Data Protection Impact Assessment for high-risk processing"
- [ ] **MASTER value:** "No"
- [ ] **Verification needed:** Does Botswana DPA require DPIA for high-risk processing?
- [ ] **Source to check:** Data Protection Act Part XII
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

---

### South Africa

#### ✅ AI_Policy_Status
- [ ] **Presentation value:** "National AI Policy Framework published (Oct 2024) for consultation; not yet law"
- [ ] **MASTER value:** "Draft/Early — AI White Paper in preparation"
- [ ] **Verification needed:** Current status of South Africa AI Policy Framework
- [ ] **Source to check:** Department of Communications and Digital Technologies
- **Correct value:** _________________
- **Source URL:** _________________
- **Notes:** _________________

---

## Medium Priority: Verbosity/Formatting Differences

These have the same core information but different detail levels. Standardize to consistent format.

### Format Standard Template

```
[Status] ([Law Name/Number Year]) – [Additional details]
```

**Examples:**
- ✅ GOOD: "In force (Law 18-07 of 2018) – ANPDP operational Aug 2022"
- ❌ BAD: "In force – Law 18-07 on Protection of Individuals in Processing Personal Data (2018)"
- ❌ BAD: "Yes"

### Countries Needing Reformatting

- [ ] Algeria: All indicators - standardize to format template
- [ ] Albania: All indicators - standardize to format template
- [ ] Botswana: All indicators - standardize to format template
- [ ] Kenya: All indicators - standardize to format template
- [ ] Nigeria: All indicators - standardize to format template
- [ ] South Africa: All indicators - standardize to format template

---

## Source URL Verification

### Files to Cross-Reference

1. **Presentation file:** `data/scorecard/scorecard_main_presentation.xlsx`
   - Check columns: `[Indicator]_Source` (10 source columns)

2. **Policy Matrix file:** `data/scorecard/_GLOBAL_Policy_Matrix_UPR_Main_FINAL.xlsx`
   - Dedicated source verification workflow

3. **Archived sources file:** `data/archive/scorecard_main_ALL_filled_sources.xlsx`
   - Check if has unique source URLs not in presentation file

### Source Verification Protocol

For each country-indicator combination:

1. [ ] Extract source URL from presentation file
2. [ ] Verify URL is accessible (not 404)
3. [ ] Check if URL content matches indicator value
4. [ ] If source is outdated/broken:
   - Search for updated official source
   - Update URL in canonical file
   - Document change in changelog
5. [ ] Mark verification date in tracking column

---

## Automated Verification Script

```python
# Run this to check which source URLs are accessible
import pandas as pd
import requests
from datetime import datetime

presentation = pd.read_excel('data/scorecard/scorecard_main_presentation.xlsx', sheet_name='UN_194')

source_cols = [col for col in presentation.columns if 'Source' in col]

results = []
for idx, row in presentation.iterrows():
    country = row['Country']
    for source_col in source_cols:
        url = row[source_col]
        if pd.notna(url) and url.strip():
            try:
                resp = requests.head(url, timeout=10, allow_redirects=True)
                status = 'OK' if resp.status_code == 200 else f'Error {resp.status_code}'
            except Exception as e:
                status = f'Failed: {str(e)[:50]}'

            results.append({
                'Country': country,
                'Indicator': source_col.replace('_Source', ''),
                'URL': url,
                'Status': status,
                'Checked': datetime.now().strftime('%Y-%m-%d')
            })

verification_df = pd.DataFrame(results)
verification_df.to_excel('data/source_verification_results.xlsx', index=False)
print(f"Verified {len(results)} source URLs. Results saved to data/source_verification_results.xlsx")
```

---

## Completion Tracking

**Total items:** 9 high-priority conflicts + source verification

**Completed:** _____ / 9

**Started:** __________
**Target completion:** __________
**Actual completion:** __________

---

## Notes & Findings

### Patterns Observed
- MASTER file may have been updated post-conference (Sept 2025) with late-2024 changes
- Presentation file has most complete source documentation
- Some conflicts are due to laws passed/updated between Sept 2025 (conference) and Jan 2026

### Recommended Follow-up
1. Establish update schedule (quarterly review of all 194 countries)
2. Set up Google Alerts for "AI policy" + country names
3. Monitor UNCTAD, GSMA, UPR databases for policy changes
4. Create automated source URL checking script (monthly)

### Questions for Review
- Should we track policy changes in a separate "Updates Log" sheet?
- Do we need a "Last Verified" date column for each indicator?
- Should we mark indicators with conflicting sources for deeper research?

---

**Last updated:** 2026-01-20
**Updated by:** _________________
