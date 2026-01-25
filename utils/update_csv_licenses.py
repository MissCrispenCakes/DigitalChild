#!/usr/bin/env python3
"""
Update CSV Export Functions to Include License Headers

This script updates CSV export functions to include SPDX license information
in their footers for REUSE compliance.

Usage:
    python utils/update_csv_licenses.py --dry-run  # Preview changes
    python utils/update_csv_licenses.py            # Apply changes
"""

import argparse
import os
import re


def find_csv_export_functions():
    """Find Python files with CSV export functionality"""
    files_with_csv = []

    # Known files that export CSVs
    csv_files = [
        "processors/tags_summary.py",
        "processors/scorecard_export.py",
        "processors/comparison_export.py",
    ]

    for filepath in csv_files:
        if os.path.exists(filepath):
            files_with_csv.append(filepath)

    return files_with_csv


def has_license_in_footer(content):
    """Check if CSV footer already has license information"""
    return "SPDX-License-Identifier" in content or "License: CC BY 4.0" in content


def add_license_to_csv_footer(filepath, dry_run=False):
    """Add license information to CSV footer"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has license
    if has_license_in_footer(content):
        return False, "Already has license in footer"

    # Find the footer section
    # Pattern: csvfile.write or writer.writerow followed by comments
    footer_pattern = r'(csvfile\.write\(["\']\\n# Project:)'

    if not re.search(footer_pattern, content):
        return False, "No standard footer found"

    # Add license lines before the Project line
    license_lines = (
        '        csvfile.write("# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights\\n")\n'
        '        csvfile.write("# SPDX-License-Identifier: CC-BY-4.0\\n")\n'
        '        csvfile.write("\\n")\n'
    )

    # Insert license lines before the footer
    new_content = re.sub(
        r"(\s+)(# Branding footer\n)",
        r"\1# License header\n" + license_lines + r"\1\2",
        content,
    )

    # If that didn't work, try alternative pattern
    if new_content == content:
        new_content = re.sub(
            r'(\s+)(csvfile\.write\(["\']\\n# Project:)',
            r"\1# License header\n" + license_lines + r"\1\2",
            content,
        )

    if new_content == content:
        return False, "Could not insert license lines"

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return True, "Added CC-BY-4.0 license to CSV footer"


def main():
    parser = argparse.ArgumentParser(
        description="Add license information to CSV export footers"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    args = parser.parse_args()

    print("🔍 Finding CSV export functions...")
    csv_files = find_csv_export_functions()
    print(f"Found {len(csv_files)} files with CSV exports\n")

    if args.dry_run:
        print("🔎 DRY RUN MODE - No files will be modified\n")

    modified_count = 0
    skipped_count = 0

    for filepath in csv_files:
        modified, message = add_license_to_csv_footer(filepath, dry_run=args.dry_run)

        if modified:
            modified_count += 1
            status = "✅ WOULD ADD" if args.dry_run else "✅ ADDED"
            print(f"{status}: {filepath}")
            print(f"   → {message}")
        else:
            skipped_count += 1
            print(f"⏭️  SKIP: {filepath}")
            print(f"   → {message}")

    print("\n" + "=" * 60)
    if args.dry_run:
        print("📊 Summary (DRY RUN):")
        print(f"   • {modified_count} files would be modified")
        print(f"   • {skipped_count} files would be skipped")
        print("\n💡 Run without --dry-run to apply changes")
    else:
        print("📊 Summary:")
        print(f"   • {modified_count} files modified")
        print(f"   • {skipped_count} files skipped")
        print("\n✅ License headers added to CSV exports!")


if __name__ == "__main__":
    main()
