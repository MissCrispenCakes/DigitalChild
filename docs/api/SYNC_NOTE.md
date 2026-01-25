# API Documentation Sync Note

## Dual Location

API documentation exists in two locations:

1. **`api/README.md`** and **`api/QUICK_START.md`** (root)
   - For developers cloning the repository
   - Part of the API codebase
   - Primary source of truth

2. **`docs/api/README.md`** and **`docs/api/QUICK_START.md`** (docs)
   - For MkDocs website build (grimdata.org)
   - **Copies** of the root files
   - Must be kept in sync

## Why Two Locations?

MkDocs only builds files from the `docs/` directory. Files in `api/` at the project root are not accessible to the website builder.

## Keeping Files in Sync

**When updating API documentation:**

```bash
# Edit the primary files
vim api/README.md
vim api/QUICK_START.md

# Copy to docs/ for website
cp api/README.md docs/api/
cp api/QUICK_START.md docs/api/

# Commit both
git add api/README.md api/QUICK_START.md docs/api/
git commit -m "Update API documentation"
git push
```

## Alternative: Automated Sync

Consider adding to `.github/workflows/sync-api-docs.yml`:

```yaml
name: Sync API Docs

on:
  push:
    paths:
      - 'api/README.md'
      - 'api/QUICK_START.md'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Copy API docs to docs/
        run: |
          cp api/README.md docs/api/
          cp api/QUICK_START.md docs/api/
      - name: Commit if changed
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add docs/api/
          git diff --quiet && git diff --staged --quiet || git commit -m "Sync API docs to docs/api/"
          git push
```

## Verification

After updating, verify both locations are in sync:

```bash
diff api/README.md docs/api/README.md
diff api/QUICK_START.md docs/api/QUICK_START.md
```

No output = files are identical ✓

---

**Last updated:** January 25, 2026
