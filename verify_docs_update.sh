#!/bin/bash
# Documentation Update Verification Script
# Checks that all documentation has been consistently updated

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║       Documentation Update Verification                         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

check_file_exists() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} File exists: $1"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} File missing: $1"
        ((FAIL++))
    fi
}

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $3"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $3"
        ((FAIL++))
    fi
}

echo "1. Checking API Documentation Files..."
check_file_exists "api/README.md"
check_file_exists "api/QUICK_START.md"
check_file_exists "docs/API_WEEK1_SUMMARY.md"
check_file_exists "docs/API_WEEK2_SUMMARY.md"
check_file_exists "test_api.py"

echo ""
echo "2. Checking Main Documentation Updates..."
check_content "README.md" "Phase 4 In Progress" "README has Phase 4 status"
check_content "README.md" "Flask" "README mentions Flask"
check_content "docs/ROADMAP.md" "IN PROGRESS - 2/4" "ROADMAP shows Phase 4 progress"
check_content "CLAUDE.md" "Run API" "CLAUDE.md has API commands"

echo ""
echo "3. Checking Metric Updates..."
check_content "docs/ROADMAP.md" "209" "Test count updated to 209"
check_content "docs/ARCHITECTURE.md" "209" "Architecture test count updated"
check_content "docs/website/index.md" "209" "Website test count updated"
check_content "README.md" "18,000" "LOC updated in README or ROADMAP"

echo ""
echo "4. Checking API References..."
check_content "docs/DOCS_INDEX.md" "API Documentation" "DOCS_INDEX has API section"
check_content "docs/ARCHITECTURE.md" "API Layer" "ARCHITECTURE has API section"
check_content "README.md" "api/README" "README links to API docs"

echo ""
echo "5. Checking Consistency..."
# Check that Phase 4 is not marked as "PLANNED" anywhere
if grep -r "Phase 4.*PLANNED" docs/ROADMAP.md README.md 2>/dev/null; then
    echo -e "${RED}✗${NC} Phase 4 still marked as PLANNED somewhere"
    ((FAIL++))
else
    echo -e "${GREEN}✓${NC} Phase 4 no longer marked as PLANNED"
    ((PASS++))
fi

# Check that test count is consistent
TEST_COUNTS=$(grep -rh "170 tests\|209 tests" README.md docs/*.md CLAUDE.md 2>/dev/null | wc -l)
if [ "$TEST_COUNTS" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Test counts found in documentation"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC}  Warning: Test counts not prominently featured"
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
    echo -e "${GREEN}✅ All documentation updates verified!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please review above.${NC}"
    exit 1
fi
