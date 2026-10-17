#!/usr/bin/env python3
"""Add clean `url:` frontmatter to each extracted post for tidy permalinks."""
import os, re, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(BASE, "content")

def fm_field(text, key):
    m = re.search(rf'^{key}:\s*(.+)$', text, re.M)
    if not m: return None
    return m.group(1).strip().strip('"')

changed = 0
for root, _, files in os.walk(CONTENT):
    for fn in files:
        if not fn.endswith(".md") or fn.startswith("_index"):
            continue
        path = os.path.join(root, fn)
        text = open(path, encoding="utf-8").read()
        if re.search(r'^url:', text, re.M):
            continue
        series = fm_field(text, "series")
        verse  = fm_field(text, "verse")
        day    = fm_field(text, "day")
        year   = fm_field(text, "year")

        if series == "shiv-tandav" and verse and verse != "null":
            url = f"/shiv-tandav/verse-{verse}/"
        elif series == "mahishasura-mardini":
            url = (f"/mahishasura-mardini/verse-{verse}/"
                   if verse and verse != "null"
                   else "/mahishasura-mardini/stotram/")
        elif series == "navratri" and day and day != "null":
            url = f"/navratri/{year}/day-{int(day)}/"
        else:
            slug = fm_field(text, "slug") or fn[:-3]
            url = f"/{series}/{slug}/"

        text = re.sub(r'^(slug:.*)$', r'\1\nurl: "%s"' % url, text, count=1, flags=re.M)
        open(path, "w", encoding="utf-8").write(text)
        changed += 1

print(f"added url: to {changed} files")
