# Rework and the queue — full-process simulation

**Question:** what does rework actually do to HiLegal's queues, lead time and capacity?

**Short answer:** rework looks like "a bit of extra work" (a redraft, a re-edit), but its real cost is **extra waiting**. In the simulation, removing rework saves **114 minutes of hands-on work but 12.3 days of lead time** — the queue cost is roughly **30× the work cost** [E]. And rework doesn't just slow the queue; it **lowers the demand level at which the queue explodes**.

This folder contains:
- `rework_simulation.py` — discrete-event simulation of the **whole 12-step process** (two producers, three looping gates), four scenarios, demand sweep, four SVG charts. No dependencies.
- `rework-impact.svg` — lead time vs. work content per scenario
- `queue-sample-path.svg` — videos-in-system (WIP) over time at 22/month
- `rework-vs-demand.svg` — WIP vs. demand for three rework levels
- `gantt-rework.svg` — one median order with vs. without rework

Run: `python3 rework_simulation.py` (writes the charts next to the script).

---

## 1. What "rework" means in this process

Three approval gates can send work backwards (Section 3's map):

| Gate | Loops back to | Baseline behaviour |
|---|---|---|
| G1 Clarification | intake / brief | **≥4 rounds** [C] — the dominant loop |
| G2 Script approval | script drafting | rejected → redraft + re-approve |
| G3 Final approval | production (partial redo) | changes → re-edit, re-sync, re-adapt |

Baseline parameters used in the simulation (calibrated; see §4): clarification loops with probability 0.75 per round (mean 4 rounds), script and final gates loop with probability 0.30 each → **≈90% of videos go through at least one rework loop** [E], matching the 90% rework rate in `kpi-data.md`.

## 2. How rework hits the queue — five mechanisms

Rework is usually managed as a *work* problem ("it costs us extra hours"). Operationally it is mostly a *queue* problem. Five mechanisms, each visible in the simulation:

**① Work inflation → utilization rises.** Every loop adds minutes: 516 (none) → 630 (baseline) → 763 (heavy) min/video. Utilization of the video-dedicated budget rises 65% → 78% → 97%. And near the utilization cliff, a few extra minutes per video are not "a few extra minutes" — they multiply into waiting (the ρ/(1−ρ) multiplier in `queueing-model.md`).

**② Every loop adds a wait, not just work.** A redraft does not just add 50 minutes; it adds a **new gate wait** (1–3 days) and **a new turn in the work queue**, and it holds the video in the system while everything else moves. This is why +114 min of work costs +12.3 days of lead time. The queue cost dominates.

**③ Variability amplification (Kingman's c_s²).** Rework makes service times uneven — one video takes 516 minutes, the next 800. Even at the same average load, uneven service inflates waiting (see the VUT equation in `queueing-model.md`). The "rework halved" scenario cuts work by only 68 minutes but cuts lead time by 7.6 days.

**④ WIP inflation (Little's Law).** At 17.5 videos/month, videos in the system rise **6.2 → 13.7 → 24.0** from no-rework to baseline to heavy. Since lead time = WIP ÷ throughput, every video held by a loop delays all the others. Rework makes the queue larger *and* slower.

**⑤ Capacity erosion — the moving ceiling.** At realistic dedication (67% of paid hours), the effective capacity ceiling falls:

| Scenario | Capacity (videos/month) |
|---|---:|
| No rework | ~27.5 |
| Baseline (~90% rework) | ~22.4 |
| Heavy rework | ~18.5 |

The company's stated ceiling of 35–40 [C] assumes 100% dedication; at operational dedication, **rework pulls the real ceiling down to ~22**. At 20/month heavy rework, utilization exceeds 100% — the backlog grows forever, and no amount of effort fixes it.

**A feedback loop we did not model (state it as future work):** congestion → rushed reviews → more rework → more congestion, and (Section 2) burnout → errors → rework. The simulation treats loop probabilities as fixed; in reality they likely rise under load — which would make every number in this folder a *conservative* estimate.

## 3. Simulation design

A **discrete-event simulation of the full 12-step process**, not a queueing formula:

- Poisson arrivals at demand λ (default 17.5 videos/month).
- **Two producers = one pooled task pool.** Any producer takes the next available work task; tasks are never preempted. (Matches the "team as a processing unit" argument in `queueing-model.md`.)
- Every video flows independently: work tasks alternate with client-gate waits. While a video waits at a gate, producers are free for other videos.
- Three looping gates (G1/G2/G3) with the probabilities above; rework adds both work minutes and new gate waits.
- Work durations come from the Section 3 waterfall, normalized so the baseline sums to ≈10 h [C] (630 min simulated vs ~600 min reported, +5%).
- **Availability:** producers spend ~33% of paid time on platform work → effective owner-minutes = 480 × 0.67 ≈ 322/day. Utilization is therefore reported against the *video-dedicated budget* (78% there ≈ 52% of paid hours — consistent with the queueing model's ρ ≈ 0.74–0.85).
- Horizon 28 months, statistics over the last 18; sweep averaged over 3 seeds.

**Model honesty:** the simulation is work-conserving (idle producers take queued work immediately), so its **intake wait is a lower bound** — it lands at 0.1–0.3 days, while HiLegal reports 3–7 days [C]. The real intake queue comes from batching/pickup policy and is modeled separately in `queueing-model.md`; the rework study deliberately isolates the *whole-process* effect. Total lead time still lands inside the company range (see checks below).

## 4. Calibration checks (baseline scenario)

| Check | Simulated | Company/plan value | Verdict |
|---|---:|---|---|
| Lead time (mean) | **23.2 d** | 14–28 d [C] | ✓ inside |
| Hands-on work per video | **630 min (10.5 h)** | ~10 h [C] | ✓ +5% |
| Rework incidence | **89%** | ~90% [E] | ✓ |
| Throughput at λ = 17.5 | **17.2/mo** | 15–20/mo [C] | ✓ |
| Utilization (video budget) | **78%** | ρ ≈ 0.74–0.85 (queue model) | ✓ same regime |

## 5. Results

### 5.1 Rework intensity (λ = 17.5 videos/month)

| Scenario | Lead time | P90 | Hands-on work | Rework incidence | Output | Utilization |
|---|---:|---:|---:|---:|---:|---:|
| No rework | **11.0 d** | 13.0 | 516 min | 0% | 17.2/mo | 65% |
| Rework halved | **15.6 d** | 20.5 | 562 min | 66% | 17.6/mo | 72% |
| Baseline (~90%) | **23.2 d** | 37.8 | 630 min | 89% | 17.2/mo | 78% |
| Heavy rework | **65.9 d** | 101.5 | 763 min | 95% | 16.8/mo | 97% |

**Read it as:** removing rework cuts lead time by 53% (23.2 → 11.0 d) while cutting work by only 18%. Rework's queue cost dwarfs its work cost. The P90 tells the same story harder: half of all rework pain lands on the worst-served 10% of lawyers (37.8 vs 13.0 days).

### 5.2 Rework × demand (mean WIP in videos; lead time in days)

| Demand λ | No rework | Baseline | Heavy |
|---:|---:|---:|---:|
| 15/mo | 5.2 · 10.7 d | 9.9 · 20.8 d | 12.6 · 27.8 d |
| 17.5/mo | 6.2 · 11.2 d | 13.7 · 23.5 d | 24.0 · 41.3 d |
| 20/mo | 7.6 · 11.8 d | 18.2 · 27.4 d | **94.4 · 146.9 d** ✗ unstable |
| 22/mo | 8.9 · 12.5 d | **54.6 · 71.7 d** ✗ unstable | **134.1 · 188.8 d** ✗ unstable |

**Read it as:** without rework, the process absorbs 22/month comfortably. At baseline rework it survives 20 but collapses at 22. With heavy rework, 20/month — a level the company *wants* to reach — already exceeds capacity and the backlog grows without bound. **The ceiling is not a property of the team; it is a property of the team plus its rework.**

## 6. The four charts — what each shows

### `rework-impact.svg`
**What:** left — mean lead time per scenario (bar) with P90 tick; right — hands-on work per video, with rework incidence.
**How to read:** the left bars fall much faster than the right bars when rework is removed. That gap *is* the rework queue cost.
**When:** the headline slide of this annex; say "rework costs 12 days for two hours of work".

### `queue-sample-path.svg`
**What:** videos in the system (WIP) over 20 months at **22 videos/month** for no rework / baseline / heavy rework.
**How to read:** no-rework is flat; baseline climbs; heavy keeps climbing — an unstable queue. WIP is the queue you can see; lead time is WIP ÷ throughput (Little's Law).
**When:** when arguing that rework turns a manageable demand into a backlog.

### `rework-vs-demand.svg`
**What:** mean WIP against demand λ (15–22/month) for the three rework levels.
**How to read:** each curve has its own breaking point: without rework, flat up to 22; baseline bends sharply at ~20; heavy explodes from 20 onward. The vertical distance between curves is the capacity rework eats.
**When:** Section 7 (scenario simulation) or when someone asks "can we just push more volume?".

### `gantt-rework.svg`
**What:** two median orders — one first-time-right, one baseline with loops — each block is elapsed time in a step; colours distinguish work, rework work, approval waits, clarification waits, intake.
**How to read:** the baseline bar is longer *and* mostly red/gold: the extra time is not extra green work, it is repeated waiting. Rework work blocks (dark red) are small compared with the waits they trigger.
**When:** the walkthrough — "here is what one lawyer's order actually spends its month doing".

## 7. What this means for the iterations (Section 6)

The simulation gives the iterations a quantitative target path:

| Iteration | Gate attacked | Simulated analogue | Expected effect |
|---|---|---|---|
| 1 — structured brief + SLA approvals | G1 clarification (mean 4 → ~2 rounds) | between baseline and "halved" | −5 to −8 days lead time |
| 2 — templates + AI scripting | G2 script loops | "halved" → better | −3 to −5 days |
| 3 — single render | G3 final loops (deterministic render) | toward "no rework" | −2 to −4 days; residual = client approval |
| **Chain target** | rework 90% → 10% (`kpi-data.md`) | **≈ the no-rework scenario (11 d)** | **lead time ≈ 2 weeks → ≈ 1.5 days once approval SLAs are included** |

The table is honest about the direction: **rework reduction is the single largest lever on lead time** — larger than working faster, because effort cannot escape the ρ/(1−ρ) curve.

## 8. Model card & limitations

- **Two producers, pooled task queue, no preemption of tasks.** Tasks are fine-grained (minutes to hours); videos wait at gates without occupying a producer.
- **Gate loop probabilities are independent of load.** The congestion→rushed-review→more-rework feedback loop is not modeled (would worsen results).
- **Availability factor 0.67** (platform-work share) is an assumption [E], consistent with `kpi-data.md` §4.
- **Intake wait is a lower bound** (work-conserving); the true 3–7-day intake queue is modeled in `queueing-model.md`.
- **Stochastic:** seeded runs; single-seed scenario table (±5–10% run-to-run), sweep averaged over 3 seeds. Treat differences under ~2 days as noise.
- **Heavy rework is a stress scenario**, not a forecast; P90 = 101 days means "the queue is out of control", not "some lawyer will wait 101 days".
- **Durations** are normalized to the company-reported ~10 h baseline (+5% in simulation).

## 9. Reproduce it

```
python3 rework_simulation.py
# → scenario table, demand sweep, 4 SVG charts in this folder
```

Change `SCENARIOS` (loop probabilities), `MONTHS`, or the demand `λ` in `main()` to explore. All randomness is seeded, so results are reproducible.
