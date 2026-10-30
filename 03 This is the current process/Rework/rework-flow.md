# The rework simulation — the flow, and what every result means

Companion to **`rework_simulation.py`**. If the results tables ever felt
opaque, this file fixes that: it shows how a request flows through the
simulated process, how the code is organized, and then reads every number in
plain language. It builds on the queue-section foundation
(`../queue_model.py` + `../queue_model-explained.md`): same units, same
one-team-as-one-unit idea — but simulating the **whole 12-step process**, not
just intake.

**How to run** (needs matplotlib, nothing else):

```
uv run rework_simulation.py
# or, in the project venv:
../../.venv/bin/python rework_simulation.py
```

Output: three console parts (each printed **with its own "how to read"
block**) and four transparent SVG charts written next to the script.

---

## The question and the one-paragraph answer

Rework looks like an *effort* problem ("another draft, another edit"). The
simulation asks what rework does to **lead time, work-in-process (WIP) and
capacity** — and the answer is that rework is mostly a *queue* problem:

> Going from "no rework" to the baseline (~90% of videos looping) adds
> **72 minutes of hands-on work but 9.7 days of lead time** — the queue cost
> is ~30× the work cost. WIP rises 6 → 12 → 20 videos and the capacity
> ceiling falls 27 → 24 → 21 videos/month. Rework doesn't just slow the
> queue; it **moves the wall closer**: demand that was manageable becomes a
> runaway backlog.

## The flow — one request through the simulated process

```
      Poisson arrivals λ = 17.5/month (random, like real requests)
                       │
                       ▼
   ┌────────────────────────────────────────────────────────┐
   │ 1  intake review · 15 min  ← first task: "intake wait"  │
   │    ends when a producer first touches the request       │
   └────────────────────────────────────────────────────────┘
                       │
   ┌────────────────────────────────────────────────────────┐
   │ 2  clarification  ── loop (p = 0.75 per round) ──┐      │
   │    wait U(1–2 wd) → 8 min reply → re-check ──────┘      │
   │    baseline mean = 1/(1−0.75) = 4 rounds [C]            │
   └────────────────────────────────────────────────────────┘
                       │
       3 content brief 45 · 4 script drafting 70 · 5 AI refinement 35
                       │
   ┌────────────────────────────────────────────────────────┐
   │ 6  script approval ── loop (p = 0.30) ──┐               │
   │    wait U(1–3 wd) → reject ⇒ 50 min rework + wait again │
   └────────────────────────────────────────────────────────┘
                       │
       7 video generation 55 · 8 audio 30 · 9 AV sync 140
                       │
   ┌────────────────────────────────────────────────────────┐
   │ 10 final approval ── loop (p = 0.30) ──┐                │
   │    wait U(1–3 wd) → reject ⇒ 70 min rework + wait again │
   └────────────────────────────────────────────────────────┘
                       │
       11 platform adaptation 95 · 12 delivery & admin 23
                       │
                       ▼
                 video delivered

  Producers: ONE shared task queue, 2 servers, no preemption — any free
  producer takes the next task. While a video waits at a gate, its producer
  works on other videos. Work minutes are converted at 480 × 0.67 ≈ 322
  effective minutes/producer-day (the same 67% dedication as queue_model).
```

The loop probabilities define the four scenarios:

| Scenario | p_clar | p_script | p_final | Mean clar rounds | Rework incidence |
|---|---:|---:|---:|---:|---:|
| no rework | 0 | 0 | 0 | 1 | 0% |
| rework halved | 0.50 | 0.15 | 0.15 | 2 | 63% |
| baseline | 0.75 | 0.30 | 0.30 | 4 [C] | 87% (~90% [E]) |
| heavy rework | 0.80 | 0.50 | 0.50 | 5 | 97% |

### Where the scenarios come from — and why #3 is *the* baseline

It's the **third** row that's the baseline (no rework → rework halved →
**baseline** → heavy) — and it's called the baseline because it's the
scenario **calibrated to reproduce HiLegal's process as it works today**,
using numbers the company reported. Nothing in it is a free guess; each
probability is solved from one company number:

#### Calculation 1 — p_clar = 0.75 comes from "≥ 4 clarification rounds" [C]

Each clarification round loops again with probability p, so the number of
rounds follows a geometric distribution with **mean = 1/(1−p)**. Set that
equal to the reported 4 rounds:

