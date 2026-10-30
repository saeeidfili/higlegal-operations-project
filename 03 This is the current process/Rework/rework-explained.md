# Rework simulation — step by step

*How the rework study works, what every moving part does, and exactly how it was built. Companion to `START.md` (findings) and `rework_simulation.py` (code). No prior simulation knowledge needed.*

---

## 0. The question

Rework looks like an *effort* problem ("another draft, another edit"). The simulation asks: **what does rework do to the queue?** It models the whole 12-step process — two producers, three looping approval gates — and compares four rework intensities under the same demand.

One-paragraph answer: at the company's ~10 h per video, rework adds **72 minutes of work but 9.7 days of lead time**; it raises work-in-process from ~6 to ~12–20 videos, and it **cuts the effective capacity ceiling** from ~27 to ~24 (baseline) to ~21 videos/month (heavy). The queue cost is ~30× the work cost.

---

## 1. Units and time

- Time runs in **working days**; one month = 22 working days.
- A producer's paid day is 8 h, but only **67%** is available for videos (the rest is platform work) → **322 effective minutes per producer-day** (480 × 0.67). All work durations are converted: `duration_days = minutes / 322`.
- Lead times are reported in **calendar days** (×1.4 to account for weekends).
- This 67% factor is the same dedication assumption used in `kpi-data.md` §4 and in the queueing model.

## 2. The engine: events on a timeline

The simulation is a **discrete-event simulation (DES)**. Nothing happens continuously; the clock jumps from one event to the next.

```
events = min-heap of (time, callback)
t = 0
while heap not empty and t <= horizon:
    pop the earliest event
    set t to its time
    run its callback          # this may schedule new events
```

Every action — an arrival, a work task finishing, a gate wait ending — is an event with a timestamp. This is what lets thousands of videos overlap correctly without simulating every second.

## 3. What a "video" is

Each request is an object with: `arrival` time, `first_work` time (when a producer first touches it), `delivered` time, accumulated work minutes and waits, loop counters, and a list of **segments** (start, end, label, kind) used for the Gantt chart.

## 4. The producers: one pooled team

Two producers, modelled as **one work queue** with two servers:

- Any free producer takes the next work task (work-conserving).
- A task, once started, is never interrupted (no preemption — matches the "team as a processing unit" argument in `queueing-model.md`).
- While a video waits at a client gate, its producer is **free** to work on other videos.

Dispatch logic:

```
request_work(minutes, video, label):
    push (minutes, video, label) onto work_queue
    while work_queue not empty and some producer is free:
        take a free producer
        start task: busy for minutes/322 days
        when done: free the producer; resume the video's next step
```

The first task a video needs is "intake review" (15 min). `first_work` is stamped when that task starts; `first_work − arrival` is the simulated intake wait.

## 5. One video's journey (the generator)

The process is written as a Python **generator** that yields actions in order — `('work', minutes)` or `('wait', days)`. The driver executes each action (request a producer / schedule a timer) and resumes the generator when it completes. The exact sequence (baseline):

| # | Step | Action | Value |
|---|---|---|---|
| 1 | Intake review | work | 15 min |
| 2 | Clarification | repeat: wait **U(1,2) d**; work 8 min — until approved | mean 4 rounds at baseline [C] |
| 3 | Content brief | work | 45 min |
| 4 | Script drafting | work | 70 min |
| 5 | AI refinement | work | 35 min |
| 6 | Script approval | wait **U(1,3) d**; if rejected → 50 min rework, wait again | 30% loop probability |
| 7 | Video generation | work | 55 min |
| 8 | Audio generation | work | 30 min |
| 9 | AV sync | work | 140 min |
| 10 | Final approval | wait **U(1,3) d**; if rejected → 70 min rework, wait again | 30% loop probability |
| 11 | Platform adaptation | work | 95 min |
| 12 | Delivery & admin | work | 23 min |

Each rejection adds a **wait** and a **rework block** — the two things the study is about.

## 6. Rework is probabilistic

Loop behaviour is a geometric process: after each review, the video escapes with probability `1 − p`, or loops with probability `p`.

