#!/usr/bin/env python3
"""Generate style_guide_shots/gallery_fragment.html — the 'every distinct design'
gallery — from clusters.json + render_map.json + all_shot_urls.json.
The main builder (build_ela_style_guide.py) reads this fragment via its GALLERY_HTML hook.
"""
import json, html
from pathlib import Path

SG = Path(__file__).parent / "style_guide_shots"
CLUSTERS = json.loads((SG / "clusters.json").read_text())
RENDER_MAP = json.loads((SG / "render_map.json").read_text())   # label -> png filename
URLS = json.loads((SG / "all_shot_urls.json").read_text())

def url_for_png(fn):
    return URLS.get(f"design/{fn}")

def act_url(aid):
    return f"https://classroom.amplify.com/activity/{aid}"

def esc(s):
    return html.escape(s or "")

# short description per design label
DESC = {
    "Free Response": "Students type into input fields — the most common ELA pattern. Constructed answers, notes, definitions.",
    "Card Match": "Drag one card to the box beside each prompt. One answer per question, one-to-one.",
    "Claim & Evidence": "Match or place evidence with the claim/step it supports — often a sequenced or two-column layout.",
    "Story / Plot Map": "Place events, elements, or labels onto a narrative structure (Hero's Journey, plot arc, story map).",
    "Sentence Builder": "Drag word/letter tiles into a frame to build a sentence (ELD English Building Blocks).",
    "Ranking / Continuum": "Order or rank cards along a scale, sequence, or continuum.",
    "Graphic Organizer (labeled diagram)": "Drag labels/evidence onto regions of an illustrated diagram; the image carries meaning.",
    "Multi-zone Organizer": "Several unvalidated zones for open categorization or collection of ideas.",
    "Compare & Contrast": "Two-side comparison — similarities/differences, or a side-by-side reading/zoom.",
    "Card Sort": "Sort many cards into a few category bins; many-to-one.",
    "Venn Diagram": "Two overlapping regions for shared vs. unique attributes ('Integration of Knowledge and Ideas').",
    "Timeline / Sequence": "Order events chronologically, or sort signal words by structure (chronology vs. cause & effect).",
    "Rhetorical Appeals": "Match quotations/examples to ethos / pathos / logos.",
    "KWL (Know / Want / Learned)": "Three labeled columns — What I Know / Want to Know / Learned — each with a text-input field below. Students type (no dragging) to activate prior knowledge, set questions, and reflect.",
    "Other": "Screens that don't fit a named pattern — usually candidates to rebuild on a standard template.",
}

# which of these map onto the 6 canonical families (for the 'see also' link)
FAMILY_ANCHOR = {
    "card_match": "#match", "card_sort": "#sort", "graphic_organizer": "#organizer",
    "free_response": "#free", "zoom_reader": "#zoom", "builder": "#builder",
    "organizer_zones": "#organizer", "other": "#types",
}

# The 6 core families already get a full spec section above (#match … #builder).
# The gallery expands only the NAMED VARIANTS. These labels are the core families
# and are skipped here (they'd duplicate the sections above).
CORE_FAMILY_LABELS = {
    "Card Match", "Card Sort", "Graphic Organizer (labeled diagram)",
    "Free Response", "Zoom Reader", "Sentence Builder", "Other",
}