```
1/(1−p) = 4   →   1−p = 0.25   →   p = 0.75
```

#### Calculation 2 — p_script = p_final = 0.30 comes from "~10 h ≈ 600 min per video" [C]

The 12 tasks with no loops at all sum to **516 min**
(15+8+45+70+35+55+30+140+95+23). The loops add:

```
extra clarification replies : (4 rounds − 1) × 8 min          =  24.0 min
script rework               : 50 × 0.30/(1−0.30)             =  21.4 min
final rework                : 70 × 0.30/(1−0.30)             =  30.0 min
                                                             ─────────
total expected work         : 516 + 24 + 21.4 + 30           = 591 ≈ 600 [C]
```

(p/(1−p) is the expected number of loops per gate; each script loop costs
50 min, each final loop 70 min.) The two probabilities are set **equal**
because no data distinguishes script rejections from final ones — the
600-min anchor only constrains their *combined* minutes, and 0.30 lands on
it.

#### The two numbers that were *not* used for fitting (the proof)

- **Rework incidence:** with those p's, P(a video loops at least once)
  = 1 − (0.25 × 0.70 × 0.70) = **88%** (simulated 87%) — matches the ~90%
  estimate [E] as a consequence, not an input.
- **Lead time:** never fitted. Run the simulation with these probabilities
  and it produces **20.7 days**, inside the reported 14–28 [C]. That's the
  out-of-sample evidence this scenario *is* the current process.

So: **baseline = "today, in simulation"**. The other rows are defined
relative to it — no rework (all loops off, the ideal), rework halved
(roughly half the p's, what SLAs plausibly buy), heavy rework (a stress
case). This is the same fit-then-verify logic as μ = 23.5 in the intake
queue model: pin the knobs to reported numbers, keep one reported number
back to check against.

### Where the task minutes come from (the 516, and the loop costs)

The per-task minutes are **not** all company data — and it's worth saying so
out loud. HiLegal reports **one total: ~10 h ≈ 600 min per video including
rework [C]**, plus two individual steps. Everything else is our
decomposition of that total, anchored to the Section-3 walkthrough table
(`../START.md`):

| task | min | source |
|---|---:|---|
| AV sync | 140 | **[C]** company-reported 2–3 h → midpoint |
| platform adaptation | 95 | **[C]** company-reported ~2 h |
| intake review | 15 | [E] decomposition — producer triage, no data |
| clarification reply (per round) | 8 | [E] decomposition (trace: ~60 min total over 2–4 rounds) |
| content brief | 45 | [E] decomposition (trace: ~50 min) |
| script drafting | 70 | [E] decomposition (trace: ~80 min incl. redo rounds) |
| AI refinement | 35 | [E] decomposition (trace: ~40 min) |
| video generation | 55 | [E] decomposition (trace: ~60 min) |
| audio generation | 30 | [E] decomposition (trace: ~35 min) |
| delivery & admin | 23 | [E] residual — makes the first-time-right total consistent |
| script rework (per loop) | 50 | [E] estimate — one redraft pass |
| final rework (per loop) | 70 | [E] estimate — partial re-edit + re-sync |

The **hard constraint is the total**: first-time-right 516 + baseline loop
costs 75 ≈ 591 ≈ the reported 600 [C] (and the simulated baseline lands at
588). How that total is *split* across tasks is our estimate, shaped by the
trace table and slightly normalized — exactly what the parent audit trail
says: *"per-step minutes in the trace are [E] — our decomposition; sums to
the reported ~10 h; replace individual steps with time-log data if HiLegal
shares any."* When real time-logs arrive, put them in the `MIN` dict in the
script and every table and chart updates.

## How the code flows (three parts, mirroring `queue_model.py`)

| Block | What it does |
|---|---|
| `Parameters` | every number in one place: units, task minutes (`MIN`), gate waits, scenario probabilities |
| `expected_work()` | closed-form expected minutes per video — **audits the engine** against theory on every run |
| Engine (`Sim`, `Video`, `Owner`, `dispatch`, `video_steps`, `drive`) | the discrete-event machinery (below) |
| `run_scenario()` | simulate months of arrivals, then measure only videos arriving in a clean window |
| Part 1 — `part1_scenarios()` | four scenarios at λ = 17.5: results + how-to-read + engine check + calibration |
| Part 2 — `part2_sweep()` | 4 demand levels × 3 rework levels × 3 seeds; WIP series at 22/month |
| Part 3 — `part3_charts()` | four matplotlib SVGs, transparent background |

