# API Quick Reference

**Fast access to GRIMdata via REST API**

## Start the API

```bash
# Install dependencies
pip install -r api_requirements.txt

# Run server
python run_api.py
```

Server runs at: `http://localhost:5000`

---

## 9 Endpoints

### Health & Info

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Health check |
| `GET /api/info` | System statistics |

### Documents

| Endpoint | Description |
|----------|-------------|
| `GET /api/documents` | List documents (with filters) |
| `GET /api/documents/:id` | Get document details |

**Filters:** country, region, tags, year, year_min, year_max, source, doc_type, page, per_page, sort_by, sort_order

### Scorecard

| Endpoint | Description |
|----------|-------------|
| `GET /api/scorecard` | All countries summary |
| `GET /api/scorecard/:country` | Country details |
| `GET /api/scorecard/indicators/statistics` | Indicator statistics |

**Filters:** region, page, per_page

---

## Quick Examples

=== "Documents"

    ```bash
    # List all documents
    curl http://localhost:5000/api/documents

    # Filter by country
    curl "http://localhost:5000/api/documents?country=Kenya"

    # Filter by tags
    curl "http://localhost:5000/api/documents?tags=ChildRights,LGBTQ"

    # Pagination
    curl "http://localhost:5000/api/documents?page=2&per_page=20"
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

=== "Python"

    ```python
    import requests

    # Get documents filtered by country
    response = requests.get("http://localhost:5000/api/documents?country=Kenya")
    documents = response.json()["data"]["items"]

    # Get scorecard for Kenya
    response = requests.get("http://localhost:5000/api/scorecard/Kenya")
    scorecard = response.json()["data"]
    print(scorecard["indicators"])

    # Get all African countries
    response = requests.get("http://localhost:5000/api/scorecard?region=Africa&per_page=50")
    countries = response.json()["data"]["items"]
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
    "message": "Document not found"
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

</div>

---

## Common Queries

**Get documents about AI policy in Africa:**

```bash
curl "http://localhost:5000/api/documents?region=Africa&tags=AI"
```

**Get LGBTQ+ legal status for all countries:**

```bash
curl http://localhost:5000/api/scorecard | jq '.data.items[] | {country, lgbtq_status: .LGBTQ_Legal_Status}'
```

**Find all documents from 2024:**

```bash
curl "http://localhost:5000/api/documents?year=2024"
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

## Full Documentation

For complete API documentation including:

- All endpoint parameters
- Response schemas
- Error codes
- Rate limiting
- Authentication
- Production deployment

See: [:octicons-book-24: Full API Documentation](../api/README/){ .md-button .md-button--primary }

Or: [:octicons-zap-24: API Quick Start Guide](../api/QUICK_START/){ .md-button }

---

## Test the API

Quick health check:

```bash
python test_api.py
```

Expected output:

```
Testing GRIMdata API Endpoints
✅ Health check
✅ System info
✅ Documents list
✅ Document detail
✅ Documents filter (country)
✅ Scorecard summary
✅ Country scorecard
✅ Indicator statistics
✅ Scorecard filter (region)

Results: 9/9 endpoints working (100.00%)
```

---

**Last updated:** January 2026
