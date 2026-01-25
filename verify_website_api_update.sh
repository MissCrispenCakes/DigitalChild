#!/bin/bash
# Website API Update Verification Script
# Checks that all website files mention the Flask REST API

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║       Website API Update Verification                           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $3"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $3"
        ((FAIL++))
    fi
}

echo "1. Checking Installation Guide..."
check_content "docs/website/getting-started/installation.md" "api_requirements.txt" "Installation guide mentions API dependencies"
check_content "docs/website/getting-started/installation.md" "Flask" "Installation guide mentions Flask"
check_content "docs/website/getting-started/installation.md" "Flask-CORS" "Installation guide mentions Flask-CORS"

echo ""
echo "2. Checking Quick Start Guide..."
check_content "docs/website/getting-started/quickstart.md" "Access Data via API" "Quick start has API access section"
check_content "docs/website/getting-started/quickstart.md" "run_api.py" "Quick start mentions run_api.py"
check_content "docs/website/getting-started/quickstart.md" "curl.*api/documents" "Quick start has API examples"
check_content "docs/website/getting-started/quickstart.md" "api/README.md" "Quick start links to API docs"

echo ""
echo "3. Checking LittleRainbowRights Project Page..."
check_content "docs/website/projects/littlerainbowrights/index.md" "Via REST API" "Project page mentions REST API"
check_content "docs/website/projects/littlerainbowrights/index.md" "requests.get.*api/scorecard" "Project page has API examples"
check_content "docs/website/projects/littlerainbowrights/index.md" "api/README.md" "Project page links to API docs"

echo ""
echo "4. Checking Scorecard Visualization Page..."
check_content "docs/website/scorecard/index.md" "Via REST API" "Scorecard page mentions REST API"
check_content "docs/website/scorecard/index.md" "run_api.py" "Scorecard page shows how to start API"
check_content "docs/website/scorecard/index.md" "curl.*api/scorecard" "Scorecard page has API examples"
check_content "docs/website/scorecard/index.md" "API for programmatic access.*COMPLETE" "Scorecard marks API as complete in future enhancements"

echo ""
echo "5. Checking Main Website Index..."
check_content "docs/website/index.md" "Access via API" "Main index mentions API access"
check_content "docs/website/index.md" "REST API" "Main index mentions REST API in features"
check_content "docs/website/index.md" "9 endpoints" "Main index mentions 9 endpoints"
check_content "docs/website/index.md" "api/README.md" "Main index links to API docs"

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    Verification Results                         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Passed: ${GREEN}${PASS}${NC}"
echo -e "Failed: ${RED}${FAIL}${NC}"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}✅ All website API updates verified!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please review above.${NC}"
    exit 1
fi
