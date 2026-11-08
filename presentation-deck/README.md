# Presentation deck — speaker-ready slide specs

One `.md` per slide in `slides/` (main deck, 17 slides, 17:00) and `appendix/`
(A1–A6, Q&A insurance, untimed). Each file gives the pptx builder everything:
title, on-slide content, figure paths, layout tokens, and speaker notes.

## Timing and speakers (4 × ~4 min)

| # | Slide | Speaker | Time |
|---|---|---|---|
| 1 | Cover | Augustin Dulon | 0:30 |
| 2 | What HiLegal told us — and what we suggest | Augustin Dulon | 0:45 |
| 3 | The challenge — ¥940 vs ¥117 | Augustin Dulon | 1:00 |
| 4 | The bleed — tier loses on video #1 | Dedi Li | 1:00 |
| 5 | Current process — 12 steps, 94% waiting | Dedi Li | 1:15 |
| 6 | Wastes & root causes | Dedi Li | 1:00 |
| 7 | Waiting is mathematics | Saeed Filizadeh | 1:15 |
| 8 | Rework — +84 min buys +10.8 days | Saeed Filizadeh | 1:15 |
| 9 | Our KPIs — how we measure success | Saeed Filizadeh | 0:45 |
| 10 | Iteration 1 — standardize briefing & approvals | Saeed Filizadeh | 1:15 |
| 11 | Iteration 2 — template-based AI scripting | Saeed Filizadeh | 1:00 |
| 12 | Iteration 3 — single-render pipeline | Saeed Filizadeh | 1:15 |
| 13 | The chain, simulated | Saeed Filizadeh | 0:45 |
| 14 | Stress test — five scenarios | Saeed Filizadeh | 1:15 |
| 15 | Organizational impact | Joel Wirth | 1:15 |
| 16 | Implementation & payback | Joel Wirth | 1:00 |
| 17 | Closing | Joel Wirth | 0:30 |

**Total: 17:00** (target 15–17). If running long: slides 9 and 13 compress to 30 s each (−0:30).

## Appendix (Q&A, untimed)

| File | Covers | Feeds slides |
|---|---|---|
| `appendix/A1-costing.md` | ¥85/h build-up, ¥940 cost, cost ladder, per-customer bleed tables | 2, 3, 4, 15 || `appendix/A2-queue-model.md` | μ calibration (anchors → quadratic → optimizer 23.66), M/M/1 predictions, tail/P90, nonlinearity, 200k-order validation, 67/65% cross-check | 5, 7 |
| `appendix/A3-rework-simulation.md` | Gate probabilities (geometric solve, pf = 2·ps), E[work] closed form, incidence, capacity math, five mechanisms, demand sweep | 6, 8 |
| `appendix/A4-iteration-simulations.md` | Per-iteration config anchors (435/350/60 min; incidence 55/30/10%), ladder results, practical-capacity criterion, SLA sensitivities | 10, 11, 12, 13 |
| `appendix/A5-scenario-matrix.md` | S0–S5 full result tables, remaining Section-7 charts | 14 |
| `appendix/A6-assumptions-and-model-cards.md` | [C]/[E]/[T] discipline, assumption ladder, model cards, falsifiable predictions, data-quality note | 2, 6, 9, 15, 16 |

## Figure manifest (all SVG, transparent background, design-system palette)

| File | Used on |
|---|---|
| 12-step process flowchart (copy from presentation branch `slides/current.html` + optional moving-dot animation) | 2 |
| `../04 These are the wastes and root causes/queue/order-timeline.svg` | 5 |
| `../04 These are the wastes and root causes/queue/queue-cliff.svg` | 7 |
| `../04 These are the wastes and root causes/Rework/rework-impact.svg` | 8 |
| `../07 Let's run and compare the processes/ladder.svg` | 13 |
| `../07 Let's run and compare the processes/timer-bars.svg` | 13 (option), A4 |
| `../07 Let's run and compare the processes/saturation.svg` | 14 |
| `../07 Let's run and compare the processes/wip-paths.svg` | A5 |
| `../07 Let's run and compare the processes/slow-lawyers.svg` | A5 |
| `../07 Let's run and compare the processes/rework-stress.svg` | A5 |
| `../04 These are the wastes and root causes/Rework/gantt-rework.svg` | A3 |
| `../04 These are the wastes and root causes/Rework/rework-vs-demand.svg` | A3 |

## Design system (from STYLE.md, presentation branch)

- **Colors:** black `#0A0A0A` · ink `#101010` · text `#262626` · body `#4A5565` · muted `#6A7282` · grey-400 `#99A1AF` · grey-200 `#E5E7EB` · bg `#F3F4F6` · white · **accent red `#D92605` (sparingly)** · gold `#C9A86A` · wait-fill `#F6EEDF` · wait-line `#A8823F` · wait-text `#6B5223`
- **Fonts:** Momo Trust Display (titles) · Inter (everything else, never below 24 px)
- **Process map geometry** (slide 4): 6 columns x = 128/413/698/983/1268/1553, box width 239, rows y = 270/446; work = white + 2 px ink border radius 8; waiting = `#F6EEDF` + `#A8823F`; gates = pill radius 56; start/end = ink pill white text; rework loops dashed 3 px `#262626`; removed = `#F3F4F6` + dashed `#99A1AF` + strike-through
- **Label every figure:** company-reported / estimate / target / calculated scenario
- **Never present iterations as results** — they are simulated designs with targets; Section 7 is labeled *calculated scenario*
- Titles are short statements; one grammar throughout

## Slide-file format

Every slide file contains: header (speaker, time, figures, related appendix),
**On-slide content** (exact text, tables, figure placement), **Layout** (STYLE
tokens), **Speaker notes** (TIME / MAIN MESSAGE / SPEAKING POINTS / DATA STATUS).
