# Section 7 — Let's run and compare the processes

**Guiding question:** How do the original process and successive improvements behave under different conditions?

**What this section must accomplish:** run the baseline vs. Iterations 1–3 through the same scenarios, vary **demand, approval delays, and rework**, and show the six KPIs responding. State inputs and assumptions openly — this is the stress-test that makes the Section 6 claims credible instead of aspirational.

---

## Model design (one paragraph you can say on stage)

Each video is an entity flowing through the version's process map. Steps consume **producer time (capacity constraint: 2 producers)**; queues and gates add **calendar waiting**; gates can **loop** with scenario-dependent probability. Lead time = request → published. All parameters come from `05 .../kpi-data.md`; distributions are uniform over the stated ranges [E] — we model ranges, not fake precision. Little's Law provides the sanity check on every run.

## Input parameters per process version (all from `kpi-data.md`, tagged there)

| Parameter | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|
| Total producer work per video (min, first pass) | 600 [C→E split] | 435 | 350 | 60 |
| Producers | 2 [C] | 2 | 2 | 2 |
| Intake queue (days) | 3–7 [C] | 0 | 0 | 0 |
| Clarification loop | 2–4 rounds, 1–2 d each [E, anchored on ≥4 total brief iterations C] | 0 | 0 | 0 |
| Gate waits — script approval (days) | 1–3 | 1–2 (48 h SLA) | ~1 | 1–2 (24–48 h) |
| Gate waits — final approval (days) | 1–3 | 1–2 (SLA) | ~1 | 0 (parallel objection window) |
| Loop probability per gate | high (≈ 90% rework [E]) | ~55% | ~30% | ~10% |
| Render time | n/a (manual) | n/a | n/a | ~0.5 d in batch |
| Tool/runtime cost per video (¥) | 90 | 90 | 100 | 95 |

## Scenario matrix (run each process version × each scenario)