**The engine, one event at a time.** The simulation is a *discrete-event*
simulation: the clock never ticks through empty time — it jumps straight to
whatever happens next on a min-heap of scheduled events
`(time, sequence-number, callback)`.

1. **Arrival.** `arrival()` draws the next gap between requests from an
   exponential distribution (mean 22/λ working days) — that is the Poisson
   process. It creates a `Video`, parks it in the intake deque, starts that
   video's generator, and schedules the *next* arrival.
2. **The generator.** `video_steps()` is a Python generator yielding the
   flow diagram above one action at a time: `("work", minutes, label)` or
   `("wait", days, label)`. At each gate it draws `rng.random()`; a roll
   below p means the loop runs again. The rng call order is fixed, so any
   change to the step sequence changes the random stream — the numbers are
   exactly reproducible from the seeds.
3. **Executing one action (`drive`).** A *work* action goes to
   `request_work` → `dispatch`: the first free producer takes the task, and
   a `done` event is scheduled `minutes ÷ 322` working days later. A *wait*
   action is just a timer — its producer is free the entire time, which is
   what lets the two producers juggle several staggered videos.
4. **Cascade.** When a task finishes, its producer is marked free, the
   video's generator resumes at its next step, and `dispatch` runs again in
   case something is queued. That is the entire scheduler:
   work-conserving, first-come-first-served, no preemption — the same
   "team as one pooled unit" rule as the intake queue model.
5. **Measuring (`run_scenario`).** After the run, only videos *arriving*
   between month 10 (warm-up over) and month 25 (3-month cutoff, so no
   video is cut off by the horizon) enter the statistics: lead =
   `delivered − arrival` × 1.4 calendar days; intake wait = first touch −
   arrival; WIP = created − delivered, sampled twice per working day;
   utilization = busy producer-days ÷ available; capacity = 2 × 22 × 322 ÷
   mean work minutes.

Micro-example (one video, both producers free): a request arrives at
t = 100.0 wd. Its generator yields "intake review, 15 min" → `dispatch`
starts it instantly, done at t = 100.05. The generator resumes and yields
"clarification wait", drawn as 1.4 d → timer at 101.45, producers free
meanwhile. The gate roll comes up 0.61 < 0.75 → loop: another 8-min reply,
another wait. Next roll 0.93 ≥ 0.75 → escape after 2 rounds, on to the
brief. Every number in the tables is the average of thousands of such
lifetimes.

---

## Part 1 results — rework intensity (λ = 17.5/month)

| scenario | lead d | P90 d | work min | rework | cap/mo | util |
|---|---:|---:|---:|---:|---:|---:|
| no rework | **11.0** | 13.1 | 516 | 0% | 27.4 | 65% |
| rework halved | **14.0** | 20.6 | 548 | 63% | 25.8 | 67% |
| baseline | **20.7** | 32.0 | 588 | 87% | 24.0 | 72% |
| heavy rework | **28.8** | 47.8 | 684 | 97% | 20.7 | 78% |

**What each column means.** *lead d* = calendar days from request to
delivery. *P90* = 1 in 10 orders takes at least this long. *work min* =
hands-on producer minutes per video (company reports ~600 incl. rework [C]).
*cap/mo* = the ceiling implied by the work content: 2 producers × 22 d × 322
min ÷ work per video. *util* = share of the video-dedicated budget that is
busy (72% there ≈ 48% of paid hours).

