# Section 4 — Queue model (summary)

Flow from Section 3: showed *where* time goes — mostly waiting. This explains the wait: it's a conditional model explanation, not a finding about individual staff performance.

## Model choice (why M/M/1)

- The single-server intake model is an aggregate surrogate [E]; shared queuing and non-preemption do not prove that two producers are one server.
- M/M/1: ρ = λ/μ, τ = 1/μ, Wq = ρ/(1−ρ)·τ, Lq = λ·Wq

**Inputs:** λ = 15/17.5/20/month [C], wait 3–7 d [C], ~10 h/video [C], 352 h/month, μ = 23.5 calibrated (Section 3).

## Predictions (μ = 23.5)

| quantity | typical λ=17.5 | heavy λ=20 |
|---|---|---|
| ρ | 0.74 | 0.85 |
| Wq | 3.77 d | 7.39 d |
| Lq (inbox) | 2.2 | 4.9 |
| P(arrival waits) | 3 in 4 | — |

## The tail (exponential waits)

P(Wq>7 d) = 19% — 1 in 5 lawyers waits >1 week before production starts. **P90 ≈ 10 d** — 1 in 10 waits 2 weeks just to be looked at. "Workload-dependent" [C] *is* this fat tail.

## Nonlinearity — why "working harder" fails

Multiplier ρ/(1−ρ): 1.8 → 2.9 → 5.7 → 9.0 → 19 → ∞ as ρ 0.64 → 0.74 → 0.85 → 0.90 → 0.95 → 1. Demand ×1.33, wait ×3.2.

## Validation — what it really checks

200k random orders through a strict FIFO single server (exponential arrivals at λ, exponential service at μ) re-derives Wq/Lq/ρ from events alone — no formulas. Matches the M/M/1 algebra at **0.7% (λ=17.5)**, **1.2% (λ=20)**.

- **Validates the algebra:** the formulas are exactly what happens when you run the modeled process — no slip, no wrong plug-in.
- **Does not validate the assumptions:** simulation draws from the same assumptions as the formulas (Poisson, exponential service, one server) — internal consistency, not real-world fit.

Real-world fit is carried by the other checks:
- **Calibration:** μ = 23.5 approximately overlaps the reported band; the endpoint pairing is assumed [C]
- **Labour accounting:** 67% model dedication, with a distinct KPI budget; not independent corroboration (below)
- **Falsifiable prediction:** inbox should hold ≈2–5 parked requests — HiLegal can count it

### Budget comparison

The M/M/1 is an aggregate serial intake surrogate [E], not a literal description of two producers. A pooled inbox or non-preemption does not turn two workers into one server. The whole-process simulation instead has two FIFO task servers and releases them during client waits; its task durations are deterministic. The models are deliberately different simplifications and their waiting times must not be added as if they were independent components. Neither is independently validated against measured order histories.

At retained mu=23.5/month the consistent 30.4/22 conversion gives intake waits of approximately 2.28, 3.77 and 7.39 calendar days at assumed arrivals 15, 17.5 and 20/month. The reported 3–7-day and 15–20-output ranges do not establish paired endpoints. This is approximate calibration, not a fit to every endpoint. Implied dedication 23.5 x 10 / 352 = 66.76% is not an independent 65% estimate. The KPI scenario uses 60% of 160 h; it is a separate budget.

## Charts

- `queue-cliff.svg` — THE slide: utilization cliff (ρ = λ/μ, same curve on two axes), observed 3–7 d band, demand dots, the wall
- `order-timeline.svg` — one order through the 12 steps: 18.8 d end-to-end, work ≈ 6%; "queue-gated, not work-gated" made visible

## Model card (say on purpose)

- μ is calibrated, not measured [E]
- Poisson arrivals defensible: independent lawyers, no coordination; bursts only make waits worse
- The single-server intake model is an aggregate surrogate [E]; shared queuing and non-preemption do not prove that two producers are one server.
- Steady state assumed — a normal month
- Falsifiable: inbox never >1 while waits run 3–7 d → delay is batch-review cadence, not queueing
- Scope: intake queue only; approval-gate waits sit on top
- With churn/overtime (Section 2), reality is likely worse than modeled

## One-liner

> "At ρ ≈ 0.74–0.85, the 3–7 day intake wait is not a people problem — it is the mathematics of standing on the steep part of the utilization cliff."

## Review correction 7 November 2026

The M/M/1 is an aggregate serial intake surrogate [E], not a literal description of two producers. A pooled inbox or non-preemption does not turn two workers into one server. The whole-process simulation instead has two FIFO task servers and releases them during client waits; its task durations are deterministic. The models are deliberately different simplifications and their waiting times must not be added as if they were independent components. Neither is independently validated against measured order histories.

At retained mu=23.5/month the consistent 30.4/22 conversion gives intake waits of approximately 2.28, 3.77 and 7.39 calendar days at assumed arrivals 15, 17.5 and 20/month. The reported 3–7-day and 15–20-output ranges do not establish paired endpoints. This is approximate calibration, not a fit to every endpoint. Implied dedication 23.5 x 10 / 352 = 66.76% is not an independent 65% estimate. The KPI scenario uses 60% of 160 h; it is a separate budget.

Current whole-process comparison and exact run settings are in `single source of truth/model-results.json` (repository root). Earlier single-seed traces are illustrations, not measured customer histories. Work of 10 h over 2–4 calendar weeks is 1.5–3.0% of wall-clock hours, or about 6–13% of an assumed 8-hour working-day clock. Neither ratio is value-added PCE.
