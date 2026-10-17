#!/usr/bin/env python3
"""
Generate 5 self-contained design previews for Mythology to Meaning.

Each preview embeds real extracted content (verse 1 of Shiv Tandav) so the
designs can be judged against the actual text they'll have to carry.

Outputs -> designs/design-<n>-<name>.html  + designs/index.html gallery.
"""
import os, re, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "designs")
os.makedirs(OUT, exist_ok=True)

# ---- real content -----------------------------------------------------------
src = open(os.path.join(BASE, "content", "shiv-tandav", "01.md"), encoding="utf-8").read()
body = re.sub(r"^---\n.*?\n---\n", "", src, flags=re.S).strip()
article_html = subprocess.run(
    ["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"],
    input=body, capture_output=True, text=True).stdout
# trim the reference list to keep previews focused
article_html = re.sub(r'<h2 id="references">.*?</ul>', '', article_html, flags=re.S)

TITLE = "Shiv Tandav Stotram: Verse 1"
SUB = ("Exploring and understanding the meaning of the first verse in the "
       "Shiv Tandav Stotram in detail, the spiritual and mythological meaning")

CARDS = [
    ("शिव", "Shiv Tandav Stotram",
     "17 verses on Shiva's cosmic dance — literal, mythological and spiritual readings.",
     "17 parts"),
    ("दुर्गा", "Mahishasura Mardini",
     "The 21-verse hymn to the Goddess who slew Mahishasura, verse by verse.",
     "22 parts"),
    ("नवरात्रि", "Navratri",
     "Nine nights, three years — one form of Maa a day, and the meaning she carries.",
     "24 parts"),
]

GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Spectral:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Tiro+Devanagari+Hindi:ital@0;1&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Yatra+One&family=Rozha+One&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">'
)


def cards_html(card_cls="card", glyph_cls="card-glyph"):
    out = []
    for glyph, title, blurb, meta in CARDS:
        out.append(
            f'<a class="{card_cls}" href="#"><span class="{glyph_cls}">{glyph}</span>'
            f'<h2 class="card-title">{title}</h2>'
            f'<p class="card-blurb">{blurb}</p>'
            f'<span class="card-meta">{meta} →</span></a>')
    return "\n".join(out)


GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' "
         "height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' "
         "baseFrequency='.82' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix "
         "type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='220' height='220' "
         "filter='url(%23n)' opacity='.34'/%3E%3C/svg%3E\")")


def page(css, svg=""):
    return f"""<!doctype html><html lang="en-in"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} — design preview</title>{GOOGLE_FONTS}
<style>{css}</style></head><body><div class="grain" aria-hidden="true"></div>{svg}
<header class="site-header"><div class="wrap">
  <a class="brand" href="#"><span class="brand-mark">ॐ</span>
  <span class="brand-text"><span class="brand-name">Mythology to Meaning</span>
  <span class="brand-sub">Stotras · Verses · Reflections</span></span></a>
  <nav class="site-nav"><a href="#">Home</a><a href="#" class="active">Shiv Tandav</a>
  <a href="#">Mahishasura Mardini</a><a href="#">Navratri</a></nav>
</div></header>

<main>
<section class="hero"><div class="wrap">
  <p class="hero-eyebrow">॥ जय माँ ॥</p>
  <h1 class="hero-title">Mythology to Meaning</h1>
  <p class="hero-sub">A journey through the vibrant tapestry of Hindu mythology and literature.</p>
</div></section>

<section class="wrap series-grid">
{cards_html()}
</section>

<article class="wrap article">
  <header class="article-head">
    <a class="eyebrow" href="#">Shiv Tandav Stotram · Verse 1</a>
    <h1 class="article-title">{TITLE}</h1>
    <p class="article-sub">{SUB}</p>
    <time class="article-date">4 November 2024</time>
  </header>
  <div class="prose">{article_html}</div>
  <nav class="series-nav">
    <span class="sn-link sn-empty"></span>
    <a class="sn-index" href="#">All 17</a>
    <a class="sn-link sn-next" href="#"><span class="sn-dir">Next →</span>
    <span class="sn-title">Verse 2</span></a>
  </nav>
</article>
</main>

<footer class="site-footer"><div class="wrap">
  <div class="foot-ornament">❊</div>
  <p class="foot-note">Ported with reverence from Mythology to Meaning.</p>
  <p class="foot-copy">© 2026 Meet</p>
</div></footer>
</body></html>"""


# =============================================================================
# DESIGN 1 — "Palm-leaf Scripture"
# Aged cream paper, saffron + vermilion ink, restrained ruled panels.
# =============================================================================
D1 = """
:root{--paper:#f4e4c1;--paper-edge:#e0c48f;--paper-deep:#ecd6a8;--ink:#3a2416;
--ink-soft:#6b4a2e;--ink-faint:#96724c;--saffron:#e8871e;--vermilion:#b3261e;
--gold:#b8860b;--maroon:#6e1414;--rule:rgba(110,20,20,.28);--rule-soft:rgba(58,36,22,.16);
--serif:"Spectral",Georgia,serif;--display:"Marcellus",serif;--deva:"Tiro Devanagari Hindi",serif;}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);
font-size:1.075rem;line-height:1.72;position:relative}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(ellipse 70% 55% at 12% 8%,rgba(255,244,214,.75),transparent 60%),
radial-gradient(ellipse 60% 50% at 88% 92%,rgba(196,150,84,.30),transparent 62%),
linear-gradient(105deg,var(--paper-edge),var(--paper) 22%,var(--paper-deep) 78%,var(--paper-edge))}
.grain{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.5;
mix-blend-mode:multiply;background-image:__GRAIN__}
.wrap{width:min(100% - 2*1.4rem,74rem);margin-inline:auto;position:relative;z-index:2}
.site-header{position:sticky;top:0;z-index:20;border-bottom:1px solid var(--rule);
background:linear-gradient(180deg,rgba(179,38,30,.06),transparent 70%)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;
gap:1rem;flex-wrap:wrap;padding-block:.85rem}
.brand{display:flex;align-items:center;gap:.7rem;text-decoration:none;color:inherit}
.brand-mark{font-family:var(--deva);font-size:1.9rem;color:var(--vermilion)}
.brand-text{display:flex;flex-direction:column;line-height:1.15}
.brand-name{font-family:var(--display);font-size:1.22rem;color:var(--maroon)}
.brand-sub{font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-faint)}
.site-nav{display:flex;gap:1.3rem;flex-wrap:wrap}
.site-nav a{text-decoration:none;color:var(--ink-soft);font-size:.84rem;
letter-spacing:.13em;text-transform:uppercase;padding-bottom:.2rem;border-bottom:2px solid transparent}
.site-nav a.active{color:var(--vermilion);border-bottom-color:var(--saffron)}
.hero{text-align:center;padding:3.5rem 0 2rem}
.hero-eyebrow{font-family:var(--deva);color:var(--vermilion);font-size:1.25rem;margin:0 0 .5rem}
.hero-title{font-family:var(--display);font-size:clamp(2.1rem,6vw,3.6rem);margin:0;color:var(--maroon)}
.hero-sub{max-width:34rem;margin:1rem auto 0;color:var(--ink-soft);font-style:italic}
.series-grid{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));margin-top:1rem}
.card{position:relative;display:block;text-decoration:none;color:inherit;padding:2rem 1.6rem 1.6rem;
background:linear-gradient(150deg,rgba(255,250,235,.6),rgba(232,196,143,.28));
border:1px solid var(--rule);border-radius:3px;box-shadow:0 2px 0 rgba(110,20,20,.08);
transition:transform .22s,border-color .22s;overflow:hidden}
.card::before{content:"";position:absolute;inset:8px;border:1px solid var(--rule-soft);pointer-events:none}
.card:hover{transform:translateY(-3px);border-color:var(--saffron)}
.card-glyph{font-family:var(--deva);display:block;font-size:2.5rem;color:var(--vermilion);margin-bottom:.5rem}
.card-title{font-family:var(--display);font-size:1.28rem;margin:0 0 .5rem;color:var(--maroon)}
.card-blurb{margin:0 0 1rem;font-size:.95rem;color:var(--ink-soft)}
.card-meta{font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--saffron)}
.article{padding:2rem 0}
.article-head{max-width:42rem;margin-inline:auto;padding-bottom:1.5rem}
.eyebrow{display:inline-block;text-decoration:none;font-size:.72rem;letter-spacing:.2em;
text-transform:uppercase;color:var(--vermilion);margin-bottom:.7rem}
.article-title{font-family:var(--display);font-size:clamp(1.7rem,4.4vw,2.65rem);margin:0;color:var(--maroon)}
.article-sub{margin:.8rem 0 0;color:var(--ink-soft);font-style:italic}
.article-date{display:block;margin-top:.9rem;font-size:.82rem;color:var(--ink-faint)}
.prose{max-width:42rem;margin-inline:auto}
.prose>*+*{margin-top:1.15em}
.prose h2{font-family:var(--display);font-size:1.5rem;color:var(--maroon);margin-top:2.4rem;
padding-top:1.2rem;border-top:1px solid var(--rule-soft)}
.prose a{color:var(--vermilion);text-decoration-color:rgba(179,38,30,.35)}
.prose strong{color:var(--maroon)}
.prose ul{padding-left:1.3rem}.prose li+li{margin-top:.4rem}.prose li::marker{color:var(--vermilion)}
.prose blockquote{margin:1.6rem 0;padding:1.1rem 1.4rem;
background:linear-gradient(135deg,rgba(255,250,235,.55),rgba(232,196,143,.25));
border-left:3px solid var(--saffron);box-shadow:inset 0 0 0 1px var(--rule-soft)}
.prose blockquote strong{font-family:var(--deva)}
.prose hr{border:0;height:1px;margin:2.2rem auto;width:60%;
background:linear-gradient(90deg,transparent,var(--rule),transparent)}
.series-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center;
max-width:42rem;margin:3rem auto 1rem;padding-top:1.6rem;border-top:1px solid var(--rule)}
.sn-link{text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.2rem}
.sn-next{text-align:right}
.sn-dir{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--vermilion)}
.sn-title{font-family:var(--display);font-size:.98rem;color:var(--maroon)}
.sn-empty{visibility:hidden}
.sn-index{text-decoration:none;font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;
color:var(--ink-faint);border:1px solid var(--rule);padding:.5rem .8rem;white-space:nowrap}
.site-footer{margin-top:4rem;padding:2.5rem 0 3rem;border-top:1px solid var(--rule);text-align:center}
.foot-ornament{color:var(--saffron);font-size:1.4rem;margin-bottom:.6rem}
.foot-note{margin:0 0 .4rem;color:var(--ink-soft);font-style:italic;font-size:.95rem}
.foot-copy{margin:0;font-size:.78rem;color:var(--ink-faint)}
"""

