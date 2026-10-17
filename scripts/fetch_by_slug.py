#!/usr/bin/env python3
"""
Fetch posts directly by slug from their public page URL.

The Substack /api/v1/archive listing silently omits some published posts, and
/api/v1/posts/by-slug 404s for every slug. Scraping the page itself is the only
reliable method — every published post embeds its full body in a
<script id="preloads-json"> block.

Usage:
    python3 fetch_by_slug.py shiv-tandav-stotram-verse-8 shiv-tandav-stotram-verse-9

Adds each to data/all_posts.json (if absent) and caches the raw page under
data/raw-html/ so extract_substack.py picks it up from cache.
"""
import json, os, re, sys, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw-html")
LIST = os.path.join(BASE, "data", "all_posts.json")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

os.makedirs(RAW, exist_ok=True)
posts = json.load(open(LIST))
known = {p["slug"] for p in posts}

for slug in sys.argv[1:]:
    url = f"https://mythstomeaning.substack.com/p/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")

    m = re.search(r'<script[^>]*id="preloads-json"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        print(f"  !! no preloads-json on page for {slug}")
        continue
    post = json.loads(m.group(1)).get("post")
    if not post or not post.get("body_html"):
        print(f"  !! empty body for {slug}")
        continue

    # cache the raw page so the extractor reuses it
    open(os.path.join(RAW, f"{slug}.html"), "w", encoding="utf-8").write(html)

    if slug in known:
        print(f"  = {slug} already in list (page cached)")
        continue

    posts.append({
        "id": post["id"], "title": post.get("title"), "slug": post["slug"],
        "post_date": post.get("post_date"), "subtitle": post.get("subtitle"),
        "cover_image": post.get("cover_image"),
        "canonical_url": post.get("canonical_url") or url,
        "wordcount": post.get("wordcount"), "audience": post.get("audience"),
    })
    print(f"  + added {slug}  ({post.get('post_date','')[:10]}, "
          f"{len(post['body_html'])} chars body)")

posts.sort(key=lambda p: p.get("post_date") or "")
json.dump(posts, open(LIST, "w"), indent=1)
print(f"\nlist now has {len(posts)} posts")
