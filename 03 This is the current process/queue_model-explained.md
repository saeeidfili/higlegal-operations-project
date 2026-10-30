# What `queue_model.py` does — the queueing model in one read

This is the companion to **`queue_model.py`** and replaces `queueing-model.md`
(that file told the same story five times: model, persuasion pack, chart guide,
cheat sheet, run instructions). This document states it once: what the script
does, part by part, with the numbers it actually prints.

**How to run** (needs matplotlib, nothing else):

```
uv run queue_model.py                 # auto-installs matplotlib
# or, in the project venv already set up:
../.venv/bin/python queue_model.py    # from this folder
```

Output: four console parts and **three SVG charts** (transparent
backgrounds, ready to drop onto slides) written next to the script —
`queue-cliff.svg` (utilization cliff + demand sweep, merged into one),
`order-timeline.svg`, `why-one-server.svg`.
Change any value in the `Parameters` block at the top of the script and every
table and chart updates consistently.

---

## The model in one paragraph

Lawyers' video requests wait **3–7 days in the intake inbox** [C] before anyone
looks at them. The two producers act as **one pooled pickup function**: a video
is held start-to-finish (no preemption), so the inbox gets answered only when a
producer *finishes* one. That is an **M/M/1 queue**: ρ = λ/μ utilization,
τ = 1/μ one "turn" of work, **Wq = ρ/(1−ρ) · τ** the expected wait, and
Lq = λ·Wq the parked requests (Little's Law). All rates are per month; times in
working days (1 month = 22 wd, 1 wd ≈ 1.4 calendar days).

## Inputs (`Parameters` block — the single source of truth)

| Symbol | Meaning | Value | Status |
|---|---|---|---|
| λ | demand | 15 / 17.5 / 20 per month | [C] company-reported |
| wait | observed intake wait | 3–7 calendar days | [C] company-reported |
| labour | active work per video | ~10 h, two producers | [C] |
| hours | producer-hours available | 2 × 176 = 352 h/month | derived |
| ceiling | stated output ceiling | 35–40/month | [C] |
| μ | effective capacity | **23.5/month** | [E] calibrated, Part 1 |

## The kernel (every number flows from these functions)

| Function | Returns |
|---|---|
| `mm1(λ, μ)` | ρ, τ, Wq, W, Lq, L — the M/M/1 results |
| `tail_prob(λ, μ, t)` | P(wait > t) = ρ·e^(−(μ−λ)t) |
| `p90_wait(λ, μ)` | solves the tail for 10 % — the P90 |
| `simulate_mm1` | discrete-event simulation of the same queue |

---

## Part 1 — Calibration (`part1_calibration`)

Fit the one unknown (μ) to the one observation (3–7 d), then verify independently.

- **Attempt 1, rejected:** 100 % dedication → μ = 352 h ÷ 10 h = **35.2**, which
  predicts Wq = 0.9 d. Reality is 3–7 d, so pickups are clearly not instant.
- **Attempt 2, kept:** μ = **23.5** →

| λ | ρ | Wq | observed [C] |
|---|---|---|---|
| 15 | 0.64 | 2.3 d | ~3 d |
| 17.5 | 0.74 | **3.8 d** | 3–7 d |
| 20 | 0.85 | 7.5 d | ~7 d |

The model reproduces the whole band, *including* its workload-dependence.

**Reality check — labour:** 23.5 × 10 h = 235 h = 67 % of the 352 available
hours (matches the ~65 % availability reasoned elsewhere in the project).

**The company's output ceiling, calculated from first principles:**

```
2 producers × 22 working days × 8 h  =  352 producer-hours per month
352 h ÷ 10 h of labour per video     =  35.2 videos per month (100 % dedication)
                                     ≈  the company-stated ceiling 35–40/month [C]
```

The stated "ceiling" is therefore not an operational target — it is the **ρ = 1
wall** of a fully-dedicated team: at λ ≥ 35.2 the queue can only grow, and
"pushing to the ceiling" is a mathematical promise of unbounded waiting.

## Part 2 — Predictions (`part2_predictions`)

Everything below is pure M/M/1 algebra at μ = 23.5, shown for the typical month
(λ = 17.5) and the heavy month (λ = 20).

### Utilization and the expected wait

| quantity | formula | typical λ = 17.5 | heavy λ = 20 |
|---|---|---|---|
| utilization ρ | λ / μ | 0.74 | 0.85 |
| one "turn" of work τ | 22 wd ÷ μ | 0.94 wd | 0.94 wd |
| expected intake wait Wq | ρ/(1−ρ) · τ | 2.73 wd = **3.8 d** | 5.35 wd = **7.5 d** |
| time in system W | Wq + τ | 3.67 wd | 6.29 wd |

Worked, typical month: ρ = 17.5 ÷ 23.5 = 0.745 → congestion multiplier
ρ/(1−ρ) = 2.92 → Wq = 2.92 × 0.94 wd = 2.73 wd × 1.4 = **3.8 calendar days**,
inside the reported band [C]. ρ is also ≈ the probability that a new request
finds the team busy: **3 out of 4 arrivals must wait.**

### How many requests sit in the inbox — the falsifiable prediction

Little's Law, Lq = λ · Wq (λ converted to per-working-day):

- typical: 17.5 ÷ 22 × 2.73 wd = **2.2 pending requests**
- heavy: 20 ÷ 22 × 5.35 wd = **4.9 pending requests**

Ask HiLegal to count the inbox: **≈ 2–5 parked requests** at a typical moment
confirms the model. If it never holds more than one while waits still run 3–7
days, the delay is batch-review cadence (producers checking intake twice a
week), not classic queueing — see model card. Widening to the whole system,
L = λ·W gives 2.9 / 5.7 videos in progress — i.e. each producer is juggling
1–2 staggered videos.

### The tail — how bad one lawyer's wait gets

M/M/1 queue waits are exponentially distributed:
P(Wq > t) = ρ · e^(−(μ−λ)/22 · t), with drain rate (23.5 − 17.5)/22 =
**0.273 per working day**:

| t (calendar days) | 5 | 7 | 10 | 14 |
|---|---|---|---|---|
| P(wait > t) | 28 % | 19 % | 11 % | 5 % |

Worked: P(> 7 d) = 0.745 · e^(−0.273 × 5.0 wd) = 0.19 — **1 in 5 lawyers waits
over a week before production even starts.** The company's phrase
"workload-dependent" [C] *is* this fat tail. The **P90** solves
0.745 · e^(−0.273·t) = 0.10 → t = ln(7.45)/0.273 = 7.4 wd ≈ **10 calendar
days**: 1 in 10 lawyers waits two weeks just to be *looked at*.

### Nonlinearity — why "working harder" fails

Wq = [ρ/(1−ρ)] · τ: the congestion multiplier is the villain — it depends on
where you stand, not how hard you push:

| ρ | 0.64 | 0.74 | 0.85 | 0.90 | 0.95 | → 1 |
|---|---|---|---|---|---|---|
| ρ/(1−ρ) | 1.8 | 2.9 | 5.7 | 9.0 | 19.0 | ∞ |

Demand 15 → 20 is ×1.33, but the wait 2.3 → 7.5 d is **×3.2**: the process
simply climbed the multiplier ladder. Effort moves λ or μ a little; the
multiplier turns small moves into large waits.

### The wall — where the ceiling calculation lands

At λ ≥ μ, ρ ≥ 1 ⇒ Wq → ∞: every month spent at or above the wall adds
permanent backlog. The ceiling calculated in Part 1 (352 h ÷ 10 h = 35.2/month)
is exactly that wall, and it matches the company-stated 35–40 [C]. At
λ = 24 (a marketing push): ρ = 24 ÷ 23.5 = 1.02 > 1 — the queue never drains.

## Part 3 — Validation (`part3_simulation`)

200 000 random orders through a strict FIFO single server (exponential
arrivals at rate λ, exponential service at rate μ, first-come-first-served):
simulation matches the formulas at **0.7 % (λ = 17.5)** and **1.2 % (λ = 20)**
— the formulas are what actually happens when you run the process.

## Part 4 — Charts (`part4_charts`, matplotlib → SVG, transparent background)

| File | What it shows | When to show it |
|---|---|---|
| `queue-cliff.svg` | **One curve, two x-axes**: expected wait vs. utilization ρ (bottom axis) and vs. monthly demand λ (top axis, constant team) — the utilization cliff and the demand sweep are the same curve, since ρ = λ/μ. Gold 3–7 d observed band, three demand dots (15 / 17.5 / 20), the ρ = 1 wall at λ = μ ≈ 23.5 with the calculated ceiling 35.2 [C], and the unstable region (ρ > 1) where backlog grows forever — including the λ = 24 marketing push | THE chart — the "you cannot stand slightly left of a cliff" slide; also carries the scale/ceiling discussion ("near μ, demand becomes queue") |
| `order-timeline.svg` | Lawyer Chen's order through the 12 steps: green work, red waiting; intake queue is the first big red block; 18.8 d end-to-end, work ≈ 6 % | the one-order walkthrough — makes "queue-gated, not work-gated" visible |
| `why-one-server.svg` | split panel: textbook M/M/c (instant dispatch, minutes-long jobs) vs HiLegal's order rail (pickup only at completion boundaries); bottom band ties the choice to the calibration fit (2.3 / 3.8 / 7.5 d across the demand range) | the "why M/M/1" moment — the only chart about the *model choice* |

All three SVGs are written with a **transparent background** (no white box) —
they composite cleanly onto slide layouts. The text/line palette is dark, so
place them on light backgrounds.

---

## Model card (say these on purpose)

1. μ is calibrated, not measured [E] — one knob, one observation, then verified
   via labour accounting (67 %) and simulation (±1 %).
2. Poisson arrivals are an assumption — defensible: independent lawyers, no
   coordination; bursts only make waits worse, strengthening the conclusion.
3. M/M/1 is a simplification (two humans, one modeled server) — chosen because
   the pickup process behaves as one pooled unit (see `why-one-server.svg`).
4. Steady state assumed — a normal month, not a launch transient.
5. Falsifiable: if the inbox never holds more than ~1 request while waits
   still run 3–7 days, the delay is batch-review cadence, not queueing — a
   self-serve intake kills either mechanism.
6. Scope: the intake queue only; client approval-gate waits sit on top of it.
7. With churn/overtime (Section 2), reality is likely *worse* than modeled.

## The one line to remember

> "At ρ ≈ 0.74–0.85, the 3–7 day intake wait is not a people problem — it is
> the mathematics of standing on the steep part of the utilization cliff."
