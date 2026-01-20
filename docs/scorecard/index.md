# Scorecard Visualization

Interactive visualization of human rights indicators across 194 countries.

!!! info "Coming Soon"
    Interactive visualizations are currently under development. This page will feature:

    - Country-level indicator heatmaps
    - Regional comparison charts
    - Time-series trend analysis
    - Source URL verification status

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

### 1. AI Policy Status

Whether a country has published an official AI strategy, framework, or comprehensive regulation.

**Sources:** UNESCO AI Policy Observatory, UNCTAD, National Government websites

**Categories:**
- Comprehensive AI Strategy
- Framework or Guidelines
- No Published Policy

### 2. Data Protection Law

Existence of comprehensive data protection legislation.

**Sources:** UNCTAD Data Protection and Privacy Legislation, National Government websites

**Examples:** GDPR (EU), POPIA (South Africa), NDPR (Nigeria)

**Categories:**
- Comprehensive Law
- Draft Legislation
- No Specific Law

### 3. LGBTQ+ Legal Status

Legal recognition and protections for LGBTQ+ individuals.

**Sources:** ILGA World State-Sponsored Homophobia Report, Human Rights Watch

**Categories:**
- Criminalization
- No Specific Protections
- Some Protections
- Comprehensive Protections

### 4. Child Online Protection

Measures to safeguard children in digital environments.

**Sources:** UNICEF, ITU, National Legislation

**Categories:**
- Comprehensive Framework
- Partial Measures
- No Specific Policy

### 5. SIM Card Biometric Registration

Requirement to provide biometric data for mobile SIM card registration.

**Sources:** Privacy International, National Telecom Regulators, Media Reports

**Categories:**
- Mandatory Biometric
- Optional or Partial
- Not Required

### 6. Encryption Backdoors

Government-mandated weaknesses in encryption for surveillance.

**Sources:** Access Now, EFF, National Legislation

**Categories:**
- Backdoors Mandated
- Proposed Legislation
- No Known Backdoors

### 7. LGBTQ+ Promotion/Propaganda Laws

Legislation restricting discussion or "promotion" of LGBTQ+ topics.

**Sources:** ILGA World, Human Rights Watch

**Categories:**
- Criminalized "Promotion"
- Restrictive Measures
- No Restrictions

### 8. Data Protection Authority Independence

Independence of the national Data Protection Authority.

**Sources:** UNCTAD, National DPA websites, Academic Research

**Categories:**
- Independent Authority
- Limited Independence
- No DPA or Dependent

### 9. Content Moderation Regulations

Regulations governing removal of harmful online content.

**Sources:** UNESCO, National Legislation, Academic Research

**Categories:**
- Comprehensive Regulation
- Sectoral Regulations
- No Specific Regulation

### 10. Age Verification Requirements

Requirements to verify user age before accessing online services.

**Sources:** National Legislation, UNICEF, Media Reports

**Categories:**
- Mandatory Age Verification
- Platform Self-Regulation
- No Requirements

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

| Country | AI_Policy_Status | Data_Protection_Law | LGBTQ_Legal_Status | ... |
|---------|-----------------|---------------------|-------------------|-----|
| Kenya | Framework | Comprehensive Law | No Protections | ... |
| South Africa | Strategy | Comprehensive Law | Some Protections | ... |

**scorecard_sources.csv:**

| Country | Indicator | Value | Source_URL | Validated | Last_Checked |
|---------|-----------|-------|------------|-----------|--------------|
| Kenya | AI_Policy | Framework | https://... | ✅ | 2026-01-15 |

## Data Explorer

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
   - Country name
   - Indicator
   - Current value vs. correct value
   - Authoritative source URL
3. **Update** - Maintainer reviews and updates
4. **Re-export** - Updated data regenerated

## Citing Scorecard Data

When using scorecard data in publications:

```bibtex
@misc{littlerainbowrights2025,
  title = {LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators},
  author = {GRIMdata / LittleRainbowRights},
  year = {2025},
  howpublished = {\url{https://github.com/MissCrispenCakes/DigitalChild}},
  note = {Licensed under CC BY 4.0}
}
```

Or:

> GRIMdata / LittleRainbowRights. (2025). LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators. Licensed under CC BY 4.0. Available at: https://github.com/MissCrispenCakes/DigitalChild

## Limitations & Disclaimers

!!! warning "Important Considerations"
    - **Point-in-time data:** Reflects information as of January 2026
    - **Binary categorization:** Complex policies simplified into discrete categories
    - **Source availability:** Some countries lack accessible English-language sources
    - **Implementation vs. policy:** Tracks official policy, not enforcement
    - **Regional variation:** Federal systems may have state/provincial differences

!!! info "Use Responsibly"
    This scorecard is a research tool, not legal advice. Always:

    - Verify source URLs before citing
    - Consider local context and nuance
    - Acknowledge limitations in publications
    - Cross-reference with other datasets

## Future Enhancements

Planned features (see [Roadmap](../ROADMAP.md)):

- [ ] Interactive heatmap visualizations (Plotly.js)
- [ ] Country comparison tool
- [ ] Time-series tracking of policy changes
- [ ] API for programmatic access
- [ ] Real-time source monitoring alerts
- [ ] Expanded indicators (15-20 total)
- [ ] Sub-national data (states/provinces)

## Technical Details

For technical documentation:

- [Scorecard Workflow Guide](../guides/SCORECARD_WORKFLOW.md) - Complete system overview
- [Metadata Schema](../standards/METADATA_SCHEMA.md) - Data structure
- [Architecture](../ARCHITECTURE.md) - System design

## Support & Feedback

- **Data quality issues:** [Open Issue](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Feature requests:** [Start Discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **General questions:** [FAQ](../FAQ.md)

---

**Note:** Interactive visualizations are under active development. Check back for updates or [watch the repository](https://github.com/MissCrispenCakes/DigitalChild) for notifications.
