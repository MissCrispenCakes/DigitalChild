# DigitalChild Flask API

REST API backend for serving DigitalChild data to the Phase 4 research dashboard.

## Quick Start

### Installation

```bash
# Activate virtual environment
source .LittleRainbow/bin/activate

# Install dependencies
pip install -r requirements.txt -r api_requirements.txt

# Create .env file from template
cp .env.example .env
# Edit .env and configure as needed
```

### Running the Development Server

```bash
python run_api.py
```

The API will be available at `http://127.0.0.1:5000`

### Testing

```bash
# Test health check
curl http://127.0.0.1:5000/api/health

# Test system info
curl http://127.0.0.1:5000/api/info
```

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

## Implementation Status

### Week 1: Foundation ✅ COMPLETE

1. ✅ API directory structure created
2. ✅ Configuration management (development, production, testing)
3. ✅ Flask extensions (CORS, Caching, Rate Limiting)
4. ✅ Flask app factory pattern
5. ✅ Metadata service layer with caching
6. ✅ Scorecard service layer (works with pandas DataFrames)
7. ✅ Health check routes
8. ✅ Standard response formatting and error handling
9. ✅ Request validators
10. ✅ API requirements file
11. ✅ Environment configuration template
12. ✅ Development and production entry points

### Week 2: Core APIs ✅ COMPLETE

1. ✅ Documents API (list with filters, detail)
2. ✅ Scorecard API (summary, country detail, statistics)
3. ✅ Caching decorators (15min documents, 1hr scorecard)
4. ✅ Request validation for all parameters
5. ✅ Pagination support (configurable page size)
6. ✅ Sorting support (any field, asc/desc)
7. ✅ 39 test cases written (12 unit + 27 integration)
8. ✅ All 9 endpoints working and tested

### Week 3: Extended APIs ✅ COMPLETE

1. ✅ Tags API (frequency analysis, version management)
   - GET /api/tags (with filters)
   - GET /api/tags/versions
2. ✅ Timeline API (temporal analysis)
   - GET /api/timeline/tags (year × tag matrix)
3. ✅ Export API (CSV downloads)
   - GET /api/export (list formats)
   - GET /api/export/:format (download CSV)
4. ✅ SPDX license headers in CSV exports
5. ✅ 31 test cases written for Week 3 endpoints
6. ✅ All 14 endpoints now working (76 total tests passing)

### Week 4: Authentication & Rate Limiting ✅ COMPLETE

1. ✅ API key authentication middleware
   - `@require_api_key` decorator for protected endpoints
   - `@optional_api_key` for flexible authentication
   - X-API-Key header validation
   - Development mode auto-allow for testing
2. ✅ Rate limiting implementation
   - Dynamic limits based on authentication status
   - Public: 100 requests/hour default
   - Authenticated: 1000 requests/hour default
   - Custom limits for expensive operations (exports: 20/200 per hour)
   - Search operations: 200/2000 per hour
3. ✅ Flask-Limiter integration
   - Custom rate limit key function (API key or IP)
   - Redis storage for production
   - Memory storage for development
4. ✅ Applied to key endpoints
   - Documents list with search rate limits
   - Export downloads with strict limits
   - Optional authentication throughout
5. ✅ 28 test cases for authentication and rate limiting
6. ✅ All 104 tests passing (100% success rate)

### Week 5: Production Ready ✅ COMPLETE

1. ✅ Docker deployment
   - Multi-stage Dockerfile with security best practices
   - docker-compose.yml with Redis and Nginx
   - Health checks and non-root user
2. ✅ Nginx configuration
   - Reverse proxy setup
   - SSL/TLS configuration
   - Security headers
   - Gzip compression
3. ✅ Production deployment guide
   - Complete setup instructions
   - Docker and manual deployment options
   - SSL certificate setup (Let's Encrypt)
   - Monitoring and logging configuration
   - Security checklist
   - Troubleshooting guide
4. ✅ Configuration management
   - Environment-based settings
   - Production validation
   - API key management
5. ✅ Ready for production deployment

### API Features

- ✅ Standard JSON response format
- ✅ Error handling with custom exceptions
- ✅ File modification time caching for metadata
- ✅ Pandas DataFrame support for scorecard data
- ✅ Environment-based configuration
- ✅ CORS support for frontend integration
- ✅ Rate limiting ready (in-memory for dev, Redis for prod)
- ✅ Logging with configurable levels

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

Services wrap existing `processors/` modules with API-friendly formatting:

```python
# Example: metadata_service.py
from processors.logger import get_logger

def get_documents(filters, page, per_page):
    """Load metadata.json, apply filters, paginate"""
    metadata = load_metadata()  # With file mtime caching
    docs = metadata.get("documents", [])
    # Apply filters...
    # Paginate...
    return {"documents": [...], "pagination": {...}}
```

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

## Phase 4 API: COMPLETE ✅

All 5 weeks of the Phase 4 API implementation are complete:

- ✅ **Week 1**: Foundation (app factory, config, extensions, middleware)
- ✅ **Week 2**: Core APIs (documents, scorecard endpoints)
- ✅ **Week 3**: Extended APIs (tags, timeline, exports)
- ✅ **Week 4**: Authentication & rate limiting
- ✅ **Week 5**: Production deployment ready

**Final Statistics:**
- **14 REST endpoints** operational
- **104 integration tests** passing (100% success rate)
- **Authentication**: API key based with flexible decorators
- **Rate limiting**: Dynamic limits (100-2000 req/hr based on auth)
- **Deployment**: Docker + docker-compose + Nginx ready
- **Documentation**: Complete API docs + production guide

## Future Enhancements

Optional improvements for future iterations:

### API Documentation
- [ ] Swagger/OpenAPI specification
- [ ] Interactive API explorer at /api/docs
- [ ] Auto-generated client libraries

### Advanced Features
- [ ] GraphQL endpoint for flexible queries
- [ ] Webhook support for data updates
- [ ] Batch operations API
- [ ] API versioning (v2)

### Performance
- [ ] Database integration (PostgreSQL)
- [ ] Full-text search (Elasticsearch)
- [ ] CDN integration for exports
- [ ] Query result streaming

### Analytics
- [ ] API usage analytics dashboard
- [ ] Per-endpoint performance metrics
- [ ] User behavior tracking
- [ ] Cost per API call analysis

### Security
- [ ] OAuth 2.0 / JWT authentication
- [ ] IP whitelisting
- [ ] Request signature validation
- [ ] DDoS protection (Cloudflare integration)

## Production Deployment

### Using Gunicorn

```bash
# Install production dependencies
pip install -r api_requirements.txt

# Set environment
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export API_KEYS=key1,key2,key3

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### Using Docker

```bash
# Build image
docker build -t digitalchild-api .

# Run container
docker run -p 5000:5000 --env-file .env digitalchild-api
```

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
