# KPI Master Data — single source of truth

Team: Augustin · Dedi · Joel · Saeed — HiLegal project, October 2026
Legend: **[C]** company-reported (confirmed with HiLegal, Sept 2026) · **[E]** estimate/assumption (ours) · **[T]** target
Key assumptions: **fully-loaded producer rate ¥85/h [E] (build-up in §3) · video dedication 60% of 160 h [E] · FX USD/CNY 7.2 [E] · subscription: most popular tier $100/month ≈ ¥720, promising 10 videos/month [C] · revenue attribution = model costs ¥90 + 30% overhead ≈ ¥117/video (HiLegal's own first assumption [C])**.

---

## 1. Labour waterfall — minutes of producer time per delivered video (monthly average, incl. rework rounds)

| Activity | Baseline | Iter 1 | Iter 2 | Iter 3 | Mechanism of change |
|---|---:|---:|---:|---:|---|
| Intake & clarification handling | 60 [E] | 15 | 15 | 10 | Iter 1: structured self-serve brief + auto completeness check replaces email ping-pong |
| Content brief creation / review | 50 [E] | 10 | 10 | 5 | Iter 1: brief auto-generated from form + lawyer profile; producer only reviews |
| Script drafting (human) | 80 [E] | 55 | 0 | 0 | Iter 1: correct brief → fewer redo rounds; Iter 2: LLM drafts, human stops writing |
| AI generation parameter check | — | — | 5 | 5 | Iter 2: select template/params, trigger generation |
| Script editing & QC (human) | 40 [E] | 25 | 30 | 15 | Iter 1: fewer loops; Iter 2: edit-not-write (slightly up per pass, loops fewer); Iter 3: mature templates + model feedback from accepted edits |
| Video generation ops | 60 [E] | 60 | 45 | 0 | Iter 2: scene-level prompt hints generated with script; Iter 3: fused into single render |
| Audio generation ops | 35 [E] | 35 | 25 | 0 | Iter 3: voice generated inside the single render |
| Audio-visual synchronization | **150 [E; reported range 2–3 h]** | 135 | 135 | 0 | Iter 1–2: only rework-reduction effect; **Iter 3: deleted by single-render avatar pipeline** |
| Render batch setup & QA | — | — | — | 20 | Iter 3: human watches output, checks likeness/names/captions (retries add ~5 min avg) |
| Platform adaptation | **100 [E; reported approximate ~2 h]** | 90 | 75 | 0 | Iter 3: auto variants 16:9 / 9:16 / 1:1 from same render |
| Delivery & administration | 25 [E] | 10 | 10 | 5 | Iter 1: auto-notify + structured delivery; Iter 3: auto-deliver + objection window |
| **TOTAL** | **600 min = 10 h 00 [C]** | **435 = 7 h 15** | **350 = 5 h 50** | **60 = 1 h 00** | |
| Δ vs previous | — | −28% | −20% | −83% | |
| Δ vs baseline | — | −28% | −42% | −90% | |

*Sums check: 600 = 60+50+80+40+60+35+150+100+25 · 435 = 15+10+55+25+60+35+135+90+10 · 350 = 15+10+5+30+45+25+135+75+10 · 60 = 10+5+5+15+20+5.*

*Iteration 3 note: 60 min is the steady-state target after ~50 videos of template/model maturation; expect 75–90 min during pilot phase [E]. A 60-minute target does not satisfy a strict under-60-minute claim. The model expectation including residual rework is 61.45 minutes; the strict proposal target is not demonstrated.*

## 2. Lead time build-up — calendar days, midpoint (range)

| Component | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| Intake queue | 3–7 d [C] | 0 (auto-route) | 0 | 0 |
| Clarification loop | 2–4 d [E] | 0 (format previews at intake) | 0 | 0 |
| Script production (draft+refine / AI+edit) | 2–3 d [E] | 1–2 d | same day | same day |
| Script approval wait | 1–3 d [E] | ≤2 d (48 h SLA, reminders) | ~1 d (in-app mobile) | ~1 d (24–48 h) |
| Video+audio production | 2–3 d [E] | 2 d | 1–2 d | 0.5 d (batch render ~30 min + queue) |
| Final approval wait | 1–3 d [E] | ≤2 d (SLA) | ~1 d | 0 d (objection window runs parallel — no serial wait) |
| Delivery | 1 d [E] | same day | same day | automatic |
| **LEAD TIME (midpoint, range)** | **~21 d (14–28) [C]** | **~9 d (7–12) [T]** | **~4 d (3–5) [T]** | **~1.5 d (1–2) [T]** |

Little's Law framing: baseline WIP sits in untracked queues (inboxes); from Iteration 1 every queue is visible and SLA-capped. **After Iteration 3 the residual lead time includes lawyer approval, render and QC — the constraint leaves HiLegal's building.** That sentence is the Section 6→8 pivot.

### Reconciled simulation snapshot

Model results below use the existing two-producer event engine, 67% video dedication, 22 working days = 30.4 calendar days per month, demand 17.5/month [E], 36 months, 16-month warm-up, 3-month cutoff and seeds 11/12/13. This replaces earlier single-seed examples using a slightly different calendar conversion. The spread between seeds is not a confidence interval. Inputs for the proposed iterations were informed by targets, so matching those targets is conditional scenario analysis, not independent validation or a tested operational improvement.

| Version | Expected work min | Simulated work min | Lead cal d | P90 cal d | Rework observed | Work-content capacity/mo |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 599.17 | 597.87 | 22.05 | 35.09 | 89.4% | 23.62 |
| iteration 1 | 435.00 | 434.83 | 6.60 | 9.67 | 53.4% | 32.53 |
| iteration 2 | 349.85 | 349.61 | 3.91 | 5.21 | 27.9% | 40.45 |
| iteration 3 | 61.45 | 61.33 | 1.60 | 2.07 | 9.0% | 230.29 |

See `model-results.json` and `../verify_analysis.py` for exact values and reproduction. These are separate from the target ranges above.

## 3. Cost per video build-up

**Human-factor pricing (Shenzhen, per producer):** gross salary ¥10,000 [E] + employer social insurance & housing fund (五险一金, ~35%) ¥3,500 [E] + equipment/software/office share ¥1,500 [E] → **¥15,000/month fully loaded ÷ 176 paid hours = ≈ ¥85/h**.

| Component | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|
| Labour (h × ¥85/h) | ¥850 (10 h [C]) | ¥615 (7¼ h) | ¥495 (5 h 50) | ¥85 (1 h) |
| Manual tool credits (ChatGPT/Seedance/TTS/stock) | ¥90 [E] | ¥90 | ¥65 (ChatGPT credits replaced by self-hosted LLM) | — |
| LLM inference (self-hosted legal LLM, marginal) | — | — | ¥20 [E] | ¥20 |
| Template/pipeline dev amortized (~500 videos) | — | — | ¥15 [E] | ¥30 |
| Single-render avatar API (voice + lip-sync + video) | — | — | — | ¥45 [E] |
| **COST PER VIDEO** | **¥940 [E]** | **¥705 [T]** | **¥595 [T]** | **¥180 [T]** |
| Δ vs previous | — | −25% | −16% | −70% |
| Δ vs baseline | — | −25% | −37% | **−81%** |

Labour is **90.6% of the baseline cost of an "AI video service"** — the frame for Section 2's money story.

## 4. Throughput and capacity: distinct denominators

Actual output is 15–20 delivered videos/month [C]. Demand/arrivals are assumed from that output; capacity is not an observed output forecast.

| Basis | Available video minutes/month | Baseline ceiling | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|---:|
| KPI scenario: 2 x 160 h x 60% | 11,520 | 19.20 | 26.48 | 32.91 | 192.00 |
| Simulation: 2 x 176 paid h x 67% | 14,150.4 | 23.62 | 32.53 | 40.45 | 230.29 |
| Full dedication illustration: 2 x 176 h / 10 h | 21,120 | 35.20 | not used | not used | not used |

The first row divides its budget by the 600/435/350/60 minute planning targets. The second divides by the implemented 599.17/435.00/349.85/61.45 minute expectations including loops. They describe different conditions. The separately reported 35–40 ceiling [C] is preserved; resemblance to 35.2 is a plausibility comparison, not proof of the assumed staffing calendar.

Service-level scenario capacity is the highest tested stable arrival rate with complete observed cohorts and mean lead <=28 calendar days: baseline 20, Iteration 1 30, Iteration 2 38, Iteration 3 230/month on the simulation budget. These are grid-dependent finite-horizon results, not certified sustainable production rates. The 28-day criterion is much weaker than the proposed 1–2-day delivery target. In particular, at 230/month Iteration 3 takes about 10 calendar days; it does not retain a two-day SLA at that volume. Arrival bursts, actual rejection rates and renderer concurrency still need measurement.

At 20 videos/month, the 10 h to 1 h planning change frees 180 staff hours/month, equivalent to 1.02 paid FTE at 176 h/FTE. Remaining video work is 20 h/month. At 40 videos/month the proposed 1 h workload is 40 h, not 4 h. Those hours are neither payroll cash nor ML engineering skills.


## 5. Rework rate & Quality Acceptance Rate

Definitions: **Rework rate** = % of delivered videos with ≥1 rework loop at any client gate. **QAR** = % accepted first-pass at *every* gate (zero loops). QAR ≈ 1 − rework rate under these definitions.

| | Baseline | Iter 1 | Iter 2 | Iter 3 | Loop family killed |
|---|---:|---:|---:|---:|---|
| Rework rate | ~90% [E] | ~55% [T] | ~30% [T] | ~10% [T] | |
| QAR | ~10% [E] | ~45% [T] | ~70% [T] | ~90% [T] | |

- Baseline anchor: brief approval loop alone runs **≥4 iterations [C]** → the mean-round interpretation is uncertain; ~90% rework remains a modelling estimate, not an observed rate.
- Iter 1 kills **clarification/brief loops** (structured brief + previews; lawyer sees the format before anything is produced).
- Iter 2 kills **script-surprise loops** (template structure + lawyer profile; lawyer approves a structure they already chose).
- Iter 3 kills **production-defect loops** (single render from the approved script — no transcription/sync errors, auto-consistent variants; residual = avatar glitches, name mispronunciation).
- Worst case per proposal (all gates × 4 iterations [C]): this is a proposal sensitivity commitment. The geometric high-rework scenario in Section 7 is a different experiment and must be labelled as such.
- Exact model incidences (independent geometric gates): baseline 88.00%, Iteration 1 55.04%, Iteration 2 30.07%, Iteration 3 9.97%. The three-seed observed rates are in the reconciled snapshot; variation is simulation noise, not evidence that quality improved in the company.
- p=.75 gives four rounds on average, with no finite maximum. It is not the proposal's literal scenario of exactly four rounds at each gate.
- QAR = 1 - rework only under the same order population, endpoint and definition of first-pass acceptance. Content accuracy, consent and compliance need separate checks.

## 6. Unit economics of the service (the Section 2/8 money story)

**Revenue side [C]:** most popular tier **$100/month ≈ ¥720 (FX 7.2 [E])**, promising **10 videos/month**. HiLegal's internal revenue attribution — their first costing assumption: **model costs ¥90 + 30% overhead ≈ ¥117/video [C]**, where the 30% (¥27) was meant to cover the human factor (actual human factor: ¥850 — the buffer covers 3% of it).

**Cost-allocation comparison (not actual revenue or margin):** 117 − cost → **−¥823 / −¥588 / −¥478 / −¥63** (baseline → Iter 3). Even fully automated, one video slightly exceeds the attribution — the attribution itself was built on the wrong assumption and needs re-basing.

**Per customer per month (the tier reality):**

| Usage of the 10-video promise | Baseline cost | Iter 3 cost | Revenue | Bleed, baseline | Bleed, Iter 3 |
|---|---:|---:|---:|---:|---:|
| 1 video | ¥940 | ¥180 | ¥720 | −¥220 | +¥540 |
| 2 videos (typical [E]) | ¥1,880 | ¥360 | ¥720 | −¥1,160 | **+¥360** |
| 5 videos | ¥4,700 | ¥900 | ¥720 | −¥3,980 | −¥180 |
| 10 (full entitlement) | ¥9,400 | ¥1,800 | ¥720 | **−¥8,680 (−$1,206)** | −¥1,080 |

→ Baseline break-even at **0.77 videos** — the allocated video cost exceeds the full subscription price at one video; this is a scenario, not an audited customer profit. **Iteration 3: the assumed two-video customer has a positive subscription-minus-video-cost residual (+¥360/month) and the full-entitlement loss shrinks 88%** (−¥8.7k → −¥1.1k, closable by tier design and volume render pricing). This is the "stop the bleed, make a little money, point it at the core" thesis.

**Aggregate (delivered volume 15–20/mo):** baseline burn vs attribution ≈ **−¥12–16k/month ≈ −¥150–195k/year [E]**; at Iter 3 ≈ −¥1.0–1.3k/month (≈ break-even) before the customer-mix upside.

**People and cash:** at unchanged volume of 15–20 videos/month, the 10 h to 1 h planning targets imply 135–180 h/month of freed staff time (0.77–1.02 paid FTE), with allocated labour-time value of ¥137,700–183,600/year at ¥85/h. Existing salaries remain payable unless management changes staffing or avoids a counterfactual hire. Do not add this allocated labour benefit to the per-video cost reduction: it is substantially the same benefit. A ¥270k/year cash reallocation is not established.

All customer tables assume the full subscription revenue can be compared with video costs. They exclude other bundled services, acquisition/support costs and fixed implementation expenditure. ¥117 is an internal attribution, not measured sales revenue per video. Therefore these tables do not establish actual profitability or actual aggregate burn.

## 7. Sanity checks (do these live if challenged)

1. **Capacity:** 11,500 min ÷ 600 min = 19.2 ≈ company-reported 15–20 [C] ✓ — the utilization assumption is back-solved from their own output, not invented.
2. **Labour waterfall sums** to the company-reported ~10 h [C] ✓ (see row sums under table 1).
3. **Little's Law spot check:** 21 calendar days x (19 videos/month / 30.4 calendar days/month) = 13.13 videos in system ≈ an illustrative stable-boundary WIP estimate, not an independent measurement.
4. **Sync + adaptation** (250 min) = 42% of baseline labour — consistent with the proposal naming them the largest blocks [C] ✓.
5. **Cost curve shape:** −25% → −37% → −81%. Iteration 2's step looks small *by design* — it fixes the middle so Iteration 3 can delete the bottom. Say this before someone else does.

## 8. Change log

- 2026-10-29 initial dataset created from proposal Table 1 [C] + derived [E] estimates; targets [T] set per iteration. Update this log whenever a baseline number is replaced by observed pilot data.
- 2026-10-29 currency switched to RMB: fully-loaded rate ¥85/h (Shenzhen build-up in §3), FX 7.2. Revenue side rebuilt on company facts: $100/month tier promising 10 videos/month, attribution = model costs + 30% overhead ≈ ¥117/video [C]. Cost curve recomputed: ¥940 → ¥705 → ¥595 → ¥180 (tool lines now persist correctly through Iter 2: Seedance/TTS credits remain until the single render replaces them in Iter 3).
- 2026-11-07 Iteration 1 simulated (`06 .../Iteration 1/iteration1_sim.py`, engine copied from the Section 4 rework study; baseline sanity-checked: 21.8 d / 600 min / 87%). Results folded in: §2 simulated lead 6.8 d (target 9 d holds, gate-dominated — SLA sensitivity 5.1–8.2 d); §4 added work-content-ceiling relabel + simulated practical capacity (baseline ~20/mo ≈ reported 15–20 [C]; Iter 1 ~30/mo, work-content 32.5/mo on the 67% sim budget); §5 simulated rework 59% / QAR ~41% vs 55%/45% targets. Iterations 2–3 to be simulated the same way as they are reached.
- 2026-11-07 Iteration 2 simulated (`06 .../Iteration 2/iteration2_sim.py`; sanity-checked against baseline + Iteration 1 published numbers). Results folded in: §2 simulated lead 4.0 d (target 4 d exact; email-fallback sensitivity 5.3 d); §4 practical capacity Iter 2 ~38/mo, work-content 40.4/mo — practical capacity now sits inside the stated ceiling 35–40 [C]; §5 simulated rework 34% / QAR ~66% vs 30%/70% targets.
- 2026-11-07 Iteration 3 simulated (`06 .../Iteration 3/iteration3_sim.py`; sanity-checked against all prior rungs). Results folded in: §2 simulated lead 1.6 d (target 1.5 d; slow-lawyer sensitivity 2.1 d — residual lead ≈ 100% client approval); §4 practical capacity Iter 3 ~230/mo, lead flat 1.6–2.2 d from 15 to 200/mo demand, util 8% at 17.5/mo — the capacity question ends; §5 simulated rework 11% / QAR ~89% vs 10%/90% targets. Simulated cost ¥183 (1.03 h labour ¥88 + render ¥45 + LLM ¥20 + amort ¥30) ≈ ¥180 [T].

- 2026-11-07 reconciliation: preserved reported inputs and planning targets; corrected capacity denominators, work/rework labels, units, financial interpretation and source attribution. Earlier change-log entries describe historical calculations, not current verified results.
