# API Quick Reference

**Fast access to GRIMdata via REST API**

## Start the API

```bash
# Install dependencies
pip install -r api_requirements.txt

# Run development server
python run_api.py

# Or with Docker
docker-compose up -d
```

Server runs at: `http://localhost:5000`

---

## 14 Production-Ready Endpoints

### Health & Info

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Health check |
| `GET /api/info` | System statistics |

### Documents

| Endpoint | Description | Rate Limit |
|----------|-------------|------------|
| `GET /api/documents` | List documents (with filters) | 200/2000 per hour* |
| `GET /api/documents/:id` | Get document details | 100/1000 per hour* |

**Filters:** country, region, tags, year, year_min, year_max, source, doc_type, page, per_page, sort_by, sort_order

### Scorecard

| Endpoint | Description |
|----------|-------------|
| `GET /api/scorecard` | All countries summary |
| `GET /api/scorecard/:country` | Country details |
| `GET /api/scorecard/indicators/statistics` | Indicator statistics |

**Filters:** region, page, per_page

### Tags

| Endpoint | Description | Rate Limit |
|----------|-------------|------------|
| `GET /api/tags` | Tag frequency analysis | 100/1000 per hour* |
| `GET /api/tags/versions` | Available tag versions | 100/1000 per hour* |

**Filters:** version, country, region, year, year_min, year_max

### Timeline

| Endpoint | Description |
|----------|-------------|
| `GET /api/timeline/tags` | Tags over time (year × tag matrix) |

**Filters:** version, country, region, year_min, year_max

### Export

| Endpoint | Description | Rate Limit |
|----------|-------------|------------|
| `GET /api/export` | List available export formats | 100/1000 per hour* |
| `GET /api/export/:format` | Download CSV datasets | 20/200 per hour* |

**Formats:** scorecard_summary, tags_summary, documents_list

<small>*Rate limits: public / authenticated (with API key)</small>

---

## Authentication (Optional)

Use API key for higher rate limits:

```bash
# Add X-API-Key header
curl -H "X-API-Key: your-api-key" http://localhost:5000/api/documents
```

**Rate Limits:**
- **Public (no key):** 100 requests/hour (20/hr for exports)
- **Authenticated:** 1000 requests/hour (200/hr for exports)

---

## Quick Examples

=== "Documents"

    ```bash
    # List all documents
    curl http://localhost:5000/api/documents

    # Filter by country
    curl "http://localhost:5000/api/documents?country=Kenya"

    # Filter by tags and region
    curl "http://localhost:5000/api/documents?tags=AI&region=Africa"

    # Pagination with sorting
    curl "http://localhost:5000/api/documents?page=1&per_page=20&sort_by=year&sort_order=desc"
    ```

=== "Scorecard"

    ```bash
    # All countries
    curl http://localhost:5000/api/scorecard

    # Specific country
    curl http://localhost:5000/api/scorecard/Kenya

    # Filter by region
    curl "http://localhost:5000/api/scorecard?region=Africa"

    # Indicator statistics
    curl http://localhost:5000/api/scorecard/indicators/statistics
    ```

=== "Tags & Timeline"

    ```bash
    # Get tag frequency for Africa
    curl "http://localhost:5000/api/tags?region=Africa&version=tags_v3"

    # Get available tag versions
    curl http://localhost:5000/api/tags/versions

    # Get tags over time (2020-2024)
    curl "http://localhost:5000/api/timeline/tags?year_min=2020&year_max=2024"
    ```

=== "Export"

    ```bash
    # List export formats
    curl http://localhost:5000/api/export

    # Download scorecard CSV
    curl "http://localhost:5000/api/export/scorecard_summary" -o scorecard.csv

    # Download tags summary
    curl "http://localhost:5000/api/export/tags_summary?version=tags_v3" -o tags.csv
    ```

=== "Python"

    ```python
    import requests

    # Optional: Use API key for higher limits
    headers = {"X-API-Key": "your-api-key"}

    # Get documents filtered by country
    response = requests.get(
        "http://localhost:5000/api/documents?country=Kenya",
        headers=headers
    )
    documents = response.json()["data"]["items"]

    # Get scorecard for Kenya
    response = requests.get(
        "http://localhost:5000/api/scorecard/Kenya",
        headers=headers
    )
    scorecard = response.json()["data"]
    print(scorecard["indicators"])

    # Get tag frequency for Africa
    response = requests.get(
        "http://localhost:5000/api/tags?region=Africa",
        headers=headers
    )
    tags = response.json()["data"]["tags"]

    # Download CSV export
    response = requests.get(
        "http://localhost:5000/api/export/scorecard_summary",
        headers=headers
    )
    with open("scorecard.csv", "wb") as f:
        f.write(response.content)
    ```

