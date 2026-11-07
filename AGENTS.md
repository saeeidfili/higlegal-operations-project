# AGENTS.md – instructions for coding agents (Codex, Claude, DeepSeek, Copilot, …)

This repo is a 15-minute Operations Management presentation (PHBS, Group 9) about HiLegal's lawyer video production. It is a plain HTML deck with no build step.

**Read `STYLE.md` before you change anything.** It defines colours, fonts, layout and the process-map geometry.

## Repo layout

| Path | What it is | Edit? |
|---|---|---|
| `deck.json` | Deck title, slide **order**, sections, `history` (repo and paths for the Version dropdown) | Yes, when adding/removing/reordering slides |
| `slides/<id>.html` | One slide per file, one `<section id="<id>">` each | **Yes – this is where content lives** |
| `assets/` | Logos, hero image, group photo | Add files; do not replace logos |
| `animations/` | Full-screen animation pages linked by the play buttons | Only if asked |
| `runtime/` | Viewer code (slide preview, present mode) | Only if asked |
| `index.html` | Viewer entry point | Only if asked |
| `tools/serve.ps1` | Local web server for Windows | No |

## Slide file format

- Exactly one `<section id="<id>" style="…">` per file. The file name must equal the id.
- The canvas is 1920 × 1080 px. Use **inline styles only**, px units, hex colours. No classes, no `<style>`, no `<script>` (except inside `<x-embed>`).
- Pin elements with `position:absolute; left; top; width; height`. Flow layout (flex/grid) is fine inside sections and divs.
- Lines and arrows: `<x-connector x1 y1 x2 y2 head="end|none|both" style="color:#…;border-width:2px;border-style:dashed">`. The viewer draws them as SVG.
- Live animation layers: `<x-embed style="position:absolute;…">…small HTML page…</x-embed>`. The viewer runs it in a sandboxed iframe.
- Speaker notes: one `<aside>` as the **last** child of the section, plain text.
- `hidden` on the section hides it in Present mode (used for the internal slides `team-questions` and `review`).
- Images: `<img src="assets/…" alt="…" style="width;height;object-fit:cover|contain">`. Optional `data-crop="1 X% Y%"` sets the crop focus.

Keeping this format means slides can still be imported back into the original Claude Slides deck.

## Workflow

1. Run the viewer (see README), open the slide, note its file path (shown under the slide).
2. Edit only the slide files you were asked to change. Keep the process-map geometry identical across current, wastes and the three iteration slides, including their shared scale wrapper.
3. Check the slide in the viewer at full size: nothing overlaps, body content stays above y 1008 and the footer sits 24 px from the bottom, body text and slide numbers at least 24 px. Source and qualification footers use 18 px as specified in STYLE.md.
4. Commit one logical change per commit, e.g. `slide iter2: shorten KPI table`.
5. Pull before you start: team members also update slide files through Git. If two people edit the same slide file, resolve the conflict by hand.

## Content rules (short version – full rules in STYLE.md §6)

- English only. No invented data. Label every number (company-reported, estimate, target, calculated, gap).
- Iterations are proposals, not tested results.
- Do not cite the group's own proposal or briefing on slides; cite the HiLegal team, company information, our analysis or lecture slides.

- Text separators: never use middle dots (Unicode U+00B7 or HTML entities). Use ` | ` for independent labels, commas for related phrases, and full stops between sentences. Apply this to slides, notes, animations and viewer labels. See STYLE.md, Text separators.

- Company naming: write **Fadada** consistently in all presentation copy, headings, speaker notes and image descriptions.
