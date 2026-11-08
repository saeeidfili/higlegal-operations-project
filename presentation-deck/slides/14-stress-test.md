# Slide 14 — Stress test: the design holds under five scenarios

- **Speaker:** Saeed Filizadeh
- **Time:** 1:15
- **Figures:** `../07 Let's run and compare the processes/saturation.svg` — mean lead time (d) vs monthly demand λ (/mo), one curve per version (baseline · v1 · v2 · v3): baseline/v1/v2 bend upward off-scale, v3 stays flat. Place large — dominant, upper zone. Label: **calculated scenario**.
- **Related appendix:** A5 (`appendix/A5-scenario-matrix.md` — S0–S5 full result tables; remaining Section-7 charts `wip-paths.svg`, `slow-lawyers.svg`, `rework-stress.svg`)

## On-slide content

**Title:** Stress test: the design holds under five scenarios

**Status chip (top-right, doubles as the figure label):** `calculated scenario (simulation)`

**Figure (dominant, upper ~55 % of the slide, centered):** `saturation.svg` — lead time against demand, all four versions on one canvas. The older versions bend and leave; v3 runs flat. Caption: *Lead time vs demand, four versions — **calculated scenario***.

**Scenario results strip (five compact cells, full width, below the figure):**

| S1 · Demand surge | S2 · Slow lawyers (waits ×2.5) | S3 · Rework stress (p = 0.75/gate) | S4 · Producer absence (1 of 2, 2 wks) | S5 · Quality dip |
|---|---|---|---|---|
| v3 flat **1.6–2.2 d** from 15 → 200/mo | v3 worst **3.0 d** beats baseline's best 14 d | baseline **295 d** vs v3 **4.5 d** | invisible in v3: **1.6 d**, WIP 4 | v3 regressed **85 min · ¥216** |
| baseline explodes past 20/mo (93 d at 25) | baseline 23.4 → 49.8 d | the process does not function | baseline 31.6 d, WIP 30 | v2 normal: 349 min · ¥595 |

**Honest-finding line (bottom strip, full width):**

> **Honest finding** — v2 saturates at ~38/mo, *below* its work-content ceiling — exactly as queueing theory predicts (practical < work-content; the same 80–85 % rule)

## Layout

- **Background:** solid `#F3F4F6`, full bleed; the SVG is transparent-background — no border box, no extra decoration.
- **Title:** Momo Trust Display, ink `#101010`, top-left, one line; short-statement grammar.
- **Status chip:** Inter 24 px, muted `#6A7282`, 2 px grey-400 `#99A1AF` pill border, top-right on the title baseline. It carries the design-system figure label for everything on the slide: *calculated scenario (simulation)* — Section 7 is never presented as results.
- **Figure:** dominant element, centered in the upper zone under the title. Native aspect ≈ 1.6:1 — height-constrained: as large as ~52–55 % of slide height allows (≈ half the slide width). Do not overlay text; let the one flat line among three exploding ones carry the message. Caption Inter 24 px muted with the *calculated scenario* label.
- **Scenario strip (one row of five equal cells, full width):** white cards, 1 px grey-200 `#E5E7EB` borders, tight padding. Tag line (S1 · Demand surge …) Inter 24 px caps muted `#6A7282`; v3 numbers Inter semibold 26 px ink `#101010` — the eye's landing zone; baseline numbers Inter 24 px body `#4A5565`. No zebra fill, no vertical rules inside cells.
- **Accent red `#D92605` used once:** `295 d` in the S3 cell — the single catastrophic number on the slide.
- **Honest-finding strip (bottom-most, full width):** wait-fill `#F6EEDF` band, 2 px wait-line `#A8823F` left border. Lead-in "Honest finding" Inter semibold 24 px `#0A0A0A`; the rest Inter 24 px body `#4A5565`; "~38/mo" and "below" semibold `#262626`; the parenthetical tail muted `#6A7282`.
- **Density check:** 1 title + 1 chip + 1 figure + 5-cell strip + 1 strip; all text ≥ 24 px. No other decoration.

## Speaker notes

**TIME** — 1:15 (Saeed Filizadeh). Bridge ~5 s → figure ~20 s → strip walk ~35 s (≈7 s per scenario, read the v3 number, gesture at the baseline number) → honest finding ~10 s → hand-off ~5 s. If running long, drop S4 and S5 from the walk (the strip still shows them) and keep the honest finding.

