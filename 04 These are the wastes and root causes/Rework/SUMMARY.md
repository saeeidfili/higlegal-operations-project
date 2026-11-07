# Section 4 — Rework simulation (summary)

Flow from queue summary: intake queue explained the 3–7 d wait. This covers the rest — what the three approval loops do to the whole process.

## Headline

Rework looks like extra work, is mostly extra waiting. No-rework → baseline: **+84 min of work but +10.8 days of lead time** — queue cost ~29× work cost. *"Rework costs ~11 days for under an hour and a half of work."*

## Setup

Discrete-event simulation of the full 12-step process — two producers as one pooled task queue, no preemption, three looping gates (G1 clarification, G2 script approval, G3 final approval). Work at 321.6 effective min/producer-day (480 × 0.67, docs round to 322).

## How the simulation works

- **Engine:** discrete-event — a min-heap of scheduled events (arrival, task done, gate wait ended); the clock jumps event to event, never ticks. Each video is a Python generator yielding `("work", minutes)` or `("wait", days)` in the 12-step order; at each gate it draws a random roll — below p → loop again.
- **Arrivals:** Poisson process — inter-arrival gaps exponential with mean 22/λ working days (λ = 17.5 → a request every ~1.26 wd).
- **Producers:** one shared task queue, two servers, first-come-first-served, work-conserving (a free producer grabs queued work instantly), no preemption. While a video waits at a client gate, its producer works other videos — that's how two producers juggle 1–2 staggered videos each.
- **Time units:** working days; 1 producer-day = 480 paid min × 0.67 = 322 effective video minutes; lead times reported ×1.4 in calendar days.
- **Measurement window:** 28-month run; videos *arriving* in months 10–25 only — first 10 months discarded (empty-start warm-up), last 3 cut (end-of-run censoring: undelivered videos would bias lead times down). Per video: lead = delivered − arrival; work = accumulated minutes; rework = ≥1 loop. WIP sampled twice per working day.
- **Sweep:** 4 demand levels × 3 rework levels × 3 seeds, 36-month runs (longer because near-capacity queues converge slowly); reports mean WIP — an unstable queue shows up honestly in WIP while censored lead times look tame.
- **Reproducible:** every run seeded; the engine is audited against the closed-form E[work] on every run (516/516 … 686/686).
- **End-to-end report:** `run_report.py` — calibrates the p's, derives the closed-form numbers, runs the four scenarios, sweeps demand, and verifies all anchors in one run.

## Calibration (fit-then-verify, same logic as μ = 23.5)

**What the p's are:** each gate loops with probability p — video passes with 1−p, goes back with p. Rounds at a gate are geometric: mean rounds = 1/(1−p), expected loops = p/(1−p).

**Fit 1 — p_clar from "≥4 clarification rounds" [C]:**
```
1/(1−p) = 4  →  p_clar = 0.75
```

**Fit 2 — p_script = 0.20, p_final = 0.40 from the ~10 h total [C]:**

First-time-right work (12 tasks, no loops):
```
15 + 8 + 45 + 70 + 35 + 55 + 30 + 140 + 95 + 23 = 516 min
```
(15 intake review · 8 clarification reply · 45 brief · 70 drafting · 35 AI refine · 55 video gen · 30 audio gen · 140 AV sync [C] · 95 adaptation [C] · 23 delivery admin)

Loop costs on top:
```
extra clarification replies : (4−1 rounds) × 8 min        =  24.0 min
script rework               : 50 × 0.20/(1−0.20)         =  12.5 min
final rework                : 70 × 0.40/(1−0.40)         =  46.7 min
                                                              ─────────
E[work] = 516 + 24 + 12.5 + 46.7                           = 599 ≈ 600 [C]
```
p_final = 2 × p_script — late-stage rejection is likelier, the client sees the real product only at the final gate. The 600-min anchor pins the pair (solved by `calibrate_loops.py`).

**Not fitted — kept back to verify, and the math behind each:**

**Lead time** (no closed form — that is why it is simulated):
```
lead_i = (delivered_i − arrival_i) [wd] × 1.4 → calendar days
L = mean over W = { i : 10 mo ≤ arrival_i ≤ 25 mo }   (warm-up + censoring cuts)
   → L = 21.8 d   vs 14–28 d [C] ✓
```

