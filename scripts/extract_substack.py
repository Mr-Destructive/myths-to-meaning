#!/usr/bin/env python3
"""
Extract all Mythology to Meaning posts from Substack -> Markdown files.

Substack's /api/v1/posts/* endpoints are locked down, but every post page
embeds a <script id="preloads-json"> containing the full post object
(including body_html). We scrape that, strip Substack chrome, and convert
the clean HTML to GitHub-flavoured Markdown via pandoc.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE, "data", "raw-html")
OUT_ROOT = os.path.join(BASE, "content")

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Substack chrome we never want in the exported markdown.
BOILERPLATE_SELECTORS = [
    ".button-wrapper",
    ".captioned-button-wrap",
    ".subscription-widget-wrap-editor",
    ".subscription-widget",
    ".subscribe-widget",
    ".post-ufi",
    ".caption",
    "[data-component-name='ButtonCreateButton']",
    "[data-component-name='CaptionedButtonToDOM']",
    "[data-component-name='SubscribeWidgetToDOM']",
]


def fetch(url, retries=4, timeout=45):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed {url}: {last}")


def get_post(slug):
    """Fetch a post page and pull the full post object out of preloads-json."""
    url = f"https://mythstomeaning.substack.com/p/{slug}"
    html = fetch(url)
    m = re.search(r'<script[^>]*id="preloads-json"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        raise RuntimeError(f"no preloads-json for {slug}")
    data = json.loads(m.group(1))
    post = data.get("post")
    if not post or not post.get("body_html"):
        raise RuntimeError(f"empty post for {slug}")
    return post


def html_to_markdown(body_html):
    """Strip Substack widgets then convert clean HTML -> GFM markdown."""
    soup = BeautifulSoup(body_html, "html.parser")

    for sel in BOILERPLATE_SELECTORS:
        for node in soup.select(sel):
            node.decompose()

    # Substack wraps section dividers as <div><hr></div>; keep the rule but
    # drop the redundant wrapper so pandoc emits a clean thematic break.
    for div in soup.find_all("div"):
        if div.find("hr", recursive=False) and len(div.contents) == 1:
            div.unwrap()

    clean = str(soup)
    if not clean.strip():
        return ""

    proc = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"],
        input=clean, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"pandoc failed: {proc.stderr[:400]}")

    md = proc.stdout
    md = re.sub(r"\n{3,}", "\n\n", md)          # collapse blank runs
    return md.strip() + "\n"


def classify(post):
    """Derive series / part metadata from slug + date."""
    slug = post["slug"]
    date = (post.get("post_date") or "")[:10]
    year_from_date = date[:4] if date else None

    if "mahishasur" in slug:
        series, label = "mahishasura-mardini", "Mahishasura Mardini Stotram"
        m = re.search(r"verse-(\d+)", slug)
        return dict(series=series, series_label=label,
                    verse=int(m.group(1)) if m else None,
                    day=None, year=None)

    if "shiv-tandav" in slug:
        series, label = "shiv-tandav", "Shiv Tandav Stotram"
        m = re.search(r"verse-(\d+)", slug)
        return dict(series=series, series_label=label,
                    verse=int(m.group(1)) if m else None,
                    day=None, year=None)

    if "navratri" in slug:
        label = "Navratri"
        m_day = re.search(r"day-(\d+)", slug)
        m_year = re.search(r"(?:navratri|day)-?(\d{4})", slug)
        year = int(m_year.group(1)) if m_year else (
            int(year_from_date) if year_from_date else None)
        return dict(series="navratri", series_label=label, verse=None,
                    day=int(m_day.group(1)) if m_day else None, year=year)

    return dict(series="misc", series_label="Mythology to Meaning",
                verse=None, day=None, year=None)


def slugify(text):
    text = (text or "").lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text).strip("-")


def emit(post, md, meta):
    series = meta["series"]
    title = post.get("title") or post["slug"]
    subtitle = (post.get("subtitle") or "").strip()
    cover = post.get("cover_image") or ""

    # Human-friendly part label, e.g. "Verse 7", "Day 3".
    if meta["verse"]:
        part = f"Verse {meta['verse']}"
    elif meta["day"]:
        part = f"Day {meta['day']}"
    else:
        part = ""

    date = (post.get("post_date") or "")[:10]

    tags = ["mythology", series]
    if meta["verse"]:
        tags.append(f"verse-{meta['verse']}")
    if meta["day"]:
        tags.append(f"day-{meta['day']}")
    if meta["year"]:
        tags.append(str(meta["year"]))

    fm = {
        "title": title,
        "subtitle": subtitle,
        "date": date,
        "slug": post["slug"],
        "series": series,
        "series_label": meta["series_label"],
        "verse": meta["verse"],
        "day": meta["day"],
        "year": meta["year"],
        "part": part,
        "cover_image": cover,
        "substack_url": post.get("canonical_url")
            or f"https://mythstomeaning.substack.com/p/{post['slug']}",
        "original_id": post.get("id"),
        "draft": False,
        "tags": tags,
    }

    def y(v):
        if v is None:
            return "null"
        if isinstance(v, str):
            return json.dumps(v)
        return str(v)

    header = "---\n" + "".join(f"{k}: {y(v)}\n" for k, v in fm.items()) + "---\n\n"

    if series == "navratri" and meta["year"]:
        outdir = os.path.join(OUT_ROOT, "navratri", str(meta["year"]))
    else:
        outdir = os.path.join(OUT_ROOT, series)
    os.makedirs(outdir, exist_ok=True)

    fname = f"{meta['verse']:02d}.md" if meta["verse"] else (
        f"day-{meta['day']:02d}.md" if meta["day"] else f"{post['slug']}.md")
    path = os.path.join(outdir, fname)

    with open(path, "w", encoding="utf-8") as f:
        f.write(header + md)
    return path


def work(item):
    slug = item["slug"]
    raw_path = os.path.join(RAW_DIR, f"{slug}.html")
    try:
        if os.path.exists(raw_path) and os.path.getsize(raw_path) > 2000:
            html = open(raw_path, encoding="utf-8").read()
            m = re.search(r'<script[^>]*id="preloads-json"[^>]*>(.*?)</script>',
                          html, re.S)
            post = json.loads(m.group(1))["post"]
        else:
            post = get_post(slug)
        md = html_to_markdown(post["body_html"])
        meta = classify(post)
        path = emit(post, md, meta)
        return (slug, "ok", path, len(md))
    except Exception as e:  # noqa: BLE001
        return (slug, "ERR", str(e)[:200], 0)


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    posts = json.load(open(os.path.join(BASE, "data", "all_posts.json")))
    print(f"extracting {len(posts)} posts ...")

    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(work, p): p["slug"] for p in posts}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            flag = "  ok " if r[1] == "ok" else " ERR "
            print(f"[{flag}] {r[0]:55} {r[2] if r[1]!='ok' else r[3]}")

    ok = [r for r in results if r[1] == "ok"]
    err = [r for r in results if r[1] != "ok"]
    print(f"\n== {len(ok)} ok, {len(err)} errors ==")
    for e in err:
        print("  ERR:", e[0], e[2])
    json.dump(results, open(os.path.join(BASE, "data", "extract-report.json"), "w"),
              indent=2)


if __name__ == "__main__":
    main()
