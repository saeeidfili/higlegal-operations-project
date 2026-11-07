# Section 4 — Queue model (summary)

Flow from Section 3: showed *where* time goes — 94% waiting. This explains the wait: it's not people, it's math.

## Model choice (why M/M/1)

- Video held start-to-finish, no preemption → inbox answered only when a producer *finishes* one → two producers behave as **one pooled server**, not two
- M/M/1: ρ = λ/μ, τ = 1/μ, Wq = ρ/(1−ρ)·τ, Lq = λ·Wq

**Inputs:** λ = 15/17.5/20/month [C], wait 3–7 d [C], ~10 h/video [C], 352 h/month, μ = 23.5 calibrated (Section 3).

## Predictions (μ = 23.5)

| quantity | typical λ=17.5 | heavy λ=20 |
|---|---|---|
| ρ | 0.74 | 0.85 |
| Wq | 3.8 d | 7.5 d |
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
- **Calibration:** μ = 23.5 reproduces the observed 3–7 d band across the whole demand range [C]
- **Labour accounting:** 67% vs 65% — two routes, same answer (below)
- **Falsifiable prediction:** inbox should hold ≈2–5 parked requests — HiLegal can count it

### The 67% / 65% cross-check

- **67% = implied by μ:** 23.5 videos/month × 10 h = 235 h ÷ 352 h available = 67% of producer time on video work
- **~65% = independent estimate** (kpi-data.md, single source of truth): producers aren't 100% dedicated — meetings, admin, context switching
- Had calibration landed at e.g. μ = 33 (94% busy) it would contradict reality. 67% ≈ 65% → the number fitted from *wait times* agrees with the number reasoned from *time availability* → μ = 23.5 is credible

## Charts

- `queue-cliff.svg` — THE slide: utilization cliff (ρ = λ/μ, same curve on two axes), observed 3–7 d band, demand dots, the wall
- `order-timeline.svg` — one order through the 12 steps: 18.8 d end-to-end, work ≈ 6%; "queue-gated, not work-gated" made visible

## Model card (say on purpose)

- μ is calibrated, not measured [E]
- Poisson arrivals defensible: independent lawyers, no coordination; bursts only make waits worse
- M/M/1 is a simplification — chosen because the pickup process behaves as one pooled unit
- Steady state assumed — a normal month
- Falsifiable: inbox never >1 while waits run 3–7 d → delay is batch-review cadence, not queueing
- Scope: intake queue only; approval-gate waits sit on top
- With churn/overtime (Section 2), reality is likely worse than modeled

## One-liner

> "At ρ ≈ 0.74–0.85, the 3–7 day intake wait is not a people problem — it is the mathematics of standing on the steep part of the utilization cliff."
