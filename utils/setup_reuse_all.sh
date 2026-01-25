#!/bin/bash
# Master script to set up complete REUSE compliance

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════"
echo "  REUSE Compliance Setup for DigitalChild"
echo "════════════════════════════════════════════════════════════"
echo ""

# Check if we're in the right directory
if [ ! -f "pipeline_runner.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Parse arguments
DRY_RUN=""
if [ "$1" = "--dry-run" ]; then
    DRY_RUN="--dry-run"
    echo "🔎 DRY RUN MODE - No files will be modified"
    echo ""
fi

# Step 1: Set up REUSE structure
echo "Step 1/3: Setting up REUSE structure..."
echo "─────────────────────────────────────────────────────────────"
python3 utils/setup_reuse.py
echo ""

# Step 2: Add SPDX headers to Python files
echo "Step 2/3: Adding SPDX headers to Python files..."
echo "─────────────────────────────────────────────────────────────"
python3 utils/add_spdx_headers.py $DRY_RUN
echo ""

# Step 3: Update CSV export functions
echo "Step 3/3: Adding licenses to CSV export footers..."
echo "─────────────────────────────────────────────────────────────"
python3 utils/update_csv_licenses.py $DRY_RUN
echo ""

# Final summary
echo "════════════════════════════════════════════════════════════"
if [ -n "$DRY_RUN" ]; then
    echo "  ✅ DRY RUN COMPLETE"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "No files were modified. Review the output above, then run:"
    echo "  bash utils/setup_reuse_all.sh"
    echo ""
    echo "to apply all changes."
else
    echo "  ✅ REUSE COMPLIANCE SETUP COMPLETE"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "📋 Next steps:"
    echo ""
    echo "1. Install REUSE tool to validate compliance:"
    echo "   pip install reuse"
    echo ""
    echo "2. Run REUSE linter to check for issues:"
    echo "   reuse lint"
    echo ""
    echo "3. Add REUSE badge to README.md:"
    echo "   [![REUSE status](https://api.reuse.software/badge/github.com/MissCrispenCakes/DigitalChild)](https://api.reuse.software/info/github.com/MissCrispenCakes/DigitalChild)"
    echo ""
    echo "4. Review changes and commit:"
    echo "   git status"
    echo "   git add -A"
    echo "   git commit -m 'Add REUSE compliance (SPDX headers, LICENSES/ directory)'"
    echo ""
    echo "5. Push to GitHub:"
    echo "   git push"
    echo ""
fi
echo "════════════════════════════════════════════════════════════"