# =============================================================================
# DESIGN 2 — "Yajna / Vedic Fire"
# Deeper, warmer: burnt orange + deep maroon + gold, fire-glow, drop caps,
# heavier double-rule ornamentation.
# =============================================================================
D2 = """
:root{--paper:#f7e9d0;--paper-edge:#e8cfa4;--ink:#2e1a10;--ink-soft:#5c3a24;
--ink-faint:#8a6136;--fire:#d1481f;--ember:#a8300f;--gold:#c08a1e;--deep:#5c1210;
--rule:rgba(92,18,16,.32);--rule-soft:rgba(46,26,16,.15);
--serif:"Cormorant Garamond",Georgia,serif;--display:"Yatra One",serif;--deva:"Tiro Devanagari Hindi",serif;}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);
font-size:1.18rem;line-height:1.75;position:relative}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(ellipse 80% 60% at 50% -10%,rgba(209,72,31,.20),transparent 60%),
radial-gradient(circle at 50% 120%,rgba(168,48,15,.22),transparent 55%),
radial-gradient(circle at 8% 30%,rgba(209,72,31,.10),transparent 40%),
linear-gradient(180deg,#faeeda,var(--paper) 30%,#f2ddbd 100%)}
.grain{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.55;
mix-blend-mode:multiply;background-image:__GRAIN__}
.wrap{width:min(100% - 2*1.4rem,70rem);margin-inline:auto;position:relative;z-index:2}
.site-header{border-top:4px double var(--ember);border-bottom:4px double var(--ember);
background:linear-gradient(180deg,rgba(168,48,15,.10),transparent)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;
gap:1rem;flex-wrap:wrap;padding-block:1rem}
.brand{display:flex;align-items:center;gap:.8rem;text-decoration:none;color:inherit}
.brand-mark{font-family:var(--deva);font-size:2.2rem;color:var(--fire);
text-shadow:0 0 18px rgba(209,72,31,.5)}
.brand-text{display:flex;flex-direction:column;line-height:1.15}
.brand-name{font-family:var(--display);font-size:1.5rem;color:var(--deep);letter-spacing:.01em}
.brand-sub{font-size:.66rem;letter-spacing:.28em;text-transform:uppercase;color:var(--ink-faint)}
.site-nav{display:flex;gap:1.6rem;flex-wrap:wrap}
.site-nav a{text-decoration:none;color:var(--ink-soft);font-family:var(--display);
font-size:.98rem;letter-spacing:.05em;padding:.2rem 0;border-bottom:2px solid transparent}
.site-nav a.active{color:var(--ember);border-bottom-color:var(--gold)}
.hero{text-align:center;padding:4rem 0 2.5rem;
border-bottom:1px solid var(--rule-soft)}
.hero-eyebrow{font-family:var(--deva);color:var(--fire);font-size:1.5rem;margin:0 0 .6rem;
text-shadow:0 0 14px rgba(209,72,31,.35)}
.hero-title{font-family:var(--display);font-size:clamp(2.4rem,7vw,4.2rem);margin:0;
color:var(--deep);letter-spacing:.02em;line-height:1.1}
.hero-sub{max-width:36rem;margin:1.1rem auto 0;color:var(--ink-soft);font-style:italic;font-size:1.2rem}
.hero::after{content:"ॐ";display:block;font-family:var(--deva);color:var(--gold);
font-size:1.6rem;margin-top:1.4rem}
.series-grid{display:grid;gap:1.8rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));
margin-top:2.5rem}
.card{position:relative;display:block;text-decoration:none;color:inherit;padding:2.3rem 1.7rem 1.8rem;
background:linear-gradient(160deg,rgba(255,246,228,.75),rgba(232,207,164,.4));
border:1px solid var(--rule);box-shadow:0 3px 0 rgba(92,18,16,.14),0 16px 30px -22px rgba(46,26,16,.7);
transition:transform .22s,box-shadow .22s;overflow:hidden}
.card::before{content:"";position:absolute;inset:9px;border:2px solid var(--rule-soft);pointer-events:none}
.card::after{content:"";position:absolute;top:0;left:0;right:0;height:4px;
background:linear-gradient(90deg,var(--ember),var(--gold),var(--ember))}
.card:hover{transform:translateY(-4px);box-shadow:0 6px 0 rgba(92,18,16,.2),0 24px 40px -22px rgba(46,26,16,.8)}
.card-glyph{font-family:var(--deva);display:block;font-size:2.8rem;color:var(--fire);margin-bottom:.5rem}
.card-title{font-family:var(--display);font-size:1.45rem;margin:0 0 .5rem;color:var(--deep)}
.card-blurb{margin:0 0 1.1rem;font-size:1.02rem;color:var(--ink-soft)}
.card-meta{font-size:.76rem;letter-spacing:.2em;text-transform:uppercase;color:var(--ember);font-weight:600}
.article{padding:3rem 0}
.article-head{max-width:40rem;margin-inline:auto;padding-bottom:1.8rem;text-align:center}
.eyebrow{display:inline-block;text-decoration:none;font-family:var(--display);font-size:.9rem;
letter-spacing:.16em;text-transform:uppercase;color:var(--ember);margin-bottom:.8rem}
.article-title{font-family:var(--display);font-size:clamp(1.9rem,5vw,3rem);margin:0;color:var(--deep);line-height:1.15}
.article-sub{margin:.9rem auto 0;max-width:34rem;color:var(--ink-soft);font-style:italic;font-size:1.12rem}
.article-date{display:block;margin-top:1rem;font-size:.85rem;color:var(--ink-faint);letter-spacing:.1em}
.prose{max-width:40rem;margin-inline:auto}
.prose>*+*{margin-top:1.25em}
.prose>p:first-of-type::first-letter{float:left;font-family:var(--display);font-size:3.6rem;
line-height:.85;padding:.1em .12em 0 0;color:var(--ember)}
.prose h2{font-family:var(--display);font-size:1.65rem;color:var(--deep);margin-top:2.8rem;
padding-top:1.3rem;border-top:3px double var(--rule)}
.prose h2::before{content:"❖ ";color:var(--gold)}
.prose a{color:var(--ember);text-decoration-color:rgba(168,48,15,.4)}
.prose strong{color:var(--deep)}
.prose ul{padding-left:1.4rem}.prose li+li{margin-top:.5rem}.prose li::marker{color:var(--fire)}
.prose blockquote{margin:1.9rem 0;padding:1.3rem 1.6rem;
background:linear-gradient(135deg,rgba(255,246,228,.7),rgba(232,207,164,.35));
border:1px solid var(--rule);border-left:5px solid var(--fire);
box-shadow:inset 0 0 0 1px rgba(255,255,255,.3)}
.prose blockquote strong{font-family:var(--deva);color:var(--deep)}
.prose hr{border:0;height:3px;margin:2.6rem auto;width:70%;
background:linear-gradient(90deg,transparent,var(--gold),transparent)}
.series-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center;
max-width:40rem;margin:3.5rem auto 1rem;padding-top:1.8rem;border-top:3px double var(--rule)}
.sn-link{text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.2rem}
.sn-next{text-align:right}
.sn-dir{font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--ember)}
.sn-title{font-family:var(--display);font-size:1.05rem;color:var(--deep)}
.sn-empty{visibility:hidden}
.sn-index{text-decoration:none;font-family:var(--display);font-size:.85rem;letter-spacing:.12em;
color:var(--ink-faint);border:1px solid var(--rule);padding:.55rem .9rem;white-space:nowrap}
.site-footer{margin-top:4.5rem;padding:3rem 0;border-top:4px double var(--ember);text-align:center;
background:linear-gradient(180deg,transparent,rgba(168,48,15,.07))}
.foot-ornament{color:var(--gold);font-size:1.7rem;margin-bottom:.7rem}
.foot-note{margin:0 0 .5rem;color:var(--ink-soft);font-style:italic;font-size:1.05rem}
.foot-copy{margin:0;font-size:.8rem;color:var(--ink-faint);letter-spacing:.1em}
"""

