# Appendix A5 — The stress tests: S0–S5 full results

**Appendix A5 · Q&A** — untimed backup, no speaker, no clock
**Drops on:** any stress-test, simulation, robustness or "where does it break?" challenge (default backup for slide 13)
**Feeds slides:** 13 (stress test — full tables behind the five-cell strip) · 12 (S0 scoreboard context)
**Figures:** `../07 Let's run and compare the processes/wip-paths.svg` (S1 · WIP paths at λ = 40/mo — baseline spirals, v3 stays ≤ 4 videos) · `../07 Let's run and compare the processes/slow-lawyers.svg` (S2 · lead time, normal vs gate waits ×2.5) · `../07 Let's run and compare the processes/rework-stress.svg` (S3 · p = 0.75/gate) — all labeled *calculated scenario*

## On-slide content

**Eyebrow:** APPENDIX A5 · Q&A BACKUP

**Title:** The stress tests: S0–S5 full results

**Status chip (top-right, doubles as the slide-wide label):** `calculated scenario (simulation)`

**1 · The scenario matrix — one table, six stress tests**

| # | Scenario · what varies | Headline — v3 vs baseline |
|---|---|---|
| **S0** | Normal conditions · λ = 20/mo (reference run) | **1.6 vs 23.4 d** · ¥182 vs ¥940 · rework 8 vs 88% |
| **S1** | Demand surge · λ = 15 → 240/mo | v3 flat **1.6–2.2 d** to 200/mo; baseline explodes past 20/mo, unstable by 60 |
| **S2** | Slow lawyers · every gate wait ×2.5 | **3.0 vs 49.8 d** — v3's worst case beats baseline's best case (14 d [C]) by 4× |
| **S3** | Rework stress · loop p = 0.75 at every gate (proposal worst case) | **4.5 vs 295 d** — baseline does not function |
| **S4** | Producer absence · 1 of 2 away, 2 weeks | **1.6 vs 31.6 d** · peak WIP **4 vs 30** |
| **S5** | Quality dip · v3 regresses to v2-level loops + deeper edits | dipped **1.8 d · ¥216** still beats v2 normal (4.0 d · ¥595) |

**2 · S0 · normal conditions (λ = 20/mo) — the anchor run**

| version | lead d | P90 d | work min | ¥/video | cap/mo | rework | QAR |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 23.4 | 36.9 | 600 | 940 | 24 | 88% | 12% |
| v1 · standardize | 7.2 | 10.5 | 437 | 709 | 32 | 56% | 44% |
| v2 · AI scripting | 4.0 | 5.3 | 349 | 595 | 41 | 30% | 70% |
| **v3 · single render** | **1.6** | **2.1** | **61** | **182** | **231** | **8%** | **92%** |

The slide-12 scoreboard, now simulated: lead 23.4 → 1.6 d, cost ¥940 → ¥182, rework 88% → 8%.

**3 · S1 · demand surge — mean lead (d) by λ**

| λ/mo | baseline | v1 · standardize | v2 · AI scripting | v3 · single render |
|---:|---:|---:|---:|---:|
| 15 | 21.2 | 6.5 | 3.8 | 1.6 |
| 20 | 23.4 | 7.2 | 4.0 | 1.6 |
| 25 | 93.2 | 8.9 | 4.5 | 1.6 |
| 30 | 271.0 | 16.2 | 5.2 | 1.6 |
| 40 | 499.5 | 243.9 | 28.8 | 1.6 |
| 60 | unstable | unstable | 453.7 | 1.6 |
| 80 | unstable | unstable | unstable | 1.6 |
| 120 | unstable | unstable | unstable | 1.7 |
| 160 | unstable | unstable | unstable | 1.8 |
| 200 | unstable | unstable | unstable | 2.2 |
| 240 | unstable | unstable | unstable | 46.0 |

- **Baseline explodes past 20/mo:** 93.2 d at 25 · 271.0 at 30 · 499.5 at 40 · unstable by 60
- **v2 degrades at 40:** 28.8 d at 40 · 453.7 at 60 · unstable by 80 (practical saturation ~38/mo)
- **v3 flat:** 1.6–2.2 d from 15 through 200/mo · bends only at 240 (46.0 d)

**4 · S2 · slow lawyers (all gate waits ×2.5)**

| version | normal d | slow d |
|---|---:|---:|
| baseline | 23.4 | 49.8 |
| v1 · standardize | 7.2 | 13.4 |
| v2 · AI scripting | 4.0 | 7.3 |
| **v3 · single render** | **1.6** | **3.0** (P90 4.0) |

v3's worst case beats baseline's best case (14 d [C]) by 4× — *the residual process time belongs to the client*.

**5 · S3 · rework stress (loop p = 0.75 at every gate)**