# Per-variant expansion: which core family it builds on, spec rows, checklist, fix.
VARIANT_SPEC = {
    "Claim & Evidence": {
        "builds_on": ("Card Match", "#match"),
        "spec": [("Layout", "sequenced steps or two columns — evidence card ↔ claim/step it supports"),
                 ("Zones", "dashed <code>#b0bed2</code> answer zone under each step; one grey source bin"),
                 ("Validation", "match-validated when each evidence has one correct home")],
        "check": ["Each evidence card has exactly one correct target.",
                  "Answer zones dashed #b0bed2; source bin holds all cards.",
                  "Illustrated step cards are locked (not editable/deletable)."],
        "fix": "Treat as Card Match: classify zones, apply the ELA palette, wire each evidence→step "
               "solution, lock the step art. Run <code>audit_and_fix_style.py --fix</code>.",
    },
    "Story / Plot Map": {
        "builds_on": ("Graphic Organizer", "#organizer"),
        "spec": [("Structure", "events/labels placed onto a narrative arc, plot line, or Hero's-Journey wheel"),
                 ("Slots", "categorizer slots over the diagram; center layout (one per region)"),
                 ("Furniture", "diagram image + card bank locked; delete removed from actionbar")],
        "check": ["Diagram/structure image is locked.", "Card bank can't be deleted.",
                  "Consistent slot styling across the map.", "One background; toolbar hidden."],
        "fix": "Lock the structure image + card bank, unify slot styling to dashed #b0bed2, "
               "set one background. Slot positioning over the art stays manual.",
    },
    "Ranking / Continuum": {
        "builds_on": ("Card Match", "#match"),
        "spec": [("Layout", "ordered positions along a scale/continuum (most→least, first→last)"),
                 ("Zones", "one center-layout, 1-tile-limit zone per position"),
                 ("Validation", "match against the correct order")],
        "check": ["One zone per rank position (Center, 1-tile limit).",
                  "Order is match-validated (or an explicit self-check).",
                  "Cards a consistent size; source bin holds them all."],
        "fix": "Set each position zone to Center + 1-tile limit, capture the ordered solution, "
               "apply the palette + lock-down.",
    },
    "Multi-zone Organizer": {
        "builds_on": ("Graphic Organizer", "#organizer"),
        "spec": [("Zones", "several collection zones, usually Flow, often unvalidated (open response)"),
                 ("Use", "gathering ideas/evidence into named buckets where any grouping is valid"),
                 ("Styling", "uniform zone styling; one background")],
        "check": ["All zones share one consistent style (no near-black fills).",
                  "Validation decision is explicit (usually intentionally open).",
                  "Toolbar hidden; text locked."],
        "fix": "Normalize zone fills/strokes to the ELA palette, lock text, hide the toolbar. "
               "Leave validation off if the task is genuinely open.",
    },
    "Compare & Contrast": {
        "builds_on": ("Card Sort", "#sort"),
        "spec": [("Layout", "two labeled sides — similarities/differences, or a side-by-side reading"),
                 ("Zones", "two Flow bins (or a zoom-reader spread for side-by-side text)"),
                 ("Validation", "match when items belong to one side; open when comparing freely")],
        "check": ["Two clearly labeled sides.", "Flow layout so multiple items fit.",
                  "Uniform zone styling; one background."],
        "fix": "Force Flow on the two bins, apply the palette, wire validation if items have a correct side.",
    },
    "Venn Diagram": {
        "builds_on": ("Graphic Organizer", "#organizer"),
        "spec": [("Structure", "two overlapping regions — left-only, shared (overlap), right-only"),
                 ("Zones", "three categorizer regions (A, A∩B, B); consistent styling"),
                 ("Note", "this is the real 'Integration of Knowledge and Ideas' organizer — NOT a KWL")],
        "check": ["Three regions (left / overlap / right), consistently styled.",
                  "Overlap zone genuinely overlaps visually.", "One background; text locked."],
        "fix": "Style all three regions with one dashed #b0bed2 treatment, lock labels, set one background. "
               "Region geometry stays manual.",
    },
    "KWL (Know / Want / Learned)": {
        "builds_on": ("Graphic Organizer", "#organizer"),
        "spec": [("Structure", "three labeled columns — <b>What I Know / What I Want to Know / What I Learned</b>"),
                 ("Header", "a pale-blue <code>#d1e4f7</code> chip per column, locked, `#111111` text"),
                 ("Input", "a <code>question-blank</code> (mode <code>text</code>) input field under each column — students type, no dragging"),
                 ("Mechanism", "this is a Free-Response organizer (input fields), grouped here by purpose, not drag-drop"),
                 ("Canvas", "cream <code>#fff8e9</code>, actionbar + toolbar hidden")],
        "check": ["Three columns, each with a locked header chip + one input field.",
                  "Headers are `#d1e4f7`; fields white; canvas `#fff8e9`.",
                  "Prompt/headers non-editable; only the fields accept typing.",
                  "Square-ish footprint so all three columns are equal and fully visible."],
        "fix": "Lay out 3 equal columns; header = locked text tile (`#d1e4f7`), body = `question-blank` "
               "mode:text. Lock the headers, hide the toolbar, set the cream background. No validation "
               "(open reflection).",
    },
    "Timeline / Sequence": {
        "builds_on": ("Card Sort", "#sort"),
        "spec": [("Layout", "order events chronologically, or sort signal words by structure"),
                 ("Zones", "sequence positions (Center, 1-tile) OR labeled sort bins (Flow)"),
                 ("Validation", "match against the correct sequence/category; Check My Work button")],
        "check": ["Positions/bins clearly labeled.",
                  "Match-validated with a real Check button (label, #0f82f2, check icon).",
                  "Cards consistent; source bin present."],
        "fix": "Pick Center+limit (ordering) or Flow (sorting), capture the solution, add a proper "
               "Check button, apply the palette.",
    },
    "Rhetorical Appeals": {
        "builds_on": ("Card Match", "#match"),
        "spec": [("Layout", "match quotations/examples to ethos / pathos / logos"),
                 ("Zones", "three (or more) match zones, one per appeal"),
                 ("Validation", "each example match-validated to its appeal")],
        "check": ["One zone per appeal, all validated.",
                  "Cards consistent; source bin holds examples.",
                  "Palette + lock-down applied."],
        "fix": "Treat as Card Match with 3 targets; wire each example→appeal solution; apply palette.",
    },
}