- Expected clarification rounds: `1 / (1 − p_clar)` → baseline p = 0.75 → **4 rounds** [C].
- Expected script loops: `p_s / (1 − p_s)` → baseline 0.30 → 0.43 loops.
- Expected final loops: same → 0.43 loops.
- Rework incidence (≥1 loop anywhere): `1 − (1 − p_clar) × (1 − p_s) × (1 − p_f)` → **87%** at baseline (matches the ~90% estimate [E]).

**Closed-form check of the work content** (this is how we know the code implements the intended model):

```
E[work] = 15 + 8/(1−p_clar) + 45 + 70 + 35
          + 50·p_s/(1−p_s) + 55 + 30 + 140 + 70·p_f/(1−p_f) + 95 + 23
```

| Scenario | Formula | Simulated |
|---|---:|---:|
| No rework | 516 min | **516** |
| Halved | 545 min | **548** |
| Baseline | 591 min | **588** |
| Heavy | 668 min | **684** (sampling noise) |

The formula and the simulation agree within a few minutes — the model does what it claims.

## 7. Arrivals

Requests arrive as a **Poisson process**: inter-arrival times are exponential with mean `22/λ` working days. At λ = 17.5/month, one request every ~1.26 working days. Each arrival creates a video and starts its generator immediately; the first task queues for a producer.

**Note:** because producers take work the moment they are free, the simulated intake wait is a **lower bound** (≈0.1–0.2 days). HiLegal's real 3–7-day intake queue comes from batching/pickup policy, modelled separately in `queueing-model.md`. This study deliberately isolates the *whole-process* effect of rework.

## 8. Measurement window and statistics

- Run length: **28 months** (616 working days).
- **Warm-up: 10 months** discarded (the pipeline starts empty).
- **Cutoff: last 3 months excluded** — videos arriving near the end have not been delivered yet, and counting only completed ones would bias lead times downward (censoring).
- Window: videos with `10 mo ≤ arrival ≤ 25 mo`; statistics over the **15-month** window.

Collected per video: lead time (`delivered − arrival`), intake wait (`first_work − arrival`), hands-on work, rework incidence. Global: utilization = total producer-busy days ÷ (2 × months × 22), WIP = videos created but not yet delivered (sampled every 0.5 working days).

**Demand sweep:** 4 demand levels × 3 rework levels × **3 seeds** (to average out stochastic noise), 36-month runs with 16-month warm-up. The sweep reports **mean WIP** rather than lead time: when a scenario is unstable, lead-time statistics are censored (only the fast videos finish inside the window), while WIP keeps growing and shows the instability honestly.

## 9. Scenarios

| Scenario | p_clar | p_script | p_final | Expected rounds | Expected rework incidence |
|---|---:|---:|---:|---:|---:|
| No rework | 0 | 0 | 0 | 1 | 0% |
| Rework halved | 0.50 | 0.15 | 0.15 | 2 | 57% (63% simulated) |
| Baseline | 0.75 | 0.30 | 0.30 | 4 | 88% (87% simulated) |
| Heavy | 0.80 | 0.50 | 0.50 | 5 | 95% (97% simulated) |

## 10. Results (λ = 17.5 videos/month)

| Scenario | Lead time | P90 | Work | Rework | Capacity | Utilization |
|---|---:|---:|---:|---:|---:|---:|
| No rework | 11.0 d | 13.1 | 516 min | 0% | 27.4/mo | 65% |
| Halved | 14.0 d | 20.6 | 548 min | 63% | 25.8/mo | 67% |
| Baseline | 20.7 d | 32.0 | 588 min | 87% | 24.0/mo | 72% |
| Heavy | 28.8 d | 47.8 | 684 min | 97% | 20.7/mo | 78% |

Capacity = `2 producers × 22 days × 322 min ÷ work per video`. Utilization is measured against the 67%-video budget; 72% there ≈ 48% of paid hours — the same regime as the queueing model (ρ ≈ 0.74–0.85).

**Demand sweep (mean WIP · lead days):**

