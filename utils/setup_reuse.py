#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Set Up REUSE Compliance Structure

This script:
1. Creates LICENSES/ directory with official license texts
2. Creates .reuse/dep5 file for bulk license declarations
3. Updates CSV export functions to include license information

Usage:
    python utils/setup_reuse.py
"""

import os


def create_licenses_directory():
    """Download official SPDX license texts"""
    print("📁 Creating LICENSES/ directory...")

    os.makedirs("LICENSES", exist_ok=True)

    # MIT license text
    mit_text = """MIT License

Copyright (c) 2025 GRIMdata / LittleRainbowRights

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    # Write MIT license
    with open("LICENSES/MIT.txt", "w", encoding="utf-8") as f:
        f.write(mit_text)
    print("   ✅ Created LICENSES/MIT.txt")

    # For CC-BY-4.0, we'll use our existing LICENSE-DATA content
    print("   📋 Copying CC-BY-4.0 from LICENSE-DATA...")
    if os.path.exists("LICENSE-DATA"):
        with open("LICENSE-DATA", "r", encoding="utf-8") as f:
            cc_content = f.read()
        with open("LICENSES/CC-BY-4.0.txt", "w", encoding="utf-8") as f:
            f.write(cc_content)
        print("   ✅ Created LICENSES/CC-BY-4.0.txt")
    else:
        print("   ⚠️  LICENSE-DATA not found, skipping CC-BY-4.0")


def create_dep5_file():
    """Create .reuse/dep5 file for bulk declarations"""
    print("\n📄 Creating .reuse/dep5 file...")

    os.makedirs(".reuse", exist_ok=True)

    dep5_content = """Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: DigitalChild
Upstream-Contact: GRIMdata <https://github.com/MissCrispenCakes/DigitalChild>
Source: https://github.com/MissCrispenCakes/DigitalChild

# Documentation
Files: docs/* *.md
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC-BY-4.0

# Configuration files (data/metadata)
Files: configs/* data/metadata/* data/exports/*
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC-BY-4.0

# Scorecard data
Files: scorecard*.xlsx data/scorecard/*
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC-BY-4.0

# Presentation files
Files: presentations/*
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC-BY-4.0

# Raw scraped data (public domain sources)
Files: data/raw/*
Copyright: Various (see source URLs in metadata)
License: CC0-1.0

# GitHub Actions workflows
Files: .github/*
Copyright: 2025 GRIMdata / LittleRainbowRights
License: MIT

# Pre-commit and git configuration
Files: .pre-commit-config.yaml .gitignore .gitattributes
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC0-1.0

# Requirements files
Files: *requirements.txt requirements/*.txt
Copyright: 2025 GRIMdata / LittleRainbowRights
License: MIT

# Test fixtures and data
Files: tests/fixtures/*
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC-BY-4.0

# CI/CD and build files
Files: pytest.ini setup.py setup.cfg pyproject.toml
Copyright: 2025 GRIMdata / LittleRainbowRights
License: MIT

# MkDocs site configuration
Files: mkdocs.yml docs/overrides/* docs/website/stylesheets/* docs/website/javascripts/*
Copyright: 2025 GRIMdata / LittleRainbowRights
License: MIT

# Citation and metadata
Files: CITATION.cff zenodo.json
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC-BY-4.0

# Zenodo badge and DOI
Files: .zenodo.json
Copyright: 2025 GRIMdata / LittleRainbowRights
License: CC0-1.0
"""

    with open(".reuse/dep5", "w", encoding="utf-8") as f:
        f.write(dep5_content)

    print("   ✅ Created .reuse/dep5")


def update_gitignore():
    """Update .gitignore to exclude REUSE cache"""
    print("\n📝 Updating .gitignore...")

    gitignore_additions = """
# REUSE compliance
.reuse/
"""

    if os.path.exists(".gitignore"):
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()

        if ".reuse/" not in content:
            with open(".gitignore", "a", encoding="utf-8") as f:
                f.write(gitignore_additions)
            print("   ✅ Added .reuse/ to .gitignore")
        else:
            print("   ⏭️  .gitignore already has .reuse/ entry")
    else:
        print("   ⚠️  .gitignore not found")


def show_next_steps():
    """Display next steps for the user"""
    print("\n" + "=" * 60)
    print("✅ REUSE structure created successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("\n1. Add SPDX headers to Python files:")
    print("   python utils/add_spdx_headers.py --dry-run  # Preview")
    print("   python utils/add_spdx_headers.py            # Apply")
    print("\n2. Install REUSE tool to validate:")
    print("   pip install reuse")
    print("   reuse lint")
    print("\n3. Add REUSE badge to README.md:")
    print(
        "   [![REUSE status](https://api.reuse.software/badge/github.com/MissCrispenCakes/DigitalChild)](https://api.reuse.software/info/github.com/MissCrispenCakes/DigitalChild)"
    )
    print("\n4. Commit changes:")
    print("   git add LICENSES/ .reuse/ .gitignore")
    print("   git commit -m 'Add REUSE compliance structure'")
    print("\n" + "=" * 60)


def main():
    print("🚀 Setting up REUSE compliance structure...\n")

    create_licenses_directory()
    create_dep5_file()
    update_gitignore()
    show_next_steps()


if __name__ == "__main__":
    main()
