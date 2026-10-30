# Assumptions & estimates [E] — ours, labelled

Everything we assumed, estimated, or decomposed. Sanity-checked against [C]
anchors; every one is replaceable when HiLegal shares real data (the pilot's
10-video time-log is designed for exactly that — Section 9, Phase 0).

## Economics

| Assumption | Value | Basis | Used in |
|---|---|---|---|
| Producer gross salary | ¥10,000/month | Shenzhen market ¥8–14k | S2, all cost figures |
| Employer burden (五险一金) | ~35% → ¥3,500/month | statutory band 30–40% | S2 |
| Equipment/software/office | ¥1,500/month | | S2 |
| **Fully-loaded producer** | **¥15,000/month ÷ 176 h = ≈ ¥85/h** | 22 d × 8 h | S2, S5, S8 |
| FX | USD/CNY 7.2 | $100 tier ≈ ¥720 | S2, S8 |
| Manual tool credits | ¥90/video | ChatGPT + Seedance + TTS + stock | S2 ¥940 build |
| Two producers fully loaded | ≈ ¥360k/year | 2 × ¥15k × 12 | S4 skills waste, S8 |
| Payroll released after Iter 3 | ≈ **¥270k/year** (~1.5 FTE) | management decision to reallocate | S8, S9 |
| Iter-3 tech costs | render API ¥45 · self-hosted LLM ¥20 · amortized pipeline ¥30 /video | market rates, dual-vendor | S5 cost ladder |
| Typical customer usage | ~2 of the 10 promised videos/month | [E] | S2/S8 tables |

## Availability, hours, utilization

| Assumption | Value | Where used |
|---|---|---|
| Paid hours | 22 wd × 8 h = **176 h/month** (2 × 176 = 352 h) | queue model, rework sim |
| Productive hours (KPI) | **160 h/month** | KPI capacity math |
| KPI utilization | **60%** → 2 × 160 × 60% ≈ **11,500 productive min/month** (back-solved from output 15–20 [C]) | S5 §4, S7 |
| Video dedication (models) | **67%** → 480 × 0.67 ≈ **322 effective min/producer-day** | queue model, rework sim |
| Calendar conversion | 1 working day ≈ 1.4 calendar days (30.4 ÷ 21.7); 1 month = 22 wd | all models |

## Decomposition of the ~10 h per video [C]

**Version A — KPI labour waterfall** (`05 .../kpi-data.md` §1; totals are the
quoted figures, split is [E]):

| Activity | Baseline min |
|---|---:|
| Intake & clarification handling | 60 |
| Content brief | 50 |
| Script drafting | 80 |
| Script editing & QC (AI refinement) | 40 |
| Video generation ops | 60 |
| Audio generation ops | 35 |
| AV sync | **150 [C 2–3 h]** |
| Platform adaptation | **100 [C ~2 h]** |
| Delivery & publishing | 25 |
| **Total** | **600 = 10 h [C]** |

**Version B — rework-simulation task minutes** (`03 .../Rework/rework_simulation.py`
`MIN` dict; first-time-right = 516, loops add the rest):

intake review 15 · clarification reply 8/round · brief 45 · drafting 70 ·
AI refinement 35 · video gen 55 · audio 30 · **AV sync 140 [C]** ·
**platform adaptation 95 [C]** · delivery & admin 23 → **516**; loops:
script rework 50, final rework 70. Baseline expectation 591, simulated 588.

Both decompose the same [C] total; **only the total is data** — replace with
the pilot time-log when it exists.

## Waits & loops (simulation inputs)

| Assumption | Value | Used in |
|---|---|---|
| Clarification wait | U(1–2) working days per round | rework sim |
| Script / final approval wait | U(1–3) working days | rework sim, S3 trace |
| Baseline loop probabilities | p_clar 0.75 (→ mean 4 rounds [C]) · p_script = p_final 0.30 (→ work ≈ 600 [C]) | rework sim calibration |
| Rework incidence | ~90% of videos loop ≥ 1 gate (QAR ~10%) | S5 KPI-5/6 |
| Arrival process | Poisson at λ = 15–20/month [C range], 17.5 typical | all queue/sim models |
| Iter-3 render | batch ~20–30 min wall-clock, ~0.5 d incl. queue | S6 Iter 3, S7 |

## Lawyer-side (illustrative — keep clearly [E])

| Assumption | Value |
|---|---|
| Cross-border lawyer billing | $200–500/h |
| Worth of one won engagement | multiples of the ¥8.6k annual subscription |
| Campaign damage mechanisms | momentum loss, content expiry, lost inbound [E — standard platform behavior] |
