# mdformat Exclusions

These files are excluded from mdformat checks in CI because they use formatting features that mdformat doesn't support well, but which improve readability.

## Excluded Files

### Grid Card Files (5 files)

Use `---` horizontal rules inside list items for visual card separation. mdformat rejects this syntax.

- `docs/index.md`
- `docs/getting-started/quickstart.md`
- `docs/projects/littlerainbowrights/index.md`
- `docs/projects/sgbv/index.md`
- `docs/scorecard/index.md`

### Admonition Files (3 files)

Use indented content inside admonitions for better readability. mdformat wants unindented content (less readable).

- `docs/getting-started/installation.md`
- `docs/RESEARCH_CONTEXT.md`
- `docs/scorecard/explorer.md`

## Why Exclude?

**Readability > Strict Formatting**

mdformat's handling of these features produces less readable output:
- Removes visual card separators
- Unindents admonition content (harder to parse)
- Mangles code fences inside admonitions

We prioritize human readability over automated formatting consistency for these files.

## How It Works

The CI workflow (`..github/workflows/ci.yml`) uses `find` with `! -path` to skip these files during mdformat checks. All other markdown files are still validated.