# =============================================================================
# DESIGN 3 — "Devalaya / Temple Night"
# Dark, lamp-lit: near-black indigo ground, gold-leaf text, vermilion accents,
# mandala watermark, high contrast for reading by oil lamp.
# =============================================================================
D3 = """
:root{--night:#120c14;--night2:#1c1320;--ink:#e9dcc4;--ink-soft:#c3ae8c;
--ink-faint:#8f7a5c;--gold:#e0a94a;--gold-lit:#f5cd7a;--vermilion:#e2452f;
--saffron:#f0932b;--line:rgba(224,169,74,.22);--line-soft:rgba(224,169,74,.11);
--serif:"Spectral",Georgia,serif;--display:"Marcellus",serif;--deva:"Tiro Devanagari Hindi",serif;}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--night);color:var(--ink);font-family:var(--serif);
font-size:1.08rem;line-height:1.78;position:relative}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(ellipse 60% 45% at 50% 0%,rgba(224,169,74,.16),transparent 60%),
radial-gradient(circle at 20% 80%,rgba(226,69,47,.10),transparent 45%),
radial-gradient(circle at 85% 30%,rgba(240,147,43,.07),transparent 40%),
linear-gradient(180deg,#181020,var(--night) 40%,#0d0810 100%)}
/* mandala watermark */
body::after{content:"ॐ";position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
font-family:var(--deva);font-size:60vw;color:rgba(224,169,74,.035);z-index:0;pointer-events:none;line-height:1}
.grain{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.32;
mix-blend-mode:overlay;background-image:__GRAIN__}
.wrap{width:min(100% - 2*1.4rem,72rem);margin-inline:auto;position:relative;z-index:2}
.site-header{border-bottom:1px solid var(--line);
background:linear-gradient(180deg,rgba(224,169,74,.07),transparent)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;
gap:1rem;flex-wrap:wrap;padding-block:1rem}
.brand{display:flex;align-items:center;gap:.8rem;text-decoration:none;color:inherit}
.brand-mark{font-family:var(--deva);font-size:2.1rem;color:var(--gold);
text-shadow:0 0 24px rgba(224,169,74,.7),0 0 48px rgba(224,169,74,.3)}
.brand-text{display:flex;flex-direction:column;line-height:1.15}
.brand-name{font-family:var(--display);font-size:1.3rem;color:var(--gold-lit);letter-spacing:.04em}
.brand-sub{font-size:.64rem;letter-spacing:.26em;text-transform:uppercase;color:var(--ink-faint)}
.site-nav{display:flex;gap:1.4rem;flex-wrap:wrap}
.site-nav a{text-decoration:none;color:var(--ink-soft);font-size:.82rem;
letter-spacing:.14em;text-transform:uppercase;padding-bottom:.25rem;border-bottom:2px solid transparent;
transition:color .2s,border-color .2s}
.site-nav a:hover{color:var(--gold-lit)}
.site-nav a.active{color:var(--vermilion);border-bottom-color:var(--vermilion)}
.hero{text-align:center;padding:5rem 0 3rem}
.hero-eyebrow{font-family:var(--deva);color:var(--saffron);font-size:1.4rem;margin:0 0 .7rem;
text-shadow:0 0 20px rgba(240,147,43,.6)}
.hero-title{font-family:var(--display);font-size:clamp(2.3rem,6.5vw,4rem);margin:0;
color:var(--gold-lit);letter-spacing:.05em;text-shadow:0 0 40px rgba(224,169,74,.35)}
.hero-sub{max-width:34rem;margin:1.2rem auto 0;color:var(--ink-soft);font-style:italic}
.hero-rule{width:200px;height:1px;margin:2rem auto 0;
background:linear-gradient(90deg,transparent,var(--gold),transparent);position:relative}
.hero-rule::after{content:"◆";position:absolute;top:50%;left:50%;
transform:translate(-50%,-50%);color:var(--gold);font-size:.6rem;background:var(--night);padding:0 .6rem}
.series-grid{display:grid;gap:1.6rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));margin-top:1rem}
.card{position:relative;display:block;text-decoration:none;color:inherit;padding:2.2rem 1.7rem 1.7rem;
background:linear-gradient(160deg,rgba(224,169,74,.06),rgba(224,169,74,.02));
border:1px solid var(--line);transition:transform .22s,border-color .22s,box-shadow .22s;overflow:hidden}
.card::before{content:"";position:absolute;inset:8px;border:1px solid var(--line-soft);pointer-events:none}
.card:hover{transform:translateY(-4px);border-color:var(--gold);
box-shadow:0 0 40px -12px rgba(224,169,74,.4)}
.card-glyph{font-family:var(--deva);display:block;font-size:2.7rem;color:var(--vermilion);
margin-bottom:.6rem;text-shadow:0 0 24px rgba(226,69,47,.6)}
.card-title{font-family:var(--display);font-size:1.32rem;margin:0 0 .5rem;color:var(--gold-lit);letter-spacing:.03em}
.card-blurb{margin:0 0 1.1rem;font-size:.95rem;color:var(--ink-soft)}
.card-meta{font-size:.76rem;letter-spacing:.18em;text-transform:uppercase;color:var(--saffron)}
.article{padding:3rem 0}
.article-head{max-width:42rem;margin-inline:auto;padding-bottom:1.8rem;text-align:center}
.eyebrow{display:inline-block;text-decoration:none;font-size:.72rem;letter-spacing:.22em;
text-transform:uppercase;color:var(--vermilion);margin-bottom:.8rem}
.eyebrow:hover{color:var(--saffron)}
.article-title{font-family:var(--display);font-size:clamp(1.8rem,4.6vw,2.8rem);margin:0;
color:var(--gold-lit);letter-spacing:.03em;line-height:1.2}
.article-sub{margin:1rem auto 0;max-width:34rem;color:var(--ink-soft);font-style:italic}
.article-date{display:block;margin-top:1rem;font-size:.82rem;color:var(--ink-faint);letter-spacing:.1em}
.prose{max-width:42rem;margin-inline:auto}
.prose>*+*{margin-top:1.2em}
.prose h2{font-family:var(--display);font-size:1.55rem;color:var(--gold-lit);margin-top:2.8rem;
padding-top:1.3rem;border-top:1px solid var(--line);letter-spacing:.03em}
.prose h3{font-family:var(--display);color:var(--saffron);font-size:1.2rem;margin-top:1.9rem}
.prose a{color:var(--saffron);text-decoration-color:rgba(240,147,43,.4)}
.prose a:hover{color:var(--gold-lit)}
.prose strong{color:var(--gold-lit);font-weight:600}
.prose ul{padding-left:1.35rem}.prose li+li{margin-top:.45rem}
.prose li::marker{color:var(--vermilion)}
.prose blockquote{margin:1.9rem 0;padding:1.4rem 1.6rem;
background:linear-gradient(135deg,rgba(224,169,74,.07),rgba(226,69,47,.04));
border-left:3px solid var(--saffron);box-shadow:inset 0 0 0 1px var(--line-soft)}
.prose blockquote strong{font-family:var(--deva);color:var(--gold-lit);
text-shadow:0 0 16px rgba(224,169,74,.3)}
.prose hr{border:0;height:1px;margin:2.6rem auto;width:60%;
background:linear-gradient(90deg,transparent,var(--gold),transparent)}
.series-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center;
max-width:42rem;margin:3.5rem auto 1rem;padding-top:1.8rem;border-top:1px solid var(--line)}
.sn-link{text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.2rem}
.sn-next{text-align:right}
.sn-dir{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--vermilion)}
.sn-title{font-family:var(--display);font-size:1rem;color:var(--gold-lit)}
.sn-link:hover .sn-title{color:var(--saffron)}
.sn-empty{visibility:hidden}
.sn-index{text-decoration:none;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;
color:var(--ink-faint);border:1px solid var(--line);padding:.55rem .85rem;white-space:nowrap}
.site-footer{margin-top:4.5rem;padding:3rem 0;border-top:1px solid var(--line);text-align:center;
background:linear-gradient(180deg,transparent,rgba(224,169,74,.05))}
.foot-ornament{color:var(--gold);font-size:1.6rem;margin-bottom:.7rem;
text-shadow:0 0 20px rgba(224,169,74,.6)}
.foot-note{margin:0 0 .5rem;color:var(--ink-soft);font-style:italic}
.foot-copy{margin:0;font-size:.78rem;color:var(--ink-faint);letter-spacing:.1em}
"""

