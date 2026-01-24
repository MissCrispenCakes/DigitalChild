"""
One-off utility script for generating URL dictionaries from direct links.

This script reads URLs from configs/direct_links_main.txt and generates
Python dictionary code with cleaned keys based on domain and path.

NOTE: This is a standalone utility script with hard-coded relative paths.
It is not part of the main pipeline and is intended for manual, one-time use
during URL dictionary preparation.
"""

import os
from urllib.parse import urlparse

URLS = {}

with open("configs/direct_links_main.txt", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        url = line.strip()
        if not url:
            continue

        # Extract last path segment
        path = urlparse(url).path
        name = os.path.basename(path)

        # If no filename, use domain + segment
        if not name:
            parts = path.strip("/").split("/")
            name = "_".join(parts[-2:]) if len(parts) > 1 else parts[-1]

        # Clean name
        if not name:
            name = f"link_{i}"
        name = name.lower().replace("-", "_").replace(".", "_")

        # Add prefix for clarity (optional)
        domain = urlparse(url).netloc.split(".")[0]
        key = f"{domain}_{name}"

        URLS[key] = url

print("URLS = {")
for k, v in URLS.items():
    print(f'    "{k}": "{v}",')
print("}")
