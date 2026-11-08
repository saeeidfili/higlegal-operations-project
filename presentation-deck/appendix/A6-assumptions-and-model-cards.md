# Appendix A6 — Assumptions, labels, and model cards

**Appendix A6 · Q&A** — untimed backup, no speaker, no clock
**Drops on:** any assumption, label, or model-validity challenge — "where does that number come from?", "what if your assumptions are wrong?", "why two different utilization figures?" (default backup for slides 5, 8, 14, 15)
**Feeds slides:** 5 (evidence tags on the waste table) · 8 (KPI baselines + tag legend) · 14 (connecting assumptions, ladder) · 15 (pilot replaces [E])
**Figures:** none — tables and model-card lists only

## On-slide content

**Eyebrow:** APPENDIX A6 · Q&A BACKUP

**Title:** Assumptions, labels, and model cards

**1 · Label discipline — no number without its tag**

| Tag | Meaning | Examples on the deck |
|---|---|---|
| **[C] company-reported** | HiLegal's own numbers | ~10 h/video · output 15–20/mo · ¥117 attribution · wait 3–7 d |
| **[E] estimate** | ours — built up, labelled, replaceable | ¥85/h rate · ~90% rework · −¥150–195k/yr |
| **[T] target** | simulated designs — **never presented as results** | iteration rungs ¥705 · ¥595 · ¥180 |
| *calculated scenario* | model output from tagged inputs | the Section-7 chain simulation |

> Every figure on every slide carries one of these. If a number has no tag, it does not belong on the slide.

**2 · The assumption ladder — every connecting assumption, stated**

| Assumption | Value | Basis | Risk if wrong |
|---|---|---|---|
| Labour rate / utilization | ¥85/h · 60% [E] | Shenzhen build-up; utilization back-solved from output [C] | Costs shift proportionally; iteration ranking unchanged |
| Revenue attribution | ¥117 [C] | HiLegal's own first assumption | Needs re-basing; direction robust (−81%) |
| Demand at scale | 20 → 40+/mo | Consistent with stated ceiling 35–40 [C] | At 20/mo, gains 2–3 still hold; gain 1 partially idles |
| Payroll reallocation | ≈ ¥270k/yr (1.5 FTE) | Management decision [E] | If absorbed by overhead, strategic gain deflates — mitigate via explicit budget decision (Section 9) |
| Quality held | QAR ≥ 90% | Pilot gates (Section 6) | Reputation risk — guarded by QC + QAR gates |
| Vendor economics | render ≈ ¥45 [E] | Market rates, dual-vendor | ±¥10 → ±6% cost — immaterial |

**3 · Queue model card — said on purpose**

- **μ is calibrated, not measured [E]** — fitted to reproduce the observed 3–7 d band [C] across the demand range
- **Poisson arrivals defensible** — independent lawyers, no coordination; bursts only make waits worse
- **M/M/1 is a simplification — chosen because the pickup process behaves as one pooled unit** (video held start-to-finish, no preemption)
- **Steady state assumed** — a normal month
- **Falsifiable:** the inbox should hold ≈ 2–5 parked requests — HiLegal can count it (inbox never >1 while waits run 3–7 d → the delay is batch-review cadence, not queueing)
- **Scope: intake queue only** — approval-gate waits sit on top
- **With churn/overtime (Section 2), reality is likely worse than modeled**

**4 · Rework model card — said on purpose**

- **Intake wait is a lower bound** — the engine is work-conserving; real interruptions only add delay
- **Loop probabilities fixed** — congestion→rework feedback not modeled → results conservative
- **Per-task minutes are our decomposition [E]** — only the total ~10 h + sync + adaptation are [C]
- **Heavy = stress scenario, not a forecast** — p = 0.80/0.40/0.60 exists to bound the downside

**5 · Baseline data quality — honest about what we hold**

- The baseline is **part [C], part [E]** — company-reported totals, our decomposition and rates
- **No controlled before/after comparison exists** — so we do not claim one
- Therefore: **simulate first → pilot before rollout → replace [E] with observations** (the Phase-0 10-video time-log pilot, Section 9, is designed for exactly that)

**6 · Two budgets, one concept — 60% vs 67%**

