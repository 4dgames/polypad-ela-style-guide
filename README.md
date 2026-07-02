# Polypad ELA Style Guide

A single, self-contained, shareable reference for building and fixing ELA Polypad
interactions. For every interaction design: what a correct screen looks like, the
exact values it must carry, a real example you can open, and how to bring a
non-conforming screen into line — by hand or with a script.

**Live page:** https://4dgames.github.io/polypad-ela-style-guide/

All images are hosted on Polypad's public S3 (`uploads.desmos.com`) — no sign-in
required to view. Live "Open live" links point to `classroom.amplify.com`
activities (those require an Amplify login to open).

## What's in it

- Where the rules come from (the 3 official ELA templates, the CKLA Drag & Drop
  guide, the K-5 Math Suite Design Handbook, and the full 331-slide catalog audit).
- Universal rules — the ELA palette and lock-down profile.
- The full interaction-design catalog: 6 families, each with its named ELA
  variants (Claim & Evidence, Ranking, Rhetorical Appeals, Compare & Contrast,
  Timeline/Sequence, Venn Diagram, Story/Plot Map, Multi-zone Organizer) nested inside.
- Drop-zone deep dive, canvas & viewport sizes, the auto-fix script, and an
  appendix of what to avoid.

## Rebuilding

`index.html` is generated:

```bash
python build_gallery_fragment.py   # builds the nested-variant blocks
python build_ela_style_guide.py    # builds the page  ->  POLYPAD_ELA_STYLE_GUIDE.html
```

(The generator reads image URLs / cluster data from a `style_guide_shots/`
directory that lives in the source repo; only the built `index.html` is published here.)