# =============================================================================
# DESIGN 4 — "Raag / Mughal Folio"
# Ivory paper, painted border frames, jewel tones — peacock teal + ruby + gold.
# Elegant, book-like, generous margins.
# =============================================================================
D4 = """
:root{--ivory:#fbf5e6;--ivory-edge:#f0e4c8;--ink:#2a2118;--ink-soft:#5a4a38;
--ink-faint:#8b7860;--ruby:#9e1b32;--peacock:#0f6b6b;--gold:#b8912f;--plum:#4a1540;
--rule:rgba(74,21,64,.22);--rule-soft:rgba(42,33,24,.12);
--serif:"Cormorant Garamond",Georgia,serif;--display:"Rozha One",serif;--deva:"Tiro Devanagari Hindi",serif;}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--ivory-edge);color:var(--ink);font-family:var(--serif);
font-size:1.2rem;line-height:1.72;position:relative}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(ellipse 70% 60% at 50% 0%,rgba(255,252,240,.9),transparent 65%),
linear-gradient(180deg,#f6ecd6,var(--ivory) 20%,#f4ead2 100%)}
.grain{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.4;
mix-blend-mode:multiply;background-image:__GRAIN__}
/* painted folio frame */
.frame{position:fixed;inset:14px;z-index:1;pointer-events:none;
border:2px solid var(--ruby);border-radius:2px;
box-shadow:inset 0 0 0 1px var(--ivory),inset 0 0 0 4px var(--gold),
inset 0 0 0 5px var(--ivory),inset 0 0 0 6px var(--peacock)}
.wrap{width:min(100% - 2*2.4rem,70rem);margin-inline:auto;position:relative;z-index:2}
.site-header{border-bottom:1px solid var(--rule);text-align:center;padding:2.2rem 0 1.4rem}
.brand{display:inline-flex;flex-direction:column;align-items:center;gap:.4rem;
text-decoration:none;color:inherit;margin-bottom:1.2rem}
.brand-mark{font-family:var(--deva);font-size:2.6rem;color:var(--ruby)}
.brand-name{font-family:var(--display);font-size:2rem;color:var(--plum);letter-spacing:.02em}
.brand-sub{font-size:.68rem;letter-spacing:.3em;text-transform:uppercase;color:var(--ink-faint)}
.site-nav{display:flex;gap:2rem;justify-content:center;flex-wrap:wrap}
.site-nav a{text-decoration:none;color:var(--ink-soft);font-family:var(--serif);
font-size:1.05rem;letter-spacing:.06em;padding-bottom:.2rem;border-bottom:1px solid transparent;
font-variant:small-caps}
.site-nav a.active{color:var(--ruby);border-bottom-color:var(--gold)}
.hero{text-align:center;padding:3rem 0 1.5rem}
.hero-eyebrow{font-family:var(--deva);color:var(--peacock);font-size:1.35rem;margin:0 0 .6rem}
.hero-title{font-family:var(--display);font-size:clamp(2.4rem,6.5vw,3.9rem);margin:0;color:var(--plum)}
.hero-sub{max-width:34rem;margin:1rem auto 0;color:var(--ink-soft);font-style:italic;font-size:1.15rem}
.ornament{color:var(--gold);letter-spacing:.5em;margin:1.4rem 0 0;font-size:1rem}
.series-grid{display:grid;gap:1.8rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));margin-top:2rem}
.card{position:relative;display:block;text-decoration:none;color:inherit;padding:2.4rem 1.8rem 1.8rem;
background:linear-gradient(160deg,rgba(255,252,240,.85),rgba(240,228,200,.5));
border:1px solid var(--gold);box-shadow:0 2px 0 rgba(74,21,64,.1),0 14px 30px -22px rgba(42,33,24,.6);
transition:transform .22s,box-shadow .22s;overflow:hidden}
.card::before{content:"";position:absolute;inset:10px;border:1px solid var(--rule-soft);pointer-events:none}
.card::after{content:"";position:absolute;inset:14px;border:3px solid transparent;
border-image:linear-gradient(135deg,var(--ruby),var(--gold),var(--peacock)) 1;opacity:0;transition:opacity .22s}
.card:hover{transform:translateY(-4px);box-shadow:0 5px 0 rgba(74,21,64,.15),0 22px 40px -22px rgba(42,33,24,.7)}
.card:hover::after{opacity:1}
.card-glyph{font-family:var(--deva);display:block;font-size:2.9rem;color:var(--ruby);margin-bottom:.5rem}
.card-title{font-family:var(--display);font-size:1.5rem;margin:0 0 .5rem;color:var(--plum)}
.card-blurb{margin:0 0 1.1rem;font-size:1.02rem;color:var(--ink-soft)}
.card-meta{font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--peacock);font-weight:600}
.article{padding:3rem 0}
.article-head{max-width:38rem;margin-inline:auto;padding-bottom:1.8rem;text-align:center}
.eyebrow{display:inline-block;text-decoration:none;font-family:var(--serif);font-variant:small-caps;
font-size:.98rem;letter-spacing:.14em;color:var(--ruby);margin-bottom:.8rem}
.article-title{font-family:var(--display);font-size:clamp(1.9rem,5vw,3rem);margin:0;color:var(--plum);line-height:1.15}
.article-sub{margin:1rem auto 0;max-width:33rem;color:var(--ink-soft);font-style:italic;font-size:1.15rem}
.article-date{display:block;margin-top:1rem;font-size:.88rem;color:var(--ink-faint);letter-spacing:.1em;font-variant:small-caps}
.prose{max-width:38rem;margin-inline:auto}
.prose>*+*{margin-top:1.25em}
.prose h2{font-family:var(--display);font-size:1.7rem;color:var(--ruby);margin-top:3rem;
padding-top:1.3rem;border-top:1px solid var(--rule)}
.prose h2::after{content:" ❖";color:var(--gold)}
.prose a{color:var(--peacock);text-decoration-color:rgba(15,107,107,.4)}
.prose strong{color:var(--plum)}
.prose ul{padding-left:1.5rem}.prose li+li{margin-top:.5rem}.prose li::marker{color:var(--ruby)}
.prose blockquote{margin:2rem 0;padding:1.5rem 1.7rem;
background:linear-gradient(135deg,rgba(255,252,240,.8),rgba(240,228,200,.4));
border:1px solid var(--gold);border-left:4px solid var(--ruby);position:relative}
.prose blockquote::before{content:"❝";position:absolute;top:-.2rem;left:1rem;
font-size:2.5rem;color:var(--gold);opacity:.5;font-family:var(--serif)}
.prose blockquote strong{font-family:var(--deva);color:var(--plum)}
.prose hr{border:0;height:1px;margin:2.8rem auto;width:65%;
background:linear-gradient(90deg,transparent,var(--gold),transparent)}
.series-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center;
max-width:38rem;margin:3.5rem auto 1rem;padding-top:1.8rem;border-top:1px solid var(--rule)}
.sn-link{text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.2rem}
.sn-next{text-align:right}
.sn-dir{font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--ruby)}
.sn-title{font-family:var(--display);font-size:1.05rem;color:var(--plum)}
.sn-empty{visibility:hidden}
.sn-index{text-decoration:none;font-variant:small-caps;font-size:.9rem;letter-spacing:.1em;
color:var(--ink-faint);border:1px solid var(--gold);padding:.5rem .9rem;white-space:nowrap}
.site-footer{margin-top:4.5rem;padding:2.8rem 0;border-top:2px solid var(--ruby);text-align:center;
background:linear-gradient(180deg,transparent,rgba(74,21,64,.05))}
.foot-ornament{color:var(--gold);font-size:1.6rem;margin-bottom:.7rem;letter-spacing:.4em}
.foot-note{margin:0 0 .5rem;color:var(--ink-soft);font-style:italic;font-size:1.05rem}
.foot-copy{margin:0;font-size:.8rem;color:var(--ink-faint)}
"""

