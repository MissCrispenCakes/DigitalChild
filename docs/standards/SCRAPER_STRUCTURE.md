# Scraper Structure

This document defines how scrapers are organized in `scrapers/`.

---

## Location

- All scrapers live in `scrapers/`.
- Each source has its own file, e.g.:
  - `au_policy.py`
  - `ohchr.py`
  - `upr.py`
  - `unicef.py`
  - `acerwc.py`
  - `achpr.py`

---

## Structure of a Scraper

Each scraper must implement:

```python
def scrape():
    """
    Downloads raw documents into data/raw/<source>/
    Skips if file already exists.
    Returns list of file paths.
    """
```

---

## Example

```python
# scrapers/au_policy.py
RAW_DIR = "data/raw/au_policy"

def scrape():
    os.makedirs(RAW_DIR, exist_ok=True)
    for name, url in URLS.items():
        filename = os.path.join(RAW_DIR, f"{name}.pdf")
        if os.path.exists(filename):
            continue
        resp = requests.get(url, timeout=30)
        with open(filename, "wb") as f:
            f.write(resp.content)
```

---

## Notes

- Each scraper writes files to `data/raw/<source>/`.
- Manual documents can be placed in `data/raw/manual/`.
- Scrapers should log using `processors.logger.get_logger`.
