#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Add SPDX License Headers to Python Files

This script adds SPDX-FileCopyrightText and SPDX-License-Identifier headers
to all Python files in the project for REUSE compliance.

Usage:
    python utils/add_spdx_headers.py --dry-run  # Preview changes
    python utils/add_spdx_headers.py            # Apply changes
"""

import argparse
import os


def get_python_files(root_dir="."):
    """Find all Python files in the project"""
    excluded_dirs = {
        ".LittleRainbow",
        "venv",
        "env",
        ".venv",
        "site-packages",
        "__pycache__",
        ".pytest_cache",
        "htmlcov",
        "build",
        "dist",
        ".git",
        "digitalchild_api.egg-info",
    }

    python_files = []
    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from search
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                python_files.append(filepath)

    return sorted(python_files)


def has_spdx_header(content):
    """Check if file already has SPDX headers"""
    return "SPDX-License-Identifier:" in content or "SPDX-FileCopyrightText:" in content


def determine_license(filepath):
    """Determine which license applies to this file"""
    # API files are MIT (code)
    if filepath.startswith("api/"):
        return "MIT"

    # Processors, scrapers, utils are MIT (code)
    if any(
        filepath.startswith(prefix)
        for prefix in ["processors/", "scrapers/", "utils/", "tests/"]
    ):
        return "MIT"

    # Main Python files are MIT
    if filepath in [
        "pipeline_runner.py",
        "init_project.py",
        "setup.py",
        "run_api.py",
        "wsgi.py",
    ]:
        return "MIT"

    # Everything else defaults to MIT (code)
    return "MIT"


def add_spdx_header(filepath, dry_run=False):
    """Add SPDX header to a Python file"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has SPDX header
    if has_spdx_header(content):
        return False, "Already has SPDX header"

    license_id = determine_license(filepath)

    # Create SPDX header
    # REUSE-IgnoreStart
    spdx_header = (
        "# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights\n"
        f"# SPDX-License-Identifier: {license_id}\n"
        "\n"
    )
    # REUSE-IgnoreEnd

    # Handle shebang lines
    if content.startswith("#!"):
        lines = content.split("\n", 1)
        shebang = lines[0] + "\n"
        rest = lines[1] if len(lines) > 1 else ""
        new_content = shebang + spdx_header + rest
    else:
        new_content = spdx_header + content

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return True, f"Added {license_id} header"


def main():
    parser = argparse.ArgumentParser(
        description="Add SPDX headers to Python files for REUSE compliance"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to search (default: current directory)",
    )
    args = parser.parse_args()

    print("🔍 Finding Python files...")
    python_files = get_python_files(args.root)
    print(f"Found {len(python_files)} Python files\n")

    if args.dry_run:
        print("🔎 DRY RUN MODE - No files will be modified\n")

    modified_count = 0
    skipped_count = 0

    for filepath in python_files:
        modified, message = add_spdx_header(filepath, dry_run=args.dry_run)

        if modified:
            modified_count += 1
            status = "✅ WOULD ADD" if args.dry_run else "✅ ADDED"
            print(f"{status}: {filepath}")
            print(f"   → {message}")
        else:
            skipped_count += 1
            if args.dry_run or modified_count + skipped_count <= 10:
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
        print("\n✅ SPDX headers added successfully!")


if __name__ == "__main__":
    main()
