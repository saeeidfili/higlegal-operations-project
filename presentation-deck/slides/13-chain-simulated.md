# Slide 13 — The chain, simulated: every target validated end-to-end

- **Speaker:** Saeed Filizadeh
- **Time:** 1:00
- **Figures:** `../07 Let's run and compare the processes/ladder.svg` — six KPI panels (lead time · P90 lead · human work · cost · work-content capacity on a log scale · rework rate), bars baseline → v1 → v2 → v3, suptitled "S0 · normal conditions (λ = 20/mo)". Place full-width or large — dominant, upper zone. Manifest option for this slide: `timer-bars.svg` (also in appendix A4).
- **Related appendix:** A4 (`appendix/A4-iteration-simulations.md` — per-iteration config anchors, ladder results, practical-capacity criterion), A5 (`appendix/A5-scenario-matrix.md` — S0–S5 full result tables)

## On-slide content

**Title:** The chain, simulated: every target validated end-to-end

**Status chip (top-right, doubles as the figure label):** `calculated scenarios (simulation) — targets, not results`

**Figure (dominant, upper ~60 % of the slide, centered):** `ladder.svg` — the scoreboard's six KPI panels, each showing baseline → v1 → v2 → v3 under normal conditions (λ = 20/mo). Five panels fall in order; the only one that rises is capacity (log scale).

**The chain table condensed (bottom-left):**

| | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|
| Lead time (d) | 21.8 | 6.8 | 4.0 | **1.6** |
| Human work (min) | 600 | 438 | 351 | **62** |
| Cost/video (¥) | 940 | 709 | 595 | **182** |
| Practical capacity (/mo) | ~20 | ~30 | ~38 | **~230** |
| Rework | 88% | 56% | 30% | **8%** |

**Chain rule (bottom-right, one line):**

> **A chain, not a menu** — each iteration consumes the previous one's data output: **Brief JSON → Script JSON → Render job**

**Constraint path (bottom strip, one line):**

> **Where the constraint went:** intake → scripting → sync → **lawyer approval** — after Iteration 3 it is client-side

## Layout

- **Background:** solid `#F3F4F6`, full bleed; the SVG is transparent-background — no border box, no extra decoration.
- **Title:** Momo Trust Display, ink `#101010`, top-left, one line if it fits, two max; short-statement grammar.
- **Status chip:** Inter 24 px, muted `#6A7282`, 2 px grey-400 `#99A1AF` pill border, top-right on the title baseline. It carries the design-system figure label for everything on the slide: *calculated scenarios (simulation) — targets, not results*.
- **Figure:** dominant element, centered in the upper zone under the title, native aspect ≈ 1.9:1, as large as ~58–60 % of slide height allows (≈ 60 % of slide width). Do not overlay text on the panels; the log-scale capacity panel is the only rising one — let the asymmetry carry the message.
- **Condensed table (bottom-left, ~55 % width):** header row Inter 24 px caps muted `#6A7282` over a 1 px grey-200 `#E5E7EB` rule; KPI labels Inter semibold 26 px `#262626` with units set muted; Baseline column Inter 24 px body `#4A5565`; Iter 1–2 columns Inter 26 px ink `#101010`; **Iter 3 column Inter semibold 30 px ink `#101010`** — the eye's landing zone. Rows tight (8 px leading), 1 px grey-200 `#E5E7EB` rules, no vertical rules, no zebra fill.
- **Accent red `#D92605` used once:** `~230` in the Iter-3 capacity cell — the same red-accent-on-capacity motif as slide 10.
- **Chain rule (bottom-right, ~40 % width):** white card, 1 px grey-200 `#E5E7EB` border, generous padding. Lead-in "A chain, not a menu" Inter semibold 26 px `#0A0A0A`; the rest Inter 24–26 px body `#4A5565`; the object chain **Brief JSON → Script JSON → Render job** semibold `#262626`, arrows in gold `#C9A86A`.
- **Constraint strip (bottom-most, full width):** wait-fill `#F6EEDF` band, 2 px wait-line `#A8823F` left border. "Where the constraint went:" Inter italic 24 px body `#4A5565`; the path intake → scripting → sync in `#262626` with grey-400 `#99A1AF` arrows; **lawyer approval** semibold `#0A0A0A`; the tail "after Iteration 3 it is client-side" muted `#6A7282`.
- **Density check:** 1 title + 1 chip + 1 figure + 5-row table + 1 rule card + 1 strip; all text ≥ 24 px. No other decoration.

