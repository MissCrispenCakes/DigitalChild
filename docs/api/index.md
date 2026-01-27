# GRIMdata REST API

**Programmatic access to 78+ documents, 194-country scorecard, and temporal analysis**

---

## Overview

The GRIMdata REST API provides programmatic access to the complete LittleRainbowRights dataset, including human rights documents, the Digital Rights Scorecard, tags analysis, and timeline data.

**API Base URL:** `http://localhost:5000/api` (development) or `https://grimdata.org/api` (production)

## Why Use the API?

<div class="grid cards" markdown>

-   :material-code-json:{ .lg .middle } **Programmatic Access**

    ---

    Query data directly from Python, R, JavaScript, or any language with HTTP support

-   :material-filter:{ .lg .middle } **Advanced Filtering**

    ---

    Filter by country, region, tags, year ranges, document type, and more

-   :material-update:{ .lg .middle } **Real-Time Data**

    ---

    Always get the latest data without downloading CSV files manually

-   :material-api:{ .lg .middle } **Integration Ready**

    ---

    Build dashboards, research tools, and applications on top of GRIMdata

</div>

## Quick Comparison

Choose the right access method for your needs:

| Access Method | Best For | Setup Time | Flexibility |
|---------------|----------|------------|-------------|
| **REST API** | Programmatic access, automation, integrations | 5 minutes | High - filter, paginate, sort |
| **CSV Export** | One-time analysis, Excel, R dataframes | 2 minutes | Medium - static snapshots |
| **Direct Files** | Deep exploration, custom processing | Immediate | High - full file access |

## Get Started

<div class="grid cards" markdown>

-   :octicons-rocket-24:{ .lg .middle } **Quick Start**

    ---

    Get the API running in 5 minutes

    [:octicons-arrow-right-24: Quick Start Guide](quickstart.md)

-   :octicons-book-24:{ .lg .middle } **Full Documentation**

    ---

    Complete API reference with all endpoints

    [:octicons-arrow-right-24: API Reference](reference.md)

-   :octicons-zap-24:{ .lg .middle } **Quick Reference**

    ---

    Cheat sheet of all 14 endpoints

    [:octicons-arrow-right-24: Endpoint Quick Reference](quick-reference.md)

</div>

---

## Features

### 14 Production-Ready Endpoints

**Health & Info:**
- System status and data statistics

**Documents API:**
- List documents with advanced filtering
- Get detailed document metadata
- Pagination and sorting

**Scorecard API:**
- Countries summary with indicators
- Country-specific details
- Indicator statistics and analysis

**Tags API:**
- Frequency analysis across documents
- Version management (v1, v2, v3, digital)
- Temporal and geographic filtering

**Timeline API:**
- Tags over time (year × tag matrix)
- Temporal trend analysis

**Export API:**
- Download CSV datasets
- SPDX license headers included

### Technical Features

<div class="grid cards" markdown>

-   :material-key:{ .lg .middle } **Authentication**

    ---

    Optional API key for higher rate limits (100 → 1000 req/hr)

-   :material-speedometer:{ .lg .middle } **Rate Limiting**

    ---

    Fair usage limits prevent abuse while allowing research

-   :material-cached:{ .lg .middle } **Caching**

    ---

    15-minute cache for documents, 1-hour for scorecard

-   :material-check-circle:{ .lg .middle } **Validation**

    ---

    All query parameters validated with clear error messages

-   :material-docker:{ .lg .middle } **Docker Ready**

    ---

    Complete deployment with Redis and Nginx

-   :material-test-tube:{ .lg .middle } **100% Tested**

    ---

    104 integration tests (100% pass rate)

</div>

---

## Example Use Cases

### Research Applications

**Analyze AI policy adoption in Africa:**
```bash
curl "http://localhost:5000/api/documents?region=Africa&tags=AI&per_page=50"
```

**Get LGBTQ+ legal status for all countries:**
```bash
curl "http://localhost:5000/api/scorecard?per_page=200" | jq '.data.items[] | {country, lgbtq: .LGBTQ_Legal_Status}'
```

**Track child rights tags over time (2018-2024):**
```bash
curl "http://localhost:5000/api/timeline/tags?year_min=2018&year_max=2024" | jq '.data.timeline'
```

### Integration Examples

**Python Research Script:**
```python
import requests
import pandas as pd

# Fetch all documents about child protection in Kenya
response = requests.get(
    "http://localhost:5000/api/documents",
    params={"country": "Kenya", "tags": "ChildRights"}
)
docs = response.json()["data"]["items"]

# Convert to DataFrame for analysis
df = pd.DataFrame(docs)
print(df[["id", "year", "doc_type", "tags"]])
```

**JavaScript Dashboard:**
```javascript
// Fetch scorecard data for visualization
fetch('http://localhost:5000/api/scorecard?per_page=200')
  .then(res => res.json())
  .then(data => {
    const countries = data.data.items;
    // Render heatmap, charts, etc.
  });
```

