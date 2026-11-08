# Appendix A3 — The rework simulation: loop math and the 29× queue cost

**Appendix A3 · Q&A** — untimed backup, no speaker, no clock
**Drops on:** any challenge to the rework numbers — where the p's come from, the ~29×, the capacity ceiling (default backup for slides 5 and 7)
**Feeds slides:** 5 (defects row: ~90% loop, +84 min → +10.8 d, ceiling 27.4 → 23.6 → 20.6/mo) · 7 (results table, headline, demand sweep)
**Figures:** `../04 These are the wastes and root causes/Rework/gantt-rework.svg` (extra time is repeated waiting, not work) · `../04 These are the wastes and root causes/Rework/rework-vs-demand.svg` (can we push more volume? — no)

## On-slide content

**Eyebrow:** APPENDIX A3 · Q&A BACKUP

**Title:** The rework simulation: loop math and the 29× queue cost

**1 · What the p's are — geometric loop logic**

Each of the three gates — G1 clarification · G2 script approval · G3 final approval — passes the video with probability 1−p and sends it back with probability p. Rounds at a gate are geometric:

```
mean rounds  = 1/(1−p)        expected loops = p/(1−p)
```

**Fit 1 — p_clar from "≥4 clarification rounds" [C]:**

```
1/(1−p) = 4   →   p_clar = 0.75
```

*Label: calculated — fitted to company-reported anchor*

**2 · Fit 2 — p_script = 0.20, p_final = 0.40 from the ~10 h total [C]**

First-time-right work (12 tasks, no loops):

```
15 + 8 + 45 + 70 + 35 + 55 + 30 + 140 + 95 + 23 = 516 min
```

(15 intake review · 8 clarification reply · 45 brief · 70 drafting · 35 AI refine · 55 video gen · 30 audio gen · 140 AV sync [C] · 95 adaptation [C] · 23 delivery admin)

Loop costs on top:

```
extra clarification replies : (4−1 rounds) × 8 min    = 24.0 min
script rework               : 50 × 0.20/(1−0.20)     = 12.5 min
final rework                : 70 × 0.40/(1−0.40)     = 46.7 min
                                                               ─────────
E[work] = 516 + 24 + 12.5 + 46.7                        = 599 ≈ 600 [C]
```

**p_final = 2 × p_script** — late-stage rejection is likelier: the client sees the real product only at the final gate. The 600-min anchor pins the pair (solved by `calibrate_loops.py`).

*Label: calculated — two unknowns, one anchor, one ratio*

**3 · Held back to verify — never fitted**

| Check | Math | Result | vs anchor |
|---|---|---:|---|
| Lead time | (delivered − arrival) × 1.4 → calendar d; mean over arrivals in months 10–25 | **21.8 d** | 14–28 d [C] ✓ |
| Work | 516 + 8×4 + 50×0.25 + 70×0.667 − 8 = 599.2 (516 already includes one 8-min reply; simulated 600) | **600 min** | ≈ 10 h [C] ✓ |
| Incidence | P(≥1 loop) = 1 − 0.25 × 0.80 × 0.60 = 1 − 0.12 | **88%** (sim. 87%) | ~90% [E] ✓ |
| Capacity | 14,150 ÷ 599 | **23.6/mo** | demand 15–20 [C] ✓ |
| Engine audit | closed form / simulated, every run | 516/516 · 547/551 · 599/600 · 686/686 | ✓ |

- Lead has **no closed form** — that is why it is simulated. It was never fitted, and it landed mid-band.
- Capacity math: budget = 2 producers × 22 wd × 321.6 eff. min (480 × 0.67) = **14,150 min/month** → capacity = budget ÷ E[work]. No rework 14,168 ÷ 516 = **27.4/mo** · halved 14,168 ÷ 551 = **25.7** · heavy 14,168 ÷ 686 = **20.6/mo**.

*Label: calculated — fitted on two anchors, verified on four more*

**4 · Results (λ = 17.5 videos/month) — and the ~29×**

