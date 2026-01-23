# Scorecard Visualization

Interactive visualization of human rights indicators across 194 countries.

!!! info "Coming Soon"
    Interactive visualizations are currently under development. This page will feature:
    ```txt
    - Country-level indicator heatmaps
    - Regional comparison charts
    - Time-series trend analysis
    - Source URL verification status
    ```

For now, you can explore the data through CSV exports or the data explorer below.

## Quick Stats

<div class="grid cards" markdown>

-   :fontawesome-solid-earth-americas:{ .lg .middle } **194 Countries**

    ---

    Comprehensive global coverage across all UN member states and territories

-   :material-chart-line:{ .lg .middle } **10 Indicators**

    ---

    AI Policy, Data Protection, LGBTQ+ Status, Child Protection, and more

-   :material-link:{ .lg .middle } **2,543 Source URLs**

    ---

    Validated authoritative sources from UNESCO, UNCTAD, ILGA, UNICEF, etc.

-   :material-update:{ .lg .middle } **January 2026**

    ---

    Last updated with latest policy changes and new data

</div>

## Indicators Tracked

!!! info "Scoring System"
    Each indicator uses a 0-1-2 scale where higher scores indicate stronger protections:

    - **2 (Best)** - Comprehensive protections or safeguards in place
    - **1 (Middle)** - Partial protections or mixed implementation
    - **0 (Worst)** - No protections, harmful policies, or heightened risk

    Categories are listed from best (2) to worst (0) below. Risk analysis examines **combinations** of indicators (e.g., LGBTQ criminalization × biometric ID linkage).

### 1. Data Protection Law (Data_Protection_Law)

Existence of comprehensive data protection legislation governing personal data processing.

**Sources:** UNCTAD Data Protection and Privacy Legislation Database; national statutes

**Categories:**

- **Comprehensive Law** (2) - Enacted data protection legislation with enforcement mechanisms
- **Draft Legislation** (1) - Bill pending or under consultation
- **No Specific Law** (0) - No comprehensive data protection law

### 2. Data Protection Authority Independence (DPA_Independence)

Whether the national Data Protection Authority operates independently from executive control.

**Sources:** UNCTAD; DPA statutes; academic and regulatory analysis

**Categories:**

- **Independent Authority** (2) - DPA operates with full operational and financial independence
- **Limited Independence** (1) - DPA exists but with constraints (appointments, budget, reporting)
- **No DPA or Dependent Authority** (0) - No DPA established or DPA fully controlled by executive

### 3. Children's Data Safeguards (Children_Data_Safeguards)

Binding child-specific privacy/data-protection safeguards in law or regulation (not general child welfare law).

**Sources:** National legislation; UNICEF; data protection laws

**Categories:**

- **Explicit Child Data Protections** (2) - Child-specific data governance provisions: limits on profiling/ads for children, heightened consent standards, age-appropriate design, "best interests of child" principle, retention/minimization rules, minors' rights (erase/access)
- **General Protections Only** (1) - Children covered under general data protection but no child-specific data governance provisions
- **No Specific Safeguards** (0) - No data protection framework or no child-specific safeguards

### 4. Child Online Protection Strategy (COP_Strategy)

National COP strategy/framework addressing online harms to children; may include parental tools/rights.

**Sources:** UNICEF; ITU; national policy documents

**Categories:**

- **National COP Strategy** (2) - Comprehensive national COP framework: governance bodies, reporting/hotlines, digital literacy programs, platform safety guidance, sectoral online safety rules, parental empowerment measures
- **Partial / Sectoral Measures** (1) - Sectoral initiatives, pilot programs, awareness campaigns, or piecemeal safety measures
- **No Strategy** (0) - No national or sectoral child online protection strategy

### 5. Sensitive Data Protections for SOGI (SOGI_Sensitive_Data)

Whether sexual orientation and gender identity are legally recognized as sensitive personal data.

**Sources:** Data protection statutes; ILGA World

**Categories:**

- **Explicitly Protected** (2) - Sexual orientation and/or gender identity explicitly listed as sensitive data
- **Implicitly Covered** (1) - Covered under "sex life" or similar broader categories
- **Not Recognized** (0) - SOGI not recognized as sensitive data or no data protection law

### 6. LGBTQ+ Legal Status (LGBTQ_Legal_Status)

Legal recognition and protection of LGBTQ+ individuals.

**Sources:** ILGA World; Human Rights Watch

**Categories:**