**R Statistical Analysis:**
```r
library(httr)
library(jsonlite)

# Get tag frequency for Africa
response <- GET("http://localhost:5000/api/tags?region=Africa")
tags <- content(response, as = "parsed")$data$tags

# Analyze distribution
tags_df <- data.frame(
  tag = names(tags),
  count = unlist(tags)
)
```

---

## Quick Examples

=== "cURL"

    ```bash
    # Get all documents
    curl http://localhost:5000/api/documents

    # Filter by country and tags
    curl "http://localhost:5000/api/documents?country=Kenya&tags=AI,ChildRights"

    # Get Kenya's scorecard
    curl http://localhost:5000/api/scorecard/Kenya

    # Download scorecard CSV
    curl "http://localhost:5000/api/export/scorecard_summary" -o scorecard.csv
    ```

=== "Python"

    ```python
    import requests

    # Get documents with filtering
    response = requests.get(
        "http://localhost:5000/api/documents",
        params={
            "region": "Africa",
            "year_min": 2020,
            "tags": "AI",
            "per_page": 50
        }
    )
    documents = response.json()["data"]["items"]

    # Get scorecard for specific country
    response = requests.get("http://localhost:5000/api/scorecard/Kenya")
    scorecard = response.json()["data"]
    print(scorecard["indicators"])
    ```

=== "JavaScript"

    ```javascript
    // Fetch documents with async/await
    async function getDocuments() {
      const response = await fetch(
        'http://localhost:5000/api/documents?region=Africa&tags=AI'
      );
      const data = await response.json();
      return data.data.items;
    }

    // Fetch scorecard
    async function getScorecard(country) {
      const response = await fetch(
        `http://localhost:5000/api/scorecard/${country}`
      );
      const data = await response.json();
      return data.data;
    }
    ```

=== "R"

    ```r
    library(httr)
    library(jsonlite)

    # Get documents
    response <- GET("http://localhost:5000/api/documents?region=Africa")
    documents <- content(response, as = "parsed")$data$items

    # Get scorecard
    response <- GET("http://localhost:5000/api/scorecard/Kenya")
    scorecard <- content(response, as = "parsed")$data
    ```

---

## Rate Limits & Authentication

### Default Rate Limits (No API Key)
- **Documents/Tags/Timeline:** 100 requests/hour
- **Export endpoints:** 20 requests/hour

### Authenticated Rate Limits (With API Key)
- **Documents/Tags/Timeline:** 1000 requests/hour
- **Export endpoints:** 200 requests/hour

### Using API Keys

```bash
# Add X-API-Key header to your requests
curl -H "X-API-Key: your-api-key" http://localhost:5000/api/documents
```

```python
# Python example with API key
headers = {"X-API-Key": "your-api-key"}
response = requests.get(
    "http://localhost:5000/api/documents",
    headers=headers
)
```

Contact the project maintainers to request an API key for research purposes.

---

## Response Format

All API responses use consistent JSON structure:

**Success Response:**
```json
{
  "status": "success",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 78,
      "total_pages": 4
    }
  },
  "timestamp": "2026-01-26T10:30:00Z"
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "Document not found",
    "details": {}
  },
  "timestamp": "2026-01-26T10:30:00Z"
}
```

---

## Production Deployment

Deploy the API with Docker:

```bash
# Clone repository
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start services (API + Redis + Nginx)
docker-compose up -d

# Verify
curl http://localhost:5000/api/health
```

See the [Production Deployment Guide](../../guides/PRODUCTION_DEPLOYMENT.md) for complete setup instructions.

---

## Documentation

<div class="grid cards" markdown>

-   :octicons-rocket-24: **Quick Start**

    ---

    Get the API running in 5 minutes

    [View Guide →](quickstart.md)

-   :octicons-book-24: **Full API Reference**

    ---

    All 14 endpoints with parameters, examples, and response schemas

    [View Reference →](reference.md)

-   :octicons-zap-24: **Quick Reference**

    ---

    Endpoint cheat sheet for quick lookup

    [View Quick Ref →](quick-reference.md)

-   :octicons-tools-24: **Production Guide**

    ---

    Deploy with Docker, configure Nginx, manage API keys

    [View Guide →](../../guides/PRODUCTION_DEPLOYMENT.md)

</div>

---

## Support

- **Issues & Bugs:** [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Feature Requests:** [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **General Questions:** [FAQ](../../FAQ.md)

---

## Technical Stack

- **Framework:** Flask 3.0
- **Caching:** Redis
- **Web Server:** Nginx (production)
- **Container:** Docker + docker-compose
- **Testing:** pytest (104 tests, 100% pass rate)

---

## License

- **API Code:** MIT License
- **Data:** CC BY 4.0

See [LICENSE](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/LICENSE) and [LICENSE-DATA](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/LICENSE-DATA) for details.
