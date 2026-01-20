# ISO Mapping

This document defines how ISO codes (country and region) are mapped in the pipeline.

______________________________________________________________________

## Countries

- **ISO 3166-1 alpha-2** codes are stored in metadata.
- Example:
  - Kenya → `KE`
  - Nigeria → `NG`
  - South Africa → `ZA`

______________________________________________________________________

## Regions

- Regions are normalized but `_raw` values are preserved.
- Example normalization:
  - `Sub-Saharan Africa` → `Africa`
  - `SSA` → `Africa`
  - `North Africa` → `Africa`
  - `Middle East and North Africa` → `MENA`

______________________________________________________________________

## Metadata Fields

- `country`: normalized country name
- `country_raw`: as extracted
- `country_iso`: ISO alpha-2 code (future extension)
- `region`: normalized region
- `region_raw`: original region string
