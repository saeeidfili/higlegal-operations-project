# Slide 8 — Rework adds 84 minutes of work and eleven days of waiting

**Speaker:** Dedi Li
**Time:** 1:15
**Figures:** `../04 These are the wastes and root causes/Rework/rework-impact.svg` (headline chart — lead + P90 per scenario vs hands-on work per video; place large)
**Related appendix:** `A3-rework-simulation.md`

## On-slide content

- Eyebrow: `DEFECTS, QUANTIFIED`
- Title: `Rework adds 84 minutes of work and eleven days of waiting`
- Stat block (the ~29× line, left column under title):
  - `+84 min of work → +10.8 days of lead` — `no rework → baseline · same team, same demand`
  - `queue cost ~29× work cost` — `the wait is the bill, not the work`
- Results table (left column, below stat block):

  | scenario | p_clar / p_script / p_final | rework % | lead | work / video | capacity |
  |---|---|---:|---:|---:|---:|
  | no rework | 0 / 0 / 0 | 0% | 11.0 d | 516 min | 27.4/mo |
  | halved | 0.50 / 0.10 / 0.20 | 66% | 15.1 d | 551 min | 25.7/mo |
  | **baseline** | **0.75 / 0.20 / 0.40** | **87%** | **21.8 d** | **600 min** | **23.6/mo** |
  | heavy | 0.80 / 0.40 / 0.60 | 93% | 31.1 d | 686 min | 20.6/mo |

- Table footnote: `baseline = simulation calibrated to [C] · no rework / halved / heavy = calculated scenarios · λ = 17.5 videos/month`
- Figure: `rework-impact.svg`, placed large, right zone — left panel: lead-time bars (mean) with P90 whiskers 13.1 / 21.8 / 34.1 / 54.8 d; right panel: hands-on work per video 516 → 686 min with the `company baseline ≈ 600 min [C]` marker
- Figure label: `calculated scenario — discrete-event simulation of the 12-step process · baseline calibrated to [C] (≥4 clarification rounds, ~10 h/video) · no rework / halved / heavy = calculated scenarios`
- Demand-sweep punchline (under the figure label, right zone):
  - `Push volume to 22 videos/month:`
  - `no rework absorbs it — WIP 8.9 · 12.5 d` · `heavy rework is past capacity — WIP 86.3 · 116.7 d ✗ unbounded backlog`
- Ceiling line (bottom band, the punchline):

  > "The ceiling is a property of the team plus its rework."

## Layout

- **Background:** solid `#F3F4F6`, full bleed. Two zones + bottom band: left column ~36 % width, right zone ~58 %, quote band full width.
- **Eyebrow:** Inter, 24 px, all caps, letter-spacing 0.15 em, gold `#C9A86A`, top-left above the title.
- **Title:** Momo Trust Display, ink `#101010`, ~44 px, left-aligned, two lines, top of left column.
- **Stat block:** lead phrases Inter semibold 28 px text `#262626` (`+84 min of work → +10.8 days of lead`, `queue cost ~29× work cost`); glosses Inter 24 px body `#4A5565`; 16 px whitespace between the two beats, no boxes.
- **Accent red `#D92605` used once in text:** the `~29×` — the single number the eye should catch. The heavy-rework bar and whiskers already carry the figure's own red; add no other red.
- **Table:** header row Inter 24 px, all caps, muted `#6A7282`; body Inter 26 px `#262626`, numbers right-aligned; 1 px grey-200 `#E5E7EB` row rules. Baseline row emphasized: white fill, 2 px gold `#C9A86A` left border, values semibold ink `#101010`. A 12 px color swatch precedes each scenario name, matching the bars: no rework grey-400 `#99A1AF` · halved wait-line `#A8823F` · baseline gold `#C9A86A` · heavy accent red `#D92605` — the table reads as a legend for the chart. Footnote Inter 24 px, muted `#6A7282`, one line under the table.
- **Figure:** dominant, top of right zone, as large as the column allows at native aspect ≈ 2.03:1 (~55 % of slide width); transparent-background SVG, no border box. In-SVG callouts do the annotation (P90 whisker labels, the 600-min [C] marker, "bar = mean · whisker = P90"); do not overlay extra text on the figure.
- **Figure label:** Inter, 24 px, muted `#6A7282`, max two lines directly under the figure, right-aligned to the figure's right edge.
- **Demand-sweep punchline:** under the figure label, right zone. Kicker `Push volume to 22 videos/month:` Inter semibold 26 px `#262626`; two lines Inter 24 px body `#4A5565` with the values (`WIP 8.9 · 12.5 d`, `WIP 86.3 · 116.7 d`) semibold text `#262626`; the `✗` in wait-line `#A8823F`.
- **Ceiling band:** full-width strip pinned ~64 px from the bottom edge, fill wait-fill `#F6EEDF`, 2 px wait-line `#A8823F` left border; line in Inter italic 26 px text `#262626`. Same band treatment as slide 6 — one motif band per Dedi slide.
- All text ≥ 24 px. No other decoration.

