# Accessing Scorecard Data

**Multiple ways to access the Digital Rights Scorecard data based on your needs**

---

## Overview

The scorecard data is available through four access methods, each suited to different use cases:

| Method | Best For | Setup Time | Flexibility |
|--------|----------|------------|-------------|
| **REST API** | Programmatic access, automation, integration | 5 minutes | High |
| **CSV Export** | Excel analysis, R/Python dataframes | 2 minutes | Medium |
| **Direct File** | Manual exploration, full data access | Immediate | High |
| **Pipeline Integration** | Document enrichment, automated workflows | N/A | High |

---

## Option 1: REST API (Recommended)

**Best for:** Programmatic access, real-time queries, integration with other tools

### Quick Start

```bash
# Install and run the API
pip install -r api_requirements.txt
python run_api.py

# API available at http://localhost:5000
```

### Scorecard Endpoints

**GET /api/scorecard** - List all countries with scorecard data

```bash
# Get all countries
curl http://localhost:5000/api/scorecard

# Filter by region
curl "http://localhost:5000/api/scorecard?region=Africa"

# Pagination
curl "http://localhost:5000/api/scorecard?page=1&per_page=50"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "country": "Kenya",
        "region": "Africa",
        "indicator_count": 10,
        "AI_Policy_Status": "Framework",
        "Data_Protection_Law": "Comprehensive Law",
        "LGBTQ_Legal_Status": "Legal, No Protections",
        ...
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 194,
      "total_pages": 10
    }
  }
}
```

**GET /api/scorecard/:country** - Get detailed scorecard for specific country

```bash
# Get Kenya's full scorecard
curl http://localhost:5000/api/scorecard/Kenya
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "country": "Kenya",
    "region": "Africa",
    "indicators": {
      "AI_Policy_Status": {
        "value": "Framework",
        "score": 1,
        "source": "https://unesco.org/...",
        "last_updated": "2025-11-15"
      },
      "Data_Protection_Law": {
        "value": "Comprehensive Law",
        "score": 2,
        "source": "https://unctad.org/...",
        "last_updated": "2024-09-10"
      },
      ...
    },
    "composite_scores": {
      "protection_score": 14,
      "risk_index": 30,
      "data_completeness": 100
    }
  }
}
```

**GET /api/scorecard/indicators/statistics** - Get indicator statistics across all countries

```bash
# Get statistics for all indicators
curl http://localhost:5000/api/scorecard/indicators/statistics
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "AI_Policy_Status": {
      "total_countries": 194,
      "values": {
        "Comprehensive Strategy": 45,
        "Framework": 72,
        "No Policy": 77
      },
      "average_score": 0.87,
      "completeness": 100.0
    },
    ...
  }
}
```

### Python Examples

**Fetch all African countries:**

```python
import requests
import pandas as pd

# Fetch scorecard data
response = requests.get(
    "http://localhost:5000/api/scorecard",
    params={"region": "Africa", "per_page": 100}
)
data = response.json()["data"]["items"]

# Convert to DataFrame
df = pd.DataFrame(data)
print(df[["country", "AI_Policy_Status", "Data_Protection_Law"]])
```

**Analyze LGBTQ+ risk patterns:**

```python
import requests

# Get all countries
response = requests.get("http://localhost:5000/api/scorecard?per_page=200")
countries = response.json()["data"]["items"]

# Find countries with LGBTQ+ criminalization AND biometric SIM requirements
at_risk = [
    c for c in countries
    if c.get("LGBTQ_Legal_Status") == "Criminalization"
    and c.get("SIM_Biometric_ID_Linkage") == "Mandatory Biometric Registration"
]

print(f"Found {len(at_risk)} countries with heightened surveillance risk:")
for country in at_risk:
    print(f"  - {country['country']} ({country['region']})")
```

**Download all scorecard data:**

```python
import requests
import pandas as pd

# Fetch all pages
all_countries = []
page = 1
while True:
    response = requests.get(
        f"http://localhost:5000/api/scorecard?page={page}&per_page=100"
    )
    data = response.json()["data"]
    all_countries.extend(data["items"])

    if not data["pagination"]["has_next"]:
        break
    page += 1

# Convert to DataFrame and save
df = pd.DataFrame(all_countries)
df.to_csv("scorecard_all_countries.csv", index=False)
print(f"Downloaded {len(df)} countries")
```

### JavaScript Example

```javascript
// Fetch scorecard data for visualization
async function getScorecard() {
  const response = await fetch('http://localhost:5000/api/scorecard?per_page=200');
  const data = await response.json();
  return data.data.items;
}

// Get specific country
async function getCountryScorecard(country) {
  const response = await fetch(`http://localhost:5000/api/scorecard/${country}`);
  const data = await response.json();
  return data.data;
}

// Example: Create heatmap
getScorecard().then(countries => {
  // Use Plotly, D3, or other viz library
  const riskData = countries.map(c => ({
    country: c.country,
    risk: c.risk_index
  }));
  // Render visualization...
});
```

### R Example

```r
library(httr)
library(jsonlite)
library(dplyr)

