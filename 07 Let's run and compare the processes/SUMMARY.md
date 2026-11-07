# Section 7 — Let's run and compare the processes (summary)

Flow from Section 6: *"That's the design. Now let's stress-test it."* Baseline vs Iterations 1–3 through the same scenarios — demand, approval delays, rework varied openly. This is what makes the Section-6 claims credible instead of aspirational.

## Model

Same engine as the whole project (Section-4 lineage): each video flows through its version's process map; steps consume producer time (2 producers), gates add calendar waiting and can loop; parameters from `single source of truth/kpi-data.md`, distributions uniform over stated ranges — ranges, not fake precision. All runs in `compare_sim.py` (this folder), 3 seeds per point; every table in `scenario-results.md`.

## S0 — Normal conditions (λ = 20/mo)

| version | lead | P90 | work | ¥/video | rework | QAR |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 23.4 d | 36.9 | 600 min | ¥940 | 88% | 12% |
| v1 · standardize | 7.2 d | 10.5 | 437 | ¥709 | 56% | 44% |
| v2 · AI scripting | 4.0 d | 5.3 | 349 | ¥595 | 30% | 70% |
| v3 · single render | **1.6 d** | **2.1** | **61** | **¥182** | **8%** | **92%** |

The Section-6 scoreboard, now simulated. Charts: `ladder.svg` (six KPI panels), `timer-bars.svg` (one median order per version — the red shrinks, the green nearly vanishes).

## S1 — Demand surge — `saturation.svg`, `wip-paths.svg`

Baseline explodes past 20/mo (93 d at 25, 271 at 30, unstable by 60); v1 unstable by 60; v2 degrades at 40 (28.8 d); **v3 flat at 1.6–2.2 d from 15 to 200/mo** — bends only at 240. WIP at 40/mo: baseline spirals, v3 stays ≤ 4 videos. *"Demand stops being a capacity problem."*

Honest note: v2 saturates at ~38/mo — *before* its 40.4 work-content ceiling, exactly as queueing theory predicts (practical < work-content; the same 80–85% rule the Section-4 models show).

## S2 — Slow lawyers (all gate waits ×2.5) — `slow-lawyers.svg`

| version | normal | slow |
|---|---:|---:|
| baseline | 23.4 d | 49.8 d |
| v1 | 7.2 | 13.4 |
| v2 | 4.0 | 7.3 |
| v3 | 1.6 | **3.0** (P90 4.0) |

**v3's worst case beats baseline's best case** (14 d) by 4×. *"The residual process time belongs to the client."*

## S3 — Rework stress (loop p = 0.75 at every gate — proposal worst case) — `rework-stress.svg`

Baseline **295 d** (P90 404) — the process does not function. v1 18.3 d · v2 10.4 d · **v3 4.5 d** (P90 8.8). Worst-case robustness is designed in: cheap loops (scene-level regeneration) survive even 4 iterations per gate.

## S4 — Producer absence (1 of 2 away, 2 weeks)

| version | cohort lead after absence | peak WIP |
|---|---:|---:|
| baseline | 31.6 d | 30 |
| v1 | 7.6 d | 10 |
| v2 | 4.3 d | 6 |
| v3 | **1.6 d** | **4** |

Capacity headroom as insurance: the absence is invisible in v3 (team load ~4 h/mo at this demand).

## S5 — Quality dip (v3's model regresses to v2-level loops + deeper edits)

| config | lead | work | rework | ¥/video |
|---|---:|---:|---:|---:|
| v3 normal | 1.6 d | 61 min | 8% | ¥182 |
| **v3 dipped** | **1.8 d** | **85 min** | **28%** | **¥216** |
| v2 normal | 4.0 d | 349 min | 30% | ¥595 |

Graceful degradation: even a regressed v3 beats v3-normal's predecessor on every axis. No iteration depends on perfection — capacity is structural, labour is QC-bound.

## Expectation check

Every pre-registered ordering held (v3 < v2 < v1 < baseline throughout). The two honest findings — v2's practical saturation below its work-content ceiling, and v3 bending at 240/mo — are shown, not hidden: a stress test that only confirms is theater.

## Assumptions (the honesty box)

Producers = 2 [C]; waits uniform over stated ranges [E]; loop rates from kpi-data targets [T] (S3 overrides to the proposal's worst case [C]); calendar days include weekends; seasonality not modeled. Calibrated so S0 reproduces company-reported baseline (23.4 d inside 14–28 [C]; capacity ≈ reported 15–20 [C]).

Bridge to Section 8: *"The process now has headroom. What is that headroom worth to HiLegal?"*
