# Scorecard Data Files

This directory contains the primary scorecard data files used for the LittleRainbowRights/GRIMdata project.

## Primary Files

### `scorecard_main_presentation.xlsx` ⭐ CANONICAL
- **Purpose:** Main scorecard data used for conference presentation
- **Date:** September 13, 2025 (post-conference)
- **Structure:** 7 sheets (UN_194, SADC, ECOWAS, Global, Sheet1, Sheet5, Sheet2)
- **Content:** 
  - 194 countries with 10 indicators
  - Color-coded regional groups (North Africa, ECOWAS)
  - Calculated indices (protection_index, Risk_index)
  - Regional analysis sheets for SADC (16 countries) and ECOWAS (13 countries)
- **Use this for:** Primary data analysis, generating reports, updating indicators

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
2. Data_Protection_Law
3. Children_Data_Safeguards
4. SOGI_Sensitive_Data
5. DPA_Independence
6. DPIA_Required_High_Risk_AI
7. LGBTQ_Legal_Status
8. Promotion_Propaganda_Offences
9. COP_Strategy
10. SIM_Biometric_ID_Linkage

## Related Files

- Exported CSVs: `data/exports/scorecard_*.csv`
- Archived versions: `data/archive/scorecard_main*.xlsx`
- Conference presentation: `presentations/QUEERAI.pdf`

## Data Updates

When updating scorecard data:
1. Use `scorecard_main_presentation.xlsx` as the primary source
2. Verify sources using `_GLOBAL_Policy_Matrix_UPR_Main_FINAL.xlsx`
3. Update visualizations using `Global_QueerAI_Child_Scorecard_MASTER.xlsx`
4. Export new CSVs to `data/exports/`

## Citation

If using this data, cite:
- Vollmer, DT and Vollmer, SC. (2025). Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa. Presented at the Second International Conference on Children's Rights, Stellenbosch, South Africa, September 9-11, 2025.