**How to read it.** No rework → baseline: **+72 min of work (+14%) but +9.7
days of lead (+88%)**. Each loop does not just add its rework minutes — it
adds a fresh gate wait and another turn in the work queue, while holding the
video in the system (Little's Law: everything else waits behind it). Removing
rework cuts lead time **47%** while cutting work only **12%** — that gap is
the whole argument.

**Engine check (printed every run):** closed-form expected work vs simulated:
516/516, 545/548, 591/588, 668/684 min — the code implements the intended
model.

**Calibration (baseline vs company [C]):** lead 20.7 d inside 14–28 ✓ · work
588 min vs ~600 (−2%) ✓ · rework 87% vs ~90% [E] ✓ · capacity 24.0 vs demand
15–20 ✓.

## Part 2 results — rework × demand (lead days / mean WIP)

| λ | no rework | baseline | heavy rework |
|---:|---:|---:|---:|
| 15/mo | 10.7 d / 5.2 | 20.4 d / 9.7 | 26.6 d / 12.8 |
| 17.5/mo | 11.2 d / 6.2 | 22.3 d / 12.5 | 32.7 d / 20.4 |
| 20/mo | 11.8 d / 7.6 | 24.0 d / 15.8 | 45.8 d / 31.2 |
| 22/mo | 12.5 d / 8.9 | 30.7 d / 23.3 | **99.6 d / 71.8** ✗ |

**How each cell is calculated.** Every (demand, rework) pair is its own
simulation: 36 months of Poisson arrivals at that λ flow through that
scenario's loop probabilities — repeated with seeds 11, 12 and 13, then
averaged. Within one run, the **lead time** is the mean of
`delivered − arrival` (× 1.4 to calendar days) over every video that
*arrives* in the clean window (after 16 months of warm-up, ending 3 months
before the horizon so nobody is censored); the **WIP** number is the mean of
the created-minus-delivered count, sampled twice per working day. In total:
4 demand levels × 3 scenarios × 3 seeds = 36 runs of several hundred videos
each. The sweep uses longer runs than Part 1 (36 vs 28 months) because the
interesting cells are the near-capacity ones, where queues take a long time
to reach steady state.

**How to read it.** Each cell is mean lead time / mean videos-in-system.
Little's Law ties them: lead ≈ WIP ÷ throughput, so climbing WIP *is*
climbing waits. Without rework the process absorbs 22/month comfortably.
Baseline rework degrades steeply past 20 (WIP 16 → 23). Heavy rework at
22/month — a level the company wants to reach — is **past capacity**: WIP
≈ 72 and lead ≈ 100 days, growing without bound. The ceiling is not a
property of the team; it is a property of **the team plus its rework**
(compare the calculated ceiling in `../queue_model-explained.md`).

## The four charts

| File | What it shows | When to show it |
|---|---|---|
| `rework-impact.svg` | left: mean lead bars with whiskers up to P90 (both labelled); right: work minutes per video with rework incidence, company 600-min baseline marked | the headline — "rework costs ~10 days for ~1 hour of work" |
| `queue-sample-path.svg` | WIP over 22 simulated months at 22/month: flat (no rework) → climbing (baseline) → runaway (heavy) | the backlog forming in real time |
| `rework-vs-demand.svg` | mean WIP vs demand for the three levels; the heavy curve blows up at 22 | "can we just push more volume?" — no, not with this rework |
| `gantt-rework.svg` | two median orders as coloured timelines: green work, dark-red rework, red/gold gate waits, grey elapsed | the walkthrough — most of the extra time is repeated *waiting*, not extra work |

## Model card (say these on purpose)

1. **Pooled, work-conserving team** — idle producers grab queued work
   instantly, so the simulated **intake wait is a lower bound** (~0.1–0.2 d);
   the real 3–7-day intake queue is modeled separately in `../queue_model.py`.
2. **Loop probabilities are fixed** — the congestion → rushed review → more
   rework feedback loop is *not* modeled; real results are likely worse.
3. **Stochastic, seeded** — scenario table is single-seed (±5–10% run-to-run);
   the sweep averages 3 seeds. Treat differences under ~2 days as noise.
4. **Heavy rework is a stress scenario**, not a forecast — P90 = 47.8 d means
   "the queue is out of control", not "this lawyer will wait 48 days".
5. **Two undifferentiated producers**, no skills or hand-offs; 67% dedication
   is an assumption [E] shared with the queue model.
6. **Per-task minutes are our decomposition [E]** — only the ~10 h total,
   AV sync (2–3 h) and platform adaptation (~2 h) are company-reported [C];
   the split across the remaining tasks is estimated against that total
   (see "Where the task minutes come from"). Swap real time-log values into
   `MIN` when HiLegal shares any.

## The one line to remember

> "Rework adds an hour of work and ten days of waiting — and it moves the
> capacity wall from 27 down to 21 videos a month. Kill the loops, not the
> overtime."
