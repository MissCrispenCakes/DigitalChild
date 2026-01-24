#!/usr/bin/env python3
"""
Export Scorecard to Multiple Formats
-------------------------------------
Exports the UN_194 sheet from canonical scorecard to multiple formats
for cross-platform compatibility.

Usage:
    python utils/export_scorecard_formats.py
"""

import json
import os
from datetime import datetime

import pandas as pd


def export_scorecard_formats(
    canonical_path="data/scorecard/scorecard_main.xlsx",
    output_dir=".",
    sheet_name="UN_194",
):
    """
    Export scorecard UN_194 sheet to multiple formats.

    Args:
        canonical_path: Path to canonical scorecard file
        output_dir: Directory for output files (default: root)
        sheet_name: Sheet to export (default: UN_194)
    """
    print(f"Reading canonical scorecard from: {canonical_path}")
    print(f"Exporting sheet: {sheet_name}")

    # Read the UN_194 sheet
    df = pd.read_excel(canonical_path, sheet_name=sheet_name)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # 1. Excel format (.xlsx)
    xlsx_path = os.path.join(output_dir, "scorecard.xlsx")
    df.to_excel(xlsx_path, sheet_name=sheet_name, index=False, engine="openpyxl")
    print(f"✓ Exported Excel: {xlsx_path}")

    # 2. OpenDocument format (.ods) for LibreOffice
    ods_path = os.path.join(output_dir, "scorecard.ods")
    df.to_excel(ods_path, sheet_name=sheet_name, index=False, engine="odf")
    print(f"✓ Exported OpenDocument: {ods_path}")

    # 3. Google Sheets metadata file
    gsheet_path = os.path.join(output_dir, "scorecard.gsheet.json")
    gsheet_meta = {
        "format": "Google Sheets",
        "source": canonical_path,
        "sheet": sheet_name,
        "exported": datetime.now().isoformat(),
        "rows": len(df),
        "columns": len(df.columns),
        "instructions": {
            "upload": [
                "1. Go to https://sheets.google.com",
                "2. File → Import → Upload",
                "3. Select scorecard.xlsx or scorecard.ods",
                "4. Choose 'Replace spreadsheet' or 'Create new'",
            ],
            "api": [
                "Use Google Sheets API v4 to upload programmatically",
                "See: https://developers.google.com/sheets/api/guides/create",
            ],
        },
        "data_preview": {
            "countries": int(len(df)),
            "indicators": [
                col for col in df.columns if "_Source" not in col and col != "Country"
            ][:10],
        },
    }

    with open(gsheet_path, "w", encoding="utf-8") as f:
        json.dump(gsheet_meta, f, indent=2)
    print(f"✓ Exported Google Sheets metadata: {gsheet_path}")

    # 4. CSV for maximum compatibility
    csv_path = os.path.join(output_dir, "scorecard.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"✓ Exported CSV: {csv_path}")

    print("\n✅ All formats exported successfully!")
    print(f"   - Excel (.xlsx): {xlsx_path}")
    print(f"   - OpenDocument (.ods): {ods_path}")
    print(f"   - Google Sheets (.gsheet.json): {gsheet_path}")
    print(f"   - CSV (.csv): {csv_path}")

    return {
        "xlsx": xlsx_path,
        "ods": ods_path,
        "gsheet": gsheet_path,
        "csv": csv_path,
    }


if __name__ == "__main__":
    export_scorecard_formats()
