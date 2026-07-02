#!/usr/bin/env python3
"""Build POLYPAD_ELA_STYLE_GUIDE.html — a single, self-contained, shareable
website synthesizing:
  - the original 178-slide audit,
  - the CKLA Drag & Drop Authoring Guide,
  - the K-5 Math Suite Design Handbook (Google Sites),
  - the 3 official ELA Polypad Templates (classroom collection).

Images are hosted on Polypad's public S3 (uploads.desmos.com) — no sign-in to
view. URL map read from style_guide_shots/all_shot_urls.json.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
URLS = json.loads((HERE / "style_guide_shots" / "all_shot_urls.json").read_text())

def U(key):
    """Public image URL for a given map key (raises if missing)."""
    if key not in URLS:
        raise KeyError(f"missing image url: {key}")
    return URLS[key]

# ---- Live activity links (classroom.amplify.com) --------------------------
COLLECTION = "https://classroom.amplify.com/collection/69373896be6a50328147f91a"
TPL_MATCHING = "https://classroom.amplify.com/activity/69376bdcd3cc4d18e424af23"
TPL_CATEGORIZE = "https://classroom.amplify.com/activity/693738c42be9046118d6c4d7"
TPL_TEXTDEMO = "https://classroom.amplify.com/activity/696138114d18ca974625ba94"

def act(aid, step=None):
    u = f"https://classroom.amplify.com/activity/{aid}"
    return u

# audit exemplar live links (activity ids from manifest.json)
LIVE = {
    "CardMatch_GOOD": act("68d0b806c14770d448f9d1c9"),
    "CardMatch_BAD": act("68d544fca02c96c77a29322b"),
    "CardSort_GOOD": act("68431bb2649c240f3e153232"),
    "CardSort_BAD": act("6a0b131c078646e7f0225b3d"),
    "Diagram_GOOD": act("68cb20f58a5c512eabecb205"),
    "Diagram_BAD": act("69839e011d1361a98005ff9e"),
    "FreeResponse_GOOD": act("6942e9ae9e3d5690a4cc498e"),
    "ZoomReader": act("68d2817c5b7e50d50f2fa0a7"),
    "Builder": act("69b06c38ee5f7353b189adb0"),
    "Debating": act("6916512883cfe080b649c6ed"),
    "Outbreak": act("696a63e96e980041b2f05a43"),
}

# reference source links
CKLA_SLIDES = "https://docs.google.com/presentation/d/1NqhJ3E2xGCSqh1r0SIR-k0IuUtCij-ubs_OPhWKdBaE"
GSITE_DROPZONES = "https://sites.google.com/amplify.com/k5mathsuitedesignstyleguide/k-5-authoring-guidelines/polypad-k-5/drop-zones-wip-k-5"
GSITE_INDEX = "https://sites.google.com/amplify.com/k5mathsuitedesignstyleguide/k-5-authoring-guidelines/polypad-k-5"

# script repo-relative links (these live in tools/)
SCRIPTS = {
    "audit_fix": "tools/audit_and_fix_style.py",
    "style_dropzones": "tools/style_dropzones_via_api.py",
    "disable_all": "tools/disable_all_via_api.py",
    "regen_thumbs": "tools/regen_thumbs_fast.py",
    "build_match": "tools/build_match_slide.py",
    "grab": "tools/grab_slide.py",
    "refresh_dropzones": "tools/refresh_dropzones.py",
}


# =========================================================================
#  HTML PIECES
# =========================================================================

CSS = """
:root{
  --ink:#1f2733; --muted:#5b6675; --line:#e3e8ef; --bg:#f7f9fc; --card:#fff;
  --brand:#0f82f2; --brand-d:#0a5fb4; --good:#1f9d63; --good-bg:#eafaf1;
  --warn:#d9822b; --warn-bg:#fdf3e7; --bad:#d64545; --bad-bg:#fdeded;
  --chip:#eef3fb; --accent:#dae3f0; --code:#0b1f33;
  --shadow:0 1px 2px rgba(16,32,54,.06),0 8px 24px rgba(16,32,54,.06);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased}