- **Comprehensive Protections** (2) - Anti-discrimination laws, marriage recognition, constitutional protections
- **Legal, No Specific Protections** (1) - Same-sex relations decriminalized but no anti-discrimination protections
- **Criminalization** (0) - Same-sex relations criminalized under law

### 7. LGBTQ+ Promotion / Propaganda Offences (Promotion_Propaganda_Offences)

Laws restricting discussion, visibility, or advocacy related to LGBTQ+ identities.

**Sources:** ILGA World; national criminal codes

**Categories:**

- **No Restrictions** (2) - No legal restrictions on LGBTQ+ expression, advocacy, or visibility
- **Restrictive Measures** (1) - Administrative restrictions, morality codes, or broadcast regulations limiting LGBTQ+ expression
- **Criminalized Promotion** (0) - Explicit propaganda laws or criminal penalties for LGBTQ+ advocacy/discussion

### 8. AI Policy Status (AI_Policy_Status)

Whether a country has adopted a national AI strategy or framework.

**Sources:** UNESCO AI Policy Observatory; UNCTAD; national governments

**Categories:**

- **Comprehensive AI Strategy** (2) - Adopted national AI strategy with implementation plan and governance framework
- **Framework or Guidelines** (1) - Draft strategy, policy guidelines, or AI addressed in broader digital transformation plans
- **No Published Policy** (0) - No AI-specific strategy or framework

### 9. DPIA Required for High-Risk AI (DPIA_Required_High_Risk_AI)

Legal requirement to conduct Data Protection Impact Assessments for high-risk AI systems.

**Sources:** AI laws; data protection statutes; regulatory guidance

**Categories:**

- **Explicitly Required** (2) - Law mandates DPIA for high-risk AI systems (profiling, automated decisions, biometric processing)
- **Partially Required** (1) - DPIA required for certain processing but not specifically for AI, or optional/recommended
- **Not Required** (0) - No DPIA requirement or no data protection framework

### 10. SIM Card Biometric ID Linkage (SIM_Biometric_ID_Linkage)

Requirement to provide biometric data when registering SIM cards, either directly or through linkage to biometric national ID systems.

**Sources:** Privacy International; telecom regulators; media reports

**Categories:**

- **Not Required** (2) - No ID requirement or minimal registration without biometric linkage
- **Non-biometric ID Required** (1) - ID number/passport required but NOT linked to biometric database (photo on card ≠ biometric unless in facial recognition database)
- **Mandatory Biometric Registration** (0) - Biometric data (fingerprints, facial scans, iris) required directly OR SIM requires national ID that is biometrically backed

## Composite Scores

In addition to the 10 individual indicators, the scorecard calculates composite metrics:

### Protection Score

**Formula:** Sum of all 10 indicator scores (0–20 scale)

- **Maximum:** 20 (all indicators score 2)
- **Minimum:** 0 (all indicators score 0)
- **Interpretation:** Higher scores indicate stronger digital rights protections

**Example:** Country with 7 indicators at (2), 2 at (1), 1 at (0) = 14 + 2 + 0 = 16 Protection Score

### Risk Index

**Formula:** 100 − (Protection_Score / 20 × 100)

- **Maximum:** 100 (no protections, highest risk)
- **Minimum:** 0 (full protections, lowest risk)
- **Interpretation:** Inverted scale where higher values indicate greater risk

**Example:** Protection Score of 16 → Risk Index = 100 − (16/20 × 100) = 100 − 80 = 20

### Data Completeness

**Formula:** (Number of known indicators / 10) × 100

- **Maximum:** 100% (all 10 indicators have data)
- **Minimum:** 0% (no indicator data available)
- **Interpretation:** Percentage of metrics with verified data for the country

**Note:** Countries with low data completeness (<50%) should be interpreted cautiously as composite scores may not reflect full picture.

## Exporting Data

### From the Pipeline

Run the scorecard export workflow:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action export
```

This generates:

- `scorecard_summary.csv` - Countries × Indicators table
- `scorecard_sources.csv` - All source URLs with validation status
- `scorecard_by_indicator.csv` - Grouped by indicator
- `scorecard_by_region.csv` - Regional aggregations

### CSV Format

**scorecard_summary.csv:**

| Country      | AI_Policy_Status | Data_Protection_Law | LGBTQ_Legal_Status | ... |
| ------------ | ---------------- | ------------------- | ------------------ | --- |
| Kenya        | Framework        | Comprehensive Law   | No Protections     | ... |
| South Africa | Strategy         | Comprehensive Law   | Some Protections   | ... |

**scorecard_sources.csv:**

| Country | Indicator | Value     | Source_URL  | Validated | Last_Checked |
| ------- | --------- | --------- | ----------- | --------- | ------------ |
| Kenya   | AI_Policy | Framework | https://... | ✅        | 2026-01-15   |

## Data Explorer

```html
<div id="scorecard-explorer">
  <p><em>Interactive data explorer will be available in future update.</em></p>