# =============================================================================
# DESIGN 5 — "Pattachitra / Folk Scroll"
# Bold folk-art: warm ochre ground, thick hand-drawn black outlines, saturated
# red/yellow, playful tribal dividers, high energy.
# =============================================================================
D5 = """
:root{--ochre:#f2c14e;--ochre-deep:#e0a838;--paper:#fdf3d7;--ink:#1a1208;
--ink-soft:#3d2b12;--red:#c62828;--red-deep:#8e0000;--green:#2e6b3e;--blue:#1e5f8a;
--rule:rgba(26,18,8,.55);--rule-soft:rgba(26,18,8,.2);
--serif:"Spectral",Georgia,serif;--display:"Yatra One",serif;--deva:"Tiro Devanagari Hindi",serif;}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--ochre);color:var(--ink);font-family:var(--serif);
font-size:1.12rem;line-height:1.7;position:relative}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(circle at 50% 0%,rgba(253,243,215,.95),transparent 55%),
repeating-linear-gradient(45deg,rgba(198,40,40,.03) 0 12px,transparent 12px 24px),
linear-gradient(180deg,var(--paper),#f6d98a 60%,var(--ochre-deep))}
.grain{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.6;
mix-blend-mode:multiply;background-image:__GRAIN__}
.wrap{width:min(100% - 2*1.4rem,72rem);margin-inline:auto;position:relative;z-index:2}
/* thick folk border strip */
.site-header{background:var(--paper);border-bottom:6px solid var(--ink);
box-shadow:0 4px 0 var(--red),0 8px 0 var(--ink)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;
gap:1rem;flex-wrap:wrap;padding-block:1rem}
.brand{display:flex;align-items:center;gap:.8rem;text-decoration:none;color:inherit}
.brand-mark{font-family:var(--deva);font-size:2.4rem;color:var(--red);
-webkit-text-stroke:1.5px var(--ink);text-stroke:1.5px var(--ink)}
.brand-text{display:flex;flex-direction:column;line-height:1.1}
.brand-name{font-family:var(--display);font-size:1.55rem;color:var(--ink);
-webkit-text-stroke:.4px var(--ink)}
.brand-sub{font-size:.64rem;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-soft);font-weight:600}
.site-nav{display:flex;gap:.6rem;flex-wrap:wrap}
.site-nav a{text-decoration:none;color:var(--ink);font-family:var(--display);font-size:.95rem;
padding:.35rem .8rem;border:2px solid var(--ink);background:var(--paper);
box-shadow:3px 3px 0 var(--ink);transition:transform .15s,box-shadow .15s,background .15s}
.site-nav a:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--ink)}
.site-nav a.active{background:var(--red);color:var(--paper)}
.hero{text-align:center;padding:3.5rem 0 2rem}
.hero-eyebrow{font-family:var(--deva);color:var(--red);font-size:1.6rem;margin:0 0 .5rem;
font-weight:600}
.hero-title{font-family:var(--display);font-size:clamp(2.5rem,7.5vw,4.4rem);margin:0;
color:var(--ink);-webkit-text-stroke:1px var(--ink);line-height:1.05;
text-shadow:5px 5px 0 var(--ochre-deep)}
.hero-sub{max-width:32rem;margin:1.1rem auto 0;color:var(--ink-soft);font-weight:500}
.folk-dance{display:flex;justify-content:center;gap:.5rem;margin-top:1.5rem;font-size:1.3rem}
.folk-dance span:nth-child(odd){color:var(--red)}
.folk-dance span:nth-child(even){color:var(--green)}
.series-grid{display:grid;gap:1.6rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));margin-top:1.5rem}
.card{position:relative;display:block;text-decoration:none;color:inherit;padding:2rem 1.6rem 1.6rem;
background:var(--paper);border:3px solid var(--ink);box-shadow:6px 6px 0 var(--ink);
transition:transform .18s,box-shadow .18s;overflow:hidden}
.card::before{content:"";position:absolute;top:0;left:0;right:0;height:8px;
background:repeating-linear-gradient(90deg,var(--red) 0 14px,var(--ochre) 14px 28px,var(--green) 28px 42px)}
.card:hover{transform:translate(-3px,-3px);box-shadow:9px 9px 0 var(--red)}
.card-glyph{font-family:var(--deva);display:block;font-size:2.8rem;color:var(--red);
margin:.6rem 0 .5rem;-webkit-text-stroke:1px var(--ink)}
.card-title{font-family:var(--display);font-size:1.4rem;margin:0 0 .5rem;color:var(--ink)}
.card-blurb{margin:0 0 1.1rem;font-size:.98rem;color:var(--ink-soft)}
.card-meta{display:inline-block;font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;
font-weight:700;color:var(--paper);background:var(--red);padding:.25rem .6rem;border:2px solid var(--ink)}
.article{padding:2.5rem 0}
.article-head{max-width:42rem;margin-inline:auto;padding-bottom:1.8rem;
border-bottom:4px double var(--rule);margin-bottom:1.8rem}
.eyebrow{display:inline-block;text-decoration:none;font-family:var(--display);font-size:.9rem;
letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin-bottom:.7rem}
.article-title{font-family:var(--display);font-size:clamp(1.9rem,5vw,3rem);margin:0;color:var(--ink);line-height:1.1}
.article-sub{margin:.9rem 0 0;color:var(--ink-soft);font-weight:500;font-size:1.08rem}
.article-date{display:block;margin-top:.9rem;font-size:.82rem;color:var(--ink-soft);
font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.prose{max-width:42rem;margin-inline:auto}
.prose>*+*{margin-top:1.2em}
.prose h2{font-family:var(--display);font-size:1.6rem;color:var(--ink);margin-top:2.6rem;
padding:0 0 .5rem;border-bottom:3px solid var(--red);letter-spacing:.02em}
.prose a{color:var(--red);text-decoration:underline;text-decoration-thickness:2px;
text-underline-offset:3px;text-decoration-color:var(--red-deep)}
.prose strong{color:var(--red-deep);font-weight:700}
.prose ul{padding-left:1.4rem}.prose li+li{margin-top:.5rem}
.prose li::marker{color:var(--red);font-size:1.1em}
.prose blockquote{margin:1.8rem 0;padding:1.3rem 1.5rem;background:var(--paper);
border:3px solid var(--ink);border-left:8px solid var(--red);box-shadow:5px 5px 0 rgba(26,18,8,.25)}
.prose blockquote strong{font-family:var(--deva);color:var(--ink);font-size:1.12em;line-height:1.9;display:inline-block}
.prose hr{border:0;height:6px;margin:2.4rem auto;width:75%;
background:repeating-linear-gradient(90deg,var(--red) 0 16px,transparent 16px 22px,var(--ink) 22px 26px,transparent 26px 42px)}
.series-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center;
max-width:42rem;margin:3rem auto 1rem;padding-top:1.8rem;border-top:4px double var(--rule)}
.sn-link{text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.2rem}
.sn-next{text-align:right}
.sn-dir{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--red);font-weight:700}
.sn-title{font-family:var(--display);font-size:1.05rem;color:var(--ink)}
.sn-empty{visibility:hidden}
.sn-index{text-decoration:none;font-family:var(--display);font-size:.9rem;color:var(--ink);
border:3px solid var(--ink);padding:.45rem .85rem;white-space:nowrap;background:var(--paper);
box-shadow:3px 3px 0 var(--ink)}
.site-footer{margin-top:4rem;padding:2.5rem 0;border-top:6px solid var(--ink);
background:var(--paper);text-align:center;box-shadow:0 -4px 0 var(--red)}
.foot-ornament{color:var(--red);font-size:1.6rem;margin-bottom:.6rem}
.foot-note{margin:0 0 .5rem;color:var(--ink-soft);font-weight:500}
.foot-copy{margin:0;font-size:.78rem;color:var(--ink-soft);font-weight:700;letter-spacing:.08em}
"""

