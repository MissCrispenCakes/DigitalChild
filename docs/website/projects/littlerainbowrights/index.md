# LittleRainbowRights

## Child and LGBTQ+ Digital Rights Research

**Analyzing digital protections for vulnerable populations through human rights document analysis**

______________________________________________________________________

## About This Project

LittleRainbowRights is a focused research initiative within the broader GRIMdata framework, specifically examining:

- **Child digital rights** - Online safety, age verification, data protection for minors
- **LGBTQ+ digital rights** - Legal protections, online discrimination, privacy concerns
- **Intersectional analysis** - How policies affect vulnerable youth who are also LGBTQ+

This project uses the DigitalChild pipeline to scrape, process, and analyze human rights documents from international organizations, tracking how well countries protect children and LGBTQ+ individuals in digital spaces.

## Key Findings

<div class="grid cards" markdown>

-   :material-earth:{ .lg .middle } **194 Countries Tracked**

    ---

    Comprehensive global coverage of digital rights indicators

-   :material-chart-line:{ .lg .middle } **10 Indicators**

    ---

    AI Policy, Data Protection, LGBTQ+ Legal Status, Child Protection, and more

-   :material-alert:{ .lg .middle } **Critical Gaps Identified**

    ---

    Many countries lack specific child online protection frameworks

-   :material-shield-check:{ .lg .middle } **Best Practices**

    ---

    Leading countries demonstrate comprehensive approaches

</div>

## Scorecard Overview

The LittleRainbowRights scorecard tracks these key indicators:

### Data Protection & Privacy

1. **Data Protection Law** - Comprehensive data protection legislation governing personal data processing
2. **DPA Independence** - Data Protection Authority operates independently from executive control
3. **Children's Data Safeguards** - Child-specific data governance safeguards in binding law (not general child welfare)
4. **SOGI Sensitive Data** - Sexual orientation and gender identity recognized as sensitive personal data

### Child Protection

5. **Child Online Protection Strategy** - National COP framework addressing online harms; may include parental tools/rights

### LGBTQ+ Rights

6. **LGBTQ+ Legal Status** - Legal recognition and protection of LGBTQ+ individuals
7. **LGBTQ+ Promotion/Propaganda Offences** - Laws restricting discussion or advocacy of LGBTQ+ identities

### Emerging Technologies

8. **AI Policy Status** - National AI strategy or framework adoption
9. **DPIA Required for High-Risk AI** - Data Protection Impact Assessments required for high-risk AI systems

### Digital Identification

10. **SIM Card Biometric ID Linkage** - Requirement to provide biometric data when registering SIM cards

[View Full Scorecard](../../scorecard/index.md){ .md-button .md-button--primary }

## Regional Analysis

### Africa

- **Strengths:** Growing AI policy adoption, strong regional frameworks (AU)
- **Challenges:** Limited LGBTQ+ protections, gaps in child online safety
- **Leaders:** South Africa (comprehensive data protection and some LGBTQ+ rights)

### Americas

- **Strengths:** Some countries with comprehensive frameworks
- **Challenges:** Regional variation, enforcement gaps
- **Leaders:** Canada, Uruguay (strong data protection and LGBTQ+ rights)

### Asia-Pacific

- **Strengths:** Technology leadership in some countries
- **Challenges:** Wide variation in human rights protections
- **Leaders:** Australia, New Zealand (comprehensive frameworks)

### Europe

- **Strengths:** GDPR, strong data protection, LGBTQ+ rights in many countries
- **Challenges:** Implementation consistency
- **Leaders:** Nordic countries, Netherlands, Spain

### Middle East

- **Strengths:** Emerging AI policies
- **Challenges:** LGBTQ+ criminalization, limited digital rights frameworks
- **Note:** Significant human rights concerns in many countries

## Data Sources

All data sourced from authoritative international organizations:

- **UNESCO** - AI policy observatory
- **UNCTAD** - Data protection legislation tracking
- **ILGA World** - LGBTQ+ legal status (State-Sponsored Homophobia report)
- **UNICEF** - Child protection measures
- **ITU** - Telecom and internet regulations
- **Privacy International** - Surveillance and privacy tracking
- **Human Rights Watch** - Human rights monitoring

Total: **2,543 validated source URLs** ensuring transparency and verification.

## Key Publications

!!! info "Research Output"
    Publications using LittleRainbowRights data will be listed here as they become available.

## How to Use This Data

### For Researchers

