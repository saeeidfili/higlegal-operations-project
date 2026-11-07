# Section 5 — These are our operational KPIs

**Guiding question:** How do we measure the success of each iteration?

**What this section must accomplish:** define the measurement system — two primary KPIs that capture the value created, and auxiliary KPIs that make the changes across each iteration visible. This is the scoreboard every later section plays on. **The master numbers (baselines, targets, labour waterfall, cost build-up, capacity math) live in `../single source of truth/kpi-data.md` — keep one source of truth and reference it everywhere.**

---

## Two primary KPIs — the value, both sides of the counter

| KPI | Whose value it captures | Definition (operational, measurable) | Baseline |
|---|---|---|---|
| **Cost per Video** | **The company's** — every manual minute is recurring cost, every saved minute is margin | Labour (hours × ¥85/h fully loaded [E]) + model/tool costs per delivered video | ¥940 [E] |
| **Lead Time per Video** | **The customer's** — the lawyer's campaign calendar pays for every queued day | Calendar days from request submission to video delivered (incl. all waiting) | 14–28 d [C] (~21) |

Cost says whether the service stops bleeding money; lead time says whether the lawyer stops waiting. Between them they capture the two currencies the process burns (Section 2) — and they are orthogonal: a process can be cheap but slow, or fast but artisanal. Every iteration must move both.

## Auxiliary KPIs — what changes inside the black box

The primary KPIs tell us *whether* an iteration worked; the auxiliaries tell us *why* — they make the mechanism visible across iterations:

| KPI | What it makes visible | Baseline |
|---|---|---|
| Human processing time per video | The labour waterfall behind cost (Section 3's work-vs-wait pair) | ~10 h [C] |
| Throughput (demand / output / capacity reported separately) | The scaling question — and whether capacity or demand gates it | output 15–20 [C]; capacity ~19 [E] |
| Rework rate (≥1 loop at any gate) | Whether the loop families are actually dying | ~90% [E] |
| **Quality Acceptance Rate (QAR)** — first-pass at *every* gate | How often we get it right the first time; catches "faster but worse" | ~10% [E] |

QAR is our addition to the proposal's five KPIs: rework rate alone hides first-time correctness — the direct measure of front-end standardization.

**Label discipline (state on the slide):** every figure tagged **[C] company-reported**, **[E] estimate**, or **[T] target**. Targets shown as ranges, never false-precision single numbers. Each target comes with its mechanism (target jump ← cause) — rehearsed from the justification table in `../single source of truth/kpi-data.md`.

## Measurement plan — simulate first, then pilot

1. **Simulate before touching anything.** Each iteration's target is validated in the process simulation (Section 7) *before* implementation: the rework/queue models (Section 4) carry the baseline, the simulation carries the to-be scenarios. An iteration is only scheduled if the model says the numbers move.
2. **Pilot inside the company.** Each iteration runs as a contained pilot (Section 9) before full rollout. The order state machine timestamps every transition (`submitted → brief_ok → script_ready → script_approved → render_done → delivered`) — from Iteration 1 on, every KPI is computed automatically, per order (this closes the "no measurement habit" gap; PDCA).
3. **Gate rule:** an iteration passes only if its primary KPIs hit target **and no auxiliary KPI regresses** (e.g., cost falls but QAR falls too → fail the gate, investigate).

## Baseline data-quality note (say this once, then move on)

Part of the baseline is self-reported [C], part is our estimate [E]; there is no controlled comparison. We therefore (a) label everything, (b) simulate before piloting and pilot before rolling out, and (c) replace [E] decompositions with observed time-log data as the pilot produces it. This is the honest version of the limitation paragraph in the proposal.

## Files

- `../single source of truth/kpi-data.md` — **master tables**: labour waterfall per iteration, cost build-up, capacity math, rework/QAR logic, unit economics, sanity checks, target-justification table. Single source of truth for Sections 5–9.
- `kpi-dashboard-mock.png` (to produce) — the per-step cycle-time dashboard the to-be process logs automatically.

## Checklist

- [ ] Every KPI has a formula anyone could recompute
- [ ] Primary (cost, lead time) vs auxiliary framing explicit on the slide
- [ ] Baseline tags [C]/[E] visible
- [ ] Targets shown as ranges, with mechanisms
- [ ] Simulate-then-pilot sequence stated — it is the bridge into Sections 6–7 and 9
