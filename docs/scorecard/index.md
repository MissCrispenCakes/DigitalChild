# Digital Rights Scorecard

**Tracking 10 key indicators across 194 countries to assess digital rights protections for vulnerable populations**

---

## What is the Scorecard?

The Digital Rights Scorecard is a comprehensive research tool that tracks **10 critical indicators** of digital rights protections across **194 countries worldwide**. It focuses specifically on the intersection of digital technology governance and the rights of vulnerable populations, particularly **LGBTQ+ individuals** and **children**.

Each country receives scores on a 0-1-2 scale for each indicator, enabling comparative analysis of digital rights frameworks globally.

---

## Why It Exists

As digital technologies—especially artificial intelligence, biometric systems, and data-driven platforms—become increasingly embedded in daily life, their impact on vulnerable communities requires systematic monitoring.

**The gap this addresses:**
- Existing digital rights indices focus on general privacy or internet freedom
- Few track LGBTQ+-specific or child-specific digital protections
- No comprehensive dataset examines the **intersection** of digital governance and vulnerable populations

**Research foundation:**
This scorecard was developed for the research paper *"Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa"* presented at the 2nd International Conference on Children's Rights (Stellenbosch, September 2025).

---

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

    Validated authoritative sources from UNESCO, UNCTAD, ILGA, UNICEF

-   :material-update:{ .lg .middle } **January 2026**

    ---

    Last updated with latest policy changes and new data

</div>

---

## What It Tracks

### The 10 Indicators

1. **Data Protection Law** - Existence of comprehensive data protection legislation
2. **DPA Independence** - Independence of Data Protection Authority from executive control
3. **Children's Data Safeguards** - Binding child-specific privacy/data-protection safeguards
4. **Child Online Protection Strategy** - National framework addressing online harms to children
5. **SOGI Sensitive Data** - Legal recognition of sexual orientation/gender identity as sensitive data
6. **LGBTQ+ Legal Status** - Legal recognition and protection of LGBTQ+ individuals
7. **LGBTQ+ Promotion/Propaganda Offences** - Laws restricting LGBTQ+ expression or advocacy
8. **AI Policy Status** - National AI strategy or framework adoption
9. **DPIA Required for High-Risk AI** - Requirement for Data Protection Impact Assessments for AI
10. **SIM Card Biometric ID Linkage** - Biometric data requirements for SIM card registration

### Scoring System

**0-1-2 Scale per indicator:**
- **2 (Best)** - Comprehensive protections or safeguards in place
- **1 (Middle)** - Partial protections or mixed implementation
- **0 (Worst)** - No protections, harmful policies, or heightened risk

**Composite Metrics:**
- **Protection Score:** Sum of all 10 indicators (0-20 scale)
- **Risk Index:** 100 − (Protection Score / 20 × 100) [inverted scale]
- **Data Completeness:** Percentage of indicators with verified data

---

## Explore the Scorecard

Choose your path based on your needs:

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Design & Methodology**

    ---

    Understand how the scorecard was designed

    - Detailed indicator definitions
    - Scoring methodology
    - Data sources and validation
    - Limitations and caveats

    [Learn About Design →](design.md)

-   :material-api:{ .lg .middle } **Data Access (API)**

    ---

    Access scorecard data programmatically

    - REST API endpoints
    - CSV exports
    - Python examples
    - Direct file access

    [Access the Data →](data-access.md)

-   :material-chart-bar:{ .lg .middle } **Visualization**

    ---

    Explore visualizations and export options

    - Current: CSV exports, API queries
    - Future: Interactive heatmaps, country cards

    [View Visualizations →](visualization.md)

-   :material-table-search:{ .lg .middle } **Data Explorer**

    ---

    Interactive data exploration tool

    - Coming soon: Filter, search, compare
    - Current: Use API or CSV exports

    [Try Explorer →](explorer.md)

</div>

---

## Use Cases

### Research Applications

**Comparative Analysis:**
Compare digital rights frameworks across regions to identify patterns and gaps

**Risk Assessment:**
Evaluate digital safety environments for vulnerable populations by country

**Policy Tracking:**
Monitor changes in digital governance policies over time

**Advocacy Evidence:**
Provide data-backed evidence for human rights advocacy

### Example Research Questions

- Which countries have comprehensive child data protections but criminalize LGBTQ+ identities?
- How does biometric SIM registration correlate with LGBTQ+ legal status?
- Which African countries have adopted AI strategies with data protection frameworks?
- Where are LGBTQ+ children most at risk from digital surveillance?

---

## Data Quality & Sources

### Authoritative Sources

All 2,543 source URLs come from authoritative international organizations:

- **UNESCO** - AI Policy Observatory
- **UNCTAD** - Data Protection and Privacy Legislation Database
- **ILGA World** - State-Sponsored Homophobia report (LGBTQ+ legal status)
- **UNICEF** - Child protection measures and COP strategies
- **ITU** - Telecom and internet regulations
- **Privacy International** - Surveillance and biometric tracking
- **Human Rights Watch** - Human rights monitoring

### Validation & Monitoring

**Quality Assurance:**
- All 2,543 URLs automatically validated (HTTP status, redirects, link rot)
- Change detection monitors when source content updates
- Manual quarterly review by researchers
- Community contributions via GitHub issues

