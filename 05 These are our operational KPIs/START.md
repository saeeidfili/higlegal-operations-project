# Section 5 — These are our operational KPIs

**Guidging question:** How does the production department perform today, and how will we evaluate improvements?

**What this section must accomplish:** define each KPI precisely (so it can be measured, not just quoted), publish the baseline, and commit to per-iteration targets. This is the scoreboard every later section plays on. **The master numbers live in `kpi-data.md` in this folder — keep one source of truth and reference it everywhere.**

---

## The KPI system (6 KPIs, each with owner, formula, and source)

| # | KPI | Definition (operational, measurable) | Baseline | Source at baseline | Source after Iter 1 |
|---|---|---|---|---|---|
| 1 | **Lead Time per Video** | Calendar days from lawyer's request submission to video delivered/published (incl. all waiting) | 14–28 d [C] (midpoint ~21) | Company-reported | Auto timestamps (request.submitted → video.delivered) |
| 2 | **Human Processing Time per Video** | Sum of all producer active minutes per delivered video, incl. rework rounds | ~10 h [C] | Company-reported, decomposed [E] | Auto timestamps + self-log |
| 3 | **Cost per Video** | Labour (hours × ¥85/h fully loaded [E]) + model/tool costs per video | ¥940 [E] | Derived | Derived + tool metering |
| 4 | **Throughput (Videos per Month)** | Delivered videos per calendar month; report **demand, output, and capacity** separately | Output 15–20 [C]; capacity ~19 [E] | Company-reported | Auto order counter |
| 5 | **Rework Rate** | Share of delivered videos that went through ≥1 rework loop at any gate | ~90% [E] (brief loop alone ≥4 iterations [C]) | Derived | Loop counter per order |
| 6 | **Quality Acceptance Rate (QAR)** | Share of videos accepted **first-pass at every client gate — zero loops** | ~10% [E] | Derived | Loop counter (inverse) |

**Label discipline (state on the slide):** every figure is tagged **[C] company-reported**, **[E] estimate/assumption**, or **[T] target**. QAR is our addition to the proposal's five KPIs because rework rate alone hides *how often we get it right the first time* — the direct measure of front-end standardization.

## Why these six (and not more)

- Lead time + human time = the speed/labour pair that Section 3's work-vs-wait split demands
- Cost per video = the Section 2 money story, made measurable
- Throughput = the scaling question HiLegal actually asked
- Rework + QAR = the quality pair that proves standardization works (and catches "automation made it faster but worse")

## The scoreboard (baseline → targets per iteration)

| KPI | Baseline | Iter 1 [T] | Iter 2 [T] | Iter 3 [T] | Total change |
|---|---|---|---|---|---|
| Lead time (midpoint) | 21 d | 9 d (7–12) | 4 d (3–5) | 1.5 d (1–2) | **−93%** |
| Human time/video | 10 h 00 | 7 h 15 | 5 h 50 | ~1 h 00 | **−90%** |
| Cost/video | ¥940 | ¥705 | ¥595 | ¥180 | **−81%** |
| Capacity (same 2 producers) | ~19/mo | ~26/mo | ~33/mo | ~190/mo | **~10×** |
| Rework rate | ~90% | ~55% | ~30% | ~10% | **−80 pts** |
| QAR (first-pass) | ~10% | ~45% | ~70% | ~90% | **+80 pts** |
| Process steps | 12 [C] | 10 | 9 | 8 | −4 steps |

**How each target is justified (mechanism → KPI — never present a target without its mechanism):**

| Target jump | Mechanism that causes it (from Sections 4 → 6) |
|---|---|
| Baseline → Iter 1: lead time 21 d → 9 d | Intake queue (3–7 d) eliminated by structured self-serve brief; clarification loop eliminated by format previews; approvals capped by 48 h SLA + auto reminders |
| Iter 1 → 2: human time 7 h 15 → 5 h 50 | LLM drafts from template + lawyer profile; humans edit instead of write; scripts carry scene breakdowns that speed video generation |
| Iter 2 → 3: cost ¥595 → ¥180, capacity 33 → 190 | Single render fuses voice + lip-sync + video (deletes 2–3 h sync [C]); auto variants delete ~2 h adaptation [C]; remaining human work = QC only |
| Rework/QAR ladder | Each iteration kills one loop family: Iter 1 = brief/clarification loops; Iter 2 = script-surprise loops; Iter 3 = production-defect loops |

## Measurement plan (how we will actually check — this is what makes it a *system*)

1. **Instrumentation first (Iteration 1 delivers this as a side effect):** the order state machine timestamps every transition (`submitted → brief_ok → script_ready → script_approved → render_done → delivered`). From Iteration 1 on, every KPI is computed automatically, per order. This closes the "no measurement habit" gap identified in the proposal (PDCA).
2. **Baseline enrichment (do during pilot, weeks 1–2):** ask HiLegal to time-log **10 videos** through the current process (per-step minutes). Replaces our [E] decomposition with observed data; if a step deviates >30% from our waterfall, update `kpi-data.md` and the dependent targets.
3. **Per-iteration gate (see each iteration's KPI-check table):** an iteration "passes" only if its **primary KPIs** hit target **and no secondary KPI regresses** (e.g., labour falls but QAR falls too → fail the gate, investigate).
4. **Worst-case sensitivity (from the proposal's risk section):** validate targets against the scenario "all three approval gates require 4 iterations [C as worst case]" — Iteration 1's SLA + structured change requests are what make that scenario survivable; recompute lead time and rework under it in `07`'s simulation.

## Baseline data-quality note (say this once, then move on)

Part of the baseline is self-reported [C] and part is our estimate [E]; there is no controlled comparison. We therefore (a) label everything, (b) designed the pilot (Section 9) to replace estimates with observations before full rollout, and (c) stress-tested targets against the worst-case loop scenario. This is the honest version of the limitation paragraph in the proposal.

## Files in this folder

- `kpi-data.md` — **master tables**: labour waterfall per iteration, cost build-up, capacity math, rework/QAR logic, unit economics, sanity checks. Single source of truth for Sections 5–9.
- `kpi-dashboard-mock.png` (to produce) — the per-step cycle-time dashboard the to-be process logs automatically (proposal's step 8 / PDCA habit)

## Checklist

- [ ] Every KPI has a formula anyone could recompute
- [ ] Baseline tags [C]/[E] visible on the slide
- [ ] Targets shown as ranges, never false-precision single numbers
- [ ] The mechanism table (target jump ← cause) rehearsed — it is the bridge into Section 6
