# CLAUDE PRE-COMMIT CHECKLIST

**CRITICAL: READ THIS BEFORE EVERY COMMIT TO AVOID WASTING USER'S MONEY AND TIME**

## Before EVERY commit, run these checks:

### 1. mdformat check (MANDATORY - CI will fail if you skip this)

```bash
python -m mdformat --check README.md docs/
```

If this fails, run without --check to fix:

```bash
python -m mdformat README.md docs/
```

### 2. pre-commit hooks (MANDATORY)

```bash
pre-commit run --all-files
```

This checks:
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- markdownlint
- trailing whitespace
- end-of-file-fixer
- check-yaml
- check-json
- detect-private-key

### 3. If you modified any scrapers or processors, run tests

```bash
pytest tests/ -v
```

## Common mistakes to avoid:

1. **Adding extra blank lines in markdown** - mdformat enforces single blank lines after headers
2. **Forgetting to stage workflow file changes** - Always check git status
3. **Making trivial edits without checking format** - Even a single line change can break mdformat
4. **Pushing without verifying pre-commit passes** - CI will fail and waste time/money

## Workflow before any git push:

1. Run mdformat check
2. If mdformat fails, fix it
3. Run pre-commit hooks
4. If pre-commit fails, fix it
5. Stage all changes: `git add .`
6. Commit with clear message
7. THEN push

## Remember:

- Every CI failure costs the user money
- Every failed push wastes the user's time
- CHECK BEFORE YOU PUSH
- If you modified markdown, ALWAYS run mdformat first