| λ | No rework | Baseline | Heavy |
|---:|---:|---:|---:|
| 15/mo | 5.2 · 10.7 | 9.7 · 20.4 | 12.8 · 26.6 |
| 17.5/mo | 6.2 · 11.2 | 12.5 · 22.3 | 20.4 · 32.7 |
| 20/mo | 7.6 · 11.8 | 15.8 · 24.0 | 31.2 · 45.8 |
| 22/mo | 8.9 · 12.5 | 23.3 · 30.7 | **71.8 · 99.6** ✗ |

## 11. The four charts

- **`rework-impact.svg`** — lead time (mean bar + P90 tick) and work per video, per scenario. The gap between the two panels is the rework queue cost.
- **`queue-sample-path.svg`** — WIP over time at 22/month: flat (no rework), climbing (baseline), runaway (heavy).
- **`rework-vs-demand.svg`** — mean WIP vs demand for the three rework levels: each curve has its own breaking point.
- **`gantt-rework.svg`** — two median orders (no rework vs baseline) as coloured timelines: green = work, dark red = rework work, red = approval waits, gold = clarification waits, blue = intake.

---

## 12. How this file was built — the exact steps

1. **Fixed the inputs** from the project data: 12 steps, ~10 h labour [C], 2 producers, demand 15–20/month [C], brief loop ≥4 rounds [C], rework ≈ 90% [E], sync/adaptation blocks. Converted everything to working days at 322 effective minutes/day.
2. **Wrote version 1** of the DES with two "owner" producers, each holding a capped WIP of videos.
3. **Ran it — and got nonsense:** lead times of 150–250 days, and the *no-rework* scenario was the slowest. Diagnosis: all seeded videos started at t=0 and moved through the gates in lockstep, so producers were idle while a backlog existed. The owner/WIP-cap structure was the culprit.
4. **Rewrote as a pooled work-conserving model** — two producers sharing one task queue, videos flowing independently. This also matches the "team as one processing unit" argument used elsewhere in Section 3.
5. **Found and fixed three measurement bugs:**
   - the measurement window included videos that arrived before warm-up ended → filter by arrival date;
   - end-of-run censoring understated throughput → added a 3-month cutoff;
   - the demand sweep was noisy and non-monotonic → run 3 seeds per point and report **WIP** instead of censored lead times.
6. **Found a modelling bug in the script loop:** a rejection re-ran the full draft+refine (155 min) *plus* the 50-min rework, contradicting the documented 50-min rework. Restructured the loop so a rejection costs one 50-min rework pass. Baseline work dropped from 630 to **588 min**, matching the ~10 h baseline [C] (−2%).
7. **Replaced the misleading "output/month" column** with **effective capacity** derived from work content (2 × 22 × 322 ÷ work). Output merely mirrored realized demand; capacity is the quantity the rework story is about.
8. **Built the four SVG charts** with a small dependency-free SVG helper; fixed a label overflow in the impact chart and converted the Gantt to calendar days.
9. **Validated:** calibration checks pass (lead 20.7 d inside 14–28 [C]; work 588 ≈ 10 h [C]; rework 87% ≈ 90% [E]; utilization 72% ≈ ρ 0.74–0.85), all SVGs parse as valid XML.
10. **Documented and shipped:** wrote `START.md` (mechanisms, results, chart guide, limitations) and this file; linked both from `03 START.md`; committed and pushed to the project repository.

## 13. Limitations (say them before someone asks)

- Gate loop probabilities are **independent of load** — the "congestion → rushed review → more rework" feedback loop is not modelled (it would make results worse, not better).
- The pooled model is **work-conserving**, so its intake wait is a lower bound; the real 3–7-day intake queue lives in `queueing-model.md`.
- **Two producers, no skills differentiation** — one task pool, no specialisation or hand-offs.
- Seeded stochastic runs: single-seed scenarios vary ±5–10%; treat small differences as noise. The sweep averages 3 seeds.
- Heavy rework is a **stress scenario**, not a forecast. P90 = 47.8 days means "the queue is out of control", not "a specific lawyer waits 48 days".

## 14. Run and modify

```
python3 rework_simulation.py
```

Edit `SCENARIOS` at the top of `main()` to change loop probabilities, `MONTHS`/`WARMUP_MONTHS` for horizon, or pass a different `lam` to `run_scenario` for demand. All randomness is seeded → results are reproducible. The script prints every table shown here and rewrites all four SVGs.
