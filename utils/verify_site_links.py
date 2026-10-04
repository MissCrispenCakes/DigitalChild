"""Check a built MkDocs site's local links/assets and optional old anchor inventory."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    """Collect link targets, IDs, and the public content's anchor IDs."""

    def __init__(self, path):
        super().__init__()
        self.links = []
        self.ids = set()
        self.article_ids = set()
        self.in_article = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.in_article = True
        anchor = attrs.get("id") or (attrs.get("name") if tag == "a" else None)
        if anchor:
            self.ids.add(anchor)
            if self.in_article:
                self.article_ids.add(anchor)
        target = attrs.get("href") if tag in {"a", "link"} else attrs.get("src")
        if target:
            self.links.append(target)

    def handle_endtag(self, tag):
        if tag == "article":
            self.in_article = False


def verify(site, origin, baseline=None):
    """Return errors; an optional baseline enforces public route/anchor survival."""
    pages = {p.relative_to(site): Page(p) for p in site.rglob("*.html")}
    errors = []
    checked = 0
    for path, page in pages.items():
        source = str(path)
        if source.endswith("index.html"):
            source = source[: -len("index.html")]
        base = origin.rstrip("/") + "/" + source
        for href in page.links:
            url = urlsplit(urljoin(base, href))
            if url.scheme not in {"http", "https"}:
                continue
            if url.netloc != urlsplit(origin).netloc:
                continue
            target = Path(unquote(url.path).lstrip("/") or ".")
            if (site / target).is_dir():
                target /= "index.html"
            checked += 1
            if not (site / target).is_file():
                errors.append(f"{path}: missing target {href}")
            elif url.fragment and target in pages:
                if unquote(url.fragment) not in pages[target].ids:
                    errors.append(f"{path}: missing anchor {href}")
    if baseline:
        for previous in baseline.rglob("*.html"):
            path = previous.relative_to(baseline)
            if path not in pages:
                errors.append(f"Lost existing route: {path}")
                continue
            removed = Page(previous).article_ids - pages[path].article_ids
            for anchor in sorted(removed):
                errors.append(f"Lost existing content anchor: {path}#{anchor}")
    print(f"Verified {len(pages)} HTML pages and {checked} local links/assets.")
    for error in errors:
        print(error)
    return errors


def main():
    """Run as a repository build verification command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, nargs="?", default=Path("site"))
    parser.add_argument("--origin", default="https://grimdata.org")
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    raise SystemExit(bool(verify(args.site, args.origin, args.baseline)))


if __name__ == "__main__":
    main()
