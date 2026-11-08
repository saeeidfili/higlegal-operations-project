# Slide 9 — Our KPIs — how we measure success

**Speaker:** Dedi Li
**Time:** 1:00
**Figures:** none (scoreboard slide — no SVG from the manifest)
**Related appendix:** `A6-assumptions-and-model-cards.md`

## On-slide content

- Eyebrow: `HOW WE MEASURE SUCCESS`
- Title: `Two primary KPIs — one for each side of the counter`
- Two primary KPI cards, side by side, hero-sized:

  | | PRIMARY 1 | PRIMARY 2 |
  |---|---|---|
  | Whose value | **The company's** | **The customer's** |
  | KPI | **Cost per Video** | **Lead Time per Video** |
  | Baseline | **¥940 [E]** | **14–28 d [C] (~21)** |
  | Why it counts | `every manual minute is recurring cost` | `the lawyer's campaign calendar pays for every queued day` |
  | It answers | `does the service stop bleeding?` | `does the lawyer stop waiting?` |

- Framing band (under the two cards, full width):

  > **Orthogonal — every iteration must move *both*.**

- Auxiliary KPIs (compressed table, "what changes inside the black box"):

  | Auxiliary KPI | Makes visible | Baseline |
  |---|---|---|
  | Human time per video | the labour waterfall behind cost | ~10 h [C] |
  | Throughput (demand / output / capacity) | the scaling question | output 15–20 [C]; capacity ~19 [E] |
  | Rework rate | whether the loop families are dying | ~90% [E] |
  | **QAR** (first-pass at every gate) | first-time correctness — catches "faster but worse" | ~10% [E] |

- Division of labour (one line, above or beside the table): `Primaries say *whether* — auxiliaries say *why*.`
- Measurement plan (bottom band, one line): `Simulate first, then pilot — pass = both primaries hit target AND no auxiliary regresses.`
- Legend footnote: `[C] company-reported · [E] estimate`

## Layout

- **Background:** solid `#F3F4F6`, full bleed. No figure — the two primary numbers are the visual.
- **Eyebrow:** Inter, 24 px, all caps, letter-spacing 0.15 em, gold `#C9A86A`.
- **Title:** Momo Trust Display, ink `#101010`, ~40 px, left-aligned, top-left; short-statement grammar, one line if it fits, two at most.
- **Primary cards:** two equal white cards (~44 % width each, 20 px gap), 1 px grey-200 `#E5E7EB` border, generous padding. Card structure top-to-bottom: "THE COMPANY'S VALUE" / "THE CUSTOMER'S VALUE" in Inter 24 px caps muted `#6A7282`; KPI name in Inter semibold 32 px `#0A0A0A`; **baseline as the hero number** in Inter Black ~64 px `#0A0A0A` (tag [C]/[E] inline, 24 px, muted `#6A7282`); the "why it counts" gloss in Inter 24 px body `#4A5565`, one line; "it answers" line in Inter italic 24 px `#262626`.
- **Framing band:** full-width strip directly under the cards, fill white, 2 px gold `#C9A86A` left border; text Inter semibold 26 px `#262626`, centered. The word ***both*** in accent red `#D92605` — the only red on the slide.
- **Auxiliary table (compressed):** single block, ~one-third of slide height, no cards, no pills; header row Inter 24 px caps muted `#6A7282` over a 1 px grey-200 `#E5E7EB` rule; KPI names Inter semibold 24–26 px `#262626` (QAR bold `#0A0A0A`); "makes visible" glosses Inter 24 px body `#4A5565`, max one line each; baselines right-aligned Inter 24 px `#262626`, tags muted. Rows tight (8 px leading) — the table must read as one dense register under the two big cards, a footnote in scale, not a peer.
- **Division-of-labour line:** Inter italic 24 px muted `#6A7282`, right-aligned above the table's header row (or as the table's caption); *whether* / *why* in semibold `#262626`.
- **Measurement-plan band:** full-width strip pinned ~64 px from the bottom edge, fill wait-fill `#F6EEDF`, 2 px wait-line `#A8823F` left border; Inter 24–26 px `#262626`, one line: `Simulate first, then pilot — pass = both primaries hit target AND no auxiliary regresses.` with `AND` in semibold.
- **Legend footnote:** Inter 24 px, muted `#6A7282`, bottom-left, one line: `[C] company-reported · [E] estimate`.
- **Density check:** eyebrow + title + 2 cards + framing band + 4-row table + plan band + legend. All text ≥ 24 px; no figure labels needed (no figure).

## Speaker notes

**TIME:** 1:00 — bridge in ~5 s, the two primaries ~25 s, auxiliaries ~20 s, measurement plan ~10 s, handoff ~5 s. If running long, this slide compresses to 0:30 (per README): name the two primaries, say "both must move," state the gate, move on.

**MAIN MESSAGE:** Two numbers decide whether an iteration worked — cost per video for the company, lead time per video for the customer — and four auxiliaries explain why; every iteration must move both primaries, and no auxiliary may regress.

**SPEAKING POINTS:**

- Bridge from slide 8: we have quantified the damage — waiting, overprocessing, rework. Before we propose any fix, here is the scoreboard: how we will know a fix *worked*.
- Two primary KPIs, one from each side of the counter. **Cost per Video** is the company's value — every manual minute is recurring cost; baseline ¥940 [E]. **Lead Time per Video** is the customer's value — the lawyer's campaign calendar pays for every queued day; baseline 14–28 days [C], around 21 typical.
- Why two and not one: cost says whether the service stops bleeding; lead time says whether the lawyer stops waiting. They are orthogonal — you can always buy speed with cost, or save cost by making lawyers wait. Cheating one at the expense of the other is exactly what we refuse to do: **every iteration must move both.**
- The auxiliaries show what changes inside the black box: human time ~10 h per video [C] — the labour waterfall behind cost; throughput — output 15–20 [C] against capacity ~19 [E], the scaling question; rework rate ~90% [E] — whether the loop families from slide 7 are dying; and QAR ~10% [E] — first-pass at every gate, the honesty check that catches "faster but worse."
- Division of labour, in one phrase: primaries say *whether* an iteration worked; auxiliaries say *why*. If lead time falls while QAR falls too, we are not improving — we are shipping defects faster.
- Measurement plan in one line: simulate first — each iteration's targets validated in the process simulation before anything is implemented — then pilot in the company; from Iteration 1 the order state machine timestamps every transition, so all KPIs are auto-computed per order. Gate rule: pass = both primaries hit target **and** no auxiliary regresses.
- Handoff: "Scoreboard set. Saeed now shows the three iterations that move both numbers — starting with standardizing briefing and approvals."

**DATA STATUS:** All numbers from the Section 5 summary (master numbers: `single source of truth/kpi-data.md`). Tag discipline per A6: Cost per Video ¥940 [E]; Lead Time 14–28 d [C] (~21); human time ~10 h [C]; throughput output 15–20 [C], capacity ~19 [E]; rework rate ~90% [E]; QAR ~10% [E]. Baselines only — targets are defined as ranges with mechanisms (justification table in `kpi-data.md`) and are shown on the iteration slides, not here. Nothing on this slide presents iterations as results; the pilot and simulation references are the *plan*, with simulation outputs belonging to Section 7 as *calculated scenario*.
