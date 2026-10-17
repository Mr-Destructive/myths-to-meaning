# Mythology to Meaning

Static port of [mythstomeaning.substack.com](https://mythstomeaning.substack.com/) →
**myths-to-meaning.meetgor.com**, built with Hugo.

## Content inventory

All **63 posts** on the Substack were extracted. They fall into exactly three series:

| Series | Parts | Notes |
|---|---|---|
| **Mahishasura Mardini Stotram** | 21 verses + 1 intro | `/mahishasura-mardini/verse-1…21`, `/stotram` — complete |
| **Shiv Tandav Stotram** | 17 verses | `/shiv-tandav/verse-1…17` — complete |
| **Navratri** | 24 posts | 2024 (9) · 2025 (9) · 2026 (6, series still publishing) |

> Mahishasura Mardini (21×1) and Shiv Tandav (17) are both **complete**.
> Navratri is 24 of the "9×3" — the 2026 cycle is mid-publish (6 of 9 days live;
> days 7–9 don't exist yet and will appear when re-run after publication).

## Pipeline

```
scripts/extract_substack.py   Substack → markdown (data/raw-html → content/)
scripts/fetch_by_slug.py      fetch specific posts by page URL (see note below)
scripts/add_urls.py           adds clean `url:` frontmatter per post
scripts/make_designs.py       regenerates the 5 design previews in designs/
content/                      extracted markdown, grouped by series
themes/myth/                  the Hugo theme ("Palm-leaf Scripture")
designs/                      5 self-contained design concepts + gallery
public/                       build output (gitignored)
```

### How extraction works
Substack's API is unreliable for this publication:
- `/api/v1/archive` builds the post list but **silently omits** some published posts
  (it dropped Shiv Tandav verses 8 & 9 — present on the site, absent from the feed).
- `/api/v1/posts/by-slug` returns `404` for **every** slug, including ones that exist.

The only reliable method is scraping the page itself, which embeds the full post
object (including `body_html`) in a `<script id="preloads-json">` block. The
extractor uses that, strips Substack chrome (share/subscribe buttons, comment
prompts), and converts the clean HTML → GFM via `pandoc`. Devanagari,
transliteration and nested word-by-word lists survive intact.

Because the archive feed can under-report, validate the list by checking date
continuity — both stotras were published daily, so any gap means a missing post.

Fetch specific posts directly when the feed misses them:

```bash
python3 scripts/fetch_by_slug.py shiv-tandav-stotram-verse-8 shiv-tandav-stotram-verse-9
```

Re-run any time the source publishes more:

```bash
python3 scripts/extract_substack.py   # needs data/all_posts.json (archive listing)
python3 scripts/add_urls.py
hugo --gc --minify
```

## Designs

`designs/index.html` is a gallery of 5 concepts, each rendered with **real verse
content** so they can be judged on the text they actually have to carry:

1. **Palm-leaf Scripture** — aged cream paper, saffron + vermilion, ruled panels *(currently implemented as the live theme)*
2. **Yajna / Vedic Fire** — burnt orange, maroon, gold; fire-glow, drop caps
3. **Devalaya / Temple Night** — dark lamp-lit temple, gold-leaf type, mandala watermark
4. **Raag / Mughal Folio** — ivory in a painted ruby–gold–peacock frame, jewel tones
5. **Pattachitra / Folk Scroll** — bold folk art, ochre, thick black outlines

The live theme is #1. To switch, port the chosen preview's `:root` palette and
component rules into `themes/myth/assets/css/main.css`.

## Deploy

`baseURL` in `hugo.toml` is already set to `https://myths-to-meaning.meetgor.com/`.
Publish the `public/` directory to any static host (Netlify, Vercel, GitHub Pages,
or the same pipeline you use for meetgor.com). Add a CNAME/DNS record pointing
`myths-to-meaning.meetgor.com` at the host.
