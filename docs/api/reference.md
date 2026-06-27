# DigitalChild Flask API

REST API **reference** — endpoints, parameters, and response formats. New to the API? Start with the [Quick Start](quickstart.md). To deploy it, see the [Production Deployment guide](../guides/PRODUCTION_DEPLOYMENT.md).

## API Endpoints

### Health & System Info

**GET /api/health**
- Returns API health status
- Use for monitoring and load balancer health checks

**GET /api/info**
- Returns system information and data statistics
- Includes document counts, scorecard coverage, and data freshness

### Documents

**GET /api/documents**
- List documents with filtering and pagination
- Query parameters:
  - `country`: Filter by country name
  - `region`: Filter by region
  - `source`: Filter by source (e.g., "au_policy", "upr")
  - `doc_type`: Filter by document type
  - `tags`: Comma-separated list of tags
  - `year`: Filter by specific year
  - `year_min`, `year_max`: Filter by year range
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 20, max: 100)
  - `sort_by`: Field to sort by (default: "last_processed")
  - `sort_order`: "asc" or "desc" (default: "desc")

Example:
```bash
curl "http://localhost:5000/api/documents?region=Africa&year_min=2020&per_page=10"
```

**GET /api/documents/:id**
- Get detailed information for a single document
- Returns full document metadata with tags_history
- Cached for 15 minutes

### Scorecard

**GET /api/scorecard**
- List all countries in scorecard with summary
- Query parameters:
  - `region`: Filter by region (optional)
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 20, max: 100)

Example:
```bash
curl "http://localhost:5000/api/scorecard?region=Africa&per_page=20"
```

**GET /api/scorecard/:country**
- Get full scorecard details for a specific country
- Returns all 10 indicators with sources
- Cached for 1 hour

Example:
```bash
curl "http://localhost:5000/api/scorecard/Kenya"
```

**GET /api/scorecard/indicators/statistics**
- Get statistics about indicator values across all countries
- Returns value distribution for each indicator
- Cached for 1 hour

### Tags

**GET /api/tags**
- Get tag frequency analysis across documents
- Query parameters:
  - `version`: Tag version (e.g., "tags_v3", "digital", "queerai")
  - `country`: Filter by country name
  - `region`: Filter by region
  - `year`: Filter by specific year
  - `year_min`, `year_max`: Filter by year range

Example:
```bash
curl "http://localhost:5000/api/tags?version=tags_v3&region=Africa&year_min=2020"
```

**GET /api/tags/versions**
- Get list of available tag versions
- Returns array of version identifiers

Example:
```bash
curl "http://localhost:5000/api/tags/versions"
```

### Timeline

**GET /api/timeline/tags**
- Get temporal analysis of tags over time (year × tag matrix)
- Query parameters:
  - `version`: Tag version (optional)
  - `year_min`, `year_max`: Filter by year range (optional)
  - `country`: Filter by country (optional)
  - `region`: Filter by region (optional)

Example:
```bash
curl "http://localhost:5000/api/timeline/tags?version=tags_v3&year_min=2018&year_max=2024"
```

### Export

**GET /api/export**
- List available export formats
- Returns format ID, filename, and description for each format

Example:
```bash
curl "http://localhost:5000/api/export"
```

**GET /api/export/:format**
- Download dataset in CSV format
- Available formats:
  - `scorecard_summary`: Scorecard data for all countries
  - `tags_summary`: Tag frequency across all documents
  - `documents_list`: Complete document list with metadata
- Query parameters (for tags_summary):
  - `version`: Tag version (optional)

Example:
```bash
curl "http://localhost:5000/api/export/scorecard_summary" -o scorecard.csv
curl "http://localhost:5000/api/export/tags_summary?version=tags_v3" -o tags.csv
```

All CSV exports include SPDX license headers (CC-BY-4.0) for data attribution.

## Implementation status

All 14 endpoints are operational. The week-by-week build trail (what was done, when) is
preserved separately in [API Implementation History](IMPLEMENTATION_HISTORY.md) so this
page stays a clean endpoint reference.

## Architecture

### Directory Structure

```
api/
├── __init__.py                  # Package initialization
├── app.py                       # Flask app factory
├── config.py                    # Configuration classes
├── extensions.py                # Flask extensions init
├── routes/                      # API endpoints
│   ├── health.py               # Health & info endpoints
│   └── ...                     # (More routes in Week 2+)
├── services/                    # Business logic layer
│   ├── metadata_service.py     # Document metadata
│   ├── scorecard_service.py    # Scorecard data
│   └── ...                     # (More services in Week 2+)
├── middleware/                  # Request/response processing
│   └── error_handlers.py       # Exception handling
└── utils/                       # Helper functions
    ├── response.py             # Response formatting
    └── validators.py           # Input validation
```

### Service Layer Pattern

Services wrap the `processors/` modules with API-friendly formatting. The internal design rationale belongs to **Explanation**, not this endpoint reference — see [Architecture](../ARCHITECTURE.md).

### Response Format

All endpoints return standardized JSON:

**Success:**
```json
{
  "status": "success",
  "data": {...},
  "timestamp": "2026-01-25T09:13:43Z"
}
```

**Error:**
```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": {}
  },
  "timestamp": "2026-01-25T09:13:43Z"
}
```

## Configuration

Environment variables (see `.env.example`):

- `FLASK_ENV`: development | production | testing
- `SECRET_KEY`: Flask secret key (required in production)
- `API_KEYS`: Comma-separated API keys (required in production)
- `CORS_ORIGINS`: Allowed CORS origins
- `CACHE_TYPE`: SimpleCache (dev) | RedisCache (prod)
- `METADATA_FILE`: Path to metadata.json
- `SCORECARD_FILE`: Path to scorecard_main.xlsx

## Beyond this reference

This page is the **endpoint reference** only (Diátaxis). For everything else:

- **Run / try the API:** [Quick Start](quickstart.md) *(tutorial)*
- **Deploy to production** (Gunicorn / Docker / Nginx): [Production Deployment guide](../guides/PRODUCTION_DEPLOYMENT.md) *(how-to)*
- **Internal architecture & design:** [Architecture](../ARCHITECTURE.md) *(explanation)*
- **Release history & status, planned API work:** [Changelog](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/CHANGELOG.md) and [Roadmap](../ROADMAP.md)

## Development Notes

- Requires Python 3.12+
- All data files must exist before starting API
- Run `python init_project.py` if metadata.json doesn't exist
- Services use file modification time caching for efficiency
- Scorecard service works with pandas DataFrames from `processors/scorecard.py`
- Always run from project root for imports to work correctly

## Troubleshooting

**ImportError: No module named 'api'**
- Make sure you're running from the project root directory

**FileNotFoundError: metadata.json**
- Run `python init_project.py` to create required files

**KeyError: 'Region'**
- Scorecard columns use "Region - Broad" not "Region"
- Service layer handles this mapping

**TypeError: '<' not supported between instances of 'NoneType' and 'str'**
- Fixed in metadata_service.py by converting None to "unknown"
- All dictionary keys must be non-None for JSON serialization