| version | lead d | P90 d | rework |
|---|---:|---:|---:|
| baseline | 295.3 | 403.9 | 97% |
| v1 · standardize | 18.3 | 31.8 | 94% |
| v2 · AI scripting | 10.4 | 17.6 | 94% |
| **v3 · single render** | **4.5** | **8.8** | 93% |

Baseline: the process does not function. Worst-case robustness is designed in — cheap scene-level loops survive even 4 iterations per gate.

**6 · S4 · producer absence (1 of 2 away, 2 weeks)**

| version | cohort lead d (3 mo after) | peak WIP |
|---|---:|---:|
| baseline | 31.6 | 30 |
| v1 · standardize | 7.6 | 10 |
| v2 · AI scripting | 4.3 | 6 |
| **v3 · single render** | **1.6** | **4** |

The absence is invisible in v3 — team load ~4 h/mo at this demand. Capacity headroom as insurance.

**7 · S5 · quality dip (v3 regresses to v2-level loops + deeper edits)**

| config | lead d | work min | rework | ¥/video |
|---|---:|---:|---:|---:|
| v3 normal | 1.6 | 61 | 8% | 182 |
| **v3 dipped** | **1.8** | **85** | **28%** | **216** |
| v2 normal | 4.0 | 349 | 30% | 595 |

Graceful degradation: a regressed v3 still beats v2 *normal* on every axis — capacity is structural, labour is QC-bound.

**Figure strip (three thumbnails, bottom zone):**

- `wip-paths.svg` — S1 · WIP paths at λ = 40/mo: baseline spirals, v3 stays ≤ 4 videos. *Calculated scenario*
- `slow-lawyers.svg` — S2 · all four versions, normal vs gate waits ×2.5. *Calculated scenario*
- `rework-stress.svg` — S3 · p = 0.75/gate: baseline 295.3 d, v3 4.5 d. *Calculated scenario*

**Honest-findings band (bottom strip, full width):**

> **Honest findings** — (1) v2 saturates at ~38/mo, *below* its work-content ceiling (40.4/mo; the S0 cap column rounds to 41) — exactly as queueing theory predicts: practical < work-content, the same 80–85% rule the Section-4 models show. (2) "Unstable" cells = the backlog grows without bound — arrivals exceed throughput; it is not a large finite number. And v3 does bend: 46.0 d at 240/mo. Every pre-registered ordering held (v3 < v2 < v1 < baseline throughout).
>
> **Method** — same engine as every section (Section-4 lineage, `compare_sim.py`) · 3 seeds per point · parameters from `single source of truth/kpi-data.md`, distributions uniform over stated ranges · everything on this slide is **calculated scenario**.

## Layout

- **Background** `#F3F4F6`; **seven white cards** + one figure strip + one honest band. 1 px `#E5E7EB` borders, generous-but-tight padding. Q&A density is acceptable; hierarchy must survive it.
- **Band 1 (full width): card 1 — the scenario matrix.** The slide's map: every other card hangs off an S-row. Six data rows, compact.
- **Band 2: card 2 (S0, ~46% width) + card 3 (S1, ~54%).** The S1 λ-table is the tallest, densest block on the slide — give it the band's full height; the S0 card top-aligns with its 8-column table (tightest tabular figures of the slide) and the scoreboard line beneath.
- **Band 3: four equal cards — S2 · S3 · S4 · S5**, one row. Small tables (3–4 rows) + one takeaway line each.
- **Band 4: figure strip** — three equal thumbnails, no borders (transparent SVGs on bg), captions beneath. Thumbnails are anchors for Q&A zoom-ins, not reading material.
- **Band 5 (bottom, full width): honest-findings band** — wait-fill `#F6EEDF`, 2 px wait-line `#A8823F` left border; lead-in "Honest findings" Inter semibold 24 px `#0A0A0A`; findings in body `#4A5565` with "~38/mo", "below", "grows without bound" semibold `#262626`; method line last, muted `#6A7282`.
- **Card headings** Inter semibold 26 px `#262626`, S-numbered ("S0 · Normal conditions…") so any audience question ("what about the lawyers one?") lands on a card instantly.
- **v3 rows are the landing zone** in every table: thin gold `#C9A86A` rule above the row, values semibold ink `#101010`. All other numerals Inter 24 px body `#4A5565`, tabular figures, right-aligned. Column headers muted `#6A7282`. All text ≥ 24 px.
- **Accent red `#D92605` reserved for the catastrophic cells:** every "unstable" cell (italic) and baseline's 295.3 / 403.9 in S3 — the "does not function" signal. Nothing else.
- **Title** Momo Trust Display, `#0A0A0A`, one line, short-statement grammar; eyebrow "APPENDIX A5 · Q&A BACKUP" muted `#6A7282`, Inter 24 px, letterspaced caps; status chip top-right on the title baseline, Inter 24 px muted with 2 px grey-400 `#99A1AF` pill border.
- **Density check:** 1 title + 1 chip + 7 cards + 3 thumbnails + 1 band. If the build overflows, compress in order: shrink thumbnails → tighten band-3 padding → tighten matrix rows. Never drop a table row.
- Figure paths (from `presentation-deck/`): `../07 Let's run and compare the processes/wip-paths.svg` · `slow-lawyers.svg` · `rework-stress.svg` — same folder.