| scenario | p_clar / p_script / p_final | rework % | lead | P90 | work / video | capacity |
|---|---|---:|---:|---:|---:|---:|
| no rework | 0 / 0 / 0 | 0% | 11.0 d | 13.1 | 516 min | 27.4/mo |
| halved | 0.50 / 0.10 / 0.20 | 66% | 15.1 d | 21.8 | 551 | 25.7 |
| **baseline** | **0.75 / 0.20 / 0.40** | **87%** | **21.8 d** | **34.1** | **600** | **23.6** |
| heavy | 0.80 / 0.40 / 0.60 | 93% | 31.1 d | 54.8 | 686 | 20.6 |

**Headline:** no rework → baseline, same team, same demand: **+84 min of work → +10.8 days of lead — queue cost ~29× work cost.** Remove rework: lead −49%, work only −14%.

Why loops cost days, not minutes — five mechanisms: ① each loop adds a fresh gate wait + another queue turn ② variability amplification ③ WIP inflation (Little's Law) ④ capacity erosion 27.4 → 23.6 → 20.6/mo ⑤ utilization toward the cliff 65% → 70% → 87%.

Figure: `gantt-rework.svg` — the extra time is repeated waiting, not work.
*Figure label: calculated scenario — baseline calibrated to [C]*

**5 · Demand sweep — the moving ceiling**

| λ /month | no rework (WIP · lead) | baseline | heavy |
|---:|---|---|---|
| 15 | 5.2 · 10.7 d | 10.1 · 21.2 | 14.5 · 29.6 |
| 17.5 | 6.2 · 11.2 | 12.7 · 22.4 | 17.2 · 30.6 |
| 20 | 7.6 · 11.8 | 15.3 · 23.4 | 36.4 · 54.6 |
| 22 | **8.9 · 12.5** | 19.4 · 28.9 | **86.3 · 116.7 ✗** |

No rework absorbs 22/month easily; heavy rework at 22 is past capacity — unbounded backlog.

> "The ceiling is a property of the team plus its rework."

Figure: `rework-vs-demand.svg`.
*Figure label: calculated scenario*

**6 · The engine in three lines + model card**

1. **Discrete-event** — a min-heap of scheduled events (arrival · task done · gate wait ended); the clock jumps event to event. Each video is a Python generator yielding `("work", minutes)` or `("wait", days)` through the 12 steps; at each gate a random roll — below p → loop again. Poisson arrivals: exponential gaps, mean 22/λ wd (λ = 17.5 → a request every ~1.26 wd).
2. **Pooled producers** — one shared task queue, two servers, first-come-first-served, work-conserving, no preemption. While a video waits at a client gate, its producer works other videos — that is how two producers juggle 1–2 staggered videos each.
3. **Clean measurement window** — 28-month run, videos arriving in months 10–25 only (first 10 months warm-up discarded, last 3 cut against censoring); WIP sampled twice per working day; sweeps 4 demand × 3 rework × 3 seeds over 36 months. Every run seeded; `run_report.py` calibrates, derives, simulates, sweeps and verifies in one run.

**Model card:** intake wait a lower bound (work-conserving) · loop probabilities fixed — no congestion→rework feedback, so results are **conservative** · per-task minutes are our decomposition [E], only the total ~10 h + sync + adaptation are [C] · heavy = stress scenario, not forecast.

## Layout

- Background `#F3F4F6`; **six white cards**, 1 px `#E5E7EB` borders, generous padding; numbered headings ("1 · What the p's are…") in Inter semibold 26 px `#262626`, thin gold `#C9A86A` rule under each. Q&A density is acceptable; hierarchy must survive it.
- Row 1: card 1 (~44% — geometric logic + fit 1) + card 2 (~56% — fit 2 with the two stacked math blocks). Card 2 is the tallest content; the `p_final = 2 × p_script` line gets the gold-rule treatment as the card's derived beat.
- Row 2: card 3 **full width** — the verification table is the slide's spine and its credibility claim; five rows, "vs anchor" column right-aligned with ✓ in gold `#C9A86A`. Give it the most height of the three table cards.
- Row 3: card 4 (~58% — results table + headline + five mechanisms) + card 5 (~42% — demand sweep + ceiling quote).
- Row 4: card 6 full width, slim, two inner columns: "engine in three lines" left (~60%), model card right (~40%) — reads as the methods footer.
- **Math blocks** in monospaced figures, 24 px, `#262626` on white; the `= 599 ≈ 600 [C]` and `p_clar = 0.75` result lines semibold with gold `#C9A86A` underline (same derived-row rule as A1). Formula parts muted `#6A7282`.
- **Tables:** header row Inter 24 px all caps muted `#6A7282`; body Inter 26 px `#262626`, numerals right-aligned, tabular figures; 1 px grey-200 row rules. Baseline row in card 4 emphasized: white fill, 2 px gold left border, semibold ink `#101010` — identical treatment to slide 7's table so the two read as the same object. Scenario swatches as on slide 7: no rework grey-400 `#99A1AF` · halved wait-line `#A8823F` · baseline gold `#C9A86A` · heavy accent red `#D92605`.
- **Accent red `#D92605`** appears exactly twice in text: the `~29×` in card 4's headline and the `86.3 · 116.7 ✗` cell in card 5 (the ✗ itself in wait-line `#A8823F`, as slide 7). Nothing else.
- **Figures, subordinate:** `gantt-rework.svg` (aspect ≈ 2.22:1) tucked at the bottom of card 4 under the mechanisms line; `rework-vs-demand.svg` (aspect ≈ 1.65:1) at the bottom of card 5 under the quote. Both small, transparent-background SVG, no border boxes, one-line labels in muted `#6A7282`. They are evidence for the two likeliest questions, not the main content — drop either if the card overflows.
- Ceiling quote in card 5: wait-fill `#F6EEDF` strip, 2 px wait-line `#A8823F` left border, Inter italic 26 px `#262626` — the same band motif as slide 7.
- Card labels (design-system line under each card, Inter 24 px muted): *calculated — fitted to company-reported anchor* (1) · *calculated — fitted to the ~10 h anchor* (2) · *calculated — fitted on two anchors, verified on four more* (3) · *calculated scenario — baseline calibrated to [C]* (4, 5). Footnote one line, muted: "[C] company-reported · [E] estimate".
- Title in Momo Trust Display, `#0A0A0A`, one line; eyebrow "APPENDIX A3 · Q&A BACKUP" Inter 24 px muted `#6A7282`, letterspaced caps. All text ≥ 24 px. No icons, no decoration beyond the rules, swatches and bands.

## Speaker notes

**MAIN MESSAGE:** This slide exists to defend slide 7's numbers end to end. The rework simulation follows the same fit-then-verify discipline as the queue model's μ = 23.5: **two anchors fitted, four held back and verified.** Answer pattern every time: *name the anchor → show the division → say what was never fitted.* Prepared answers:

1. *"Where do the p's come from?"* → Card 1: each gate passes with 1−p, loops with p; rounds are geometric, mean 1/(1−p), loops p/(1−p). Fit 1: the company reports ≥4 clarification rounds [C], so 1/(1−p) = 4 → p_clar = 0.75. Fit 2: first-time-right work sums to 516 min; loop costs 24 + 12.5 + 46.7 on top → E[work] = 599 ≈ 600 min [C], the ~10 h anchor. Two unknowns (p_script, p_final), one anchor, one ratio — p_final = 2 × p_script, because the client sees the real product only at the final gate; `calibrate_loops.py` solves the pair → 0.20 / 0.40.
2. *"You fitted the work — so the 600-min match is circular."* → Card 3: work used **two** anchors (4 rounds, ~10 h) and verified on **four it never saw**: lead time 21.8 d lands mid-band of 14–28 d [C] — and lead has no closed form, that is why it is simulated; incidence 1 − 0.25 × 0.80 × 0.60 = 88% vs ~90% [E] (simulated 87%); capacity 14,150 ÷ 599 = 23.6/mo vs demand 15–20 [C]; and the engine is audited against the closed-form E[work] on every run — 516/516, 547/551, 599/600, 686/686.
3. *"Is the ~29× real or a simulation artifact?"* → Same team, same demand, only the loops change: +84 min of hands-on work buys +10.8 days of lead. Five mechanisms, card 4: every loop is a fresh gate wait plus another queue turn; variability amplifies; WIP inflates (Little's Law); capacity erodes 27.4 → 23.6 → 20.6/mo; utilization climbs 65% → 70% → 87%, back onto slide 6's cliff. The gantt figure shows it directly: the extra time is repeated waiting, not work. Note the asymmetry — remove rework: lead −49%, work only −14%.
4. *"Can't they just push more volume / add overtime?"* → Card 5: at 22 videos/month, no rework absorbs it easily (WIP 8.9, 12.5 d); heavy rework is already past capacity — WIP 86.3, ≈ 117 d, unbounded backlog. The ceiling moves with the rework: the ceiling is a property of the team plus its rework. Overtime cannot buy back a utilization cliff.
5. *"Why should we trust the engine?"* → Card 6, three lines: discrete-event (clock jumps event to event; each video a generator yielding work/wait; a roll below p loops the gate); pooled producers (one shared queue, two servers, work-conserving, no preemption — gate waits free the producer, which is how two producers juggle 1–2 staggered videos each); clean window (months 10–25 arrivals only — warm-up cut, censoring cut; WIP sampled twice per working day; sweeps 4 × 3 × 3 seeds over 36 months). Every run seeded; `run_report.py` does calibrate → derive → simulate → sweep → verify in one run.
6. Never defend a number without naming its tag, and say "calibrated simulation", never "measured". Volunteer the model card before it is asked: intake wait is a lower bound (work-conserving); loop probabilities are fixed — no congestion→rework feedback, so the results are conservative, not flattering; per-task minutes are our decomposition [E], only the total ~10 h plus sync and adaptation are [C]; heavy is a stress scenario, not a forecast.

**DATA STATUS:** All numbers from the rework simulation summary only. **Fitted to [C] anchors:** ≥4 clarification rounds → p_clar = 0.75; ~10 h total work per video (516 first-time-right + 24 + 12.5 + 46.7 = 599 ≈ 600 min) → p_script = 0.20, p_final = 0.40 via p_final = 2 × p_script (`calibrate_loops.py`). **Verified against anchors never fitted:** lead 21.8 d vs 14–28 d [C]; work 600 vs ≈ 10 h [C]; incidence 88% closed form / 87% simulated vs ~90% [E]; capacity 23.6/mo vs demand 15–20 [C]. **[E] estimates:** ~90% loop incidence; the per-task minute decomposition (only the ~10 h total, 140-min AV sync and 95-min adaptation are [C]). **Calculated:** budget 2 × 22 wd × 321.6 = 14,150 min/month (docs round to 322 → 14,168; no-rework/halved/heavy rows use it); capacities 27.4 / 25.7 / 23.6 / 20.6/mo; +84 min / +10.8 d / ~29×; the −49% lead vs −14% work split; utilization ladder 65% → 70% → 87%. **Simulated:** leads 11.0 / 15.1 / 21.8 / 31.1 d, P90 13.1 / 21.8 / 34.1 / 54.8, rework % 0 / 66 / 87 / 93, the demand-sweep WIP · lead pairs. Labeling per deck rules: baseline = simulation calibrated to [C]; no rework / halved / heavy = calculated scenarios — heavy is a stress scenario, not a forecast. **Reproducibility:** every run seeded; engine audited against closed-form E[work] on every run (516/516 · 547/551 · 599/600 · 686/686); `run_report.py` is the end-to-end report. Model-card caveats as in point 6 — results conservative on both counts.
