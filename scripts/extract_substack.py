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
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE, "data", "raw-html")
OUT_ROOT = os.path.join(BASE, "content")

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Substack's edge 403s requests from cloud-provider IP ranges (GitHub Actions
# runners live in exactly such a range) no matter how browser-like the headers
# are. When direct fetch is blocked we fall back in order to: curl_cffi, which
# replays Chrome's exact TLS + HTTP/2 fingerprint; then public CORS relays
# that fetch server-side from a different IP pool. Everything crossing these
# hops is a public feed and public post pages -- no credentials, no private
# data.
RELAYS = (
    "https://api.allorigins.win/raw?url={q}",
    "https://api.codetabs.com/v1/proxy?quest={q}",
)

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


def _direct(url, timeout):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _jina_via_urllib(url, respond_with, timeout):
    headers = {"User-Agent": UA}
    if respond_with:
        headers["x-respond-with"] = respond_with
    req = urllib.request.Request(f"https://r.jina.ai/{url}", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _jina_via_curl(url, respond_with, timeout):
    cmd = ["curl", "-sS", "--max-time", str(timeout)]
    if respond_with:
        cmd += ["-H", f"x-respond-with: {respond_with}"]
    cmd.append(f"https://r.jina.ai/{url}")
    p = subprocess.run(cmd, capture_output=True, text=True,
                       timeout=timeout + 15)
    if p.returncode != 0:
        raise RuntimeError(f"curl exit {p.returncode}: "
                           f"{p.stderr.strip()[:200]}")
    return p.stdout


def jina_fetch(url, respond_with=None, timeout=90):
    """Fetch through r.jina.ai, which has none of the IP problems above.

    Two modes, both verified against this publication:
    - respond_with="html": returns the raw document. Post pages keep their
      <script id="preloads-json"> intact, so get_post works unchanged.
    - default (markdown): renders the page. An RSS feed LOSES its <item>
      tags this way, but every post link survives in order, which is enough
      for slug discovery when the raw XML is unreachable.

    Jina fingerprints its clients: the identical request gets HTTP 403 through
    python-urllib and HTTP 200 through curl from the same IP (verified), so we
    speak through curl_cffi (Chrome TLS, present in CI) or the curl binary
    (present everywhere) before ever trying urllib.
    """
    errors = []
    try:
        from curl_cffi import requests as cffi  # optional dependency
        kw = {"headers": {"x-respond-with": respond_with}} if respond_with else {}
        r = cffi.get(f"https://r.jina.ai/{url}", impersonate="chrome",
                     timeout=timeout, **kw)
        r.raise_for_status()
        if r.text.strip():
            return r.text
        errors.append("curl_cffi: empty body")
    except Exception as e:  # noqa: BLE001
        errors.append(f"curl_cffi: {e}")

    try:
        body = _jina_via_curl(url, respond_with, timeout)
        if body.strip():
            return body
        errors.append("curl: empty body")
    except Exception as e:  # noqa: BLE001
        errors.append(f"curl: {e}")

    try:
        body = _jina_via_urllib(url, respond_with, timeout)
        if body.strip():
            return body
        errors.append("urllib: empty body")
    except Exception as e:  # noqa: BLE001
        errors.append(f"urllib: {e}")

    raise RuntimeError(f"jina unreachable ({'; '.join(errors)})")


def _curl_cffi(url, timeout):
    from curl_cffi import requests as cffi  # optional dependency

    r = cffi.get(url, impersonate="chrome", timeout=timeout)
    r.raise_for_status()
    return r.text


def _relay(url, template, timeout):
    proxied = template.format(q=urllib.parse.quote(url, safe=""))
    req = urllib.request.Request(proxied, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", "replace")
    if not body.strip():
        raise RuntimeError("relay returned empty body")
    return body


def _note(msg):
    print(f"[fetch] {msg}", file=sys.stderr, flush=True)


def fetch(url, retries=4, timeout=45, jina_html=False):
    """Fetch a URL, layered: direct -> curl_cffi -> jina -> public relays.

    Each layer logs why it gave up, so a CI log shows exactly which path
    served the bytes. Retry applies only to flaky errors (timeouts, 5xx);
    a 403/429 is a policy block and retrying from the same IP is wasted.

    jina_html=True adds the jina raw-HTML layer before the relays; use it
    for HTML documents (post pages), never for XML (jina renders feeds).
    """
    last = None
    for attempt in range(retries):
        try:
            return _direct(url, timeout)
        except urllib.error.HTTPError as e:
            last = e
            _note(f"direct: HTTP {e.code} for {url}")
            if e.code in (401, 403, 429):
                break
            time.sleep(1.5 * (attempt + 1))
        except Exception as e:  # noqa: BLE001
            last = e
            _note(f"direct: {e}")
            time.sleep(1.5 * (attempt + 1))

    try:
        body = _curl_cffi(url, timeout)
        _note("curl_cffi (Chrome TLS fingerprint) succeeded")
        return body
    except Exception as e:  # noqa: BLE001
        _note(f"curl_cffi unavailable/failed: {e}")
        last = e

    if jina_html:
        try:
            body = jina_fetch(url, "html", timeout)
            _note("jina raw-HTML relay succeeded")
            return body
        except Exception as e:  # noqa: BLE001
            _note(f"jina raw-HTML relay failed: {e}")
            last = e

    for template in RELAYS:
        host = template.split("/")[2]
        try:
            body = _relay(url, template, timeout)
            _note(f"relay {host} succeeded")
            return body
        except Exception as e:  # noqa: BLE001
            _note(f"relay {host} failed: {e}")
            last = e

    raise RuntimeError(f"failed {url}: {last}")


def get_post(slug):
    """Fetch a post page and pull the full post object out of preloads-json."""
    url = f"https://mythstomeaning.substack.com/p/{slug}"
    # jina_html=True: on blocked IPs the raw-HTML relay preserves the
    # preloads-json script byte-for-byte (verified), so extraction is identical.
    html = fetch(url, jina_html=True)
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
