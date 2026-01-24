# Scorecard Data Files

This directory contains the primary scorecard data files used for the LittleRainbowRights/GRIMdata project.

## Primary Files

### `scorecard_main.xlsx` ⭐ CANONICAL

- **Purpose:** Main scorecard data (source of truth for all pipeline operations)
- **Date:** January 22, 2026 (last updated)
- **Structure:** 7 sheets (UN_194, SADC, ECOWAS, Global, Sheet1, Sheet5, Sheet2)
- **Content:**
  - 194 countries with 10 indicators
  - Color-coded regional groups (North Africa, ECOWAS)
  - Calculated indices (protection_index, Risk_index)
  - Regional analysis sheets for SADC (16 countries) and ECOWAS (13 countries)
- **Use this for:** Primary data analysis, generating reports, updating indicators
- **Pipeline reads from:** `data/scorecard/scorecard_main.xlsx`
- **Convenience copy:** `scorecard.xlsx` (root directory, for quick reference)

### `Global_QueerAI_Child_Scorecard_MASTER.xlsx`

- **Purpose:** Clean visualization version
- **Date:** September 9, 2025 (pre-conference)
- **Structure:** 5 sheets (Scorecard, Heatmap, Coverage, Sources, Legend)
- **Content:** Core data without source URLs, plus metadata sheets
- **Use this for:** Generating heatmaps, checking data coverage, understanding scoring rules

### `_GLOBAL_Policy_Matrix_UPR_Main_FINAL.xlsx`

- **Purpose:** Source verification and validation workflow
- **Date:** September 9, 2025
- **Structure:** 1 sheet with verification tracking columns
- **Content:** Source URLs organized by category, verification process steps
- **Use this for:** Validating sources, updating URLs, tracking verification status

## Data Schema

All files track these 10 indicators:

1. AI_Policy_Status
1. Data_Protection_Law
1. Children_Data_Safeguards
1. SOGI_Sensitive_Data
1. DPA_Independence
1. DPIA_Required_High_Risk_AI
1. LGBTQ_Legal_Status
1. Promotion_Propaganda_Offences
1. COP_Strategy
1. SIM_Biometric_ID_Linkage

## Related Files

- Exported CSVs: `data/exports/scorecard_*.csv`
- Archived versions: `data/archive/scorecard_main*.xlsx`
- Conference presentation: `presentations/QUEERAI.pdf`

## Data Updates

When updating scorecard data:

1. Edit `data/scorecard/scorecard_main.xlsx` (canonical source - 4 sheets: UN_194, SADC, ECOWAS, Global)
1. Verify sources using `_GLOBAL_Policy_Matrix_UPR_Main_FINAL.xlsx`
1. Update visualizations using `Global_QueerAI_Child_Scorecard_MASTER.xlsx`
1. Run multi-format export:
   ```bash
   python utils/export_scorecard_formats.py
   ```
   This generates convenience copies in root (UN_194 sheet only):
   - `scorecard.xlsx` (Excel format)
   - `scorecard.ods` (OpenDocument for LibreOffice)
   - `scorecard.csv` (CSV for maximum compatibility)
   - `scorecard.gsheet.json` (Google Sheets upload instructions)
1. Run pipeline to export new CSVs to `data/exports/`:
   ```bash
   python pipeline_runner.py --mode scorecard --scorecard-action export
   ```

## Citation

If using this data, cite:

- Vollmer, DT and Vollmer, SC. (2025). Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa. Presented at the Second International Conference on Children's Rights, Stellenbosch, South Africa, September 9-11, 2025.