# Fetch scorecard data
response <- GET("http://localhost:5000/api/scorecard?per_page=200")
scorecard <- content(response, as = "parsed")$data$items

# Convert to dataframe
df <- do.call(rbind, lapply(scorecard, as.data.frame))

# Analysis
african_countries <- df %>%
  filter(region == "Africa") %>%
  select(country, AI_Policy_Status, Data_Protection_Law, LGBTQ_Legal_Status)

print(african_countries)
```

### Rate Limits

- **Public (no API key):** 100 requests/hour
- **Authenticated (with API key):** 1000 requests/hour

To request an API key, see the [API documentation](../api/index.md).

---

## Option 2: CSV Export

**Best for:** One-time analysis, Excel, R dataframes, statistical analysis

### Generate Exports

```bash
# Run scorecard export
python pipeline_runner.py --mode scorecard --scorecard-action export
```

### Generated Files

**Location:** `data/exports/`

1. **scorecard_summary.csv** - Countries × Indicators matrix

   | Country | AI_Policy_Status | Data_Protection_Law | LGBTQ_Legal_Status | ... |
   |---------|------------------|---------------------|---------------------|-----|
   | Kenya   | Framework        | Comprehensive Law   | Legal, No Protections | ... |
   | South Africa | Comprehensive Strategy | Comprehensive Law | Comprehensive Protections | ... |

2. **scorecard_sources.csv** - All source URLs with validation status

   | Country | Indicator | Value | Source_URL | Validated | Last_Checked |
   |---------|-----------|-------|------------|-----------|--------------|
   | Kenya | AI_Policy_Status | Framework | https://... | ✅ | 2026-01-15 |

3. **scorecard_by_indicator.csv** - Grouped by indicator

   | Indicator | Category | Countries | Percentage |
   |-----------|----------|-----------|------------|
   | AI_Policy_Status | Comprehensive Strategy | 45 | 23.2% |
   | AI_Policy_Status | Framework | 72 | 37.1% |

4. **scorecard_by_region.csv** - Regional aggregations

   | Region | Avg_Protection_Score | Countries_with_Data_Protection | ... |
   |--------|----------------------|--------------------------------|-----|
   | Africa | 11.2 | 32 | ... |

### Using CSV Exports

**Excel/Google Sheets:**
```
1. Open scorecard_summary.csv in Excel
2. Create pivot tables for analysis
3. Use conditional formatting for heatmaps
4. Export charts for presentations
```

**Python pandas:**
```python
import pandas as pd

# Load scorecard data
df = pd.read_csv("data/exports/scorecard_summary.csv")

# Filter and analyze
africa = df[df["region"] == "Africa"]
print(africa.describe())

# Find countries with comprehensive protections
comprehensive = df[df["Data_Protection_Law"] == "Comprehensive Law"]
print(f"Countries with comprehensive data protection: {len(comprehensive)}")
```

**R:**
```r
library(readr)
library(dplyr)

# Load data
scorecard <- read_csv("data/exports/scorecard_summary.csv")

# Analysis
summary_stats <- scorecard %>%
  group_by(region) %>%
  summarize(
    avg_protection = mean(protection_score, na.rm = TRUE),
    countries = n()
  )

print(summary_stats)
```

---

## Option 3: Direct File Access

**Best for:** Manual exploration, custom processing, full data access

### Primary File

**Location:** `scorecard_main.xlsx`

**Contains:**
- All 194 countries
- All 10 indicators with values and scores
- Source URLs for every indicator
- Validation timestamps
- Composite scores (Protection Score, Risk Index, Data Completeness)

### Using the File

**Excel:**
```
1. Open scorecard_main.xlsx
2. Navigate to "Indicators" sheet
3. Use filters to explore data
4. Verify sources in "Sources" sheet
```

**Python with openpyxl:**
```python
import pandas as pd

# Read Excel file
df = pd.read_excel("scorecard_main.xlsx", sheet_name="Indicators")

# Explore
print(df.head())
print(df.columns.tolist())

# Filter
kenya = df[df["Country"] == "Kenya"]
print(kenya.T)  # Transpose for readability
```

**Python with pandas:**
```python
import pandas as pd

# Load all sheets
scorecard = pd.read_excel(
    "scorecard_main.xlsx",
    sheet_name=None  # Load all sheets
)

# Access sheets
indicators = scorecard["Indicators"]
sources = scorecard["Sources"]