# =============================================================================
# DESIGNS 6-8 — design 5's bold pattachitra linework, laid on real material.
# The "ancient" quality comes from an actual substrate: a torn deckle-edged
# sheet, a palm-leaf folio, or a charred scroll. Edges are genuinely torn by
# displacing them with feTurbulence -> feDisplacementMap, not faked with borders.
# =============================================================================

SHEET_SVG = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<filter id="{fid}" x="-7%" y="-7%" width="114%" height="114%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{oct}" seed="{seed}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="{scale}" xChannelSelector="R" yChannelSelector="G"/>
</filter></defs></svg><div class="sheet" aria-hidden="true"></div>"""

# --- shared component kit: keeps design 5's chunky hand-painted folk language ---
FOLK = """
.site-header,main,.site-footer{position:relative;z-index:3}
/* header is a solid chrome band ABOVE the torn sheet — the tear must never
   reach into the nav row, so the sheet starts below this band. */
.site-header{position:sticky;top:0;z-index:20;background:var(--table);
padding-top:.85rem;border-bottom:none}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;
gap:.85rem 1.4rem;flex-wrap:wrap;padding-bottom:.8rem;border-bottom:3px solid var(--ink)}
.brand{display:flex;align-items:center;gap:.8rem;text-decoration:none;color:inherit}
.brand-mark{font-family:var(--deva);font-size:2.3rem;color:var(--red);
-webkit-text-stroke:1.5px var(--ink)}
.brand-text{display:flex;flex-direction:column;line-height:1.1}
.brand-name{font-family:var(--display);font-size:1.45rem;color:var(--ink)}
.brand-sub{font-size:.62rem;letter-spacing:.24em;text-transform:uppercase;
color:var(--ink-soft);font-weight:600}
.site-nav{display:flex;gap:clamp(.7rem,2vw,1.3rem);flex-wrap:wrap;align-items:center}
.site-nav a{text-decoration:none;color:var(--ink-soft);font-family:var(--display);
font-size:.95rem;letter-spacing:.02em;padding-bottom:.15rem;
border-bottom:3px solid transparent;transition:color .15s,border-color .15s}
.site-nav a:hover{color:var(--red);border-bottom-color:var(--red)}
.site-nav a.active{color:var(--red);border-bottom-color:var(--red)}
.hero{text-align:center;padding:3.2rem 0 1.6rem}
.hero-eyebrow{font-family:var(--deva);color:var(--red);font-size:1.5rem;margin:0 0 .5rem}
.hero-title{font-family:var(--display);font-size:clamp(2.3rem,7vw,4rem);margin:0;
color:var(--ink);line-height:1.05;text-shadow:4px 4px 0 var(--tint)}
.hero-sub{max-width:31rem;margin:1rem auto 0;color:var(--ink-soft);font-weight:500}
.series-grid{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));margin-top:1.4rem}
.card{position:relative;display:block;text-decoration:none;color:inherit;padding:1.9rem 1.5rem 1.5rem;
background:var(--card);border:3px solid var(--ink);box-shadow:6px 6px 0 var(--ink);
transition:transform .18s,box-shadow .18s;overflow:hidden}
.card::before{content:"";position:absolute;top:0;left:0;right:0;height:8px;
background:repeating-linear-gradient(90deg,var(--red) 0 14px,var(--tint) 14px 28px,var(--green) 28px 42px)}
.card:hover{transform:translate(-3px,-3px);box-shadow:9px 9px 0 var(--red)}
.card-glyph{font-family:var(--deva);display:block;font-size:2.7rem;color:var(--red);
margin:.6rem 0 .5rem;-webkit-text-stroke:1px var(--ink)}
.card-title{font-family:var(--display);font-size:1.35rem;margin:0 0 .5rem;color:var(--ink)}
.card-blurb{margin:0 0 1.1rem;font-size:.96rem;color:var(--ink-soft)}
.card-meta{display:inline-block;font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;
font-weight:700;color:var(--paper);background:var(--red);padding:.22rem .55rem;border:2px solid var(--ink)}
.article{padding:2.4rem 0}
.article-head{max-width:41rem;margin-inline:auto;padding-bottom:1.6rem;
border-bottom:4px double var(--ink);margin-bottom:1.7rem}
.eyebrow{display:inline-block;text-decoration:none;font-family:var(--display);font-size:.88rem;
letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin-bottom:.7rem}
.article-title{font-family:var(--display);font-size:clamp(1.85rem,5vw,2.9rem);margin:0;
color:var(--ink);line-height:1.1}
.article-sub{margin:.85rem 0 0;color:var(--ink-soft);font-weight:500;font-size:1.06rem}
.article-date{display:block;margin-top:.85rem;font-size:.8rem;color:var(--ink-soft);
font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.prose{max-width:41rem;margin-inline:auto}
.prose>*+*{margin-top:1.2em}
.prose h2{font-family:var(--display);font-size:1.55rem;color:var(--ink);margin-top:2.5rem;
padding:0 0 .5rem;border-bottom:3px solid var(--red)}
.prose h3{font-family:var(--display);color:var(--red);font-size:1.18rem;margin-top:1.8rem}
.prose a{color:var(--red);text-decoration:underline;text-decoration-thickness:2px;
text-underline-offset:3px}
.prose strong{color:var(--red);font-weight:700}
.prose ul{padding-left:1.35rem}.prose li+li{margin-top:.5rem}
.prose li::marker{color:var(--red);font-size:1.1em}
.prose blockquote{margin:1.8rem 0;padding:1.3rem 1.5rem;background:var(--card);
border:3px solid var(--ink);border-left:8px solid var(--red);box-shadow:5px 5px 0 rgba(20,14,6,.3)}
.prose blockquote strong{font-family:var(--deva);color:var(--ink);font-size:1.1em;line-height:1.9;
display:inline-block;font-weight:400;-webkit-text-stroke:.3px var(--ink)}
.prose hr{border:0;height:6px;margin:2.4rem auto;width:72%;
background:repeating-linear-gradient(90deg,var(--red) 0 16px,transparent 16px 22px,var(--ink) 22px 26px,transparent 26px 42px)}
.series-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center;
max-width:41rem;margin:3rem auto 1rem;padding-top:1.7rem;border-top:4px double var(--ink)}
.sn-link{text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.2rem}
.sn-next{text-align:right}
.sn-dir{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--red);font-weight:700}
.sn-title{font-family:var(--display);font-size:1.02rem;color:var(--ink)}
.sn-empty{visibility:hidden}
.sn-index{text-decoration:none;font-family:var(--display);font-size:.88rem;color:var(--ink);
border:3px solid var(--ink);padding:.4rem .8rem;white-space:nowrap;box-shadow:3px 3px 0 var(--ink)}
.site-footer{margin-top:3.5rem;padding:2.4rem 0;border-top:5px solid var(--ink);
text-align:center;box-shadow:0 -3px 0 var(--red)}
.foot-ornament{color:var(--red);font-size:1.5rem;margin-bottom:.6rem}
.foot-note{margin:0 0 .5rem;color:var(--ink-soft);font-weight:500}
.foot-copy{margin:0;font-size:.76rem;color:var(--ink-soft);font-weight:700;letter-spacing:.08em}
@media (max-width:640px){
 body{font-size:1.02rem}
 .series-nav{grid-template-columns:1fr;text-align:center}
 .sn-next{align-items:center;text-align:center}
 .sn-empty{display:none}
 .wrap{width:min(100% - 2.6rem,66rem)}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}"""

# --- Design 6: pattachitra painted on torn handmade paper ---------------------
D6 = """
:root{--table:#cfb789;--paper:#f7ecd0;--card:#fdf6e2;--tint:#e8b74a;
--ink:#1b1208;--ink-soft:#473117;--red:#c62828;--green:#2e6b3e;
--serif:"Spectral",Georgia,serif;--display:"Yatra One",cursive;
--deva:"Tiro Devanagari Hindi",serif}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;min-height:100vh;background:var(--table);color:var(--ink);
font-family:var(--serif);font-size:1.1rem;line-height:1.7;position:relative}
/* pale sun-warmed wood under the sheet — light, not gloomy */
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:repeating-linear-gradient(93deg,rgba(110,75,35,.07) 0 4px,transparent 4px 11px),
radial-gradient(ellipse 85% 65% at 50% 6%,rgba(255,252,240,.85),transparent 72%),
linear-gradient(158deg,#dcc79b,#cfb789 60%,#c4aa7a)}
/* the sheet — edges physically torn by the SVG displacement filter.
   top inset clears the sticky header AND the tear's ±22px reach. */
.sheet{position:absolute;inset:92px 16px 24px 16px;z-index:1;pointer-events:none;
filter:url(#torn6) drop-shadow(0 16px 30px rgba(0,0,0,.35)) drop-shadow(0 3px 5px rgba(0,0,0,.25));
background:
 radial-gradient(circle at 11% 22%,rgba(150,96,40,.22) 0 8px,transparent 17px),
 radial-gradient(circle at 85% 15%,rgba(140,88,36,.17) 0 12px,transparent 27px),
 radial-gradient(circle at 67% 79%,rgba(150,96,40,.19) 0 10px,transparent 23px),
 radial-gradient(circle at 24% 87%,rgba(120,74,30,.15) 0 14px,transparent 31px),
 radial-gradient(circle at 47% 44%,rgba(163,113,50,.11) 0 22px,transparent 50px),
 radial-gradient(circle at 90% 58%,rgba(140,88,36,.13) 0 9px,transparent 21px),
 repeating-linear-gradient(0deg,rgba(120,86,40,.04) 0 1px,transparent 1px 4px),
 linear-gradient(157deg,#fbf2d9,#f3e2bd 44%,#dfc795)}
/* uneven aging toward the edges */
.sheet::after{content:"";position:absolute;inset:0;mix-blend-mode:multiply;
background:radial-gradient(ellipse 125% 115% at 50% 45%,transparent 52%,rgba(124,82,34,.3))}
.grain{position:fixed;inset:0;z-index:2;pointer-events:none;opacity:.6;
mix-blend-mode:multiply;background-image:__GRAIN__}
.wrap{position:relative;z-index:3;width:min(100% - 5rem,66rem);margin-inline:auto}
""" + FOLK

# --- Design 7: the same language on a palm-leaf folio -------------------------
D7 = """
:root{--table:#c9ad7c;--paper:#fdf6e2;--card:rgba(255,250,236,.94);--tint:#e0a020;
--ink:#2a1c0a;--ink-soft:#54401a;--red:#b91c1c;--green:#2e6b3e;
--serif:"Spectral",Georgia,serif;--display:"Marcellus",serif;
--deva:"Tiro Devanagari Hindi",serif}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;min-height:100vh;background:var(--table);color:#2a1c0a;
font-family:var(--serif);font-size:1.1rem;line-height:1.7;position:relative}
/* warm daylight surface the leaf rests on — not a dark room */
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(255,250,238,.8),transparent 70%),
linear-gradient(170deg,#dcc392,#c9ad7c 60%,#bda06f)}
/* palm-leaf strip: horizontal fibre grain, darkened cured ends.
   top inset clears the sticky header (tear reach is only ±8px here). */
.sheet{position:absolute;inset:86px 20px 24px 20px;z-index:1;pointer-events:none;
filter:url(#torn7) drop-shadow(0 18px 36px rgba(0,0,0,.4));
background:
 repeating-linear-gradient(0deg,rgba(74,48,16,.09) 0 1px,transparent 1px 3px),
 repeating-linear-gradient(0deg,rgba(74,48,16,.05) 0 2px,transparent 2px 8px),
 radial-gradient(ellipse 70% 45% at 18% 26%,rgba(120,88,36,.35),transparent 62%),
 radial-gradient(ellipse 60% 40% at 82% 74%,rgba(96,68,26,.4),transparent 60%),
 radial-gradient(ellipse 130% 120% at 50% 50%,transparent 34%,rgba(86,60,24,.75) 92%),
 linear-gradient(176deg,#dcc089,#c3a05f 34%,#b8944f 68%,#a8874a)}
/* binding holes punched through the leaf */
.sheet::after{content:"";position:absolute;left:2.7rem;top:0;bottom:0;width:44px;
background:radial-gradient(circle 14px at 22px 20%,var(--table) 97%,transparent 100%),
radial-gradient(circle 14px at 22px 80%,var(--table) 97%,transparent 100%)}
.grain{position:fixed;inset:0;z-index:2;pointer-events:none;opacity:.5;
mix-blend-mode:multiply;background-image:__GRAIN__}
.wrap{position:relative;z-index:3;width:min(100% - 7rem,64rem);margin-inline:auto}
/* text sits as if written onto the leaf */
.site-header,main,.site-footer{position:relative;z-index:3}
.hero-title,.article-title,.card-title,.brand-name,.sn-title{color:#241706}
""" + FOLK

# --- Design 8: charred temple scroll ------------------------------------------
D8 = """
:root{--table:#d7bf94;--paper:#f6ecd4;--card:#fdf8ea;--tint:#d4761c;
--ink:#180f06;--ink-soft:#4a3312;--red:#c62828;--green:#8a6a1e;
--serif:"Spectral",Georgia,serif;--display:"Yatra One",cursive;
--deva:"Tiro Devanagari Hindi",serif}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;min-height:100vh;background:var(--table);color:var(--ink);
font-family:var(--serif);font-size:1.1rem;line-height:1.7;position:relative}
/* warm daylight surface with only a faint ember warmth at the foot */
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(ellipse 70% 45% at 50% 108%,rgba(196,84,20,.2),transparent 68%),
radial-gradient(ellipse 55% 40% at 88% 8%,rgba(255,250,236,.7),transparent 66%),
linear-gradient(165deg,#e6d3ac,#d7bf94 62%,#ccb186)}
/* burnt scroll: scorch lives on the RIM only (transparent out to ~62%) so the
   page stays light and readable — no full dark vignette over the text. */
.sheet{position:absolute;inset:88px 14px 24px 14px;z-index:1;pointer-events:none;
filter:url(#torn8) drop-shadow(0 20px 42px rgba(0,0,0,.4));
background:
 radial-gradient(ellipse 135% 120% at 50% 50%,transparent 62%,rgba(96,52,16,.62) 88%,rgba(38,20,7,.92) 100%),
 radial-gradient(circle at 6% 10%,rgba(30,16,6,.55) 0 16px,transparent 42px),
 radial-gradient(circle at 95% 22%,rgba(30,16,6,.45) 0 12px,transparent 36px),
 radial-gradient(circle at 12% 92%,rgba(30,16,6,.5) 0 18px,transparent 46px),
 radial-gradient(circle at 88% 88%,rgba(30,16,6,.5) 0 14px,transparent 40px),
 /* glowing ember flecks along the burnt rim */
 radial-gradient(circle 6px at 4% 46%,rgba(226,120,30,.8) 0 60%,transparent 100%),
 radial-gradient(circle 5px at 97% 64%,rgba(226,120,30,.7) 0 60%,transparent 100%),
 linear-gradient(155deg,#fbf3e0,#f6ecd4 46%,#e6d5b3);
box-shadow:inset 0 0 44px rgba(84,44,10,.3),inset 0 0 12px rgba(58,30,8,.3)}
/* soot speckle + scorch blotches */
.sheet::after{content:"";position:absolute;inset:0;mix-blend-mode:multiply;opacity:.55;
background-image:__GRAIN__}
.grain{position:fixed;inset:0;z-index:2;pointer-events:none;opacity:.5;
mix-blend-mode:overlay;background-image:__GRAIN__}
.wrap{position:relative;z-index:3;width:min(100% - 4.5rem,66rem);margin-inline:auto}
""" + FOLK

DESIGNS = [
    ("palmleaf",     "Palm-leaf Scripture", D1,
     "Aged cream paper, saffron + vermilion ink, restrained ruled panels. "
     "Quiet and reverent — the manuscript as it sits on the shelf."),
    ("yajna",        "Yajna / Vedic Fire", D2,
     "Burnt orange, deep maroon and gold. Fire-glow gradients, drop caps, "
     "double-rule ornamentation. Warmer and more ceremonial."),
    ("temple-night", "Devalaya / Temple Night", D3,
     "Dark, lamp-lit temple interior. Gold-leaf type on near-black indigo, "
     "vermilion accents, mandala watermark. High contrast, dramatic."),
    ("folioraag",    "Raag / Mughal Folio", D4,
     "Ivory paper inside a painted ruby–gold–peacock frame. Jewel tones, "
     "small-caps, book-like margins. Elegant and formal."),
    ("pattachitra",  "Pattachitra / Folk Scroll", D5,
     "Bold folk art. Ochre ground, thick black outlines, saturated red and "
     "green, chunky shadows. Playful, high-energy, hand-painted."),
    ("torn-paper",   "Torn Manuscript · Pattachitra", D6,
     "Design 5's painted folk linework laid on a REAL torn deckle-edged sheet — "
     "ragged displaced edges, foxing stains, on a worn oak table. Ancient + bold."),
    ("palm-leaf",    "Tāḷapatra · Palm-leaf Folio", D7,
     "The same bold language written onto an actual palm-leaf strip — horizontal "
     "fibre grain, punched binding holes, cured dark edges, dark stylus ink."),
    ("charred",      "Charred Scroll · Ember Ruin", D8,
     "Design 5 on a burnt scroll — scorched rim, soot speckle, glowing ember "
     "flecks, ash-darkened paper. Recovered-from-the-fire drama."),
]

# filter params — each sheet gets its own tear signature
FILTERS = {
    "torn-paper": dict(fid="torn6", freq="0.016 0.02",  oct=5, seed=7,  scale=34),
    "palm-leaf":  dict(fid="torn7", freq="0.008 0.055", oct=4, seed=21, scale=16),
    "charred":    dict(fid="torn8", freq="0.022 0.03",  oct=6, seed=13, scale=44),
}

# ---- write previews ---------------------------------------------------------
paths = []
for i, (slug, name, css, desc) in enumerate(DESIGNS, 1):
    css = css.replace("__GRAIN__", GRAIN)
    svg = SHEET_SVG.format(**FILTERS[slug]) if slug in FILTERS else ""
    html = page(css, svg)
    fn = f"design-{i}-{slug}.html"
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(html)
    paths.append((fn, i, name, desc))
    print(f"wrote {fn}  ({len(html)//1024} KB)")

# ---- gallery ----------------------------------------------------------------
cards = "\n".join(
    f'<a class="g" href="{fn}"><span class="n">Design {i}</span>'
    f'<h2>{name}</h2><p>{desc}</p><span class="go">Open preview →</span></a>'
    for fn, i, name, desc in paths)

gallery = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mythology to Meaning — {len(DESIGNS)} design concepts</title>{GOOGLE_FONTS}
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f4e4c1;color:#3a2416;font-family:"Spectral",Georgia,serif;
background-image:radial-gradient(ellipse 70% 55% at 12% 8%,rgba(255,244,214,.7),transparent 60%),
linear-gradient(105deg,#e0c48f,#f4e4c1 22%,#ecd6a8 78%,#e0c48f)}}
.wrap{{width:min(100% - 2rem,80rem);margin-inline:auto;padding:3rem 0}}
h1{{font-family:"Marcellus",serif;font-size:clamp(1.9rem,5vw,3rem);color:#6e1414;margin:0 0 .4rem;text-align:center}}
.sub{{text-align:center;color:#6b4a2e;font-style:italic;margin:0 0 2.5rem}}
.grid{{display:grid;gap:1.4rem;grid-template-columns:repeat(auto-fit,minmax(17rem,1fr))}}
.g{{display:block;text-decoration:none;color:inherit;padding:1.8rem 1.6rem;
background:linear-gradient(150deg,rgba(255,250,235,.6),rgba(232,196,143,.3));
border:1px solid rgba(110,20,20,.28);border-radius:3px;position:relative;
box-shadow:0 2px 0 rgba(110,20,20,.08);transition:transform .2s,border-color .2s}}
.g::before{{content:"";position:absolute;inset:8px;border:1px solid rgba(58,36,22,.14);pointer-events:none}}
.g:hover{{transform:translateY(-3px);border-color:#e8871e}}
.n{{font-size:.7rem;letter-spacing:.22em;text-transform:uppercase;color:#b3261e}}
.g h2{{font-family:"Marcellus",serif;font-size:1.35rem;color:#6e1414;margin:.4rem 0 .5rem}}
.g p{{margin:0 0 1rem;font-size:.95rem;color:#6b4a2e;line-height:1.6}}
.go{{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#e8871e;font-weight:600}}
.note{{text-align:center;margin-top:2.5rem;font-size:.9rem;color:#6b4a2e;font-style:italic}}
</style></head><body><div class="wrap">
<h1>Mythology to Meaning</h1>
<p class="sub">{len(DESIGNS)} design concepts for <b>mythstomeaning.meetgor.com</b> — each shown with real verse content. Designs 6–8 are the pattachitra language on real torn / palm-leaf / charred material.</p>
<div class="grid">{cards}</div>
<p class="note">Every preview is a self-contained HTML file — open them side by side to compare.</p>
</div></body></html>"""

open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(gallery)
print("wrote index.html (gallery)")