</div>

<style>
#scorecard-explorer {
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 2rem;
  text-align: center;
  margin: 2rem 0;
}

/* Placeholder for future plotly visualization */
.plotly-chart {
  width: 100%;
  height: 600px;
}
</style>
```

## Validation & Quality

### URL Validation

All 2,543 source URLs are automatically validated:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action validate
```

Generates `validation_report.csv` with:

- HTTP status codes
- Redirect chains
- Broken links
- Response times

### Change Detection

Monitor sources for updates:

```bash
python processors/scorecard_diff.py
```

Detects:

- Content changes (via hashing)
- Policy updates
- Broken links
- New data available

### Data Quality

**Authoritative Sources:**

- UNESCO - AI policies and digital education
- UNCTAD - Data protection legislation
- ILGA World - LGBTQ+ legal status
- UNICEF - Child protection measures
- ITU - Telecom regulations
- Privacy International - Surveillance measures

**Update Frequency:**

- Manually reviewed quarterly
- Automated monitoring alerts when sources change
- Community contributions via GitHub issues

## Contributing Data

Found an error or have updated information?

1. **Verify** - Check the source URL in `scorecard_main.xlsx`
2. **Report** - Open [GitHub Issue](https://github.com/MissCrispenCakes/DigitalChild/issues) with:
    ```txt
    - Country name
    - Indicator
    - Current value vs. correct value
    - Authoritative source URL
    ```
3. **Update** - Maintainer reviews and updates
4. **Re-export** - Updated data regenerated

## Citing Scorecard Data

When using scorecard data in publications:

```bibtex
@misc{littlerainbowrights2025,
  title = {LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators},
  author = {Vollmer, S.C.},
  year = {2025},
  howpublished = {\url{https://github.com/MissCrispenCakes/DigitalChild}},
  note = {Licensed under CC BY 4.0. ORCID: 0000-0002-3359-2810}
}
```

Or:

> Vollmer, D.T., & Vollmer, S.C. (2025). LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators.
> Licensed under CC BY 4.0.
> Available at: https://github.com/MissCrispenCakes/DigitalChild
> ORCID: [0000-0002-3359-2810](https://orcid.org/0000-0002-3359-2810) (S.C. Vollmer)

## Limitations & Disclaimers

!!! warning "Important Considerations"
    **Point-in-time data:** Reflects information as of January 2026
    **Binary categorization:** Complex policies simplified into discrete categories
    **Source availability:** Some countries lack accessible English-language sources
    **Implementation vs. policy:** Tracks official policy, not enforcement
    **Regional variation:** Federal systems may have state/provincial differences

!!! info "Use Responsibly"
    This scorecard is a research tool, not legal advice. Always:
    ```txt
    - Verify source URLs before citing
    - Consider local context and nuance
    - Acknowledge limitations in publications
    - Cross-reference with other datasets
    ```

## Future Enhancements

Planned features (see [Roadmap](../../ROADMAP.md)):

- [ ] Interactive heatmap visualizations (Plotly.js)
- [ ] Country comparison tool
- [ ] Time-series tracking of policy changes
- [ ] API for programmatic access
- [ ] Real-time source monitoring alerts
- [ ] Expanded indicators (15-20 total)
- [ ] Sub-national data (states/provinces)

## Technical Details

For technical documentation:

- [Scorecard Workflow Guide](../../guides/SCORECARD_WORKFLOW.md) - Complete system overview
- [Metadata Schema](../../standards/METADATA_SCHEMA.md) - Data structure
- [Architecture](../../ARCHITECTURE.md) - System design

## Support & Feedback

- **Data quality issues:** [Open Issue](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Feature requests:** [Start Discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **General questions:** [FAQ](../../FAQ.md)

______________________________________________________________________

**Note:** Interactive visualizations are under active development. Check back for updates or [watch the repository](https://github.com/MissCrispenCakes/DigitalChild) for notifications.