| # | Scenario | Knob settings | What it demonstrates |
|---|---|---|---|
| S0 | **Normal conditions** | Demand 20/mo · gate waits at expected values · loop rates at targets | The standard comparison — the Section 6 scoreboard, now simulated |
| S1 | **Demand surge** | Demand 20 → 40 → 80/mo | Where each version saturates: baseline breaks ~19–24, v2 ~33, v3 serves 80 with hours of slack |
| S2 | **Slow lawyers** (approval delays) | Gate waits ×2–3 (3–6 d) | v1's SLA caps the damage; v3 lead time stays ≈ client-gated (~2–3 d) while baseline balloons past 5 weeks |
| S3 | **Rework stress** (the proposal's worst case) | All gates loop up to 4 iterations [C worst case] | v2/v3 templates + structured change requests absorb loops; baseline lead time explodes; rework-KPI divergence |
| S4 | **Producer absence** | 1 producer for 2 weeks | Baseline queue spirals; v3 unaffected (4 h/mo team load at 20 videos) |
| S5 | **Quality dip** (AI regression) | v3 loop rate 30% (back to v2 level) + edit depth 25% | Guardrail test: does v3 still beat v2? (Yes — capacity is structural, labour is QC-bound) |

**Outputs per run (the dashboard):** lead time (mean + P90), throughput vs demand (backlog growth), producer utilization, WIP, cost/video, rework rate, QAR. Show **P90, not just mean** — professors and clients both respect tail awareness.

## Expected qualitative results (pre-register them before running — then confirm)

| Scenario | Expected ordering (best→worst) | Expected headline |
|---|---|---|
| S0 | v3 < v2 < v1 < baseline (lead time) | 21 d → 1.5 d |
| S1 | v3 keeps lead time < 2.5 d at 80/mo; baseline hits backlog explosion at ~19–24/mo | "Demand is no longer a capacity problem" |
| S2 | Everyone slows, but v3 worst case ≈ 3–4 d ≈ baseline's *best* case | "The residual process time belongs to the client" |
| S3 | Baseline median > 5 weeks; v3 worst case ≈ 3 d | Worst-case robustness — the proposal's design commitment |
| S4 | Baseline: queue grows unbounded; v3: invisible | Capacity headroom as insurance |
| S5 | v3 labour rises to ~1 h 30, still ≪ v2's 5 h 50 | Graceful degradation — no iteration depends on perfection |

If a run contradicts these expectations, **show it anyway** and explain — a stress test that only confirms is theater. This sentence buys enormous credibility.

## Implementation options (pick by effort budget)

1. **Spreadsheet queueing approximation (2–3 h):** deterministic per-version calculators (work ÷ capacity, waits summed by loop expectation). Fine for S0/S1; weak for loops.
2. **Python discrete-event simulation (recommended; ~100 lines with `simpy`)** — skeleton below, parameters from the table above.
3. **Animation for the deck (no sim):** one order's timer bar per version (21 d / 9 d / 4 d / 1.5 d) with work-vs-wait colouring — the visual companion to whichever numeric option you choose. The S1 backlog spiral (baseline) vs flat line (v3) is the single most persuasive animation.

### simpy skeleton (parameters live in one dict per version)

```python
import simpy, random

VERSIONS = {  # fill from the parameter table / kpi-data.md
  "baseline": dict(work_min=600, intake=(3,7), clar_rounds=(2,4), clar_day=(1,2),
                   script_wait=(1,3), final_wait=(1,3), loop_p=0.9, render_days=None),
  "v1":       dict(work_min=435, intake=(0,0), clar_rounds=(0,0), clar_day=(0,0),
                   script_wait=(1,2), final_wait=(1,2), loop_p=0.55, render_days=None),
  "v2":       dict(work_min=350, intake=(0,0), clar_rounds=(0,0), clar_day=(0,0),
                   script_wait=(1,1), final_wait=(1,1), loop_p=0.30, render_days=None),
  "v3":       dict(work_min=60,  intake=(0,0), clar_rounds=(0,0), clar_day=(0,0),
                   script_wait=(1,2), final_wait=(0,0), loop_p=0.10, render_days=0.5),
}

def video(env, name, p, producer, stats):
    t0 = env.now
    arrive = lambda lo, hi: random.uniform(lo, hi)
    for _ in range(random.randint(*p["clar_rounds"])):          # clarification loop
        yield env.timeout(arrive(*p["clar_day"]))
    yield env.timeout(arrive(*p["intake"]))                     # intake queue
    while True:                                                 # script gate
        with producer.request() as req:
            yield req; yield env.timeout(p["work_min"] / 480 / 3)  # 1/3 of work before gate
        yield env.timeout(arrive(*p["script_wait"]))
        if random.random() > p["loop_p"]: break
    while True:                                                 # final gate
        with producer.request() as req:
            yield req; yield env.timeout(p["work_min"] / 480 / 2)  # remaining work
        if p["render_days"]: yield env.timeout(p["render_days"])
        yield env.timeout(arrive(*p["final_wait"]))
        if random.random() > p["loop_p"]: break
    stats.append(env.now - t0)                                  # lead time in days

def run(version, demand_pm, days=90):
    p = VERSIONS[version]
    env = simpy.Environment()
    producer = simpy.Resource(env, capacity=2)
    stats = []
    for i in range(int(demand_pm / 30 * days)):
        env.process(video(env, f"v{i}", p, producer, stats))
    env.run(until=days)
    n = len(stats); import statistics as s
    return dict(mean=s.mean(stats), p90=sorted(stats)[int(.9*n)] if n else None, done=n)

# scenarios: for v, k in VERSIONS.items(): print(v, run(v, demand_pm=20))
```

*(Skeleton: adjust work-split fractions per version so first-pass work ≈ waterfall values; calibrate S0 output to reproduce `kpi-data.md` §2 midpoints before running S1–S5 — calibration against company-reported baselines [C] is what makes the model defensible.)*

## Assumptions to state on the slide (the honesty box)

- Producers = 2 [C]; utilization ~60% [E]; 8 h working day, ~21.7 working days/month [E]
- Waits uniform over stated ranges [E]; loop rates from `kpi-data.md` targets [T]
- Calendar-day waits include weekends; render queue is FIFO batch [E]
- Model ignores seasonality and marketing-driven demand spikes (add a scenario if asked)
- Calibrated so S0 reproduces company-reported baseline output 15–20/mo [C] and lead time 14–28 d [C]

## Files to produce for this folder

- `simulation.py` (if simpy route) or `model.xlsx` (spreadsheet route)
- `scenario-results.md` — results table per scenario + the two money charts (lead-time bars by version; backlog spiral S1)
- `animation-timer.png`/mp4 — the work-vs-wait timer bars per version

## Checklist

- [ ] Inputs table shown on the slide (with tags [C]/[E]/[T])
- [ ] All four process versions run through all scenarios (same conditions)
- [ ] P90 reported, not just averages
- [ ] At least one surprising/robustness result presented honestly
- [ ] Bridge to Section 8: *"The process now has headroom. What is that headroom worth to HiLegal?"*
