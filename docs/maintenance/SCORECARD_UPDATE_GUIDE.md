# Scorecard Update Quick Reference

## How to Update Stale Entries

### Step 1: Identify Entries to Update

Run the diff report to identify stale entries:
```bash
python pipeline_runner.py --mode scorecard --scorecard-action diff
```

Review the report at: `data/exports/scorecard_diff_report.json`

### Step 2: Research Updates

#### Data Protection Laws
- **Primary Source**: [UNCTAD Data Protection Tracker](https://unctad.org/page/data-protection-and-privacy-legislation-worldwide)
- **Secondary**: National DPA websites
- Check for:
  - New laws enacted
  - Amendments to existing laws
  - Enforcement status changes

#### LGBTQ+ Legal Status
- **Primary Source**: [ILGA World Maps](https://ilga.org/maps-sexual-orientation-laws)
- **Secondary**: [ILGA State-Sponsored Homophobia Report](https://ilga.org/downloads) (annual)
- Check for:
  - Decriminalization/criminalization changes
  - New anti-LGBTQ+ legislation
  - Legal recognition changes

#### AI Policies
- **Primary Source**: [UNESCO AI Observatory](https://en.unesco.org/artificial-intelligence/observatory)
- **Secondary**: [OECD AI Policy Observatory](https://oecd.ai/)
- Check for:
  - New AI strategies adopted
  - Draft policies moving to "Adopted" status
  - Strategy updates or revisions

#### SIM Registration
- **Primary Source**: [Privacy International](https://privacyinternational.org/learn/biometric-id-databases)
- **Secondary**: National telecom regulator websites
- Check for:
  - New mandatory registration requirements
  - Biometric linkage requirements
  - Policy changes

### Step 3: Update the Excel File

1. Open `data/scorecard/scorecard_main.xlsx`
2. Navigate to the **UN_194** sheet
3. Find the country row and indicator column
4. Update the value in format:

```
[Status] — [Law/Policy Name] ([Year], [additional context])
```

Examples:
```
In force — Data Protection Act 2023
Adopted — National AI Strategy 2024
Criminalised — Penal Code 2021
```

### Step 4: Update the Source Column

Update the adjacent "Source" column with:
```
[Source Name], accessed [YYYY-MM-DD]
```

Example:
```
UNCTAD Data Protection Tracker, accessed 2026-01-25
```

### Step 5: Save and Re-export

1. Save the Excel file
2. Update the convenience copy:
   ```bash
   cp data/scorecard/scorecard_main.xlsx scorecard.xlsx
   ```
3. Re-export CSV files:
   ```bash
   python pipeline_runner.py --mode scorecard --scorecard-action export
   ```

### Step 6: Re-run Enrichment

Update document metadata with new scorecard data:
```bash
python pipeline_runner.py --mode scorecard --scorecard-action enrich
```

### Step 7: Validate Changes

Run validation to ensure no broken links:
```bash
python pipeline_runner.py --mode scorecard --scorecard-action validate
```

## Priority Countries for Update

### Phase 1 (Immediate - 20+ years old)
1. Tunisia - Data Protection Law (2004)
2. Cabo Verde - LGBTQ Status (2004)
3. Senegal - Data Protection Law (2008)
4. Benin - Data Protection Law (2009)
5. Cameroon - Data Protection Law (2010)
6. Gabon - Data Protection Law (2011)

### Phase 2 (High Priority - 10-15 years old)
7. Ghana - Data Protection Law (2012)
8. Sao Tome and Principe - LGBTQ Status (2012)
9. Mali - Data Protection Law (2013)
10. Côte d'Ivoire - Data Protection Law (2013)

## Common Value Formats

### Data Protection Laws
```
In force — [Law Name] ([Year])
Draft — [Bill Name] (under consideration)
None — No data protection law
```

### LGBTQ+ Legal Status
```
Legal — decriminalised [Year], [additional protections]
Criminalised — [Penal Code section], penalty: [punishment]
Decriminalised — [Year], no formal recognition
```

### AI Policies
```
Adopted — [Strategy Name], [Year]
Draft/Early — [Policy Name] under development ([Year])
None — No formal AI strategy
```

### SIM Registration
```
Yes — mandatory [type] registration since [Year]
ID mandatory — SIM registration with ID, not biometric
No — voluntary registration
```

## Verification Checklist

Before saving changes:
- [ ] Value format matches existing entries
- [ ] Year is current (2024-2026)
- [ ] Source is cited with access date
- [ ] Cross-referenced with 2+ sources where possible
- [ ] Notes capture important context (enforcement, amendments)

## After Bulk Updates

1. Run diff tool to update cache:
   ```bash
   python pipeline_runner.py --mode scorecard --scorecard-action diff
   ```

2. Commit changes:
   ```bash
   git add data/scorecard/scorecard_main.xlsx scorecard.xlsx
   git add data/cache/scorecard_sources/*.json
   git commit -m "Update scorecard: [brief description of updates]"
   ```

3. Re-export for publication:
   ```bash
   python pipeline_runner.py --mode scorecard --scorecard-action all
   ```

## Maintenance Schedule

- **Weekly**: Check for major legislative changes (news monitoring)
- **Monthly**: Review changed sources from diff tool
- **Quarterly**: Systematic update of oldest entries (>10 years)
- **Annually**: Comprehensive review of all 194 countries

## Resources

- Maintenance Report: `docs/maintenance/SCORECARD_MAINTENANCE_REPORT.md`
- Scorecard Workflow: `docs/guides/SCORECARD_WORKFLOW.md`
- Data Standards: `docs/standards/METADATA_SCHEMA.md`
- Update tracking: `data/exports/scorecard_diff_report.json`
