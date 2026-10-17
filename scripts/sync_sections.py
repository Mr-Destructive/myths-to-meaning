#!/usr/bin/env python3
"""Ensure every top-level content section has an _index.md carrying the keys
the homepage card needs: title, weight, glyph, blurb.

Why this exists: the homepage derives its cards from the section tree, so a
section without an _index.md renders a bare, glyph-less card. Extracting a new
series from Substack creates the folder and posts but not the _index.md, so
this script closes that gap.

Idempotent and non-destructive: existing editorial content is never touched.
Only missing keys are appended, and a missing _index.md is created. Re-running
on a complete tree writes nothing.

Usage:
    python3 scripts/sync_sections.py            # report + fix
    python3 scripts/sync_sections.py --dry-run  # report only
"""
import os
import re
import sys
from collections import Counter

CONTENT = os.path.join(os.path.dirname(__file__), "..", "content")
KEYS = ("title", "weight", "glyph", "blurb")


def walk_mds(directory):
    """All .md paths beneath `directory`, at any depth.

    Recursive on purpose: Navratri nests every post under a year folder, so a
    shallow listdir finds nothing and the section looks empty.
    """
    for root, _, files in os.walk(directory):
        for f in sorted(files):
            if f.endswith(".md"):
                yield os.path.join(root, f)


def is_section(directory):
    """A section is a folder holding at least one post (recursively)."""
    return any(os.path.basename(p) != "_index.md" for p in walk_mds(directory))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def split_frontmatter(text):
    """-> (frontmatter lines, body). Tolerates a file with no frontmatter."""
    if not text.startswith("---"):
        return [], text
    end = text.find("\n---", 3)
    if end == -1:
        return [], text
    fm_block = text[3:end]
    body = text[end + 4:].lstrip("\n")
    return fm_block.split("\n"), body


def keys_present(fm_lines):
    return {m.group(1) for line in fm_lines
            if (m := re.match(r"^([a-z_]+):", line))}


def derive_title(section_dir):
    """Most common series_label in the section's posts, at any depth."""
    labels = Counter()
    for path in walk_mds(section_dir):
        if os.path.basename(path) == "_index.md":
            continue
        m = re.search(r'^series_label:\s*"([^"]+)"', read(path), re.M)
        if m:
            labels[m.group(1)] += 1
    return labels.most_common(1)[0][0] if labels else None


def existing_weight(section_dir):
    ipath = os.path.join(section_dir, "_index.md")
    if not os.path.exists(ipath):
        return None
    m = re.search(r"^weight:\s*(\d+)", read(ipath), re.M)
    return int(m.group(1)) if m else None


def main():
    dry = "--dry-run" in sys.argv
    croot = os.path.abspath(CONTENT)
    sections = sorted(
        d for d in os.listdir(croot)
        if not d.startswith("_")
        and os.path.isdir(os.path.join(croot, d))
        and is_section(os.path.join(croot, d))
    )

    # New sections must append after the highest existing weight, otherwise a
    # name that sorts early (ganesh-aarti) steals weight 1 and reshuffles the
    # homepage cards.
    weights = [w for w in (existing_weight(os.path.join(croot, s))
                           for s in sections) if w is not None]
    next_weight = (max(weights) + 1) if weights else 1

    print(f"{len(sections)} sections found\n")
    problems = 0

    for name in sections:
        sdir = os.path.join(croot, name)
        ipath = os.path.join(sdir, "_index.md")

        if os.path.exists(ipath):
            fm_lines, body = split_frontmatter(read(ipath))
            have = keys_present(fm_lines)
        else:
            fm_lines, body, have = [], "", set()
            title = derive_title(sdir)
            print(f"  ! {name}: no _index.md"
                  + (f' -> title would be "{title}"' if title else
                     " and no series_label to derive from"))
            problems += 1

        missing = [k for k in KEYS if k not in have]

        if os.path.exists(ipath) and not missing:
            print(f"  ok {name}: complete")
            continue

        if not os.path.exists(ipath):
            title = derive_title(sdir) or name.replace("-", " ").title()
            new_lines = [
                f'title: "{title}"',
                f"weight: {next_weight}",
                'glyph: ""',
                'blurb: ""',
            ]
            next_weight += 1
            out = "---\n" + "\n".join(new_lines) + "\n---\n\n" + body
            print(f"  + {name}: created _index.md (needs glyph + blurb)")
        else:
            additions = []
            if "weight" in missing:
                additions.append(f"weight: {next_weight}")
                next_weight += 1
            if "glyph" in missing:
                additions.append('glyph: ""')
            if "blurb" in missing:
                additions.append('blurb: ""')
            out = ("---\n" + "\n".join(fm_lines + additions)
                   + "\n---\n\n" + body)
            print(f"  ~ {name}: appended "
                  f"{', '.join(a.split(':')[0] for a in additions)}")

        if not dry:
            with open(ipath, "w", encoding="utf-8") as fh:
                fh.write(out)

    if problems and not dry:
        print(f"\n{problems} section(s) needed attention. "
              "Fill in glyph + blurb by hand: they are editorial.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