**MAIN MESSAGE** — Under five openly hostile scenarios the redesigned process keeps its numbers: robustness is structural, not lucky — and where the designs do bend, they bend exactly where queueing theory says they should.

**SPEAKING POINTS**

1. Bridge from slide 13: that was normal demand — now let's be hostile. Same engine, same scenarios, demand / approvals / rework varied openly: five stress scenarios, all four versions each time.
2. Figure first: lead time against demand. Baseline explodes past 20/mo — 93 d at 25, 271 d at 30, unstable by 60; v1 unstable by 60; v2 degrades at 40 (28.8 d). v3 is flat at 1.6–2.2 d from 15 to 200/mo — it only bends at 240. WIP at 40/mo: baseline spirals, v3 stays at ≤ 4 videos. Demand stops being a capacity problem.
3. Strip walk, one breath per cell — read the v3 number, point at the baseline number:
   - **S2 slow lawyers** (every gate wait ×2.5): v3 1.6 → 3.0 d, baseline 23.4 → 49.8 d. v3's worst case beats baseline's best case (14 d) by 4×. The residual process time belongs to the client.
   - **S3 rework stress** (loop p = 0.75 at every gate — the proposal's worst case): baseline 295 d — the process does not function. v3: 4.5 d (P90 8.8). Worst-case robustness is designed in: cheap scene-level loops survive even 4 iterations per gate.
   - **S4 producer absence** (1 of 2 producers away, 2 weeks): invisible in v3 — 1.6 d, peak WIP 4; team load at this demand is ~4 h/mo. Baseline: 31.6 d, WIP 30. Capacity headroom is insurance.
   - **S5 quality dip** (v3's model regresses to v2-level loops plus deeper edits): dipped v3 still delivers 1.8 d, 85 min, ¥216 — far ahead of v2 *normal* at 349 min, ¥595. Graceful degradation: no iteration depends on perfection — capacity is structural, labour is QC-bound.
4. The honest finding, said proudly: v2 saturates at ~38/mo — *before* its work-content ceiling — practical capacity sits below work-content capacity, the same 80–85 % utilization rule the Section-4 models show. And v3 does bend at 240/mo. A stress test that only confirms is theater; ours shows the failures too.
5. Expectation check: every pre-registered ordering held — v3 < v2 < v1 < baseline throughout. And keep the label honest once: calculated scenario — simulated designs, not field results.
6. Hand-off: the process now has headroom. What is that headroom worth to HiLegal? → slide 14 (organizational impact).

**DATA STATUS** — Everything on this slide is Section-7 simulation output, labelled on-slide *calculated scenario (simulation)* (design-system rule: iterations are never presented as results; Section 7 is labelled *calculated scenario*). All runs from `compare_sim.py` in `07 Let's run and compare the processes/` — same engine lineage as the Section-4 study, 3 seeds per point, parameters from `single source of truth/kpi-data.md` [T], distributions uniform over stated ranges [E]; S3 overrides loop rates to the proposal's worst case p = 0.75 [C]; calendar days include weekends; seasonality not modeled. Engine calibrated so S0 reproduces the company-reported baseline: 23.4 d inside the reported 14–28 d [C], capacity ≈ reported 15–20/mo [C]. Figure (`saturation.svg`) shows the S1 sweep: baseline 93.2 d at 25/mo, 271.0 at 30, unstable by 60; v1 unstable by 60; v2 28.8 d at 40, unstable by 80; v3 1.6–2.2 d from 15 through 200/mo, 46.0 d at 240. Strip numbers: S2 baseline 23.4 → 49.8 d, v1 7.2 → 13.4, v2 4.0 → 7.3, v3 1.6 → 3.0 (P90 4.0); baseline best case 14 d [C]. S3 baseline 295.3 d (P90 403.9), v1 18.3, v2 10.4, v3 4.5 (P90 8.8). S4 baseline 31.6 d / WIP 30, v1 7.6 / 10, v2 4.3 / 6, v3 1.6 / 4; ~4 h/mo team load. S5 v3 normal 1.6 d / 61 min / 8 % / ¥182; v3 dipped 1.8 d / 85 min / 28 % / ¥216; v2 normal 4.0 d / 349 min / 30 % / ¥595. Honest finding: v2 practical saturation ~38/mo vs work-content ceiling 40.4/mo (the S0 table rounds to 41). Every pre-registered ordering held (v3 < v2 < v1 < baseline). Full tables in `scenario-results.md`; detail in appendix A5.