```python
# Load scorecard data
import pandas as pd

df = pd.read_excel('scorecard_main.xlsx', sheet_name='Indicators')

# Filter for child protection analysis
child_protection = df[['Country', 'Region', 'Child_Online_Protection', 'Age_Verification']]

# Analyze LGBTQ+ protections
lgbtq_analysis = df[['Country', 'LGBTQ_Legal_Status', 'Promotion_Propaganda']]

# Regional aggregations
regional_summary = df.groupby('Region').agg({
    'AI_Policy_Status': lambda x: (x != 'No Policy').sum(),
    'Data_Protection_Law': lambda x: (x == 'Comprehensive Law').sum(),
    'Child_Online_Protection': lambda x: (x == 'Comprehensive Framework').sum()
})
```

[Installation Guide](../../getting-started/installation.md) | [API Documentation](../../../ARCHITECTURE.md)

### For Advocates

Use the data to:

- **Build evidence-based campaigns** - Cite specific country policies and gaps
- **Track policy changes** - Monitor improvements or regressions over time
- **Compare approaches** - Identify best practices from leading countries
- **Support litigation** - Evidence for human rights cases

### For Policy Makers

Insights for:

- **Benchmarking** - Compare your country's policies against regional peers
- **Policy design** - Learn from comprehensive frameworks in other countries
- **Gap analysis** - Identify missing protections in your jurisdiction
- **International cooperation** - Coordinate with countries facing similar challenges

## Interactive Tools

<div class="grid cards" markdown>

-   :material-chart-box:{ .lg .middle } **Scorecard Visualization**

    ---

    Interactive charts showing indicators across countries

    [:octicons-arrow-right-24: Explore Data](../scorecard/index.md)

-   :material-table-search:{ .lg .middle } **Data Explorer**

    ---

    Filter and search through all indicators

    [:octicons-arrow-right-24: Search Data](../../scorecard/explorer.md)

-   :material-download:{ .lg .middle } **Export Data**

    ---

    Download CSV files for your own analysis

    [:octicons-arrow-right-24: Get Data](../../../guides/RUNBOOK.md)

-   :material-code-tags:{ .lg .middle } **Use the Pipeline**

    ---

    Run the analysis yourself on your own machine

    [:octicons-arrow-right-24: Quick Start](../../getting-started/quickstart.md)

</div>

## Contributing

Found an error in the scorecard data? Have updated information?

1. **Check the source** - Verify the current value and source URL
1. **Report** - Open [GitHub Issue](https://github.com/MissCrispenCakes/DigitalChild/issues) with details
1. **Provide evidence** - Include authoritative source URL
1. **Track update** - Follow the issue for confirmation

[Contributing Guidelines](../../../CONTRIBUTING.md){ .md-button }

## Citing This Work

When using LittleRainbowRights data:

```bibtex
@misc{littlerainbowrights2025,
  title = {LittleRainbowRights: Child and LGBTQ+ Digital Rights Scorecard},
  author = {Vollmer, S.C.},
  year = {2025},
  howpublished = {\url{https://grimdata.org/projects/littlerainbowrights/}},
  note = {Licensed under CC BY 4.0. ORCID: 0000-0002-3359-2810}
}
```

Or:

> Vollmer, D.T., & Vollmer, S.C. (2025). LittleRainbowRights: Child and LGBTQ+ Digital Rights Scorecard.
> Available at: https://grimdata.org/projects/littlerainbowrights/
> Licensed under CC BY 4.0.
> ORCID: [0000-0002-3359-2810](https://orcid.org/0000-0002-3359-2810) (S.C. Vollmer)

[Full Citation Guide](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/CITATION.cff)

## Data Governance

This project follows strict ethical guidelines:

- **Publicly available sources only** - No confidential or leaked documents
- **Transparent methodology** - All processing steps documented
- **Source attribution** - Every data point linked to authoritative source
- **Regular validation** - Automated checking of 2,543 source URLs
- **Community review** - Open to corrections and updates

[Read Full Data Governance Policy](../../../DATA_GOVERNANCE.md)

## Support This Work

- ⭐ [Star the repository](https://github.com/MissCrispenCakes/DigitalChild)
- 📢 Share with researchers and advocates
- 🐛 Report data quality issues
- 💻 Contribute code or documentation
- 📝 Cite in your publications

## Related Projects

- **[GRIMdata](../../index.md)** - Main project hub
- **[SGBV-UPR](../sgbv/index.md)** - Sexual and gender-based violence analysis ([GitHub](https://github.com/MissCrispenCakes/HumanRights) - *private, under construction*)
- **[DigitalChild Pipeline](https://github.com/MissCrispenCakes/DigitalChild)** - Technical implementation

## Contact

- **Issues:** [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **Collaboration:** Contact via GitHub

______________________________________________________________________

**LittleRainbowRights** is part of the GRIMdata (Global Rights Information Monitoring) initiative.

**Mission:** Protect vulnerable populations in the digital age through evidence-based research and advocacy.