---

## Response Format

**Success:**

```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2026-01-25T10:30:00Z"
}
```

**Paginated:**

```json
{
  "status": "success",
  "data": {
    "items": [ ... ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 78,
      "total_pages": 4,
      "has_next": true,
      "has_prev": false
    }
  },
  "timestamp": "2026-01-25T10:30:00Z"
}
```

**Error:**

```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "Document not found",
    "details": {}
  },
  "timestamp": "2026-01-25T10:30:00Z"
}
```

**Rate Limit Error (429):**

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again later or use an API key for higher limits."
  },
  "timestamp": "2026-01-25T10:30:00Z"
}
```

---

## Features

<div class="grid cards" markdown>

-   :material-filter:{ .lg .middle } **Advanced Filtering**

    ---

    Filter by country, region, tags, year, source, document type

-   :material-page-layout-sidebar-left:{ .lg .middle } **Pagination**

    ---

    Configurable page size (max 100 items per page)

-   :material-sort:{ .lg .middle } **Sorting**

    ---

    Sort by any field, ascending or descending

-   :material-cached:{ .lg .middle } **Caching**

    ---

    15-minute cache for documents, 1-hour for scorecard

-   :material-check-circle:{ .lg .middle } **Validation**

    ---

    All query parameters validated with clear error messages

-   :material-code-json:{ .lg .middle } **Standard Responses**

    ---

    Consistent JSON structure across all endpoints

-   :material-key:{ .lg .middle } **Authentication**

    ---

    Optional API keys for higher rate limits

-   :material-speedometer:{ .lg .middle } **Rate Limiting**

    ---

    100-2000 requests/hour based on authentication

-   :material-docker:{ .lg .middle } **Docker Ready**

    ---

    Complete Docker + docker-compose setup

</div>

---

## Common Queries

**Get documents about AI policy in Africa:**

```bash
curl "http://localhost:5000/api/documents?region=Africa&tags=AI"
```

**Get tag frequency for child rights in 2024:**

```bash
curl "http://localhost:5000/api/tags?tags=ChildRights&year=2024"
```

**Get LGBTQ+ legal status for all countries:**

```bash
curl http://localhost:5000/api/scorecard | jq '.data.items[] | {country, lgbtq_status: .LGBTQ_Legal_Status}'
```

**Download all scorecard data:**

```bash
curl "http://localhost:5000/api/export/scorecard_summary" -o scorecard.csv
```

**Get timeline of AI tags (2018-2024):**

```bash
curl "http://localhost:5000/api/timeline/tags?year_min=2018&year_max=2024" | jq '.data.timeline'
```

**Get countries with comprehensive data protection:**

```python
import requests
response = requests.get("http://localhost:5000/api/scorecard?per_page=200")
countries = response.json()["data"]["items"]
comprehensive = [c for c in countries if c.get("Data_Protection_Law") == "Comprehensive Law"]
print(f"Found {len(comprehensive)} countries with comprehensive data protection")
```

---

## Production Deployment

Deploy with Docker:

```bash
# Clone repository
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild

# Configure environment
cp .env.example .env
# Edit .env with your API keys and settings

# Start services (API + Redis + Nginx)
docker-compose up -d

# Check status
docker-compose ps
curl http://localhost:5000/api/health
```

**Complete deployment guide:** [:octicons-rocket-24: Production Deployment](../../guides/PRODUCTION_DEPLOYMENT/)

---

## Full Documentation

For complete API documentation including:

- All endpoint parameters and schemas
- Response codes and error handling
- Authentication setup
- Rate limiting details
- Docker deployment guide
- Performance optimization
- Security best practices

See: [:octicons-book-24: Full API Documentation](../../api/README/){ .md-button .md-button--primary }

Or: [:octicons-zap-24: API Quick Start Guide](../../api/QUICK_START/){ .md-button }

---

## Test the API

Quick health check:

```bash
# Check all endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/info
curl http://localhost:5000/api/documents
curl http://localhost:5000/api/scorecard
curl http://localhost:5000/api/tags
curl http://localhost:5000/api/export
```

**All 104 integration tests passing (100% success rate)**

```bash
# Run test suite
pytest tests/api/ -v
```

---

**Last updated:** January 2026 (Phase 4 Complete - 14 endpoints operational)
