# Accessing Scorecard Data

## Published snapshot downloads

Download the **26 June 2026 visualization snapshot**, including scores, written assessments and source links. JSON retains nested indicator metadata; CSV puts each indicator's score, assessment and sources into columns. Both retain the generation date and **9 September 2025** source-verification stamp.

[Download scorecard JSON](data/scorecard.json){ .md-button download="scorecard.json" }
[Download scorecard CSV](data/scorecard.csv){ .md-button download="scorecard.csv" }

CSV text beginning with spreadsheet formula characters is prefixed with an apostrophe. JSON retains the original text. Identify the snapshot date and assessments used when citing the data; see [citation guidance](../website/projects/littlerainbowrights/index.md#citing-this-work).

## Overview

The published browser snapshot and local pipeline workbook are distinct research outputs:

| Material | Location | Contents |
| --- | --- | --- |
| Published visualization snapshot | Downloads above | Three-point scores, written assessments, sources and documentation counts |
| Canonical pipeline workbook | `data/scorecard/scorecard_main.xlsx`, sheet `UN_194` | Country indicator values and paired source columns |
| Visualization workbook | `data/scorecard/Global_QueerAI_Child_Scorecard_MASTER.xlsx`, sheet `Scorecard` | Scored visualization input |
| Convenience exports | Root `scorecard.xlsx`, `.csv`, `.ods` | Copies generated from the canonical workbook |

The self-hosted API reads the canonical workbook. It does not return the same schema as the scored browser snapshot.

## Option 1: REST API (self-hosted) {#option-1-rest-api-recommended}

<span id="__span-0-4"></span>
<span id="__codelineno-0-4"></span>
<span id="__span-0-5"></span>
<span id="__codelineno-0-5"></span>

### Quick Start

Follow the [API Quick Start](../api/quickstart.md) to install dependencies and start your instance, then query it:

```bash
curl http://localhost:5000/api/health
curl 'http://localhost:5000/api/scorecard?region=Africa&per_page=100'
curl http://localhost:5000/api/scorecard/Kenya
```

<span id="__span-2-5"></span>
<span id="__codelineno-2-5"></span>
<span id="__span-2-6"></span>
<span id="__codelineno-2-6"></span>
<span id="__span-2-7"></span>
<span id="__codelineno-2-7"></span>
<span id="__span-2-8"></span>
<span id="__codelineno-2-8"></span>
<span id="__span-2-9"></span>
<span id="__codelineno-2-9"></span>
<span id="__span-2-10"></span>
<span id="__codelineno-2-10"></span>
<span id="__span-2-11"></span>
<span id="__codelineno-2-11"></span>
<span id="__span-2-12"></span>
<span id="__codelineno-2-12"></span>
<span id="__span-2-13"></span>
<span id="__codelineno-2-13"></span>
<span id="__span-2-14"></span>
<span id="__codelineno-2-14"></span>
<span id="__span-2-15"></span>
<span id="__codelineno-2-15"></span>
<span id="__span-2-16"></span>
<span id="__codelineno-2-16"></span>
<span id="__span-2-17"></span>
<span id="__codelineno-2-17"></span>
<span id="__span-2-18"></span>
<span id="__codelineno-2-18"></span>
<span id="__span-2-19"></span>
<span id="__codelineno-2-19"></span>
<span id="__span-2-20"></span>
<span id="__codelineno-2-20"></span>
<span id="__span-2-21"></span>
<span id="__codelineno-2-21"></span>
<span id="__span-2-22"></span>
<span id="__codelineno-2-22"></span>
<span id="__span-4-2"></span>
<span id="__codelineno-4-2"></span>
<span id="__span-4-3"></span>
<span id="__codelineno-4-3"></span>
<span id="__span-4-4"></span>
<span id="__codelineno-4-4"></span>
<span id="__span-4-5"></span>
<span id="__codelineno-4-5"></span>
<span id="__span-4-6"></span>
<span id="__codelineno-4-6"></span>
<span id="__span-4-7"></span>
<span id="__codelineno-4-7"></span>
<span id="__span-4-8"></span>
<span id="__codelineno-4-8"></span>
<span id="__span-4-9"></span>
<span id="__codelineno-4-9"></span>
<span id="__span-4-10"></span>
<span id="__codelineno-4-10"></span>
<span id="__span-4-11"></span>
<span id="__codelineno-4-11"></span>
<span id="__span-4-12"></span>
<span id="__codelineno-4-12"></span>
<span id="__span-4-13"></span>
<span id="__codelineno-4-13"></span>
<span id="__span-4-14"></span>
<span id="__codelineno-4-14"></span>
<span id="__span-4-15"></span>
<span id="__codelineno-4-15"></span>
<span id="__span-4-16"></span>
<span id="__codelineno-4-16"></span>
<span id="__span-4-17"></span>
<span id="__codelineno-4-17"></span>
<span id="__span-4-18"></span>
<span id="__codelineno-4-18"></span>
<span id="__span-4-19"></span>
<span id="__codelineno-4-19"></span>
<span id="__span-4-20"></span>
<span id="__codelineno-4-20"></span>
<span id="__span-4-21"></span>
<span id="__codelineno-4-21"></span>
<span id="__span-4-22"></span>
<span id="__codelineno-4-22"></span>
<span id="__span-4-23"></span>
<span id="__codelineno-4-23"></span>
<span id="__span-4-24"></span>
<span id="__codelineno-4-24"></span>
<span id="__span-4-25"></span>
<span id="__codelineno-4-25"></span>
<span id="__span-4-26"></span>
<span id="__codelineno-4-26"></span>
<span id="__span-4-27"></span>
<span id="__codelineno-4-27"></span>
<span id="__span-6-5"></span>
<span id="__codelineno-6-5"></span>
<span id="__span-6-6"></span>
<span id="__codelineno-6-6"></span>
<span id="__span-6-7"></span>
<span id="__codelineno-6-7"></span>
<span id="__span-6-8"></span>
<span id="__codelineno-6-8"></span>
<span id="__span-6-9"></span>
<span id="__codelineno-6-9"></span>
<span id="__span-6-10"></span>
<span id="__codelineno-6-10"></span>
<span id="__span-6-11"></span>
<span id="__codelineno-6-11"></span>
<span id="__span-6-12"></span>
<span id="__codelineno-6-12"></span>
<span id="__span-6-13"></span>
<span id="__codelineno-6-13"></span>
<span id="__span-6-14"></span>
<span id="__codelineno-6-14"></span>
<span id="__span-6-15"></span>
<span id="__codelineno-6-15"></span>
<span id="__span-6-16"></span>
<span id="__codelineno-6-16"></span>

### Scorecard Endpoints

| Endpoint | Response under `data` |
| --- | --- |
| `/api/scorecard` | `items` containing country, region, region-specific label and indicator count; `pagination` describes the result pages |
| `/api/scorecard/:country` | Country details and `indicators`; each indicator contains `value` and `source` |
| `/api/scorecard/indicators/statistics` | Per-field `total_countries` and `value_distribution` |

The list endpoint returns summaries. Use country detail for indicator values and sources. The default maximum page size is **100**; follow pagination to retrieve the complete collection.

<span id="__span-7-5"></span>
<span id="__codelineno-7-5"></span>
<span id="__span-7-6"></span>
<span id="__codelineno-7-6"></span>
<span id="__span-7-7"></span>
<span id="__codelineno-7-7"></span>
<span id="__span-7-8"></span>
<span id="__codelineno-7-8"></span>
<span id="__span-7-9"></span>
<span id="__codelineno-7-9"></span>
<span id="__span-7-10"></span>
<span id="__codelineno-7-10"></span>
<span id="__span-7-11"></span>
<span id="__codelineno-7-11"></span>
<span id="__span-7-12"></span>
<span id="__codelineno-7-12"></span>
<span id="__span-7-13"></span>
<span id="__codelineno-7-13"></span>
<span id="__span-8-2"></span>
<span id="__codelineno-8-2"></span>
<span id="__span-8-3"></span>
<span id="__codelineno-8-3"></span>
<span id="__span-8-4"></span>
<span id="__codelineno-8-4"></span>
<span id="__span-8-5"></span>
<span id="__codelineno-8-5"></span>
<span id="__span-8-6"></span>
<span id="__codelineno-8-6"></span>
<span id="__span-8-7"></span>
<span id="__codelineno-8-7"></span>
<span id="__span-8-8"></span>
<span id="__codelineno-8-8"></span>
<span id="__span-8-9"></span>
<span id="__codelineno-8-9"></span>
<span id="__span-8-10"></span>
<span id="__codelineno-8-10"></span>
<span id="__span-8-11"></span>
<span id="__codelineno-8-11"></span>
<span id="__span-8-12"></span>
<span id="__codelineno-8-12"></span>
<span id="__span-8-13"></span>
<span id="__codelineno-8-13"></span>
<span id="__span-8-14"></span>
<span id="__codelineno-8-14"></span>
<span id="__span-8-15"></span>
<span id="__codelineno-8-15"></span>
<span id="__span-8-16"></span>
<span id="__codelineno-8-16"></span>
<span id="__span-9-4"></span>
<span id="__codelineno-9-4"></span>
<span id="__span-9-5"></span>
<span id="__codelineno-9-5"></span>
<span id="__span-9-6"></span>
<span id="__codelineno-9-6"></span>
<span id="__span-9-7"></span>
<span id="__codelineno-9-7"></span>
<span id="__span-9-8"></span>
<span id="__codelineno-9-8"></span>
<span id="__span-9-9"></span>
<span id="__codelineno-9-9"></span>
<span id="__span-9-10"></span>
<span id="__codelineno-9-10"></span>
<span id="__span-9-11"></span>
<span id="__codelineno-9-11"></span>
<span id="__span-9-12"></span>
<span id="__codelineno-9-12"></span>
<span id="__span-9-13"></span>
<span id="__codelineno-9-13"></span>
<span id="__span-9-14"></span>
<span id="__codelineno-9-14"></span>
<span id="__span-9-15"></span>
<span id="__codelineno-9-15"></span>
<span id="__span-9-16"></span>
<span id="__codelineno-9-16"></span>
<span id="__span-9-17"></span>
<span id="__codelineno-9-17"></span>
<span id="__span-9-18"></span>
<span id="__codelineno-9-18"></span>
<span id="__span-9-19"></span>
<span id="__codelineno-9-19"></span>
<span id="__span-9-20"></span>
<span id="__codelineno-9-20"></span>
<span id="__span-9-21"></span>
<span id="__codelineno-9-21"></span>

### Python Examples

Fetch all country summaries, then inspect one country's indicators:

```python
import requests

base = "http://localhost:5000/api"
countries = []
page = 1
while True:
    response = requests.get(
        f"{base}/scorecard", params={"page": page, "per_page": 100}, timeout=30
    )
    response.raise_for_status()
    result = response.json()["data"]
    countries.extend(result["items"])
    if not result["pagination"]["has_next"]:
        break
    page += 1

response = requests.get(f"{base}/scorecard/Kenya", timeout=30)
response.raise_for_status()
kenya = response.json()["data"]
print(kenya["indicators"]["LGBTQ_Legal_Status"])
print(len(countries))
```

<span id="__span-10-2"></span>
<span id="__codelineno-10-2"></span>
<span id="__span-10-3"></span>
<span id="__codelineno-10-3"></span>
<span id="__span-10-4"></span>
<span id="__codelineno-10-4"></span>
<span id="__span-10-5"></span>
<span id="__codelineno-10-5"></span>
<span id="__span-10-6"></span>
<span id="__codelineno-10-6"></span>
<span id="__span-10-7"></span>
<span id="__codelineno-10-7"></span>
<span id="__span-10-8"></span>
<span id="__codelineno-10-8"></span>
<span id="__span-10-9"></span>
<span id="__codelineno-10-9"></span>
<span id="__span-10-10"></span>
<span id="__codelineno-10-10"></span>
<span id="__span-10-11"></span>
<span id="__codelineno-10-11"></span>
<span id="__span-10-12"></span>
<span id="__codelineno-10-12"></span>
<span id="__span-10-13"></span>
<span id="__codelineno-10-13"></span>
<span id="__span-10-14"></span>
<span id="__codelineno-10-14"></span>
<span id="__span-10-15"></span>
<span id="__codelineno-10-15"></span>
<span id="__span-10-16"></span>
<span id="__codelineno-10-16"></span>
<span id="__span-10-17"></span>
<span id="__codelineno-10-17"></span>
<span id="__span-10-18"></span>
<span id="__codelineno-10-18"></span>
<span id="__span-10-19"></span>
<span id="__codelineno-10-19"></span>
<span id="__span-10-20"></span>
<span id="__codelineno-10-20"></span>
<span id="__span-10-21"></span>
<span id="__codelineno-10-21"></span>
<span id="__span-10-22"></span>
<span id="__codelineno-10-22"></span>
<span id="__span-10-23"></span>
<span id="__codelineno-10-23"></span>

### JavaScript Example

Query one country's indicator values from your locally running service:

```javascript
const response = await fetch('http://localhost:5000/api/scorecard/Kenya');
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const { data } = await response.json();
console.log(data.indicators.LGBTQ_Legal_Status);
```

<span id="__span-11-2"></span>
<span id="__codelineno-11-2"></span>
<span id="__span-11-3"></span>
<span id="__codelineno-11-3"></span>
<span id="__span-11-4"></span>
<span id="__codelineno-11-4"></span>
<span id="__span-11-5"></span>
<span id="__codelineno-11-5"></span>
<span id="__span-11-6"></span>
<span id="__codelineno-11-6"></span>
<span id="__span-11-7"></span>
<span id="__codelineno-11-7"></span>
<span id="__span-11-8"></span>
<span id="__codelineno-11-8"></span>
<span id="__span-11-9"></span>
<span id="__codelineno-11-9"></span>
<span id="__span-11-10"></span>
<span id="__codelineno-11-10"></span>
<span id="__span-11-11"></span>
<span id="__codelineno-11-11"></span>
<span id="__span-11-12"></span>
<span id="__codelineno-11-12"></span>
<span id="__span-11-13"></span>
<span id="__codelineno-11-13"></span>
<span id="__span-11-14"></span>
<span id="__codelineno-11-14"></span>
<span id="__span-11-15"></span>
<span id="__codelineno-11-15"></span>
<span id="__span-11-16"></span>
<span id="__codelineno-11-16"></span>
<span id="__span-11-17"></span>
<span id="__codelineno-11-17"></span>

### R Example

```r
library(httr)
response <- GET("http://localhost:5000/api/scorecard/Kenya")
stop_for_status(response)
kenya <- content(response, as = "parsed")$data
print(kenya$indicators$LGBTQ_Legal_Status)
```

### Rate Limits

Default limits are 100 requests/hour without a key and 1,000 with a key; some routes use different limits. The instance operator configures keys and limits through the [deployment guide](../guides/PRODUCTION_DEPLOYMENT.md).

## Option 2: CSV Export

### Generate Exports

Run from the repository root:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action export
```

### Generated Files

The standard export writes:

- `data/exports/scorecard_summary.csv`: country, region and indicator values.
- `data/exports/scorecard_sources.csv`: `country`, `indicator` and `url` for each extracted source URL.
- `data/exports/scorecard_indicator_counts.csv`: indicator, status and count.

Regional and individual-indicator exports are separate operations:

```python
from processors.scorecard_export import ScorecardExporter

exporter = ScorecardExporter()
exporter.export_by_region("Africa")
exporter.export_by_indicator("AI_Policy_Status")
```

<span id="__span-13-1"></span>
<span id="__codelineno-13-1"></span>
<span id="__span-13-2"></span>
<span id="__codelineno-13-2"></span>
<span id="__span-13-3"></span>
<span id="__codelineno-13-3"></span>
<span id="__span-13-4"></span>
<span id="__codelineno-13-4"></span>
<span id="__span-14-1"></span>
<span id="__codelineno-14-1"></span>
<span id="__span-14-2"></span>
<span id="__codelineno-14-2"></span>
<span id="__span-14-3"></span>
<span id="__codelineno-14-3"></span>
<span id="__span-14-4"></span>
<span id="__codelineno-14-4"></span>
<span id="__span-14-5"></span>
<span id="__codelineno-14-5"></span>
<span id="__span-14-6"></span>
<span id="__codelineno-14-6"></span>
<span id="__span-14-7"></span>
<span id="__codelineno-14-7"></span>
<span id="__span-14-8"></span>
<span id="__codelineno-14-8"></span>
<span id="__span-14-9"></span>
<span id="__codelineno-14-9"></span>
<span id="__span-14-10"></span>
<span id="__codelineno-14-10"></span>
<span id="__span-14-11"></span>
<span id="__codelineno-14-11"></span>
<span id="__span-14-12"></span>
<span id="__codelineno-14-12"></span>
<span id="__span-15-1"></span>
<span id="__codelineno-15-1"></span>
<span id="__span-15-2"></span>
<span id="__codelineno-15-2"></span>
<span id="__span-15-3"></span>
<span id="__codelineno-15-3"></span>
<span id="__span-15-4"></span>
<span id="__codelineno-15-4"></span>
<span id="__span-15-5"></span>
<span id="__codelineno-15-5"></span>
<span id="__span-15-6"></span>
<span id="__codelineno-15-6"></span>
<span id="__span-15-7"></span>
<span id="__codelineno-15-7"></span>
<span id="__span-15-8"></span>
<span id="__codelineno-15-8"></span>
<span id="__span-15-9"></span>
<span id="__codelineno-15-9"></span>
<span id="__span-15-10"></span>
<span id="__codelineno-15-10"></span>
<span id="__span-15-11"></span>
<span id="__codelineno-15-11"></span>
<span id="__span-15-12"></span>
<span id="__codelineno-15-12"></span>
<span id="__span-15-13"></span>
<span id="__codelineno-15-13"></span>
<span id="__span-15-14"></span>
<span id="__codelineno-15-14"></span>
<span id="__span-15-15"></span>
<span id="__codelineno-15-15"></span>

### Using CSV Exports

```python
import pandas as pd

df = pd.read_csv("data/exports/scorecard_summary.csv")
print(df[["Country", "AI_Policy_Status", "Data_Protection_Law"]].head())
```

## Option 3: Direct File Access

### Primary File

Open `data/scorecard/scorecard_main.xlsx`, sheet **UN_194**, for the canonical pipeline inputs.

<span id="__span-16-1"></span>
<span id="__codelineno-16-1"></span>
<span id="__span-16-2"></span>
<span id="__codelineno-16-2"></span>
<span id="__span-16-3"></span>
<span id="__codelineno-16-3"></span>
<span id="__span-16-4"></span>
<span id="__codelineno-16-4"></span>
<span id="__span-17-1"></span>
<span id="__codelineno-17-1"></span>
<span id="__span-17-2"></span>
<span id="__codelineno-17-2"></span>
<span id="__span-17-3"></span>
<span id="__codelineno-17-3"></span>
<span id="__span-17-4"></span>
<span id="__codelineno-17-4"></span>
<span id="__span-17-5"></span>
<span id="__codelineno-17-5"></span>
<span id="__span-17-6"></span>
<span id="__codelineno-17-6"></span>
<span id="__span-17-7"></span>
<span id="__codelineno-17-7"></span>
<span id="__span-17-8"></span>
<span id="__codelineno-17-8"></span>
<span id="__span-17-9"></span>
<span id="__codelineno-17-9"></span>
<span id="__span-17-10"></span>
<span id="__codelineno-17-10"></span>
<span id="__span-17-11"></span>
<span id="__codelineno-17-11"></span>
<span id="__span-17-12"></span>
<span id="__codelineno-17-12"></span>
<span id="__span-18-1"></span>
<span id="__codelineno-18-1"></span>
<span id="__span-18-2"></span>
<span id="__codelineno-18-2"></span>
<span id="__span-18-3"></span>
<span id="__codelineno-18-3"></span>
<span id="__span-18-4"></span>
<span id="__codelineno-18-4"></span>
<span id="__span-18-5"></span>
<span id="__codelineno-18-5"></span>
<span id="__span-18-6"></span>
<span id="__codelineno-18-6"></span>
<span id="__span-18-7"></span>
<span id="__codelineno-18-7"></span>
<span id="__span-18-8"></span>
<span id="__codelineno-18-8"></span>
<span id="__span-18-9"></span>
<span id="__codelineno-18-9"></span>
<span id="__span-18-10"></span>
<span id="__codelineno-18-10"></span>
<span id="__span-18-11"></span>
<span id="__codelineno-18-11"></span>
<span id="__span-18-12"></span>
<span id="__codelineno-18-12"></span>
<span id="__span-18-13"></span>
<span id="__codelineno-18-13"></span>
<span id="__span-18-14"></span>
<span id="__codelineno-18-14"></span>
<span id="__span-18-15"></span>
<span id="__codelineno-18-15"></span>

### Using the File

```python
import pandas as pd

df = pd.read_excel("data/scorecard/scorecard_main.xlsx", sheet_name="UN_194")
print(df[["Country", "LGBTQ_Legal_Status", "LGBTQ_Legal_Status_Source"]].head())
```

### File Structure

Country and region columns sit alongside indicator values and paired `_Source` columns. The current canonical workbook has one sheet; supporting visualization material is in the separate visualization workbook. For the browser's numerical scores and written justifications, use the published JSON/CSV or the visualization workbook rather than assuming the pipeline workbook has that schema.

## Option 4: Pipeline Integration

<span id="__span-19-1"></span>
<span id="__codelineno-19-1"></span>
<span id="__span-19-2"></span>
<span id="__codelineno-19-2"></span>

### Enrichment Process

Document processing adds country indicators where a country match is available. Refresh enrichment in an existing metadata collection with:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action enrich
```

<span id="__span-20-1"></span>
<span id="__codelineno-20-1"></span>
<span id="__span-20-2"></span>
<span id="__codelineno-20-2"></span>
<span id="__span-20-3"></span>
<span id="__codelineno-20-3"></span>
<span id="__span-20-4"></span>
<span id="__codelineno-20-4"></span>
<span id="__span-20-5"></span>
<span id="__codelineno-20-5"></span>
<span id="__span-20-6"></span>
<span id="__codelineno-20-6"></span>
<span id="__span-20-7"></span>
<span id="__codelineno-20-7"></span>
<span id="__span-20-8"></span>
<span id="__codelineno-20-8"></span>
<span id="__span-20-9"></span>
<span id="__codelineno-20-9"></span>
<span id="__span-20-10"></span>
<span id="__codelineno-20-10"></span>
<span id="__span-20-11"></span>
<span id="__codelineno-20-11"></span>
<span id="__span-20-12"></span>
<span id="__codelineno-20-12"></span>
<span id="__span-20-13"></span>
<span id="__codelineno-20-13"></span>
<span id="__span-20-14"></span>
<span id="__codelineno-20-14"></span>
<span id="__span-20-15"></span>
<span id="__codelineno-20-15"></span>
<span id="__span-20-16"></span>
<span id="__codelineno-20-16"></span>
<span id="__span-20-17"></span>
<span id="__codelineno-20-17"></span>
<span id="__span-20-18"></span>
<span id="__codelineno-20-18"></span>
<span id="__span-20-19"></span>
<span id="__codelineno-20-19"></span>
<span id="__span-20-20"></span>
<span id="__codelineno-20-20"></span>
<span id="__span-20-21"></span>
<span id="__codelineno-20-21"></span>
<span id="__span-20-22"></span>
<span id="__codelineno-20-22"></span>
<span id="__span-20-23"></span>
<span id="__codelineno-20-23"></span>

### Enriched Metadata

A document's `scorecard` object records the matched country, enrichment timestamp and indicator values/sources. [Metadata Schema](../standards/METADATA_SCHEMA.md#scorecard-integration) describes these fields.

<span id="__span-21-1"></span>
<span id="__codelineno-21-1"></span>
<span id="__span-21-2"></span>
<span id="__codelineno-21-2"></span>
<span id="__span-21-3"></span>
<span id="__codelineno-21-3"></span>
<span id="__span-21-4"></span>
<span id="__codelineno-21-4"></span>
<span id="__span-21-5"></span>
<span id="__codelineno-21-5"></span>
<span id="__span-21-6"></span>
<span id="__codelineno-21-6"></span>
<span id="__span-21-7"></span>
<span id="__codelineno-21-7"></span>
<span id="__span-21-8"></span>
<span id="__codelineno-21-8"></span>
<span id="__span-21-9"></span>
<span id="__codelineno-21-9"></span>
<span id="__span-21-10"></span>
<span id="__codelineno-21-10"></span>
<span id="__span-21-11"></span>
<span id="__codelineno-21-11"></span>
<span id="__span-21-12"></span>
<span id="__codelineno-21-12"></span>
<span id="__span-21-13"></span>
<span id="__codelineno-21-13"></span>
<span id="__span-21-14"></span>
<span id="__codelineno-21-14"></span>
<span id="__span-21-15"></span>
<span id="__codelineno-21-15"></span>
<span id="__span-21-16"></span>
<span id="__codelineno-21-16"></span>
<span id="__span-21-17"></span>
<span id="__codelineno-21-17"></span>
<span id="__span-21-18"></span>
<span id="__codelineno-21-18"></span>

### Programmatic Access

```python
from processors.scorecard import get_all_indicators

print(get_all_indicators("Kenya"))
```

## Comparison Matrix

| Need | Use |
| --- | --- |
| Browser snapshot scores and written assessments | Published JSON/CSV |
| Local country values and sources through HTTP | Self-hosted API country detail |
| Workbook research and editing | Canonical `UN_194` sheet |
| Generated summaries and source lists | Pipeline exports |
| Add country context to processed documents | Pipeline enrichment |

## Data Validation

<span id="__span-22-1"></span>
<span id="__codelineno-22-1"></span>
<span id="__span-22-2"></span>
<span id="__codelineno-22-2"></span>

### Automated Validation

```bash
python processors/scorecard_validator.py --workers 10
```

URL checks record reachability, redirects and errors. They do not establish whether a legal interpretation is correct. Outputs are documented in the [Scorecard Workflow](../guides/SCORECARD_WORKFLOW.md#4-validate-source-urls).

<span id="__span-23-1"></span>
<span id="__codelineno-23-1"></span>
<span id="__span-23-2"></span>
<span id="__codelineno-23-2"></span>

### Change Detection

```bash
python processors/scorecard_diff.py
```

Content hashes identify changed source pages for review. Years found in assessment text flag possible review candidates; a law's age alone does not make its current status obsolete.

## Common Queries

<span id="__span-24-1"></span>
<span id="__codelineno-24-1"></span>
<span id="__span-24-2"></span>
<span id="__codelineno-24-2"></span>
<span id="__span-25-1"></span>
<span id="__codelineno-25-1"></span>
<span id="__span-25-2"></span>
<span id="__codelineno-25-2"></span>
<span id="__span-25-3"></span>
<span id="__codelineno-25-3"></span>
<span id="__span-25-4"></span>
<span id="__codelineno-25-4"></span>
<span id="__span-25-5"></span>
<span id="__codelineno-25-5"></span>

### Find countries with specific indicators

For the browser snapshot, use its scored fields directly:

```python
import requests

response = requests.get("https://grimdata.org/scorecard/data/scorecard.json", timeout=30)
response.raise_for_status()
snapshot = response.json()
countries = [
    c["country"] for c in snapshot["countries"]
    if c["scores"].get("LGBTQ") == 0 and c["scores"].get("SIM") == 0
]
print(countries)
```

This selects countries assigned zero on both indicators in this snapshot. Open their written assessments to examine the classification.

<span id="__span-26-1"></span>
<span id="__codelineno-26-1"></span>
<span id="__span-26-2"></span>
<span id="__codelineno-26-2"></span>
<span id="__span-27-1"></span>
<span id="__codelineno-27-1"></span>
<span id="__span-27-2"></span>
<span id="__codelineno-27-2"></span>
<span id="__span-27-3"></span>
<span id="__codelineno-27-3"></span>
<span id="__span-27-4"></span>
<span id="__codelineno-27-4"></span>
<span id="__span-27-5"></span>
<span id="__codelineno-27-5"></span>

### Regional analysis

Filter by region in the [country explorer](explorer.md), or pass `region=Africa` to the API summary endpoint.

<span id="__span-28-1"></span>
<span id="__codelineno-28-1"></span>
<span id="__span-28-2"></span>
<span id="__codelineno-28-2"></span>
<span id="__span-28-3"></span>
<span id="__codelineno-28-3"></span>
<span id="__span-28-4"></span>
<span id="__codelineno-28-4"></span>
<span id="__span-28-5"></span>
<span id="__codelineno-28-5"></span>
<span id="__span-28-6"></span>
<span id="__codelineno-28-6"></span>
<span id="__span-28-7"></span>
<span id="__codelineno-28-7"></span>
<span id="__span-28-8"></span>
<span id="__codelineno-28-8"></span>
<span id="__span-28-9"></span>
<span id="__codelineno-28-9"></span>
<span id="__span-28-10"></span>
<span id="__codelineno-28-10"></span>
<span id="__span-28-11"></span>
<span id="__codelineno-28-11"></span>
<span id="__span-28-12"></span>
<span id="__codelineno-28-12"></span>

### Intersectional risk analysis

[Research Context](../RESEARCH_CONTEXT.md#reading-indicator-combinations) explains how identification requirements and restrictions on LGBTQ+ expression can interact. The additive score does not calculate those interactions.

## Support

[API reference](../api/reference.md) · [Scorecard Workflow](../guides/SCORECARD_WORKFLOW.md) · [FAQ](../FAQ.md)

## Documentation

[Scorecard overview](index.md) · [Methodology](design.md) · [Visualization](visualization.md) · [Country explorer](explorer.md)