## Speaker notes

**MAIN MESSAGE:** This slide is the receipt for slide 13. Every stress-test number quoted from the stage has its full table here — six scenarios, four versions each, same engine, 3 seeds per point, everything tagged *calculated scenario*. Answer pattern: **find the S-row in the matrix → open the card → read the v3 row (gold) → read the baseline row → name the honest finding if one attaches.** Prepared answers:

1. *"What does 'unstable' actually mean?"* → In those cells arrivals exceed sustained throughput: the backlog grows without bound within the run — we print "unstable" instead of a meaninglessly large number. Baseline unstable by 60/mo, v1 by 60, v2 by 80.
2. *"Is v2's early saturation a bug?"* → No — it's the finding. v2 saturates at ~38/mo, *below* its 40.4/mo work-content ceiling, exactly as queueing theory predicts (practical < work-content; the same 80–85% rule the Section-4 models show). We show it because it validates the engine, not despite it.
3. *"Where does v3 finally break?"* → At 240/mo: 46.0 d against the 1.6–2.2 d flat zone from 15 through 200. The S0 cap column says 231/mo — roughly 12× the company-reported 15–20/mo demand [C].
4. *"p = 0.75 per gate is extreme."* → It is the proposal's documented worst case [C], applied at *every* gate. The point is contrast: baseline 295.3 d (P90 403.9) — the process does not function; v3 4.5 d (P90 8.8), because its loops are cheap scene-level regenerations. Robustness is designed in, not hoped for.
5. *"What if the AI model regresses?"* → S5: v3 dipped to v2-level loops plus deeper edits still delivers 1.8 d, 85 min, 28%, ¥216 — ahead of v2 *normal* (4.0 d, 349 min, 30%, ¥595) on every axis. Graceful degradation; no iteration depends on perfection.
6. *"Why believe the engine?"* → It is calibrated so S0 reproduces the company-reported baseline: 23.4 d inside the reported 14–28 d [C], capacity ≈ the reported 15–20/mo [C]. Same engine lineage as every section; parameters from the single source of truth; ranges, not fake precision.
7. Figures on demand: zoom `wip-paths.svg` (S1 at 40/mo — baseline spirals, v3 ≤ 4 videos), `slow-lawyers.svg` (S2), `rework-stress.svg` (S3) when the question is about a specific scenario.

**DATA STATUS:** Everything on this slide is Section-7 simulation output, labeled on-slide *calculated scenario (simulation)* (design-system rule: iterations are never presented as results). All tables from `scenario-results.md`, generated by `compare_sim.py` in `07 Let's run and compare the processes/` — same engine lineage as the Section-4 study, **3 seeds per point**; parameters from `single source of truth/kpi-data.md` [T], distributions uniform over stated ranges [E]; S3 overrides loop rates to the proposal's worst case p = 0.75 [C]; calendar days include weekends; seasonality not modeled. Engine calibration: S0 reproduces company-reported baseline — 23.4 d inside 14–28 d [C], capacity ≈ 15–20/mo [C]; baseline best case 14 d [C] (S2 comparison). **[C] anchors:** 14–28 d baseline lead; 15–20/mo output; 14 d best case; S3's p = 0.75. **[E]:** uniform wait/work distributions. **[T]:** version parameters from kpi-data targets. Honest findings as stated: v2 practical saturation ~38/mo vs work-content ceiling 40.4/mo (S0 cap column rounds to 41); "unstable" = backlog grows without bound; v3 bends at 240/mo (46.0 d); every pre-registered ordering held (v3 < v2 < v1 < baseline throughout). Figures (`wip-paths.svg` · `slow-lawyers.svg` · `rework-stress.svg`) are Section-7 output, same label. Numbers quoted: S0 lead 23.4/7.2/4.0/1.6 d, rework 88/56/30/8%, cost ¥940/709/595/182; S1 93.2 d at 25, 271.0 at 30, 499.5 at 40, v2 28.8 at 40 and 453.7 at 60, v3 1.6–2.2 d for 15–200/mo and 46.0 at 240; S2 49.8 vs 3.0 d (v3 slow P90 4.0); S3 295.3 vs 4.5 d; S4 31.6 vs 1.6 d and peak WIP 30 vs 4; S5 dipped 1.8 d / 85 min / 28% / ¥216 vs v2 normal 4.0 d / 349 min / 30% / ¥595.
