# STYLE.md – HiLegal presentation design system

Every slide in `slides/` follows these rules. Agents and people: read this before you change a slide, and copy existing slides rather than inventing new patterns.

## 1. Canvas

- Every slide is exactly **1920 × 1080 px** (16:9). The viewer scales it to fit.
- Safe margins: **128 px** left and right. Nothing important goes outside x 128–1792.
- Content area on light slides: **y 216–960**. The footer sits at `bottom:64px`.

## 2. Colour tokens

Taken from hilegal.com CSS, except the gold tones, which are derived from the site's hero image.

| Token | Hex | Use |
|---|---|---|
| `black` | `#0A0A0A` | Header band, dark slides (cover, decision, thanks, appendix divider) |
| `ink` | `#101010` | Headings and strong text on light slides, work boxes |
| `text` | `#262626` | Body text, rework lines |
| `body` | `#4A5565` | Secondary body text |
| `muted` | `#6A7282` | Footers, captions |
| `grey-400` | `#99A1AF` | Eyebrow on dark header, removed-step outline |
| `grey-300` | `#D1D5DC` | Light text on dark backgrounds |
| `grey-200` | `#E5E7EB` | Alternate slide background, table headers on light slides |
| `bg` | `#F3F4F6` | Default light slide background |
| `bg-soft` | `#F9FAFB` | Table row banding |
| `white` | `#FFFFFF` | Cards, boxes, tables |
| `accent` | `#D92605` | Brand red: labels, process **changes**, key rules. Use sparingly. |
| `accent-tint` | `#FBE4DF` | Fill of a box that is **new** in this iteration |
| `accent-tint-2` | `#FDF3F1` | Fill of a box changed in an **earlier** iteration |
| `gold` | `#C9A86A` | Fine 2 px line under the header, play-button outline, "company-reported" tags on dark |
| `wait-fill` | `#F6EEDF` | Fill of **waiting** steps and approval gates |
| `wait-line` | `#A8823F` | Border of waiting steps |
| `wait-text` | `#6B5223` | Text in waiting steps |

## 3. Typography

| Role | Font | Size | Weight | Notes |
|---|---|---|---|---|
| Cover / closing title (h1) | Momo Trust Display | 120 px | 400 | line-height 1.05 |
| Slide title in header (h2) | Momo Trust Display | 52 px | 400 | white, `white-space:nowrap`, max 1440 px wide |
| Title on dark slides (h2) | Momo Trust Display | 56 px | 400 | |
| Big number | Inter | 96 px | 800 | |
| Lead text | Inter | 32 px | 400 | |
| Eyebrow (chapter line) | Inter | 24 px | 600 | uppercase, letter-spacing 2 px |
| Body, labels, tables, footers | Inter | 24 px | 400 / 600 | **never below 24 px** |

Both fonts are Google Fonts and load in `index.html`. Do not add other fonts.

## 4. Layout patterns

### Light content slide (header band)
- Black band `left:0; top:0; width:1920px; height:184px; background:#0A0A0A`.
- Gold line `top:184px; height:2px; background:#C9A86A`.
- Eyebrow `left:128px; top:40px`, colour `#99A1AF`.
- Title h2 `left:128px; top:80px; width:1440px`, white.
- HiLegal logo (white) `left:1662px; top:52px; width:130px; height:80px`.
- Optional play button `left:1370px; top:70px; width:260px`, gold 2 px border, radius 8 px.
- Flow content starts at `padding-top:232px` (or absolute content from `top:216px`).
- Footer: source text `left:128px; bottom:64px; width:1400px; 24px; #6A7282`, page number `left:1672px; width:120px; text-align:right`.

### Dark slide (cover, challenge, decision, thanks, appendix divider)
- Background `#0A0A0A` or `#101010`. Logo top right (or top left on cover). Red or gold rules as accents.

### Text block
- Label 24 px 600 in `accent`, body 24 px `body`, separated by a 2 px top rule (`#101010`).
- Highlight block: same structure, white background, 2 px top rule in `accent`. No thick side bars, no shadows.

## 5. Process map (slides 4–9)

The process map must keep the **same geometry on every slide**, so changes are visible between iterations.

- 6 columns, x = **128, 413, 698, 983, 1268, 1553**, box width **239**.
- Row 1 y = **270**, row 2 y = **446**, box height **112** (stacked half boxes: 52 px at 446 and 506).
- Arrows between boxes at y 326 (row 1) and 502 (row 2), drawn with `<x-connector>`.
- Rework loops: dashed 3 px `#262626`, above row 1 at y 246 and below row 2 at y 590; label on the line with `bg` background.

| Step type | Fill | Border | Shape |
|---|---|---|---|
| Work | `#FFFFFF` | 2 px `#101010` | radius 8 |
| Waiting | `#F6EEDF` | 2 px `#A8823F` | radius 8 |
| Approval gate | `#F6EEDF` | 2 px `#A8823F` | pill (radius 56) |
| Start / end | `#101010` | 2 px `#101010` | pill, white text |
| Changed in this iteration | `#FBE4DF` | **4 px** `#D92605` | as above |
| Changed in an earlier iteration | `#FDF3F1` | 2 px `#D92605` | as above |
| Removed | `#F3F4F6` | 2 px dashed `#99A1AF` | strike-through name |

Colour never carries meaning alone: every box also says "Work", "Wait", "Gate", "New", "It. 1" or "Removed" in text.

## 6. Content rules

- Language: **English** on slides and in notes.
- Do not invent company information, measurements, pilot results or financial figures.
- Label every figure: *company-reported*, *estimate*, *target*, *calculated scenario* or *gap*.
- Proposed iterations are **not tested**; never present them as results.
- Sources on slides: the HiLegal team, company-provided information, our own analysis, or lecture slides. Do not cite our own proposal or briefing.
- Titles: short statements, one grammar throughout.
- Speaker notes go in one `<aside>` at the end of the slide: TIME, MAIN MESSAGE, SPEAKING POINTS, DATA STATUS / CALCULATION where relevant.
