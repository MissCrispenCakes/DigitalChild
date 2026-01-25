# API Quick Start Guide

## Start the API (Development)

```bash
# Activate virtual environment
source .LittleRainbow/bin/activate

# Run development server
python run_api.py
```

Server starts at: **http://127.0.0.1:5000**

## Test Endpoints

### Health Check
```bash
curl http://127.0.0.1:5000/api/health
```

### System Info
```bash
curl http://127.0.0.1:5000/api/info
```

### List Documents
```bash
# All documents (paginated)
curl http://127.0.0.1:5000/api/documents

# With filters
curl "http://127.0.0.1:5000/api/documents?region=Africa&year_min=2020&per_page=10&sort_by=year&sort_order=desc"

# By country
curl "http://127.0.0.1:5000/api/documents?country=Kenya"

# By tags
curl "http://127.0.0.1:5000/api/documents?tags=AI"
```

### Get Document Detail
```bash
curl http://127.0.0.1:5000/api/documents/YOUR_DOC_ID
```

### List Countries (Scorecard)
```bash
# All countries
curl "http://127.0.0.1:5000/api/scorecard?per_page=20"

# African countries only
curl "http://127.0.0.1:5000/api/scorecard?region=Africa"
```

### Get Country Scorecard
```bash
curl http://127.0.0.1:5000/api/scorecard/Kenya
```

### Get Indicator Statistics
```bash
curl http://127.0.0.1:5000/api/scorecard/indicators/statistics
```

### Get Tag Frequency
```bash
# All tags
curl http://127.0.0.1:5000/api/tags

# By version
curl "http://127.0.0.1:5000/api/tags?version=tags_v3"

# Filtered by region and year
curl "http://127.0.0.1:5000/api/tags?region=Africa&year_min=2020&year_max=2024"
```

### Get Tag Versions
```bash
curl http://127.0.0.1:5000/api/tags/versions
```

### Get Timeline (Tags Over Time)
```bash
# All years
curl http://127.0.0.1:5000/api/timeline/tags

# Filtered by version and year range
curl "http://127.0.0.1:5000/api/timeline/tags?version=tags_v3&year_min=2018&year_max=2024"

# By region
curl "http://127.0.0.1:5000/api/timeline/tags?region=Africa"
```

### Export Data (CSV Downloads)
```bash
# List available export formats
curl http://127.0.0.1:5000/api/export

# Download scorecard summary
curl "http://127.0.0.1:5000/api/export/scorecard_summary" -o scorecard.csv

# Download tags summary
curl "http://127.0.0.1:5000/api/export/tags_summary?version=tags_v3" -o tags.csv

# Download documents list
curl "http://127.0.0.1:5000/api/export/documents_list" -o documents.csv
```

## Response Format

### Success Response
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2026-01-25T09:00:00Z"
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": {}
  },
  "timestamp": "2026-01-25T09:00:00Z"
}
```

### Paginated Response
```json
{
  "status": "success",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 78,
      "total_pages": 4,
      "has_next": true,
      "has_prev": false
    }
  },
  "timestamp": "2026-01-25T09:00:00Z"
}
```

## Query Parameters

### Documents
- `country` - Filter by country name
- `region` - Filter by region
- `source` - Filter by source (e.g., "au_policy")
- `doc_type` - Filter by document type
- `tags` - Comma-separated tags (e.g., "AI,ChildRights")
- `year` - Specific year
- `year_min`, `year_max` - Year range
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)
- `sort_by` - Sort field (default: "last_processed")
- `sort_order` - "asc" or "desc" (default: "desc")

### Scorecard
- `region` - Filter by region
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)

### Tags
- `version` - Tag version (e.g., "tags_v3", "digital", "queerai")
- `country` - Filter by country name
- `region` - Filter by region
- `year` - Specific year
- `year_min`, `year_max` - Year range

### Timeline
- `version` - Tag version (optional)
- `country` - Filter by country (optional)
- `region` - Filter by region (optional)
- `year_min`, `year_max` - Year range (optional)

### Export
- `version` - Tag version (for tags_summary export only)

## Common Filter Examples

### Documents by Region and Year
```bash
curl "http://127.0.0.1:5000/api/documents?region=Africa&year_min=2022&year_max=2024"
```

### Documents with Multiple Tags
```bash
curl "http://127.0.0.1:5000/api/documents?tags=AI,ChildRights"
```

### African Countries Scorecard
```bash
curl "http://127.0.0.1:5000/api/scorecard?region=Africa&per_page=50"
```

### Recent Documents
```bash
curl "http://127.0.0.1:5000/api/documents?sort_by=last_processed&sort_order=desc&per_page=10"
```

## Error Codes

- `200` - Success
- `400` - Validation error (invalid parameters)
- `404` - Resource not found
- `429` - Rate limit exceeded
- `500` - Internal server error

## Caching

- Document detail: 15 minutes
- Scorecard country: 1 hour
- Indicator statistics: 1 hour
- Metadata list: File modification time caching

## Development Tips

1. **Check logs**: API logs to console in development mode
2. **Reload on changes**: Development server auto-reloads on code changes
3. **Use jq for formatting**: `curl ... | jq .`
4. **Test pagination**: Try `per_page=1` to see pagination behavior
5. **Test filters**: Combine multiple filters to test AND logic

## Production Deployment

```bash
# Install dependencies
pip install -r requirements.txt -r api_requirements.txt

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export API_KEYS=key1,key2,key3

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## Troubleshooting

**Port already in use:**
```bash
# Change port in run_api.py or use environment variable
export DEV_PORT=5001
python run_api.py
```

**Module not found:**
```bash
# Make sure you're in the project root
cd /path/to/DigitalChild
python run_api.py
```

**No data returned:**
```bash
# Check that data files exist
ls data/metadata/metadata.json
ls data/scorecard/scorecard_main.xlsx

# If missing, run init script
python init_project.py
```

## Next Steps

- See `api/README.md` for complete API documentation (all 14 endpoints)
- See `.env.example` for configuration options
- Check test coverage: `pytest tests/api/ -v` (76 tests passing)