# Analysis
print(f"Total countries: {len(indicators)}")
print(f"Total sources: {len(sources)}")
```

### File Structure

**Indicators sheet:**
- Country, Region, ISO3
- 10 indicator columns (values)
- 10 score columns (0-1-2)
- Composite scores (Protection Score, Risk Index)
- Data completeness percentage
- Last updated timestamp

**Sources sheet:**
- Country
- Indicator name
- Source URL
- Last validated
- Validation status
- Notes

---

## Option 4: Pipeline Integration

**Best for:** Automated workflows, document enrichment, batch processing

### Enrichment Process

The scorecard automatically enriches document metadata during pipeline runs:

```bash
# Run pipeline with scorecard enrichment
python pipeline_runner.py --source au_policy
```

### Enriched Metadata

Documents in `data/metadata/metadata.json` include scorecard data:

```json
{
  "id": "Kenya_Digital_Policy_2024.pdf",
  "country": "Kenya",
  "scorecard": {
    "matched_country": "Kenya",
    "enriched_at": "2026-01-26T10:30:00Z",
    "indicators": {
      "AI_Policy_Status": {
        "value": "Framework",
        "score": 1,
        "source": "https://..."
      },
      "Data_Protection_Law": {
        "value": "Comprehensive Law",
        "score": 2,
        "source": "https://..."
      },
      ...
    },
    "protection_score": 14,
    "risk_index": 30
  }
}
```

### Programmatic Access

```python
import json

# Load metadata
with open("data/metadata/metadata.json", "r") as f:
    metadata = json.load(f)

# Filter documents with scorecard data
enriched_docs = [
    doc for doc in metadata["documents"]
    if "scorecard" in doc
]

print(f"Found {len(enriched_docs)} documents with scorecard enrichment")

# Analyze by country
from collections import Counter
countries = Counter(doc["scorecard"]["matched_country"] for doc in enriched_docs)
print(countries.most_common(10))
```

---

## Comparison Matrix

Choose the right method for your needs:

| Feature | API | CSV Export | Direct File | Pipeline |
|---------|-----|-----------|-------------|----------|
| **Real-time data** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Filtering** | ✅ Advanced | ⚠️ Manual | ⚠️ Manual | ⚠️ Limited |
| **Pagination** | ✅ Yes | N/A | N/A | N/A |
| **Requires API server** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Programming required** | ⚠️ Optional | ⚠️ Optional | ⚠️ Optional | ✅ Yes |
| **Best for automation** | ✅ Excellent | ⚠️ OK | ❌ Poor | ✅ Excellent |
| **Best for exploration** | ⚠️ OK | ✅ Excellent | ✅ Excellent | ❌ Poor |
| **Source URLs** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Update frequency** | Real-time | On export | Manual | Auto |

---

## Data Validation

All access methods include validated data:

### Automated Validation

```bash
# Validate all 2,543 source URLs
python pipeline_runner.py --mode scorecard --scorecard-action validate
```

**Checks:**
- HTTP status codes
- Redirect chains
- Response times
- SSL certificates
- Link rot detection

**Output:** `data/scorecard/validation_report.csv`

### Change Detection

```bash
# Detect content changes in sources
python processors/scorecard_diff.py
```

**Detects:**
- Content changes (via hashing)
- Policy updates
- Broken links
- New data availability

---

## Common Queries

### Find countries with specific indicators

**API:**
```bash
# Countries with comprehensive data protection
curl "http://localhost:5000/api/scorecard" | jq '.data.items[] | select(.Data_Protection_Law == "Comprehensive Law") | .country'
```

**Python:**
```python
import pandas as pd

df = pd.read_csv("data/exports/scorecard_summary.csv")
comprehensive = df[df["Data_Protection_Law"] == "Comprehensive Law"]
print(comprehensive["Country"].tolist())
```

### Regional analysis

**API:**
```bash
# Get all African countries
curl "http://localhost:5000/api/scorecard?region=Africa&per_page=100"
```

**Python:**
```python
import pandas as pd

df = pd.read_csv("data/exports/scorecard_summary.csv")
africa = df[df["region"] == "Africa"]
print(africa[["Country", "protection_score", "risk_index"]].sort_values("risk_index"))
```

### Intersectional risk analysis

```python
import pandas as pd

df = pd.read_csv("data/exports/scorecard_summary.csv")

# Find countries with LGBTQ+ criminalization AND biometric SIM requirements
at_risk = df[
    (df["LGBTQ_Legal_Status"] == "Criminalization") &
    (df["SIM_Biometric_ID_Linkage"] == "Mandatory Biometric Registration")
]

print(f"\nCountries with heightened surveillance risk for LGBTQ+ individuals:")
print(at_risk[["Country", "region", "protection_score"]].to_string(index=False))
```

---

## Support

- **API Issues:** [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Data Questions:** [FAQ](../FAQ.md)
- **Export Problems:** [Scorecard Workflow Guide](../guides/SCORECARD_WORKFLOW.md)

---

## Documentation

- [Scorecard Overview](index.md) - What the scorecard is and why it exists
- [Design & Methodology](design.md) - How indicators are defined and scored
- [Visualization](visualization.md) - Charts and visual exports
- [Data Explorer](explorer.md) - Interactive exploration tool
- [API Documentation](../api/index.md) - Complete API reference