| Where | Utilization | Budget | What it produces |
|---|---|---|---|
| KPI capacity math | 60% | 2 × 160 h × 60% ≈ **11,500 min/month** | ÷ 600 min/video ≈ 19/mo ≈ reported output 15–20 [C] ✓ |
| Simulations (Section 4 models + iteration sims) | 67% dedication | 2 producers × 22 wd × 322 effective min (480 × 0.67) = **14,150 min/month** | queue capacity 23.5 · rework capacity 23.6/mo |

> Deliberate, documented in the single source of truth: the same concept at different granularity — **never mixed inside one calculation.**

## Layout

- Background `#F3F4F6`; **six white cards**, 1 px `#E5E7EB` borders, generous padding. Q&A density is acceptable; the tag column and card numbering must stay scannable.
- **Row 1 (full width, compact band):** card 1, the label discipline — four tag chips set as a 4-column row ([C] / [E] / [T] / calculated scenario), each chip: tag in Inter semibold 26 px `#0A0A0A`, meaning in Inter 24 px body `#4A5565`, examples in Inter 24 px muted `#6A7282`. The closing rule ("Every figure on every slide carries one…") in Inter italic 24–26 px `#262626`, with **never presented as results** in accent red `#D92605` — the only red on the slide.
- **Row 2 (full width, the spine — most height):** card 2, the assumption ladder. Four columns: assumption Inter semibold 24–26 px `#262626`; value right-aligned `#0A0A0A` semibold; basis Inter 24 px body `#4A5565`; risk-if-wrong Inter 24 px body with the mitigations ("iteration ranking unchanged", "guarded by QC + QAR gates") in `#262626`. Thin gold `#C9A86A` rules under the value column. Header row Inter 24 px caps muted `#6A7282` over a 1 px `#E5E7EB` rule.
- **Row 3 (two equal cards):** card 3 (queue model card) + card 4 (rework model card) — bullet lists, one claim per line, Inter 24 px; the claim's lead phrase semibold `#262626`, the gloss regular body `#4A5565`; tags inline, muted `#6A7282`. Card 3's falsifiable line and card 4's conservative line carry a 2 px gold `#C9A86A` left rule each — the "said on purpose" beats.
- **Row 4 (two cards, ~40/60):** card 5 (data quality — three lines, "simulate first → pilot before rollout → replace [E]" as three chips joined by arrows, arrows in grey-400 `#99A1AF`) + card 6 (two budgets — two-row table, value column with the minute budgets 11,500 / 14,150 in Inter semibold 26 px `#0A0A0A` under gold rules; closing rule in Inter italic 24 px `#262626` with **never mixed inside one calculation** semibold).
- Card headings: Inter semibold 26 px `#262626`, numbered ("1 · Label discipline…") so the answer pattern is scannable — same treatment as A1.
- Title in Momo Trust Display, `#0A0A0A`, one line, short-statement grammar; eyebrow "APPENDIX A6 · Q&A BACKUP" in muted `#6A7282`, Inter 24 px, letterspaced caps. All text ≥ 24 px. No figure, no icons, no decoration beyond the rules and the single red phrase.

## Speaker notes

**MAIN MESSAGE:** This slide is the deck's credibility floor. Nothing we presented asks to be believed — every number carries a tag, every model states its own limits on purpose, and every connecting assumption in the impact story is written down with its risk-if-wrong. The move in Q&A is always the same: **name the tag → point at the ladder or model card → offer the falsifiable prediction or the pilot that replaces the estimate.** Prepared answers:

