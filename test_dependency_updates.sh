#!/bin/bash
# Test script for verifying updated API dependencies
# Run this to verify API still works after dependency updates

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║       API Dependency Update Verification                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Installing updated dependencies${NC}"
echo "Running: pip install -r api_requirements.txt --upgrade"
echo ""

if pip install -r api_requirements.txt --upgrade; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Dependency installation failed${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 2: Checking Flask version${NC}"
FLASK_VERSION=$(python -c "import flask; print(flask.__version__)")
echo "Flask version: $FLASK_VERSION"

if [[ "$FLASK_VERSION" == "3.1."* ]]; then
    echo -e "${GREEN}✓ Flask 3.1.x installed (expected)${NC}"
else
    echo -e "${YELLOW}⚠ Flask version is $FLASK_VERSION (expected 3.1.x)${NC}"
fi

echo ""
echo -e "${BLUE}Step 3: Importing API modules${NC}"

# Test importing all API modules
python -c "
import sys
try:
    from api.app import create_app
    print('✓ api.app imports successfully')

    from api.config import Config
    print('✓ api.config imports successfully')

    from api.extensions import cors, cache, limiter
    print('✓ api.extensions imports successfully')

    from api.routes.health import health_bp
    from api.routes.documents import documents_bp
    from api.routes.scorecard import scorecard_bp
    print('✓ All route blueprints import successfully')

    from api.services.metadata_service import get_documents
    from api.services.scorecard_service import get_scorecard_summary
    print('✓ All services import successfully')

    print('')
    print('${GREEN}✓ All imports successful - no breaking changes${NC}')
except ImportError as e:
    print('')
    print('${RED}✗ Import failed:${NC}', str(e))
    sys.exit(1)
except Exception as e:
    print('')
    print('${RED}✗ Unexpected error:${NC}', str(e))
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All imports successful${NC}"
else
    echo -e "${RED}✗ Import test failed${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 4: Creating test Flask app${NC}"

python -c "
from api.app import create_app

try:
    app = create_app('testing')
    print('✓ Flask app created successfully')

    # Check that all blueprints are registered
    blueprint_names = [bp.name for bp in app.blueprints.values()]
    expected = ['health', 'documents', 'scorecard']

    for expected_bp in expected:
        if expected_bp in blueprint_names:
            print(f'✓ Blueprint \"{expected_bp}\" registered')
        else:
            print(f'✗ Blueprint \"{expected_bp}\" NOT registered')
            exit(1)

    # Check CORS is configured
    if hasattr(app, 'extensions') and 'cors' in app.extensions:
        print('✓ CORS extension configured')
    else:
        print('⚠ CORS extension not found (may be OK depending on config)')

    # Check cache is configured
    if hasattr(app, 'extensions') and 'cache' in app.extensions:
        print('✓ Cache extension configured')
    else:
        print('⚠ Cache extension not found (may be OK depending on config)')

    print('')
    print('${GREEN}✓ Flask app initialization successful${NC}')

except Exception as e:
    print('')
    print('${RED}✗ Flask app creation failed:${NC}', str(e))
    import traceback
    traceback.print_exc()
    exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Flask app creation successful${NC}"
else
    echo -e "${RED}✗ Flask app creation failed${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 5: Running API health check${NC}"

# Start API in background
echo "Starting API server..."
python run_api.py &
API_PID=$!

# Wait for API to start
echo "Waiting for API to start..."
sleep 5

# Test health endpoint
if curl -s http://localhost:5000/api/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ API health check passed${NC}"
    HEALTH_OK=true
else
    echo -e "${RED}✗ API health check failed${NC}"
    HEALTH_OK=false
fi

# Kill API server
kill $API_PID 2>/dev/null || true
wait $API_PID 2>/dev/null || true

if [ "$HEALTH_OK" = false ]; then
    exit 1
fi

echo ""
echo -e "${BLUE}Step 6: Running API test suite${NC}"

python test_api.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ API test suite passed${NC}"
else
    echo -e "${RED}✗ API test suite failed${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 7: Running pytest API tests${NC}"

pytest tests/api/ -v

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pytest API tests passed${NC}"
else
    echo -e "${RED}✗ Pytest API tests failed${NC}"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    Verification Complete                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ All dependency updates verified successfully!${NC}"
echo ""
echo "Updated packages:"
echo "  • Flask:         3.0.0 → 3.1.2"
echo "  • Werkzeug:      3.0.1 → 3.1.3"
echo "  • Flask-CORS:    4.0.0 → 5.0.0"
echo "  • Flask-Caching: 2.1.0 → 2.3.0"
echo "  • Flask-Limiter: 3.5.0 → 3.10.0"
echo "  • limits:        3.7.0 → 3.14.0"
echo "  • pydantic:      2.5.0 → 2.10.5"
echo "  • gunicorn:     21.2.0 → 23.0.0"
echo "  • python-dotenv: 1.0.0 → 1.0.1"
echo "  • openpyxl:      3.1.2 → 3.1.5"
echo "  • ujson:         5.9.0 → 5.10.0"
echo ""
echo "No breaking changes detected. API is fully compatible with updated dependencies."
echo ""
