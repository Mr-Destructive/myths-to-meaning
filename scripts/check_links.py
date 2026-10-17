#!/usr/bin/env python3
"""Fail if the built site contains broken internal links or missing assets.

Run by build-deploy.yml before publishing, so a malformed frontmatter key or a
template typo can never ship. Also usable locally:

    python3 scripts/check_links.py public

Handles both quoting styles. This matters: `hugo --minify` strips attribute
quotes (href=/navratri/ rather than href="/navratri/"), so a checker that only
regexes the quoted form matches zero links on production output and passes
vacuously -- which is exactly the bug this script replaced.

Rules:
  * external URLs, fragments, mailto/data/javascript are skipped
  * query strings are stripped before resolving
  * root-relative (/x) resolves from the output root; relative (x) from the
    page's own directory
  * a path ending in / must contain index.html; otherwise it must be a file
"""
import os
import re
import sys
from html import unescape as entity_unescape

# href=/src= in any of the three quoting styles a minifier may leave behind.
ATTR = re.compile(r"\b(?:href|src)=(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))")
SKIP = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", re.I)


def normalize(raw):
    """Un-entity an attribute value and trim it to a bare URL.

    Post bodies embedded in RSS arrive entity-escaped, so a capture can begin
    with an encoded quote and drag trailing markup behind the URL
    (href=&#34;https://en.wikipedia.org/...&#34;&gt;Shiv). Read naively that
    external link becomes a bogus internal path and the check reports
    phantom breakage -- it did, on 86 links, before this existed.
    """
    val = entity_unescape(raw).strip().lstrip("\"'")
    return re.split(r'[\s>"\']', val, 1)[0]


def find_broken(outdir):
    broken = []
    checked = 0
    pages = 0

    for root, _, files in os.walk(outdir):
        for fn in files:
            if not fn.endswith((".html", ".xml")):
                continue
            page = os.path.join(root, fn)
            pages += 1
            text = open(page, encoding="utf-8", errors="replace").read()

            for m in ATTR.finditer(text):
                raw = next(g for g in m.groups() if g is not None)
                if not raw:
                    continue
                path = normalize(raw)
                if not path or SKIP.match(path):
                    continue
                path = path.split("#", 1)[0].split("?", 1)[0]
                if not path:
                    continue
                # hugo server injects /livereload.js into its dev copy of the
                # output dir; it never exists in a real build, so it is a
                # dev-server artifact rather than breakage.
                if path == "/livereload.js":
                    continue

                if path.startswith("/"):
                    target = os.path.join(outdir, path.lstrip("/"))
                else:
                    target = os.path.normpath(
                        os.path.join(os.path.dirname(page), path))

                checked += 1
                if path.endswith("/"):
                    ok = os.path.isfile(os.path.join(target, "index.html"))
                else:
                    ok = os.path.exists(target)
                if not ok:
                    broken.append((page, raw))

    return broken, checked, pages


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "public"
    if not os.path.isdir(outdir):
        print(f"no such output directory: {outdir}")
        return 1

    broken, checked, pages = find_broken(outdir)
    if broken:
        print(f"BROKEN LINKS: {len(broken)} of {checked} checked "
              f"(scanned {pages} pages)")
        for page, href in broken[:25]:
            print(f"  {os.path.relpath(page, outdir)} -> {href}")
        if len(broken) > 25:
            print(f"  ... and {len(broken) - 25} more")
        return 1

    print(f"links OK: {checked} internal references across {pages} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
