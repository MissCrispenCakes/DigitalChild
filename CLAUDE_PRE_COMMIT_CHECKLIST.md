# CLAUDE PRE-COMMIT CHECKLIST

**CRITICAL: READ THIS BEFORE EVERY COMMIT TO AVOID WASTING USER'S MONEY AND TIME**

## Before EVERY commit, run these checks:

### 1. pre-commit hooks (MANDATORY)

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

### 2. If you modified any scrapers or processors, run tests

```bash
pytest tests/ -v
```

## Common mistakes to avoid:

1. **Forgetting to stage workflow file changes** - Always check git status
2. **Pushing without verifying pre-commit passes** - CI will fail and waste time/money
3. **Missing end-of-file newlines** - pre-commit will catch this

## Workflow before any git push:

1. Run pre-commit hooks
2. If pre-commit fails, fix it
3. Stage all changes: `git add .`
4. Commit with clear message
5. THEN push

## Remember:

- Every CI failure costs the user money
- Every failed push wastes the user's time
- CHECK BEFORE YOU PUSH
- pre-commit catches: black, isort, flake8, markdownlint, and basic file issues
