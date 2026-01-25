#!/bin/bash
# API Navigation Verification Script
# Verifies that API is discoverable across the website

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║       API Navigation & Discoverability Verification             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

check_file_exists() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} File exists: $1"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} File missing: $1"
        ((FAIL++))
    fi
}

echo -e "${BLUE}1. Navigation Structure${NC}"
check_content "mkdocs.yml" "API Reference:" "mkdocs.yml has API Reference navigation"
check_content "mkdocs.yml" "website/api-reference.md" "mkdocs.yml includes quick reference page"
check_content "mkdocs.yml" "api/README.md" "mkdocs.yml includes API overview"
check_content "mkdocs.yml" "api/QUICK_START.md" "mkdocs.yml includes API quick start"

echo ""
echo -e "${BLUE}2. Quick Reference Page${NC}"
check_file_exists "docs/website/api-reference.md"
check_content "docs/website/api-reference.md" "9 Endpoints" "Quick reference lists all endpoints"
check_content "docs/website/api-reference.md" "Quick Examples" "Quick reference has examples"
check_content "docs/website/api-reference.md" "Response Format" "Quick reference shows response formats"

echo ""
echo -e "${BLUE}3. Homepage Visibility${NC}"
check_content "docs/website/index.md" "NEW: REST API" "Homepage has API announcement callout"
check_content "docs/website/index.md" "Quick Links" "Homepage has Quick Links section"
check_content "docs/website/index.md" "API Quick Start" "Homepage has API Quick Start card"
check_content "docs/website/index.md" "api/README.md" "Homepage links to API docs"

echo ""
echo -e "${BLUE}4. Installation Guide${NC}"
check_content "docs/website/getting-started/installation.md" "Just want to access the data" "Installation has API alternative callout"
check_content "docs/website/getting-started/installation.md" "API Dependencies" "Installation lists API dependencies"
check_content "docs/website/getting-started/installation.md" "api_requirements.txt" "Installation mentions api_requirements.txt"
check_content "docs/website/getting-started/installation.md" "Flask" "Installation mentions Flask"

echo ""
echo -e "${BLUE}5. Quick Start Guide${NC}"
check_content "docs/website/getting-started/quickstart.md" "Fastest Way: Use the API" "Quick start has API callout"
check_content "docs/website/getting-started/quickstart.md" "python run_api.py" "Quick start shows how to run API"
check_content "docs/website/getting-started/quickstart.md" "curl.*api/documents" "Quick start has curl examples"

echo ""
echo -e "${BLUE}6. Project Overview${NC}"
check_content "docs/website/projects/littlerainbowrights/index.md" "Access via REST API" "Project page has API callout"
check_content "docs/website/projects/littlerainbowrights/index.md" "requests.get" "Project page has Python example"

echo ""
echo -e "${BLUE}7. Scorecard Page${NC}"
check_content "docs/website/scorecard/index.md" "Access Scorecard Data via API" "Scorecard has API callout"
check_content "docs/website/scorecard/index.md" "curl.*api/scorecard" "Scorecard has API examples"

echo ""
echo -e "${BLUE}8. Documentation Index${NC}"
check_content "docs/README.md" "REST API Documentation" "Docs README mentions API"
check_content "docs/README.md" "api/README.md" "Docs README links to API docs"
check_content "docs/README.md" "api-reference.md" "Docs README links to quick reference"

echo ""
echo -e "${BLUE}9. Main README${NC}"
check_content "README.md" "Using the API" "Main README has API section"
check_content "README.md" "python run_api.py" "Main README shows how to run API"
check_content "README.md" "9 endpoints available" "Main README lists endpoint count"
check_content "README.md" "api/README.md" "Main README links to API docs"

echo ""
echo -e "${BLUE}10. Cross-References${NC}"
# Count total mentions of API across website files
API_MENTIONS=$(grep -r "REST API\|api/README\|run_api.py" docs/website/ 2>/dev/null | wc -l)
if [ "$API_MENTIONS" -gt 20 ]; then
    echo -e "${GREEN}✓${NC} API mentioned $API_MENTIONS times across website (good discoverability)"
    ((PASS++))
else
    echo -e "${RED}✗${NC} API only mentioned $API_MENTIONS times (low discoverability)"
    ((FAIL++))
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    Verification Results                         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Passed: ${GREEN}${PASS}${NC}"
echo -e "Failed: ${RED}${FAIL}${NC}"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}✅ All navigation improvements verified!${NC}"
    echo ""
    echo -e "${BLUE}API is now discoverable from:${NC}"
    echo "  • Main navigation (top-level tab)"
    echo "  • Homepage (callout + Quick Links)"
    echo "  • Installation guide (alternative callout)"
    echo "  • Quick start guide (fastest path)"
    echo "  • Project pages (code examples)"
    echo "  • Scorecard page (data access)"
    echo "  • Documentation index"
    echo "  • Main README.md"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please review above.${NC}"
    exit 1
fi