## Speaker notes

**TIME:** 1:15 (Dedi Li) — ~15 s what we simulated, ~25 s chart + table, ~15 s the ~29× arithmetic, ~15 s the ceiling, ~10 s the demand sweep, ~5 s close into slide 8 (KPIs).

**MAIN MESSAGE:** Rework looks like extra work but is mostly extra waiting — +84 minutes of hands-on work buys +10.8 days of lead time — and it moves the team's capacity ceiling, because the ceiling is a property of the team plus its rework.

**SPEAKING POINTS:**

- Bridge from slide 7: the intake queue explained the 3–7 day wait. This slide is the rest — what the three approval loops do to the whole 12-step chain.
- Method in one breath: discrete-event simulation of the full process — two producers, one pooled task queue, no preemption, three looping gates (clarification, script approval, final approval). Same fit-then-verify discipline as μ = 23.5: the loop probabilities are fitted to company facts — ≥4 clarification rounds [C] gives p_clar = 0.75; ~10 h of work [C] pins p_script = 0.20 and p_final = 0.40 — then lead time, work, incidence and capacity are held back and verified: 21.8 d lands inside 14–28 d [C], 600 min matches [C], 23.6/mo against demand 15–20 [C], 88% vs ~90% loops [E].
- Walk the chart, left panel: same team, same demand — no rework 11.0 d, baseline 21.8 d, heavy 31.1 d. Whiskers are P90: 13.1 → 34.1 → 54.8 d. The worst-served 10% of lawyers take half the pain.
- Right panel: hands-on work barely moves — 516 → 600 → 686 min. That is the headline arithmetic: +84 minutes of work, +10.8 days of lead — queue cost ~29× work cost. "Rework costs ~11 days for under an hour and a half of work."
- Why loops cost days, not minutes (one breath): every loop is a fresh gate wait plus another turn in the producer queue; variability amplifies; WIP inflates (Little's Law); capacity erodes 27.4 → 23.6 → 20.6 videos/month; utilization climbs 65% → 70% → 87% — back onto slide 6's cliff.
- The ceiling line: same two producers, same 22 working days, same 322 effective minutes — remove the loops and the ceiling is 27.4/month; keep them and it is 23.6; heavy, 20.6. Land the on-slide quote: the ceiling is a property of the team plus its rework.
- Demand-sweep punchline: push volume to 22 videos/month — no rework absorbs it easily (WIP 8.9, 12.5 d); heavy rework is already past capacity — WIP ≈ 86, lead ≈ 117 days, unbounded backlog. Volume growth is unreachable until the loops shrink; overtime cannot buy this back.
- Close: kill the loops, not the overtime — rework reduction is the single largest lead-time lever. Next slide: the KPIs we will hold ourselves to, then Saeed shows the iterations aimed at exactly these three gates.

**DATA STATUS:** All numbers from the rework simulation summary only. Company-reported [C]: ≥4 clarification rounds (→ p_clar = 0.75), ~10 h total work per video (→ p_script = 0.20, p_final = 0.40), lead 14–28 d, demand 15–20/month, the ≈600-min baseline marker in the chart. Estimate [E]: ~90% loop incidence (model predicts 88% closed-form, 87% simulated). Calculated: everything in the table and both punchlines — leads 11.0 / 15.1 / 21.8 / 31.1 d, P90 13.1 / 21.8 / 34.1 / 54.8, work 516 / 551 / 600 / 686 min, capacities 27.4 / 25.7 / 23.6 / 20.6/mo, +84 min / +10.8 d / ~29×, and the demand-sweep WIP/lead pairs. Labeling per deck rules: baseline = simulation calibrated to [C]; no rework / halved / heavy = calculated scenarios — heavy is a stress scenario, not a forecast. Reproducibility: every run seeded, engine audited against the closed-form E[work] on every run (516/516 … 686/686). Model-card caveats (A3): intake wait a lower bound (work-conserving), loop probabilities fixed — no congestion→rework feedback, so results are conservative; per-task minutes are our decomposition [E]. Say "calibrated simulation", never "measured". Detail in appendix A3.