## Speaker notes

**TIME** — 1:00 (Saeed Filizadeh). Bridge ~5 s → ladder walk ~25 s → condensed table ~15 s → chain rule ~8 s → constraint path ~5 s → hand-off ~2 s. If running long, this slide compresses to 0:30 (per README): point at the last bar of each panel, read the Iter-3 column once, state the chain rule, move on.

**MAIN MESSAGE** — The three iterations are a chain, not a menu — each one consumes the previous one's data output — and simulated end-to-end at normal demand every target holds: lead 21.8 → 1.6 days, cost ¥940 → ¥182, practical capacity ~20 → ~230 videos/month.

**SPEAKING POINTS**

1. Bridge from slide 12: that was the third rung — here is the whole ladder. All four versions, same engine, same scenarios, normal conditions, λ = 20/month.
2. Walk the figure once, panel by panel: every panel falls in order — lead, P90, human work, cost, rework — and the only panel that rises is capacity (note the log scale): ~20 → ~230/month. Every pre-registered ordering held: v3 < v2 < v1 < baseline throughout.
3. The condensed scoreboard — read the Iter-3 column, gesture at the rest: lead 21.8 → 6.8 → 4.0 → 1.6 d; work 600 → 438 → 351 → 62 min; cost ¥940 → ¥709 → ¥595 → ¥182 — minus 81 % cumulative; practical capacity ~20 → ~30 → ~38 → ~230/mo; rework 88 → 56 → 30 → 8 %. These are the same numbers you saw on slides 9–11 — every target validated end-to-end in one engine, not three separate promises. At Iteration 3 utilization is ~8 % — the queue is dead; capacity stops being the question.
4. The rule that makes it work — say it as a rule: **a chain, not a menu.** Each iteration consumes the previous one's data output — Brief JSON → Script JSON → Render job. Iteration 2's model needs structured Briefs; Iteration 3's renderer needs machine-readable Scripts. Skip a link and the chain breaks: automate production before standardizing intake and you auto-produce the wrong video faster.
5. Theory of Constraints, exactly as taught: identify (sync is the constraint) → exploit/subordinate (Iterations 1–2 standardize around it) → elevate (Iteration 3 deletes it) → repeat. The constraint's path: intake → scripting → sync → lawyer approval. After Iteration 3 it has left HiLegal — residual lead time ≈ 100 % client-side, 1.6 d SLA-shaped, 2.1 d if the lawyer rides the 48 h cap. Further improvement means managing the client, not more automation.
6. Keep the label honest, once: these are calculated scenarios — simulated designs with targets, not tested results. The stress test is what makes them credible rather than aspirational.
7. Hand-off: "That's the design, simulated. Now let's stress-test it." → slide 15 (Joel, five scenarios).

**DATA STATUS** — Everything on this slide is simulation output, labelled on-slide *calculated scenarios (simulation) — targets, not results* (design-system rule: iterations are never presented as results; Section 7 is labelled *calculated scenario*). Condensed table: lead (21.8/6.8/4.0/1.6 d), human work (600/438/351/62 min) and practical capacity (~20/~30/~38/~230/mo) are the Section-6 iteration simulations (`iterationN_sim.py`, same engine lineage as the Section-4 study, sanity-checked rung over rung) — quoted identically to slides 9–11 for continuity; cost (¥940/709/595/182) and rework (88/56/30/8 %) are from the Section-7 S0 run (`compare_sim.py`, 3 seeds per point, λ = 20/mo). The figure shows that same S0 run, where the four versions re-simulate to lead 23.4/7.2/4.0/1.6 d, P90 36.9/10.5/5.3/2.1, work 600/437/349/61 min, work-content capacity 24/32/41/231/mo (the log panel), rework 88/56/30/8 % — same orderings; the small deltas against the Section-6 numbers (e.g. 21.8 vs 23.4 d lead, 438 vs 437 min work) are run-to-run configuration differences between the two simulation studies, not measurements. Cost steps −25 % / −37 % / −81 % cumulative per the Section-6 summary (the S0 costs round to the same percentages). Constraint path, client-side residual framing and utilization 8 % from the Section-6 summary. Detail in appendices A4 and A5.