**Transparency:**
- Every indicator value links to its authoritative source URL
- Validation reports available in `data/scorecard/validation_report.csv`
- Full methodology documented in [Design & Methodology](design.md)

---

## Quick Start Examples

### API Access

```bash
# Get Kenya's scorecard
curl http://localhost:5000/api/scorecard/Kenya

# Get all African countries
curl "http://localhost:5000/api/scorecard?region=Africa"

# Get indicator statistics
curl http://localhost:5000/api/scorecard/indicators/statistics
```

### Python Analysis

```python
import requests
import pandas as pd

# Fetch scorecard data via API
response = requests.get("http://localhost:5000/api/scorecard?per_page=200")
countries = response.json()["data"]["items"]

# Convert to DataFrame
df = pd.DataFrame(countries)

# Find countries with LGBTQ+ criminalization AND biometric SIM requirements
at_risk = df[
    (df["LGBTQ_Legal_Status"] == "Criminalization") &
    (df["SIM_Biometric_ID_Linkage"] == "Mandatory Biometric Registration")
]
print(f"Found {len(at_risk)} countries with heightened surveillance risk for LGBTQ+ individuals")
```

### CSV Export

```bash
# Export scorecard data
python pipeline_runner.py --mode scorecard --scorecard-action export

# Generates:
# - data/exports/scorecard_summary.csv (countries × indicators)
# - data/exports/scorecard_sources.csv (all source URLs)
# - data/exports/scorecard_by_indicator.csv (grouped by indicator)
# - data/exports/scorecard_by_region.csv (regional aggregations)
```

---

## Citation

When using scorecard data in publications:

```bibtex
@misc{littlerainbowrights2025scorecard,
  title = {LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators},
  author = {Vollmer, D.T. and Vollmer, S.C.},
  year = {2025},
  howpublished = {\url{https://grimdata.org/scorecard/}},
  note = {Licensed under CC BY 4.0. ORCID: 0000-0002-3359-2810 (S.C. Vollmer)},
  doi = {10.5281/zenodo.18318098}
}
```

Or in text:

> Vollmer, D.T., & Vollmer, S.C. (2025). *LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators*. Available at: https://grimdata.org/scorecard/. DOI: 10.5281/zenodo.18318098. Licensed under CC BY 4.0.

---

## Limitations & Disclaimers

!!! warning "Important Considerations"

    **Point-in-time data:** Reflects information as of January 2026. Policies change frequently.

    **Binary categorization:** Complex policies are simplified into discrete 0-1-2 categories for comparability.

    **Source availability:** Some countries lack accessible English-language sources or transparent policy documentation.

    **Implementation vs. policy:** Tracks official policy and law, not enforcement effectiveness or lived experience.

    **Regional variation:** Federal systems may have significant state/provincial differences not captured at national level.

    **Intersectional risk:** Real-world risk is determined by **combinations** of indicators (e.g., LGBTQ+ criminalization + biometric SIM requirements), not single indicators in isolation.

!!! info "Use Responsibly"

    This scorecard is a **research tool**, not legal advice. Always:

    - Verify source URLs before citing in publications
    - Consider local context, enforcement patterns, and lived experience
    - Acknowledge limitations in research methodology sections
    - Cross-reference with other datasets and qualitative research
    - Consult local human rights organizations for on-the-ground context

---

## Future Enhancements

Planned features (see [Roadmap](../ROADMAP.md)):

- [x] **REST API for programmatic access** ✅ **COMPLETE** (14 endpoints live, production-ready)
- [ ] Interactive heatmap visualizations (Plotly.js)
- [ ] Country comparison tool (side-by-side view)
- [ ] Time-series tracking of policy changes
- [ ] Real-time source monitoring alerts
- [ ] Expanded indicators (target: 15-20 total)
- [ ] Sub-national data (states/provinces for federal systems)
- [ ] Integration with other digital rights indices

---

## Contributing

Found an error or have updated information?

**Report Issues:**
1. Verify the source URL in `scorecard_main.xlsx`
2. Open [GitHub Issue](https://github.com/MissCrispenCakes/DigitalChild/issues) with:
   - Country name
   - Indicator
   - Current value vs. correct value
   - Authoritative source URL
3. Maintainer reviews and updates
4. Updated data regenerated and published

**Contribute Code:**
- See [Contributing Guide](../CONTRIBUTING.md)
- Check [open issues](https://github.com/MissCrispenCakes/DigitalChild/issues?q=is%3Aissue+is%3Aopen+label%3Ascorecard)

---

## Technical Documentation

For developers and researchers working with the scorecard system:

- [Scorecard Workflow Guide](../guides/SCORECARD_WORKFLOW.md) - Complete system overview
- [Metadata Schema](../standards/METADATA_SCHEMA.md) - Data structure
- [Architecture](../ARCHITECTURE.md) - System design
- [API Documentation](../api/index.md) - Programmatic access

---

## Support & Feedback

- **Data quality issues:** [Open Issue](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Feature requests:** [Start Discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **General questions:** [FAQ](../FAQ/)
- **Research collaboration:** Contact via [GitHub](https://github.com/MissCrispenCakes/DigitalChild)

---

## License

- **Scorecard Data:** CC BY 4.0
- **Code & Pipeline:** MIT License

See [LICENSE-DATA](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/LICENSE-DATA) and [LICENSE](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/LICENSE) for details.
