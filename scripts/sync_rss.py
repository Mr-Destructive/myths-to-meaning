#!/usr/bin/env python3
"""Pull new posts from the Substack RSS feed into content/.

Run daily by .github/workflows/sync-substack.yml. Discovers which posts are new
by diffing the feed's slugs against what already exists in content/, then pulls
only those.

Architecture note: the feed's <content:encoded> is byte-identical to the
body_html we scrape off each post page (verified empirically), so the feed is
authoritative for body text. We still fetch the individual page for *new* posts
only, because the page carries cover_image and the exact subtitle, which the
feed omits. That is one or two page fetches per run, not sixty, so it stays
well inside rate limits.

Unknown series are handled rather than dumped into "misc": a slug we cannot
classify gets its own section derived from the slug prefix, and sync_sections.py
creates that section's _index.md. glyph + blurb stay empty because they are
editorial and cannot be invented -- the run reports them as needing attention.

Reuse over duplication: html_to_markdown, classify and emit come from
extract_substack, so new posts are converted identically to the original 63.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_substack import classify, emit, get_post, html_to_markdown  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(BASE, "content")
FEED = "https://mythstomeaning.substack.com/feed"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def fetch(url, retries=4, timeout=45):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed {url}: {last}")


def feed_slugs():
    """-> [(slug, title)] newest first, straight from the RSS feed."""
    root = ET.fromstring(fetch(FEED))
    out = []
    for item in root.iter("item"):
        link = (item.findtext("link") or "").strip()
        if "/p/" not in link:
            continue
        slug = link.rsplit("/p/", 1)[-1].split("?")[0].strip("/")
        title = (item.findtext("title") or "").strip()
        out.append((slug, title))
    return out


def existing_slugs():
    """Every slug already present in content/, from frontmatter."""
    have = set()
    for root, _, files in os.walk(CONTENT):
        for fn in files:
            if not fn.endswith(".md") or fn == "_index.md":
                continue
            p = os.path.join(root, fn)
            m = re.search(r'^slug:\s*"(.*)"\s*$',
                          open(p, encoding="utf-8").read(), re.M)
            if m:
                have.add(m.group(1))
    return have


def classify_fallback(post):
    """Same as extract_substack.classify, but unknown slugs get a real section.

    The base version routes anything unrecognised to "misc", which would pile
    unrelated posts into one bucket and never surface a card. Here we derive a
    section from the slug prefix so a brand-new series appears on the homepage
    on its own.
    """
    meta = classify(post)
    if meta["series"] != "misc":
        return meta

    slug = post["slug"]
    base = re.sub(r"-(verse|day)-?\d+$", "", slug)
    base = re.sub(r"-\d{4}$", "", base)
    base = re.sub(r"-\d+$", "", base).strip("-")
    if not base:
        base = "misc"

    label = base.replace("-", " ").title()
    m_day = re.search(r"day-(\d+)", slug)
    m_verse = re.search(r"verse-(\d+)", slug)
    year = re.search(r"(20\d{2})", slug)
    return dict(
        series=base,
        series_label=label,
        verse=int(m_verse.group(1)) if m_verse else None,
        day=int(m_day.group(1)) if m_day else None,
        year=int(year.group(1)) if year else None,
    )


def main():
    dry = "--dry-run" in sys.argv
    feed = feed_slugs()
    if not feed:
        print("feed returned no items -- refusing to touch anything")
        return 1

    # Guard: the feed only carries the 20 most recent posts. If the OLDEST item
    # in the feed is also unknown to us, we have fallen behind the window and a
    # plain diff would silently drop the gap.
    oldest_known = feed[-1][0] in existing_slugs()
    have = existing_slugs()
    new = [(s, t) for s, t in feed if s not in have]

    print(f"feed: {len(feed)} items | already have: {len(feed) - len(new)} "
          f"| new: {len(new)}")
    if not oldest_known:
        print("  ! oldest feed item is NOT local -- you may be behind the "
              "20-item window. Run scripts/extract_substack.py for a full "
              "backfill.")

    if not new:
        print("nothing to do")
        return 0

    added, flagged = [], []
    for slug, title in new:
        if dry:
            print(f"  would add: {slug}")
            continue
        try:
            post = get_post(slug)                     # proven page path
            meta = classify_fallback(post)
            md = html_to_markdown(post["body_html"])
            path = emit(post, md, meta)
            added.append((slug, meta["series"], path))
            print(f"  + {slug:52} -> {path.replace(BASE + os.sep, '')}")
            time.sleep(1.5)                           # be polite
        except Exception as e:  # noqa: BLE001
            print(f"  ERR {slug}: {e}")
            return 1

    if dry:
        return 0

    # Create / top up section _index.md for anything new (incl. new sections).
    subprocess.run([sys.executable,
                    os.path.join(BASE, "scripts", "sync_sections.py")],
                   check=False)

    # emit() writes no `url:`, so permalinks would be missing and the post
    # would never render. add_urls.py adds clean url: frontmatter, with a
    # fallback pattern for sections it does not know about.
    subprocess.run([sys.executable,
                    os.path.join(BASE, "scripts", "add_urls.py")],
                   check=False)

    # Report sections whose editorial keys are still empty.
    for _, series, _ in added:
        ip = os.path.join(CONTENT, series, "_index.md")
        if os.path.exists(ip):
            body = open(ip, encoding="utf-8").read()
            if 'glyph: ""' in body or 'blurb: ""' in body:
                flagged.append(series)

    print(f"\n== {len(added)} post(s) added ==")
    for s in {a[1] for a in added}:
        print(f"   section: {s}")
    if flagged:
        print(f"\n!! needs editorial glyph + blurb: {', '.join(sorted(set(flagged)))}")
        print("   cards render without them, but a phrase would look better.")

    # Machine-readable summary for the workflow's commit message / step summary.
    json.dump(
        {"added": [a[0] for a in added],
         "sections": sorted({a[1] for a in added}),
         "needs_editorial": sorted(set(flagged))},
        open(os.path.join(BASE, "data", "sync-report.json"), "w"), indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
