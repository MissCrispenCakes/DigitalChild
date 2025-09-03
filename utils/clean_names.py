import os, re, json

# Input files
input_files = {
    "acerwc": "../data/acerwc_links_found.txt",
    "achpr": "../data/achpr_links_found.txt",
    "au_treaty": "../data/au_treaty_links_found.txt",
    "ohchr": "../data/ohchr_links_found.txt",
    "unicef": "../data/unicef_links_found.txt",
    "upr": "../data/upr_links_found.txt",
}

EXCLUDE_PATTERNS = [
    "facebook.com", "twitter.com", "linkedin.com", "instagram.com", "youtube.com",
    "donate", "about", "contact", "careers", "privacy", "terms", "javascript:void", "#"
]

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text

def build_url_dict(label, filepath):
    urls_dict = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            # Extract only the URL part (strip pre-text like "[no text] → ...")
            url = None
            if "http" in line:
                url = line[line.find("http"):].strip()
            if not url:
                continue
            if any(p in url for p in EXCLUDE_PATTERNS):
                continue
            # Try to build key from any pre-text before URL
            pre_text = line[:line.find("http")].strip(" -→\u2192") if "http" in line else ""
            key_base = None
            if pre_text and not pre_text.lower().startswith("[no text]"):
                key_base = slugify(pre_text)
            if not key_base:
                # fallback to URL slug
                slug = os.path.basename(url).split("?")[0]
                if not slug:
                    parts = url.strip("/").split("/")
                    slug = parts[-1] if parts else f"{label}_{i}"
                key_base = slugify(slug)
            key = f"{label}_{key_base}"
            if key in urls_dict:
                key = f"{key}_{i}"
            urls_dict[key] = url
    return urls_dict

# Build dicts and save them
output_files = {}
for label, filepath in input_files.items():
    urls_dict = build_url_dict(label, filepath)
    outpath = f"/mnt/data/urls_dict_{label}.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(urls_dict, f, indent=2)
    output_files[label] = outpath

output_files