**Work** (closed form, geometric expectation per gate):
```
E[work] = 15 + 8·E[rounds_clar] + 45 + 70 + 35
          + 50·E[loops_script] + 55 + 30 + 140
          + 70·E[loops_final] + 95 + 23
E[rounds_clar]   = 1/(1−0.75) = 4            →  8 × 4  = 32.0 min
E[loops_script]  = 0.20/(1−0.20) = 0.25      → 50 × 0.25 = 12.5 min
E[loops_final]   = 0.40/(1−0.40) = 0.667     → 70 × 0.667 = 46.7 min
E[work] = 516 + 32 + 12.5 + 46.7 − 8 = 599.2 ≈ 600 [C] ✓
   (516 first-time-right already includes one 8-min reply; extra replies = (4−1)×8 = 24)
simulated: 600 min ✓   engine check: 516/516, 547/551, 599/600, 686/686
```

**Rework incidence** (probability of ≥1 loop anywhere, gates independent):
```
P(≥1 loop) = 1 − (1−p_clar)(1−p_script)(1−p_final)
           = 1 − 0.25 × 0.80 × 0.60
           = 1 − 0.12 = 88%   vs ~90% [E] ✓   (simulated 87%)
```

**Capacity** (derived from work content, not simulated):
```
budget = 2 producers × 22 wd × 321.6 eff. min (480 × 0.67) = 14,150 min/month
capacity = budget ÷ E[work] = 14150 ÷ 599 = 23.6 videos/month
   vs demand 15–20 [C] ✓
no rework:  14168 ÷ 516 = 27.4/mo
heavy:      14168 ÷ 686 = 20.6/mo
```

## Results (λ = 17.5/month)

| scenario | p_clar / p_script / p_final | rework % | lead | P90 | work | capacity |
|---|---|---:|---:|---:|---:|---:|
| no rework | 0 / 0 / 0 | 0% | 11.0 d | 13.1 | 516 min | 27.4/mo |
| halved | 0.50 / 0.10 / 0.20 | 66% | 15.1 d | 21.8 | 551 | 25.7 |
| **baseline** | **0.75 / 0.20 / 0.40** | **87%** | **21.8 d** | **34.1** | **600** | **23.6** |
| heavy | 0.80 / 0.40 / 0.60 | 93% | 31.1 d | 54.8 | 686 | 20.6 |

Remove rework: lead −49%, work only −14%. P90 story: half the pain lands on the worst-served 10% of lawyers.

## Rework × demand (WIP · lead)

| λ | no rework | baseline | heavy |
|---:|---|---|---|
| 15 | 5.2 · 10.7 d | 10.1 · 21.2 | 14.5 · 29.6 |
| 17.5 | 6.2 · 11.2 | 12.7 · 22.4 | 17.2 · 30.6 |
| 20 | 7.6 · 11.8 | 15.3 · 23.4 | 36.4 · 54.6 |
| 22 | 8.9 · 12.5 | 19.4 · 28.9 | **86.3 · 116.7 ✗** |

No rework absorbs 22/month easily; heavy rework at 22 is past capacity — unbounded backlog. **The ceiling is a property of the team plus its rework.**

## Five mechanisms (why loops cost days, not minutes)

Loops add fresh gate waits and queue turns, not just minutes; variability amplification; WIP inflation (Little's Law); capacity erosion (27.4 → 23.6 → 20.6); utilization rises toward the cliff (65% → 70% → 87%).

## Charts

`rework-impact.svg` (headline), `queue-sample-path.svg` (WIP runaway at 22/mo), `rework-vs-demand.svg` ("can we push more volume?" — no), `gantt-rework.svg` (extra time is repeated waiting, not work).

## Iteration targets (Section 6 hook)

G1 → halved (−5–7 d), G2 → better (−2–4 d), G3 → toward no-rework (−1–2 d). Rework 90% → 10% ≈ no-rework scenario. Rework reduction = single largest lead-time lever — effort can't escape ρ/(1−ρ).

## Model card

Intake wait a lower bound (work-conserving); loop probabilities fixed (congestion→rework feedback not modeled → results conservative); per-task minutes our decomposition [E], only total ~10 h + sync + adaptation [C]; heavy = stress scenario, not forecast.

## One-liner

> "Rework adds 84 minutes of work and eleven days of waiting — and it moves the capacity wall from 27 down to 21 videos a month. Kill the loops, not the overtime."