# each variant's parent-family anchor (where its sub-card nests)
VARIANT_PARENT = {
    "Claim & Evidence": "#match",
    "Ranking / Continuum": "#match",
    "Rhetorical Appeals": "#match",
    "Timeline / Sequence": "#sort",       # signal-word sort / ordering
    "Compare & Contrast": "#sort",
    "Venn Diagram": "#organizer",
    "Story / Plot Map": "#organizer",
    "Multi-zone Organizer": "#organizer",
    "KWL (Know / Want / Learned)": "#organizer",
}

def build():
    by_parent = {}   # family anchor -> list of variant card HTML
    n_variants = 0
    for c in CLUSTERS:
        label = c["label"]
        if label in CORE_FAMILY_LABELS:
            continue  # the family itself is the section; only variants nest inside
        parent = VARIANT_PARENT.get(label)
        if not parent:
            continue  # unmapped (e.g. "Other") — not shown as a design variant
        n_variants += 1
        png = RENDER_MAP.get(label)
        img_url = url_for_png(png) if png else None
        ideal = c["ideal"]
        fams = ", ".join(f"{k.replace('_',' ')} ×{v}" for k, v in
                         sorted(c["families"].items(), key=lambda kv: -kv[1]))
        # collect distinct example activities (up to 6) with live links
        seen = set(); examples = []
        for m in c["members"]:
            if m["activity"] in seen: continue
            seen.add(m["activity"])
            examples.append(m)
            if len(examples) >= 6: break
        ex_links = " · ".join(
            f'<a href="{act_url(m["activity"])}">{esc((m["title"] or "")[:32])}</a>'
            + (f' <span class="small">({esc(m["curriculum"])})</span>' if m.get("curriculum") else "")
            for m in examples)
        notes = [m["notes"] for m in c["members"] if m.get("notes")]
        note_html = ""
        if notes:
            uniq = list(dict.fromkeys(notes))[:3]
            note_html = ('<p class="small"><b>Audit notes:</b> '
                         + "; ".join(esc(n) for n in uniq) + "</p>")

        # expanded spec/checklist/fix (like the 6 families)
        v = VARIANT_SPEC.get(label, {})
        spec_html = ""
        if v.get("spec"):
            spec_html = ('<div class="vspec"><b>Spec</b><dl>'
                         + "".join(f"<dt>{esc(dt)}</dt><dd>{dd}</dd>" for dt, dd in v["spec"])
                         + "</dl></div>")
        check_html = ""
        if v.get("check"):
            check_html = ('<div class="vspec"><b>Checklist</b><ul class="vcheck">'
                          + "".join(f"<li>{esc(x)}</li>" for x in v["check"]) + "</ul></div>")
        fix_html = ""
        if v.get("fix"):
            fix_html = f'<div class="vfix"><b>Conform it:</b> {v["fix"]}</div>'
        builds_on_html = ""
        if v.get("builds_on"):
            bn, ba = v["builds_on"]
            builds_on_html = f'<span class="vbadge">builds on <a href="{ba}">{esc(bn)}</a></span>'

        img_html = (f'<img src="{img_url}" alt="{esc(label)} ideal example" loading="lazy">'
                    if img_url else '<div class="noimg">render pending</div>')

        anchor_id = "design-" + label.lower().replace(' ','-').replace('/','').replace('&','and').replace('(','').replace(')','')
        card = f"""
        <div class="vcard" id="{esc(anchor_id)}">
          <div class="vthumb">{img_html}</div>
          <div class="vbody">
            <div class="vhead"><span class="gcount">{c['count']}×</span>
              <h4>{esc(label)}</h4></div>
            <p class="small">{esc(DESC.get(label, ''))}</p>
            {spec_html}
            {check_html}
            {fix_html}
            <p class="small"><b>Best example:</b>
              <a href="{act_url(ideal['activity'])}">{esc(ideal['title'])}</a>
              {f"<span class='small'>({esc(ideal.get('curriculum'))}, Gr {esc(str(ideal.get('grade')))})</span>" if ideal.get('curriculum') else ""}
              &nbsp;·&nbsp; <a class="btnlink ghost" href="{act_url(ideal['activity'])}">Open live ↗</a></p>
            {note_html}
            <details><summary class="small">More examples ({len(examples)})</summary>
              <p class="small">{ex_links}</p></details>
          </div>
        </div>"""
        by_parent.setdefault(parent, []).append(card)

    # Emit one HTML block per parent family (variants nested under the family).
    blocks = {}
    for anchor, cardlist in by_parent.items():
        blocks[anchor] = (
            '<div class="variants"><h4 class="vtitle">Named variants of this family</h4>'
            '<p class="small">Same mechanism, specialized for an ELA task. Each shows its cleanest real example.</p>'
            + "".join(cardlist) + "</div>")
    (SG / "family_variants.json").write_text(json.dumps(blocks, indent=2))

    # Shared CSS for the variant sub-cards (injected once, in the builder's head via this file).
    css = """
    .variants{margin-top:22px;padding-top:14px;border-top:2px dashed var(--line)}
    .vtitle{margin:0 0 2px;font-size:15px;color:var(--brand-d);text-transform:uppercase;letter-spacing:.04em}
    .vcard{display:grid;grid-template-columns:300px 1fr;gap:0;background:#fbfcff;border:1px solid var(--line);
      border-radius:12px;overflow:hidden;margin:14px 0;box-shadow:var(--shadow)}
    .vthumb{background:#fff;border-right:1px solid var(--line);display:flex;align-items:center;justify-content:center;padding:10px}
    .vthumb img{width:100%;height:auto;border-radius:8px;display:block}
    .vthumb .noimg{color:var(--muted);font-size:13px;padding:30px}
    .vbody{padding:13px 16px}
    .vhead{display:flex;align-items:baseline;gap:9px} .vhead h4{margin:0;font-size:17px}
    .vspec{margin:6px 0} .vspec b{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
    .vspec dl{display:grid;grid-template-columns:120px 1fr;gap:1px 12px;margin:3px 0;font-size:13.5px}
    .vspec dt{font-weight:700} .vspec dd{margin:0;color:var(--muted)}
    .vcheck{margin:3px 0 3px 0;padding-left:18px;font-size:13.5px;color:var(--muted)}
    .vfix{font-size:13.5px;background:#eef7ff;border-radius:8px;padding:7px 11px;margin:7px 0}
    .vbadge{font-size:11px;font-weight:700;background:var(--chip);color:var(--brand-d);padding:2px 9px;border-radius:999px}
    .gcount{background:var(--chip);color:var(--brand-d);font-weight:800;font-size:12px;padding:2px 9px;border-radius:999px}
    .vbody details{margin-top:5px} .vbody summary{cursor:pointer;color:var(--brand-d)}
    @media(max-width:760px){.vcard{grid-template-columns:1fr}.vthumb{border-right:none;border-bottom:1px solid var(--line)}}
    """
    (SG / "variants_css.txt").write_text(css)
    print(f"wrote family_variants.json — {n_variants} variants across {len(blocks)} families")

if __name__ == "__main__":
    build()