1. *"How much of this is your estimate vs their data?"* → Card 1: company-reported totals are [C] (~10 h, 15–20/mo, ¥117, 3–7 d); rates, decompositions and behavioural shares are [E] and labelled as ours; every iteration rung is a [T] target — simulated designs, never presented as results; the Section-7 chain is labelled *calculated scenario*.
2. *"What if ¥85/h or the utilization is wrong?"* → Ladder row 1: the utilization is not invented — it is back-solved from their own output [C] (11,500 min ÷ 600 min/video ≈ 19/mo ≈ the reported 15–20). If the rate shifts, costs shift proportionally; the iteration *ranking* is unchanged.
3. *"Your models assume away reality — what's the worst case?"* → The model cards are the answer, said on purpose: queue model — μ calibrated not measured [E], M/M/1 because pickup behaves as one pooled unit, intake queue only, and with churn/overtime reality is likely *worse* than modeled; rework model — intake wait is a lower bound, fixed loop probabilities make results conservative, heavy is a stress scenario, not a forecast. The biases point against us, not for us.
4. *"Can you prove the queue story with data we already have?"* → Yes — the falsifiable inbox prediction: at ρ ≈ 0.74–0.85 the inbox should hold ≈ 2–5 parked requests. Count it tomorrow. If the inbox never exceeds 1 while waits run 3–7 d, the delay is batch-review cadence, not queueing — and we would say so.
5. *"Why do you quote 60% in the KPIs and 67% in the simulations?"* → Card 6: two budgets, one concept at different granularity. KPI math: 2 × 160 h × 60% ≈ 11,500 min → 19/mo, which reproduces their reported output. Simulations: 67% dedication → 14,150 min/month, the Section-4 basis (queue 23.5, rework 23.6/mo). Deliberate, documented in the single source of truth, never mixed inside one calculation.
6. *"What happens to the impact story if an assumption breaks?"* → Walk the ladder's right column: demand at 20/mo — gains 2–3 still hold, gain 1 partially idles; payroll absorbed as overhead — strategic gain deflates, so Section 9 makes the budget decision explicit; QAR below 90% — reputation risk, guarded by pilot gates; render ±¥10 → ±6% — immaterial. Every risk has its mitigation named before the audience does.
7. *"Is the baseline itself trustworthy?"* → Card 5: part [C], part [E], no controlled comparison exists — which is exactly why the plan is simulate first, pilot before rollout, and replace [E] with observations. The Phase-0 10-video time-log pilot is designed for exactly that; the change log in the single source of truth is where each replacement gets recorded.

**DATA STATUS:** Label discipline: [C] company-reported · [E] estimate · [T] target · *calculated scenario* (Section 7) — every figure on every slide carries one (README design system). Assumption ladder is the Section-8 summary verbatim: ¥85/h · 60% [E] (utilization back-solved from output [C]); ¥117 [C] (direction robust at −81%); demand 20 → 40+/mo consistent with stated ceiling 35–40 [C]; ≈ ¥270k/yr (1.5 FTE) payroll reallocation [E — management decision]; QAR ≥ 90% via pilot gates; render ≈ ¥45 [E], ±¥10 → ±6%. Queue model card is the Section-4 queue summary verbatim: μ = 23.5 calibrated not measured [E]; Poisson defensible (independent lawyers; bursts worsen waits); M/M/1 chosen because pickup behaves as one pooled unit (no preemption); steady state = a normal month; falsifiable inbox prediction ≈ 2–5 parked requests (Lq 2.2 at λ = 17.5, 4.9 at λ = 20); intake-only scope (approval-gate waits on top); churn/overtime → reality likely worse. Rework model card is the Section-4 rework summary verbatim: intake wait a lower bound (work-conserving); loop probabilities fixed → conservative (congestion→rework feedback not modeled); per-task minutes our decomposition [E], only total ~10 h + sync + adaptation [C]; heavy (0.80/0.40/0.60) a stress scenario, not a forecast. Data-quality note: baseline part [C] part [E], no controlled comparison → simulate first, pilot before rollout, replace [E] with observations (single-source-of-truth governance; Phase-0 time-log pilot). Two budgets: 60% KPI utilization → 2 × 160 h × 60% ≈ 11,500 productive min/month → ÷ 600 min ≈ 19/mo ≈ reported 15–20 [C]; 67% dedication → 2 × 22 wd × 321.6 effective min (480 × 0.67) = 14,150 min/month (queue μ = 23.5, rework 23.6/mo) — same concept at different granularity, documented in the single source of truth, never mixed inside one calculation. Sources: Section-8 summary (ladder, risks), Section-4 queue summary (model card, predictions), Section-4 rework summary (model card), `single source of truth/assumptions.md` + `kpi-data.md` §4 + `README.md` (two budgets, governance).
