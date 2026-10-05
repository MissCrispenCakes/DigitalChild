# LittleRainbowRights

[🌈 Visit LittleRainbowRights.com](https://littlerainbowrights.com){ .md-button .md-button--primary target="_blank" rel="noopener" }
[:octicons-arrow-left-24: Research tracks](../../../projects/index.md){ .md-button }

## Child and LGBTQ+ Digital Rights Research

**Analyzing digital protections for vulnerable populations through human rights document analysis**

!!! example "Use the self-hosted REST API"
    [Install and start the API locally](../../../api/quickstart.md), then query your dataset:

    ```python
    import requests
    response = requests.get("http://localhost:5000/api/scorecard/Kenya")
    data = response.json()["data"]
    ```

    [:octicons-rocket-24: API Documentation](../../../api/reference.md){ .md-button .md-button--primary }

______________________________________________________________________

## Methodological contributions

LittleRainbowRights broadened the earlier inquiry across countries and multiple document sources. The computational researcher developed the retrieval and representation approach and identified a further need: an index that could preserve a dated, inspectable assessment of documented conditions, with sources, gaps and uncertainty available for examination.

The public tools make those assessments easier to inspect and compare. Country coverage does not imply equal evidence completeness or validated accuracy. Global and multi-source work also revealed the substantial maintenance and interpretation demands on one computational researcher and one human-rights lawyer.

[Research history](../../../research-history/index.md) · [Next investigations](../../../research-directions/index.md#littlerainbowrights)

## About This Project

LittleRainbowRights is a focused research initiative within the broader GRIMdata framework, specifically examining:

- **Child digital rights** - Online safety, age verification, data protection for minors
- **LGBTQ+ digital rights** - Legal protections, online discrimination, privacy concerns
- **Intersectional analysis** - How policies affect vulnerable youth who are also LGBTQ+

This project uses the DigitalChild pipeline to retrieve and process human-rights documents. Its scorecard describes selected legal and policy frameworks; it is a screening tool rather than a direct measure of lived protection or enforcement outcomes.

## Published assessment scope {#key-findings}

<div class="grid cards" markdown>

-   :material-earth:{ .lg .middle } **194 Countries Tracked**

    ---

    Country coverage in the published scorecard; documentation completeness varies

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

[View Scorecard](../../../scorecard/index.md){ .md-button .md-button--primary }

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

The broader source register records **2,543 source URLs**. URL availability checks and substantive validation have different meanings; inspect the source and its date before drawing conclusions.

## Key Publications

!!! info "Research Output"
    The 2025 conference research is recorded as *Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa*. [Research record](https://doi.org/10.5281/zenodo.18318098).

## How to Use This Data

### For Researchers

**Via REST API (Recommended):**

```python
import requests

# Get all scorecard data
response = requests.get("http://localhost:5000/api/scorecard")
countries = response.json()["data"]["items"]

# Filter for specific country
response = requests.get("http://localhost:5000/api/scorecard/Kenya")
kenya_data = response.json()["data"]
print(kenya_data["indicators"])

# Get documents filtered by tags
response = requests.get("http://localhost:5000/api/documents?tags=ChildRights,LGBTQ")
documents = response.json()["data"]["items"]

# Filter by region
response = requests.get("http://localhost:5000/api/scorecard?region=Africa&per_page=50")
african_countries = response.json()["data"]["items"]
```

See [API Documentation](../../../api/reference.md) for all endpoints and filtering options.

**Via Direct File Access:**

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

[Installation Guide](../../getting-started/installation.md) | [Quick Start](../../getting-started/quickstart.md)

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

    [:octicons-arrow-right-24: View Scorecard](../../../scorecard/index.md)

-   :material-table-search:{ .lg .middle } **Data Explorer**

    ---

    Filter and search through all indicators

    [:octicons-arrow-right-24: Search Data](../../../scorecard/explorer.md)

-   :material-download:{ .lg .middle } **Export Data**

    ---

    Download CSV files for your own analysis

    [:octicons-arrow-right-24: Get Data](../../../guides/RUNBOOK.md)

-   :material-code-tags:{ .lg .middle } **Use the Pipeline**

    ---

    Run the analysis yourself on your own machine

    [:octicons-arrow-right-24: Quick Start](../../getting-started/quickstart.md)

</div>

<span id="__span-3-1"></span>
<span id="__codelineno-3-1"></span>
<span id="__span-3-2"></span>
<span id="__codelineno-3-2"></span>
<span id="__span-3-3"></span>
<span id="__codelineno-3-3"></span>
<span id="__span-3-4"></span>
<span id="__codelineno-3-4"></span>
<span id="__span-3-5"></span>
<span id="__codelineno-3-5"></span>
<span id="__span-3-6"></span>
<span id="__codelineno-3-6"></span>
<span id="__span-3-7"></span>
<span id="__codelineno-3-7"></span>
<span id="__span-3-8"></span>
<span id="__codelineno-3-8"></span>

## Citing This Work

**Conference research:** Vollmer, D. T., & Vollmer, S. C. (2025). *Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa.* Second International Conference on Children's Rights, Stellenbosch, September 2025. [DOI: 10.5281/zenodo.18318098](https://doi.org/10.5281/zenodo.18318098).

**Public scorecard snapshot:** state the snapshot generation date (26 June 2026), access date and the particular source-linked assessments used. The source-verification stamp (9 September 2025) describes a different event. A citation to the conference record alone does not identify the version of a later download.

**Software:** use the [software citation and technical overview](../../../docs/technical-overview.md#citation) and [repository citation record](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/CITATION.cff).

<span id="contributing"></span>

## Data Governance

Published assessments represent selected aspects of a situation. Check source dates and written justifications, distinguish missing documentation from a finding, and consider how linked information can increase exposure for those described.

[Data Governance](../../../DATA_GOVERNANCE.md) · [Research Context](../../../RESEARCH_CONTEXT.md) · [Site practices](../../../practices/index.md)

<span id="support-this-work"></span>
<span id="contact"></span>

## Related Projects

- [GRIMdata](../../../index.md) — umbrella research programme.
- [SGBV-UPR](../sgbv/index.md) — published legal and computational research with planned renewal.
- [Research directions](../../../research-directions/index.md) — intended investigations across the programme.
- [DigitalChild implementation](../../../docs/technical-overview.md) — public software, methods and instructions.

LittleRainbowRights is part of **Global Rights Index Monitoring**.