a{color:var(--brand-d);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
header.hero{background:linear-gradient(135deg,#0f82f2,#0a5fb4);color:#fff;padding:56px 0 48px}
header.hero .wrap{max-width:1080px}
header.hero h1{font-size:38px;line-height:1.15;margin:0 0 10px;font-weight:800;letter-spacing:-.02em}
header.hero p.sub{font-size:18px;opacity:.95;margin:0 0 20px;max-width:760px}
.pillrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.pill{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28);
  color:#fff;padding:5px 12px;border-radius:999px;font-size:13px;font-weight:600}
.layout{display:grid;grid-template-columns:236px 1fr;gap:36px;align-items:start;margin-top:36px}
nav.toc{position:sticky;top:20px;font-size:14px;background:var(--card);border:1px solid var(--line);
  border-radius:14px;padding:16px 14px;box-shadow:var(--shadow)}
nav.toc h4{margin:2px 0 10px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
nav.toc a{display:block;color:var(--ink);padding:5px 8px;border-radius:8px;font-weight:500}
nav.toc a:hover{background:var(--chip);text-decoration:none}
nav.toc a.sub{padding-left:20px;color:var(--muted);font-size:13px}
nav.toc a.sub2{padding-left:34px;color:var(--muted);font-size:12.5px;opacity:.9}
main{min-width:0;padding-bottom:80px}
section{margin:0 0 44px;scroll-margin-top:20px}
h2{font-size:27px;letter-spacing:-.01em;margin:0 0 6px;padding-top:14px;font-weight:800}
h2 .num{color:var(--brand);font-weight:800}
h3{font-size:20px;margin:26px 0 8px;font-weight:700}
h4{font-size:16px;margin:18px 0 6px;font-weight:700}
p{margin:8px 0}
.lede{font-size:17px;color:var(--muted);margin:0 0 6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 24px;
  box-shadow:var(--shadow);margin:16px 0}
.callout{border-left:4px solid var(--brand);background:#f0f7ff;border-radius:0 12px 12px 0;
  padding:12px 16px;margin:14px 0}
.callout.good{border-color:var(--good);background:var(--good-bg)}
.callout.warn{border-color:var(--warn);background:var(--warn-bg)}
.callout.bad{border-color:var(--bad);background:var(--bad-bg)}
.callout .t{font-weight:700;margin-bottom:2px}
code,kbd{font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;font-size:13.5px;
  background:#eef1f6;color:#0b3a63;padding:1.5px 6px;border-radius:6px}
pre{background:var(--code);color:#e7eef7;border-radius:12px;padding:16px 18px;overflow:auto;
  font-size:13px;line-height:1.55;margin:12px 0}
pre code{background:none;color:inherit;padding:0}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14.5px;background:var(--card);
  border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f2f6fc;font-weight:700;font-size:13px;letter-spacing:.01em}
tr:last-child td{border-bottom:none}
.swatch{display:inline-block;width:14px;height:14px;border-radius:4px;border:1px solid #cfd8e3;
  vertical-align:-2px;margin-right:6px}
.figure{margin:16px 0}
.figure img{width:100%;border:1px solid var(--line);border-radius:12px;display:block;background:#fff;box-shadow:var(--shadow)}
.figcap{font-size:13.5px;color:var(--muted);margin-top:8px}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:16px 0}
.compare .col{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}
.compare .col img{width:100%;display:block;border-bottom:1px solid var(--line);background:#fff}
.compare .col .body{padding:12px 15px}
.tag{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;
  padding:3px 9px;border-radius:999px;margin-bottom:6px}
.tag.good{background:var(--good-bg);color:var(--good)}
.tag.bad{background:var(--bad-bg);color:var(--bad)}
.tag.ref{background:var(--chip);color:var(--brand-d)}
.checklist{list-style:none;padding:0;margin:12px 0}
.checklist li{position:relative;padding:7px 0 7px 30px;border-bottom:1px dashed var(--line)}
.checklist li:before{content:"✓";position:absolute;left:2px;top:7px;color:var(--good);font-weight:800}
.checklist li:last-child{border-bottom:none}
.spec{display:grid;grid-template-columns:180px 1fr;gap:2px 16px;font-size:14.5px;margin:10px 0}
.spec dt{font-weight:700;color:var(--ink);padding:4px 0;border-bottom:1px solid var(--line)}
.spec dd{margin:0;padding:4px 0;border-bottom:1px solid var(--line);color:var(--muted)}
.btnlink{display:inline-flex;align-items:center;gap:6px;background:var(--brand);color:#fff;
  padding:6px 13px;border-radius:9px;font-size:13.5px;font-weight:700;margin:3px 6px 3px 0}
.btnlink:hover{background:var(--brand-d);text-decoration:none;color:#fff}
.btnlink.ghost{background:transparent;color:var(--brand-d);border:1.5px solid #cfe0f5}
.btnlink.ghost:hover{background:var(--chip);color:var(--brand-d)}
.scriptbox{background:#0b1f33;color:#dfe9f4;border-radius:12px;padding:14px 16px;margin:12px 0;font-size:14px}
.scriptbox .h{font-weight:800;color:#7fc0ff;margin-bottom:4px;font-size:13px;letter-spacing:.03em;text-transform:uppercase}
.scriptbox code{background:rgba(255,255,255,.1);color:#bfe0ff}
.scriptbox a{color:#8fd0ff}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.small{font-size:13.5px;color:var(--muted)}
.divider{height:1px;background:var(--line);margin:34px 0}
.kicker{font-size:12px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--brand);margin-bottom:2px}
.srcbadge{font-size:11px;font-weight:700;padding:2px 8px;border-radius:6px;background:var(--chip);color:var(--brand-d);margin-left:8px;vertical-align:middle}
footer{border-top:1px solid var(--line);padding:28px 0;color:var(--muted);font-size:14px}
@media(max-width:900px){.layout{grid-template-columns:1fr}nav.toc{position:static}.compare,.grid2{grid-template-columns:1fr}.spec{grid-template-columns:1fr}}
"""

def swatch(hexcode):
    return f'<span class="swatch" style="background:{hexcode}"></span>'

def script_ref(title, body_html):
    return f'<div class="scriptbox"><div class="h">🛠 In a fix script</div><div>{body_html}</div></div>'


# =========================================================================
#  CONTENT
# =========================================================================

def build_html():
    P = []  # page fragments
    a = P.append

    # ---------- HERO ----------
    a(f"""<header class="hero"><div class="wrap">
      <div class="kicker" style="color:#bfe0ff">Amplify · ELA Polypad</div>
      <h1>Polypad ELA Style Guide</h1>
      <p class="sub">One prescriptive reference for building and fixing ELA Polypad interactions.
      For every interaction design: what a correct screen looks like, the exact values it must carry,
      a real example you can open, and how to bring a non-conforming screen into line —
      by hand or with a script.</p>
      <div class="pillrow">
        <span class="pill">331 slides audited</span>
        <span class="pill">255 activities</span>
        <span class="pill">13 distinct designs · 6 families</span>
        <span class="pill">3 official templates</span>
        <span class="pill">CKLA + K-5 Design Handbook reconciled</span>
        <span class="pill">Auto-fix script included</span>
      </div>
    </div></header>""")

    a('<div class="wrap"><div class="layout">')

    # ---------- TOC (exact document order) ----------
    a("""<nav class="toc"><h4>On this page</h4>
      <a href="#how">How to use this guide</a>
      <a href="#sources">Where these rules come from</a>
      <a href="#universal">Universal rules (every screen)</a>
      <a href="#palette" class="sub">The ELA palette</a>
      <a href="#lockdown" class="sub">The lock-down profile</a>
      <a href="#types">Interaction designs — full catalog</a>
      <a href="#match" class="sub">Card Match</a>
      <a href="#design-claim-and-evidence" class="sub2">↳ Claim &amp; Evidence</a>
      <a href="#design-ranking--continuum" class="sub2">↳ Ranking / Continuum</a>
      <a href="#design-rhetorical-appeals" class="sub2">↳ Rhetorical Appeals</a>
      <a href="#sort" class="sub">Card Sort</a>
      <a href="#design-compare-and-contrast" class="sub2">↳ Compare &amp; Contrast</a>
      <a href="#design-timeline--sequence" class="sub2">↳ Timeline / Sequence</a>
      <a href="#organizer" class="sub">Graphic Organizer</a>
      <a href="#design-venn-diagram" class="sub2">↳ Venn Diagram</a>
      <a href="#design-story--plot-map" class="sub2">↳ Story / Plot Map</a>
      <a href="#design-multi-zone-organizer" class="sub2">↳ Multi-zone Organizer</a>
      <a href="#free" class="sub">Free Response</a>
      <a href="#zoom" class="sub">Zoom Reader</a>
      <a href="#builder" class="sub">Sentence Builder</a>
      <a href="#dropzones">Drop-zone deep dive</a>
      <a href="#canvas">Canvas &amp; viewport</a>
      <a href="#fixscript">The auto-fix script</a>
      <a href="#appendix">Appendix — what to avoid</a>
    </nav>""")

    a('<main>')

    # ---------- HOW TO USE ----------
    a(f"""<section id="how">
      <h2><span class="num">§</span> How to use this guide</h2>
      <p class="lede">Read top-to-bottom once. After that, jump to the interaction type you're building.</p>
      <div class="card">
      <p>Each interaction type has the same four parts, in this order:</p>
      <ol>
        <li><b>Plain-language name &amp; when to use it</b> — how to describe it in a ticket or to a teacher.</li>
        <li><b>The intended look</b> — the best real example, embedded, with a link to open it live.</li>
        <li><b>The spec that must be true every time</b> — exact colors, sizes, layout, validation, lock-down.</li>
        <li><b>How to conform a non-standard screen</b> — a step-by-step you can do by hand <i>or</i> run as a
        script. Script steps link straight to the tool that performs them.</li>
      </ol>
      <p class="small">"Should be there every time" items are written as a checklist. A screen that fails any
      checklist item is <b>non-conforming</b> and is a candidate for the <a href="#fixscript">auto-fix pass</a>.</p>
      </div>
    </section>""")

    # ---------- SOURCES ----------
    a(f"""<section id="sources">
      <h2><span class="num">§</span> Where these rules come from</h2>
      <p class="lede">Four sources, reconciled. When they disagree, the order below wins for ELA.</p>
      <table>
        <tr><th>Rank</th><th>Source</th><th>What it governs</th><th>Authority for ELA</th></tr>
        <tr><td><b>1</b></td><td><a href="{COLLECTION}">ELA Polypad Templates collection</a>
          — the three official templates (Caitlyn Burns, David Poras)</td>
          <td>The real, shipping ELA look: cream canvas, card &amp; zone styling, "Screen&nbsp;2" authoring rules.</td>
          <td><b>Primary.</b> These are ELA-authored and ELA-approved.</td></tr>
        <tr><td><b>2</b></td><td><a href="{CKLA_SLIDES}">CKLA Drag &amp; Drop Authoring Guide</a> (Dec 2024)</td>
          <td>Exact numeric spec for Matching / Sorting / Ordering drag-drop.</td>
          <td>Fills gaps the templates leave (focus states, spacing grid).</td></tr>
        <tr><td><b>3</b></td><td><a href="{GSITE_INDEX}">K-5 Math Suite Design Handbook</a> (Google Sites)</td>
          <td>The design-system layer: named color tokens, use-case→layout map, canvas sizes, action-bar lock-down.</td>
          <td>Adopt the <i>discipline</i> and mechanics; ELA keeps its own palette.</td></tr>
        <tr><td><b>4</b></td><td>The full catalog audit — <b>331 slides across all 255 activities</b>
          (ELA + Caminos + Language&nbsp;Studio)</td>
          <td>What is actually shipping today, every way it drifts, and every distinct design
          (see the <a href="#types">design catalog</a>).</td>
          <td>Tells us what to fix — not what's correct.</td></tr>
      </table>
      <div class="callout"><div class="t">The one thing to internalize</div>
      The ELA templates and the K-5 math handbook use <b>different palettes</b>. ELA screens are built on a
      warm cream canvas with pale-blue zones; the K-5 math handbook uses a cool Gray/Blue token system.
      This guide follows the <b>ELA templates</b> for color, and borrows the handbook's <b>rules and mechanics</b>
      (layout per use case, lock-down procedure, "starting drop zone"). Don't paste math tokens into ELA screens.</div>
    </section>""")

    # ---------- UNIVERSAL RULES ----------
    a(f"""<section id="universal">
      <h2><span class="num">§</span> Universal rules — true on every ELA screen</h2>
      <p class="lede">These apply regardless of interaction type. If a screen breaks one of these, fix it first.</p>
      <ul class="checklist">
        <li>The Polypad sits in the <b>right column</b> of the step; the prompt lives in the <b>subtitle</b> so
          the two components align vertically. <span class="srcbadge">ELA templates, Screen&nbsp;2</span></li>
        <li>Text and card <b>sizes are not edited</b> from the template. If your text overflows a card, reword it
          or choose a different template — never stretch the card. <span class="srcbadge">ELA templates</span></li>
        <li>Titles above drop zones <b>do not overlap the reset button.</b> <span class="srcbadge">ELA templates</span></li>
        <li>The action bar is <b>locked down</b> — see the profile below. No stray math/geometry tools, no eraser
          unless the task needs sketch. <span class="srcbadge">K-5 Handbook · Audit</span></li>
        <li>Every draggable is <b>Stay-in-Dropzones ON</b> and <b>not editable / not deletable.</b></li>
        <li>The canvas uses <b>one house background</b> (never left transparent, never a random hand-typed hex).</li>
        <li>Validation is either <b>fully wired or intentionally absent</b> — never a mix of validated and
          unvalidated answer zones on the same screen. <span class="srcbadge">Audit finding C3</span></li>
      </ul>

      <h3 id="palette">The ELA palette</h3>
      <p>Taken directly from the official templates. Use these exact hexes. Do not import the K-5 math tokens
        (Gray-07, Blue-02) into ELA screens — they're a different, cooler system.</p>
      <table>
        <tr><th>Role</th><th>Value</th><th>Where</th></tr>
        <tr><td>Canvas background (Matching)</td><td>{swatch('#fff8e9')}<code>#fff8e9</code> cream</td>
          <td>Polypad <code>options.background</code></td></tr>
        <tr><td>Answer drop zone — border</td><td>{swatch('#b0bed2')}<code>#b0bed2</code>, <b>dashed</b>, weight&nbsp;2</td>
          <td>categorizer with <code>validation:"match"</code>, white fill</td></tr>
        <tr><td>Source / home drop zone — fill</td><td>{swatch('#b0bed3')}<code>#b0bed3</code>, <b>solid</b>, weight&nbsp;2</td>
          <td>categorizer with <code>validation:"none"</code></td></tr>
        <tr><td>Draggable card — fill / border</td><td>{swatch('#ffffff')}<code>#ffffff</code> / {swatch('#b0bed3')}<code>#b0bed3</code> border, weight&nbsp;1</td>
          <td>text tile, <code>cornerRadius:10</code></td></tr>
        <tr><td>Card text</td><td>{swatch('#111111')}<code>#111111</code></td><td>tile <code>color</code></td></tr>
        <tr><td>Row / accent band</td><td>{swatch('#d1e4f7')}<code>#d1e4f7</code> fill, {swatch('#a4caf0')}<code>#a4caf0</code> stroke, locked</td>
          <td>decorative <code>rectangle</code> behind matched pairs</td></tr>
        <tr><td>Step (AB) background</td><td>warm gradient e.g. <code>#fff8e9 → #f1e4c3</code></td>
          <td>step <code>background.value</code></td></tr>
        <tr><td>Primary button (if used)</td><td>{swatch('#0f82f2')}<code>#0f82f2</code></td>
          <td>Check / primary action <span class="srcbadge">= K-5 primary token RGB(15,130,242)</span></td></tr>
      </table>
      <div class="callout warn"><div class="t">The <code>#b0bed2</code> vs <code>#b0bed3</code> question — settled</div>
        Earlier the audit treated <code>#b0bed2</code> as a one-digit typo of <code>#b0bed3</code>. The official
        template proves otherwise: <b>both are intentional.</b> <code>#b0bed2</code> is the <b>dashed answer-zone
        border</b>; <code>#b0bed3</code> is the <b>solid source-zone fill and the card border</b>. The real defect
        is when either value lands on the <i>wrong</i> role, or drifts to grey/near-black
        (<code>#242436</code>, <code>#111111</code> as a <i>zone fill</i>).</div>

      <h3 id="lockdown">The lock-down profile</h3>
      <p>Every ELA Polypad ships with the tool UI locked. The procedure (from the K-5 Handbook) is
        <b>Disable All, then re-enable only what the task needs.</b></p>
      <div class="spec">
        <dt>actionbar</dt><dd><code>"hidden"</code> for drag-drop / free-response. Never the full math/geo enum.</dd>
        <dt>toolbar</dt><dd><code>"hidden"</code>. Re-enable <code>eraser</code>/pen only for genuine sketch tasks.</dd>
        <dt>grid</dt><dd><code>"none"</code> for ELA content screens (templates ship gridless).</dd>
        <dt>noPinchPan</dt><dd><code>true</code> on fixed-viewport screens (K-3 find pan/zoom confusing).</dd>
        <dt>noUndoRedo</dt><dd><code>true</code> unless the task is step-by-step sketch.</dd>
        <dt>delete on tiles</dt><dd>OFF — students must not be able to delete cards or the card bank.</dd>
      </div>
      <div class="figure">
        <img src="{U('gsite/gsite_action_bars_img07.png')}" alt="Disable-all then toggle on needed tools">
        <div class="figcap"><span class="tag ref">K-5 Handbook</span> The lock-down procedure: click
          <b>Disable All</b>, then toggle on only the tools the interaction needs.
          <a href="{GSITE_INDEX}">Source ↗</a></div>
      </div>
      {script_ref("", f'''Apply the lock-down profile to every screen in an activity by copying a clean
        screen's <code>options</code> to all others: <a href="{SCRIPTS['disable_all']}">disable_all_via_api.py</a>.
        The <a href="#fixscript">auto-fix pass</a> also normalizes <code>actionbar</code>/<code>toolbar</code>
        to <code>"hidden"</code> and strips stray tool enums.''')}
    </section>""")

    # ---------- INTERACTION DESIGNS INTRO ----------
    a(f"""<section id="types">
      <h2><span class="num">§</span> Interaction designs — the full catalog</h2>
      <p class="lede">Every ELA Polypad screen is one of these designs. The <b>331-slide audit clusters into
        13 distinct designs</b>, organized under <b>six interaction families</b>. Each family has a full spec;
        its named ELA <i>variants</i> (same mechanism, specialized task) are expanded right inside that family's
        section. Jump to any design below.</p>
      <table>
        <tr><th>Family</th><th>Count</th><th>Named variants (nested in the section)</th></tr>
        <tr><td><a href="#free"><b>Free Response</b></a> — type an answer</td><td>132×</td>
          <td class="small">—</td></tr>
        <tr><td><a href="#match"><b>Card Match</b></a> — one answer per question</td><td>53×+</td>
          <td class="small"><a href="#design-claim-and-evidence">Claim &amp; Evidence</a> ·
            <a href="#design-ranking--continuum">Ranking / Continuum</a> ·
            <a href="#design-rhetorical-appeals">Rhetorical Appeals</a></td></tr>
        <tr><td><a href="#sort"><b>Card Sort</b></a> — organize into categories</td><td>7×+</td>
          <td class="small"><a href="#design-compare-and-contrast">Compare &amp; Contrast</a> ·
            <a href="#design-timeline--sequence">Timeline / Sequence</a></td></tr>
        <tr><td><a href="#organizer"><b>Graphic Organizer</b></a> — label a diagram</td><td>14×+</td>
          <td class="small"><a href="#design-venn-diagram">Venn Diagram</a> ·
            <a href="#design-story--plot-map">Story / Plot Map</a> ·
            <a href="#design-multi-zone-organizer">Multi-zone Organizer</a></td></tr>
        <tr><td><a href="#free"><b>Free Response</b></a> (input fields)</td><td>—</td>
          <td class="small">see above</td></tr>
        <tr><td><a href="#zoom"><b>Zoom Reader</b></a> — read / scroll a sequence</td><td>—</td>
          <td class="small">—</td></tr>
        <tr><td><a href="#builder"><b>Sentence Builder</b></a> — assemble word tiles</td><td>23×</td>
          <td class="small">—</td></tr>
      </table>
      <p class="small">Spanish (Caminos / Language Studio) exemplars are equal value to English — the "best
        example" for each design is simply the cleanest one, regardless of language. <b>Note:</b> there is
        <b>no true KWL chart</b> in the catalog — the overlap organizer people mean by that is the
        <a href="#design-venn-diagram">Venn Diagram</a>.</p>
    </section>""")

    # =====================================================================
    # helper for a full interaction section
    # =====================================================================
    def interaction(idnum, anchor, name, tagline, when, best_img, best_cap, best_live,
                    spec_rows, checklist_items, fix_steps, compare=None, extra=""):
        h = []
        h.append(f'<section id="{anchor}"><h2><span class="num">{idnum}</span> &nbsp;{name}</h2>')
        h.append(f'<p class="lede">{tagline}</p>')
        h.append(f'<div class="callout"><div class="t">When to use it</div>{when}</div>')
        # best example
        h.append(f'<h3>The intended look</h3>')
        h.append(f'''<div class="figure"><img src="{best_img}" alt="{name} intended example">
          <div class="figcap"><span class="tag good">Intended style</span> {best_cap}
          &nbsp;<a class="btnlink" href="{best_live}">Open live ↗</a></div></div>''')
        # spec
        h.append(f'<h3>Spec — true every time</h3><div class="spec">')
        for dt, dd in spec_rows:
            h.append(f'<dt>{dt}</dt><dd>{dd}</dd>')
        h.append('</div>')
        # checklist
        h.append('<h4>Conformance checklist</h4><ul class="checklist">')
        for c in checklist_items:
            h.append(f'<li>{c}</li>')
        h.append('</ul>')
        # compare good/bad
        if compare:
            gimg, gcap, glive, bimg, bcap, blive = compare
            h.append(f'''<h4>Conforming vs. non-conforming (from the audit)</h4>
              <div class="compare">
                <div class="col"><img src="{gimg}" alt="conforming">
                  <div class="body"><span class="tag good">Conforming</span><p class="small">{gcap}</p>
                  <a href="{glive}">Open live ↗</a></div></div>
                <div class="col"><img src="{bimg}" alt="non-conforming">
                  <div class="body"><span class="tag bad">Non-conforming</span><p class="small">{bcap}</p>
                  <a href="{blive}">Open live ↗</a></div></div>
              </div>''')
        # fix steps
        h.append('<h4>How to conform a non-standard screen</h4>')
        h.append(fix_steps)
        h.append(extra)
        # nested named variants of THIS family (integrated — no separate gallery)
        h.append(FAMILY_VARIANTS.get(f"#{anchor}", ""))
        h.append('</section>')
        return "".join(h)

    # ----- 1. CARD MATCH -----
    a(interaction(
        1, "match", "Card Match",
        "Drag one card to the box beside each prompt. One answer per question, one-to-one.",
        "Use when there is <b>exactly one correct answer per question</b> — matching a quotation to a "
        "technique, a term to a definition, a cause to an effect.",
        U('template/Matching__template__2col_match.png'),
        "The official <b>Matching</b> template. Left: prompt cards on a pale-blue <code>#d1e4f7</code> band. "
        "Center: dashed white answer zones (<code>#b0bed2</code>). Right: the source cards to drag. "
        "Clean cream canvas, no toolbar.",
        TPL_MATCHING,
        spec_rows=[
            ("Answer zone", f"{swatch('#b0bed2')}<code>#b0bed2</code> border, <b>dashed</b>, weight 2, white fill, "
             "<code>layout:\"center\"</code>, <code>cornerRadius:10</code>, <code>validation:\"match\"</code>"),
            ("Source/home zone", f"{swatch('#b0bed3')}<code>#b0bed3</code> solid fill, weight 2, "
             "<code>layout:\"center\"</code>, <code>validation:\"none\"</code>"),
            ("Cards", f"white fill, {swatch('#b0bed3')}<code>#b0bed3</code> border weight 1, "
             "<code>cornerRadius:10</code>, text <code>#111111</code>, <code>editable:false</code>, "
             "<code>stayInDropzones:true</code>"),
            ("Zone count", "One answer zone per prompt. <b>Every</b> answer zone validated — never 3 of 4."),
            ("Canvas", f"{swatch('#fff8e9')}<code>#fff8e9</code>, grid none, actionbar + toolbar hidden"),
            ("Validation", "Wired after editing — each answer zone gets a captured <code>storedSolution</code>. "
             "A Check button is optional in ELA (many screens self-validate on drop)."),
        ],
        checklist_items=[
            "Every answer zone has <code>validation:\"match\"</code> with a stored solution — none left <code>none</code>.",
            "Answer zones are dashed <code>#b0bed2</code>; source zones are solid <code>#b0bed3</code>.",
            "Cards are white with a <code>#b0bed3</code> border, radius 10, not editable, Stay-in-Dropzones on.",
            "No off-screen tiles; the initial viewport frames all content with margin.",
            "actionbar &amp; toolbar hidden; canvas <code>#fff8e9</code>.",
            "Card text fits its card without resizing the card.",
        ],
        fix_steps=f"""<ol>
          <li><b>Grab it.</b> <code>python <a href="{SCRIPTS['grab']}">grab_slide.py</a> &lt;activity-url&gt;</code>
            dumps every screen's <code>polypadState</code>.</li>
          <li><b>Classify zones.</b> Any categorizer with <code>validation</code> match/compare, or the upper of a
            stacked pair, is an <b>answer (drag-TO)</b> zone; the rest are <b>source (drag-FROM)</b>.
            The <a href="{SCRIPTS['style_dropzones']}">style_dropzones_via_api.py</a> heuristic already does this.</li>
          <li><b>Restyle.</b> Answer → dashed <code>#b0bed2</code>/white; source → solid <code>#b0bed3</code>.
            Set card fill/border/radius. Lock text (<code>editable:false</code>, <code>stayInDropzones:true</code>).</li>
          <li><b>Fill validation gaps.</b> For any answer zone missing a solution, capture the correct card into
            <code>storedSolution</code> (see <a href="{SCRIPTS['build_match']}">build_match_slide.py</a> for the
            exports+wrapper-script pattern).</li>
          <li><b>Lock down + re-thumbnail.</b> <a href="{SCRIPTS['disable_all']}">disable_all_via_api.py</a> then
            <a href="{SCRIPTS['regen_thumbs']}">regen_thumbs_fast.py</a>.</li>
        </ol>
        {script_ref("", f'''One command does steps 2–5 across a whole activity:
          <code>python <a href="{SCRIPTS['audit_fix']}">audit_and_fix_style.py</a> &lt;url&gt; --fix</code>.
          It reports each deviation, applies the ELA palette, and re-thumbnails.''')}""",
        compare=(
            U('audit/CardMatch__GOOD__meet-polyphemus-4-zones-validated-clean.png'),
            "<i>Meet Polyphemus</i> — all four rows validated, clean layout.",
            LIVE['CardMatch_GOOD'],
            U('audit/CardMatch__INCONSISTENT__diff-dreams-only-3-zones-validated-butto.png'),
            "<i>Different Dreams</i> — only 3 of 4 rows validated; Check button shoved off to a corner.",
            LIVE['CardMatch_BAD'],
        ),
    ))

    # ----- 2. CARD SORT -----
    a(interaction(
        2, "sort", "Card Sort",
        "Drag many cards into a few category bins. Many-to-one; order inside a bin doesn't matter.",
        "Use when students <b>organize information into 2 (sometimes 3) categories</b> — sorting evidence, "
        "classifying examples, grouping by theme.",
        U('template/TextIntoPolypad__inputfields.png'),
        "The cleanest sort in the collection (from David Poras's demo): two dashed white category zones "
        "(<i>\"Telling\"</i> / <i>\"Showing\"</i>) with a grey source bin of pale-blue cards below.",
        TPL_TEXTDEMO,
        spec_rows=[
            ("Category zones", f"dashed border, white fill, {swatch('#b0bed2')}<code>#b0bed2</code>, "
             "<code>layout:\"flow\"</code> (multiple cards land inside), radius 10"),
            ("Source bin", f"one grey bin holding all cards, <code>layout:\"flow\"</code>, "
             f"padding 40 so cards space out; fill {swatch('#eeeeee')} light grey or {swatch('#b0bed3')}"),
            ("Cards", "consistent sizes, white or pale-blue fill, radius 10, cannot copy/delete, "
             "Stay-in-Dropzones on"),
            ("Zone sizing", "Zones sized for <b>more</b> answers than expected — sorting is many-to-one."),
            ("Canvas", "cream/white, grid none, actionbar + toolbar hidden"),
            ("Validation", "wired after editing, or intentionally a self-check — applied <b>uniformly</b>."),
        ],
        checklist_items=[
            "Category zones use Flow layout (not Center) so multiple cards fit.",
            "Exactly one source bin; all cards start inside it (or in home placeholders).",
            "Cards are a consistent size and cannot be copied or deleted.",
            "No leaked math/geo actionbar or eraser toolbar (a real defect even in the Categorize template).",
            "If validated, every category zone is validated — no partial wiring.",
        ],
        fix_steps=f"""<ol>
          <li><b>Confirm it's really a sort.</b> If it's built as a free-form organizer but the content is a clean
            2-category sort, rebuild it on the <a href="{TPL_CATEGORIZE}">Categorize &amp; Organize</a> template
            (audit finding H1).</li>
          <li><b>Fix layout mode.</b> Category zones must be <code>layout:"flow"</code>, not <code>center</code>.</li>
          <li><b>Consolidate the source.</b> One bin, Flow, padding 40; all cards inside with Stay-in-Dropzones on.</li>
          <li><b>Strip the toolbar.</b> The Categorize template itself leaks <code>geo-midpoint</code> +
            <code>eraser</code> — set actionbar/toolbar to hidden.</li>
          <li><b>Lock down + re-thumbnail</b> as above.</li>
        </ol>
        {script_ref("", f'''<code>audit_and_fix_style.py</code> classifies the bins, forces Flow on multi-card
          zones, wires Return-to-Dropzone on source cards, and strips the toolbar. See also
          <a href="{SCRIPTS['refresh_dropzones']}">refresh_dropzones.py</a> for re-flowing after a resize.''')}""",
        compare=(
            U('audit/CardSort__GOOD__phineas-should-ve-been-dead-match-check-.png'),
            "<i>Phineas Should've Been Dead</i> — blue-dashed source → grey targets, match validation + check.",
            LIVE['CardSort_GOOD'],
            U('audit/CardSort__INCONSISTENT__world-of-chocolate-activating-3categorie.png'),
            "<i>World of Chocolate</i> — no validation, no check, full math toolbar exposed.",
            LIVE['CardSort_BAD'],
        ),
    ))

    # ----- 3. GRAPHIC ORGANIZER -----
    a(interaction(
        3, "organizer", "Graphic Organizer",
        "Drag labels or evidence onto the right region of a diagram — a Hero's-Journey wheel, a Venn diagram, a story map.",
        "Use when placement is <b>spatial and meaningful</b> — the diagram itself carries information and cards "
        "land in named regions. Often un-scored (spatial judgment) rather than match-validated.",
        U('audit/Diagram__GOOD__hero-s-journey-structure-diagram-card-ba.png'),
        "<i>Hero's Journey Structure</i> — an illustrated wheel on one tan background, labeled drop slots, and a "
        "clear Card Bank. The most cohesive organizer in the catalog.",
        LIVE['Diagram_GOOD'],
        spec_rows=[
            ("Diagram", "a single background <code>image</code>, <code>status:\"locked\"</code> — students can't move it"),
            ("Slots", "categorizers positioned over regions; <code>layout:\"center\"</code> (one label per region) "
             "or <code>\"none\"</code> for free placement"),
            ("Card Bank", "one labeled source area; cards Stay-in-Dropzones on, <b>delete removed from actionbar</b> "
             "so the bank can't be deleted (audit finding H4)"),
            ("Consistency", "fixed vs. unlimited cards decided once and kept identical across copies (finding C5)"),
            ("Canvas", "one house background; no leaked toolbar; grid none"),
        ],
        checklist_items=[
            "Diagram image is locked and can't be dragged or deleted.",
            "The Card Bank and its cards can't be deleted (no <code>delete</code> in actionbar).",
            "Every copy of the organizer uses the same fixed/unlimited card behavior.",
            "One background color; no mixed zone styles or oversized headings.",
            "Slots are visually consistent (same stroke/fill), not a mix of blue-dashed and grey-solid.",
        ],
        fix_steps=f"""<ol>
          <li><b>Lock the furniture.</b> Set the diagram image and Card Bank to <code>status:"locked"</code>;
            remove <code>delete</code> from the actionbar enum.</li>
          <li><b>Unify slot styling.</b> Give every slot the same stroke/fill (dashed <code>#b0bed2</code> for
            drop targets); purge near-black and off-palette blues/golds.</li>
          <li><b>Normalize the heading.</b> One title size — don't leave a stray <code>fontSize:5</code>.</li>
          <li><b>Set one background</b> and lock down the toolbar.</li>
        </ol>
        {script_ref("", f'''The auto-fix pass restyles categorizer slots to the ELA palette and locks text/furniture.
          Slot <i>positioning</i> over a diagram is layout-specific — do that by hand, then run
          <a href="{SCRIPTS['regen_thumbs']}">regen_thumbs_fast.py</a>.''')}""",
        compare=(
            U('audit/Diagram__GOOD__hero-s-journey-structure-diagram-card-ba.png'),
            "<i>Hero's Journey</i> — cohesive wheel + card bank on one tan background.",
            LIVE['Diagram_GOOD'],
            U('audit/Diagram__INCONSISTENT__venn-diagram-reading-mixed-zone-styles-f.png'),
            "<i>Venn Diagram</i> — drawn as rectangles not circles, off-palette strokes, oversized heading, bare boxes.",
            LIVE['Diagram_BAD'],
        ),
    ))

    # ----- 4. FREE RESPONSE -----
    a(interaction(
        4, "free", "Free Response",
        "Type an answer into a box. No dragging — students write. The most consistent pattern in the catalog.",
        "Use when the answer is <b>constructed text</b> — definitions, short responses, notes. Two labeled "
        "columns with input fields, or a single passage + response.",
        U('template/TextIntoPolypad__passage_match.png'),
        "The <b>Text-into-Polypad</b> demo (David Poras): text pulled into Polypad via the CL sink, with input "
        "fields and passage components. This is the modern ELA free-response pattern.",
        TPL_TEXTDEMO,
        spec_rows=[
            ("Input fields", "<code>question-blank</code> tiles or CL input fields; non-editable prompt text, "
             "editable answer field"),
            ("Text layouts", "Auto-height (left-aligned, nothing fixed) · Fixed (center-aligned, width fixed) · "
             "Scrollable (left-aligned, W/H fixed) — pick one per box and keep it consistent"),
            ("Text styling", "author may set Fill, Stroke, Text color, Corner Radius, Drop Shadow"),
            ("CL niceties", "placeholder text via CL; <code>resetOnChange</code> when a field should clear on edit"),
            ("Canvas", f"{swatch('#ffffff')}white, actionbar + toolbar hidden — the gold-standard lock-down"),
        ],
        checklist_items=[
            "White background, everything hidden — borrow this options profile for other types too.",
            "Prompt text is non-editable; only the answer field accepts input.",
            "One text-layout mode per box (don't mix Fixed and Scrollable arbitrarily).",
            "No categorizers, no stray script unless CL placeholder/reset is intended.",
        ],
        fix_steps=f"""<ol>
          <li><b>Adopt the ELD/Text-into-Polypad options profile</b> ({swatch('#ffffff')}white, all hidden) as the
            baseline — it's the cleanest in the whole catalog.</li>
          <li><b>Lock the prompts.</b> Prompt text <code>editable:false</code>; only input fields editable.</li>
          <li><b>Pick one text layout</b> per box and normalize color to a single value.</li>
        </ol>
        {script_ref("", f'''Free-response screens rarely need geometry fixes — the auto-fix pass mainly normalizes
          the options profile and text-tile lock status here.''')}""",
        extra=f"""<div class="figure"><img src="{U('audit/FreeResponse__GOOD__responding-to-passage-1-eld-gold-standar.png')}"
            alt="ELD Responding to Passage gold standard">
          <div class="figcap"><span class="tag good">Gold standard</span> <i>Responding to Passage&nbsp;1</i> (ELD) —
            two labeled columns, four input fields, white background, everything hidden. Identical across hundreds
            of reuses. <a href="{LIVE['FreeResponse_GOOD']}">Open live ↗</a></div></div>""",
    ))

    # ----- 5. ZOOM READER -----
    a(interaction(
        5, "zoom", "Zoom Reader",
        "Read or scroll through a sequence of panels; tap to zoom in. Passive — no answer to submit.",
        "Use for <b>graphic-novel spreads, scavenger-hunt panels, or long illustrated passages</b> where the "
        "student reads and zooms rather than manipulates.",
        U('audit/ZoomReader__INCONSISTENT__odyssey-graphic-novel-tall-stacked-image.png'),
        "<i>Odyssey graphic novel</i> — nine image panels stacked in one tall column with a single zoom "
        "interaction. This pattern works, but has no shared template yet — each screen is hand-built.",
        LIVE['ZoomReader'],
        spec_rows=[
            ("Panels", "stacked <code>image</code> tiles in one column, locked"),
            ("Interaction", "a single <code>zoom</code> interaction; optional <code>geo</code> hotspots"),
            ("Column width", "define one column width and reuse it across every screen in the set"),
            ("Canvas", "one background; pan/zoom allowed here (this is the one type where pan is expected)"),
        ],
        checklist_items=[
            "Panels are locked images in a single consistent-width column.",
            "One zoom interaction pattern reused across the whole set (not re-invented per screen).",
            "One background color across all screens in the sequence.",
            "Pan/zoom intentionally enabled (unlike the fixed-viewport drag-drop screens).",
        ],
        fix_steps=f"""<p>This type has <b>no shared template today</b> — the fix is to define one and apply it across
          the set. Until then, the auto-fix pass will lock the images and normalize the background, but the
          column width and zoom wiring should be standardized by hand.</p>
        {script_ref("", "The auto-fix pass locks image tiles and sets one background; it does not touch the zoom "
                    "interaction (type-specific). Flag Zoom Readers as <i>needs a template</i>.")}""",
    ))

    # ----- 6. SENTENCE BUILDER -----
    a(interaction(
        6, "builder", "Sentence Builder",
        "Drag word tiles into a frame to build a sentence. Uses Polypad's letter tiles with built-in pronunciation.",
        "Use for <b>sentence construction, word ordering, or fill-the-frame</b> tasks — common in ELD English "
        "Building Blocks (EBB).",
        U('audit/Builder__INCONSISTENT__ebb-compound-sentences-letter-tiles-no-v.png'),
        "<i>EBB Compound Sentences</i> — draggable <code>letter</code> word-tiles into Flow frames. The pattern "
        "is sound; it currently ships unvalidated.",
        LIVE['Builder'],
        spec_rows=[
            ("Word tiles", "<code>letter</code> tiles (built-in pronunciation, <code>voice</code>) — "
             "strict schema: only name/text/voice/sense/POS/altPron"),
            ("Frames", "categorizer frames, <code>layout:\"flow\"</code> so words line up"),
            ("Validation", "decide self-check vs. graded; if graded, add <code>match</code> + a check button"),
            ("Canvas", "one background; toolbar hidden"),
        ],
        checklist_items=[
            "Word tiles use the strict letter-tile schema (extra fields silently drop the tile).",
            "Frames are Flow layout so multiple words fit in order.",
            "Validation decision is explicit — either wired, or intentionally a self-check.",
            "Toolbar hidden; one background.",
        ],
        fix_steps=f"""<ol>
          <li><b>Decide graded vs. self-check.</b> If graded, add <code>match</code> validation to the frame and a
            Check button (<a href="{SCRIPTS['build_match']}">build_match_slide.py</a> shows the words-mode wiring).</li>
          <li><b>Verify the letter-tile schema</b> — strip any non-schema fields.</li>
          <li><b>Flow the frames</b> and lock down the toolbar.</li>
        </ol>
        {script_ref("", "The auto-fix pass normalizes frame layout and toolbar; it will NOT invent validation "
                    "(that's an authoring decision). It flags unvalidated builders for review.")}""",
    ))

    # (Named variants are now nested INSIDE each family section above — no separate gallery.)

    # ---------- DROP-ZONE DEEP DIVE ----------
    a(f"""<section id="dropzones">
      <h2><span class="num">§</span> Drop-zone deep dive</h2>
      <p class="lede">Drop zones (categorizers) are where most inconsistency lives. Get these right and half the
        catalog's problems disappear.</p>

      <h3>Use case → layout (from the K-5 Handbook)</h3>
      <table>
        <tr><th>Use case</th><th>Layout</th><th>Notes</th></tr>
        <tr><td>Selecting &amp; sorting assets</td><td><code>flow</code></td><td>multiple cards land loosely</td></tr>
        <tr><td>Filling in an area</td><td><code>none</code> + tile snapping</td><td>cards snap to a region</td></tr>
        <tr><td>Word bank</td><td><code>center</code> + 1-tile limit</td><td>one word per slot</td></tr>
        <tr><td>Card sort (general)</td><td><code>flow</code></td><td>many-to-one bins</td></tr>
        <tr><td>Ordering</td><td><code>center</code> + 1-tile limit</td><td>one card per position</td></tr>
        <tr><td>Card sort (draw from a pile)</td><td><code>center</code> + limit = # cards</td><td>diagonal-stacked pile</td></tr>
      </table>

      <h3>The "starting drop zone" pattern</h3>
      <p>Cards should <b>start inside an invisible home zone</b>, not loose on the canvas. Turn <b>Visible OFF</b>,
        <b>Stay-in-Dropzones ON</b>, Center layout with a tile limit equal to the number of cards. This means a
        card is always <i>in</i> a zone — home or answer — so validation works either way, and click-to-place
        lights up every hover state (including the invisible home).</p>
      <div class="figure"><img src="{U('template/TextIntoPolypad__passage_match.png')}"
          alt="starting drop zone pattern">
        <div class="figcap"><span class="tag ref">ELA template</span> Grey home placeholders on the left hold the
          answer cards; the source bin at the bottom holds the draggables. Every card starts in a zone.</div></div>

      <h3>Focus &amp; spacing (from CKLA)</h3>
      <div class="spec">
        <dt>Focus state</dt><dd>teal {swatch('#269988')}<code>#269988</code> when a card hovers a valid zone</dd>
        <dt>Spacing</dt><dd>4 grid-tiles label↔zone and zone↔draggable; 2 between draggables (3/2 on half-screen)</dd>
        <dt>Corner radius</dt><dd>ELA templates use <code>10</code> px on zones &amp; cards</dd>
        <dt>Zone sizing</dt><dd>placeholder sized to the draggable it holds; leave room for more answers than expected</dd>
      </div>
      {script_ref("", f'''<code>audit_and_fix_style.py</code> classifies every categorizer (answer vs. source vs.
        generator), applies the correct fill/stroke/layout, wires Stay-in-Dropzones + Return-to-Dropzone on source
        cards, and syncs <code>storedSolution</code> for cloned chips. It reuses the proven logic in
        <a href="{SCRIPTS['style_dropzones']}">style_dropzones_via_api.py</a>.''')}
    </section>""")

    # ---------- CANVAS & VIEWPORT ----------
    a(f"""<section id="canvas">
      <h2><span class="num">§</span> Canvas &amp; viewport</h2>
      <p class="lede">Fixed, accessible drag targets beat an infinite pannable canvas for most ELA screens.</p>
      <table>
        <tr><th>Context</th><th>1:1</th><th>4:3</th><th>Full-screen</th></tr>
        <tr><td>Digital-First K-1</td><td>fixed 6×6</td><td>fixed 8×6</td><td>infinite, iv 600×250</td></tr>
        <tr><td>Digital-First 2-5</td><td>fixed 9×9</td><td>fixed 12×9</td><td>infinite, iv 800×350</td></tr>
        <tr><td>Teacher-Presentation K-5</td><td>iv 350×350</td><td>iv 450×350</td><td>iv 1000×450</td></tr>
      </table>
      <p class="small">Grade bands from the K-5 Handbook; ELA uses these as accessibility defaults. Deviation is
        allowed with reason. The key rule for ELA drag-drop: <b>set an initial viewport that frames all content
        with ~1 tile of margin, and keep tiles on-screen</b> — the audit found several screens relying on the
        viewport to pan back to content parked at large negative coordinates (finding F1).</p>
      <div class="callout warn"><div class="t">No off-screen content</div>
        If <code>customInitialViewport</code> is doing the work of hiding tiles at <code>x ≈ -892</code>, the screen
        breaks the moment the viewport is slightly off. Bring content into positive coordinates.</div>
    </section>""")

    # ---------- FIX SCRIPT ----------
    a(f"""<section id="fixscript">
      <h2><span class="num">§</span> The auto-fix script</h2>
      <p class="lede">A single pass that scans any activity for deviations from this guide and corrects them.</p>
      <div class="card">
      <p><a href="{SCRIPTS['audit_fix']}"><code>tools/audit_and_fix_style.py</code></a> pulls an activity,
        checks every screen against the conformance checklists above, prints a per-screen report of what's off,
        and (with <code>--fix</code>) rewrites the <code>polypadState</code> to the ELA palette and lock-down,
        then re-thumbnails.</p>
      <pre><code># scan only — report deviations, change nothing
python tools/audit_and_fix_style.py &lt;activity-url&gt;

# scan + fix + re-thumbnail
python tools/audit_and_fix_style.py &lt;activity-url&gt; --fix</code></pre>
      <h4>What it checks &amp; fixes</h4>
      <table>
        <tr><th>Check</th><th>Auto-fixed?</th><th>How</th></tr>
        <tr><td>Canvas background off-palette / missing</td><td>✅</td><td>set to <code>#fff8e9</code> (or white for free-response)</td></tr>
        <tr><td>Zone fill near-black / off-palette</td><td>✅</td><td>answer→dashed <code>#b0bed2</code>/white; source→solid <code>#b0bed3</code></td></tr>
        <tr><td>Card fill/border/radius drift</td><td>✅</td><td>white fill, <code>#b0bed3</code> border, radius 10</td></tr>
        <tr><td>Text tiles unlocked / editable</td><td>✅</td><td><code>editable:false</code> → status locked/fixed</td></tr>
        <tr><td>Source cards missing Return-to-Dropzone</td><td>✅</td><td><code>stayInDropzones</code> + <code>returnDropzone</code></td></tr>
        <tr><td>actionbar/toolbar not hidden</td><td>✅</td><td>normalized to <code>"hidden"</code>; stray enums stripped</td></tr>
        <tr><td>Sort zone using Center not Flow</td><td>✅</td><td>multi-card zones → <code>layout:"flow"</code></td></tr>
        <tr><td>Answer zone missing validation</td><td>⚠️ flagged</td><td>reported — wiring a solution is an authoring decision</td></tr>
        <tr><td>Content parked off-screen</td><td>⚠️ flagged</td><td>reported — repositioning is layout-specific</td></tr>
        <tr><td>Wrong template for the task</td><td>⚠️ flagged</td><td>reported (e.g. sort built as a generic organizer)</td></tr>
      </table>
      <p class="small">Fixes reuse the proven logic in
        <a href="{SCRIPTS['style_dropzones']}">style_dropzones_via_api.py</a>,
        <a href="{SCRIPTS['disable_all']}">disable_all_via_api.py</a>, and
        <a href="{SCRIPTS['regen_thumbs']}">regen_thumbs_fast.py</a>. Things marked ⚠️ are surfaced for a human
        because they change meaning, not just appearance.</p>
      </div>
    </section>""")

    # ---------- APPENDIX ----------
    a(f"""<section id="appendix">
      <h2><span class="num">§</span> Appendix — what to avoid</h2>
      <p class="lede">The clearest failure modes from the 178-screen audit. If you see these, fix them.</p>
      <div class="compare">
        <div class="col"><img src="{U('audit/Misc__INCONSISTENT__debating-p1-near-black-zones-no-lock-pro.png')}" alt="near-black zones">
          <div class="body"><span class="tag bad">Avoid</span><p class="small"><i>Debating, Part 1</i> — drop zones
          filled near-black (<code>#242436</code>/<code>#111111</code>); missing the lock-down profile entirely.</p>
          <a href="{LIVE['Debating']}">Open live ↗</a></div></div>
        <div class="col"><img src="{U('audit/Misc__INCONSISTENT__outsmarting-outbreak-sort-as-organizer-d.png')}" alt="sort as organizer">
          <div class="body"><span class="tag bad">Avoid</span><p class="small"><i>Outsmarting an Outbreak</i> — a sort
          task built as a free-form organizer with dark zones, scrollable text, no validation.</p>
          <a href="{LIVE['Outbreak']}">Open live ↗</a></div></div>
      </div>
      <h3>The recurring offenders</h3>
      <ul class="checklist">
        <li><b>Missing / hand-typed backgrounds</b> — the audit found 22 distinct background values and 67 screens
          with none. Pick one house background.</li>
        <li><b>Zone fill drifting to grey/near-black</b> — <code>#242436</code>, <code>#111111</code>,
          <code>#777777</code> as a <i>zone fill</i> is always wrong.</li>
        <li><b>Partial validation</b> — 3 of 4 answer zones wired. All or none.</li>
        <li><b>Default <code>"Button"</code> label</b> — the most common check-button label in the catalog was the
          un-renamed default. Use a real label if you keep the button.</li>
        <li><b>Leaked full math/geo toolbar</b> — 21 screens shipped the whole tool enum; students see irrelevant
          clutter. Lock it down.</li>
        <li><b>Off-screen content</b> propped up by <code>customInitialViewport</code>. Bring it on-screen.</li>
      </ul>
      <p class="small">Full histograms (background × 22, zone fill × 14, body-text color × 9, validation coverage,
        layout mix) are in the original audit write-up
        <code>POLYPAD_STYLE_GUIDE.md</code> Part 4.</p>
    </section>""")

    # ---------- FOOTER ----------
    a(f"""<section>
      <div class="divider"></div>
      <p class="small">Sources:
        <a href="{COLLECTION}">ELA Polypad Templates collection</a> ·
        <a href="{CKLA_SLIDES}">CKLA Drag &amp; Drop Authoring Guide</a> ·
        <a href="{GSITE_INDEX}">K-5 Math Suite Design Handbook</a> ·
        the 178-screen ELA audit. Images hosted on Polypad's public S3 (no sign-in to view).</p>
    </section>""")

    a('</main></div></div>')  # close main, layout, wrap
    a(f"""<footer><div class="wrap">
      Polypad ELA Style Guide · generated from the audit + the three official templates + the CKLA and K-5 design specs.
      Rebuild with <code>python build_ela_style_guide.py</code>.
    </div></footer>""")

    # ---------- SHELL ----------
    head = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <title>Polypad ELA Style Guide</title>
      <style>{CSS}\n{VARIANTS_CSS}</style></head><body>"""
    return head + "".join(P) + "</body></html>"


# Named-variant sub-cards, integrated into each family section (no separate gallery).
# family_variants.json: {"#match": "<html>", "#organizer": "...", "#sort": "..."}
FAMILY_VARIANTS = {}
VARIANTS_CSS = ""
try:
    _fv = (HERE / "style_guide_shots" / "family_variants.json")
    if _fv.exists():
        FAMILY_VARIANTS = json.loads(_fv.read_text())
    _vc = (HERE / "style_guide_shots" / "variants_css.txt")
    if _vc.exists():
        VARIANTS_CSS = _vc.read_text()
except Exception:
    FAMILY_VARIANTS = {}


if __name__ == "__main__":
    html = build_html()
    out_path = HERE / "POLYPAD_ELA_STYLE_GUIDE.html"
    out_path.write_text(html)
    print(f"wrote {out_path} ({len(html):,} bytes)")
