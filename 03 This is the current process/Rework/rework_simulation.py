#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib"]
# ///
"""
rework_simulation.py — rework and the queue: whole-process simulation
=====================================================================
Section 3 annex, "Rework" (Operations Management project, HiLegal).
Builds on the intake-queue model in ../queue_model.py (same units, same
one-team-as-one-unit idea) — but simulates the WHOLE 12-step process.

Question: rework looks like "a bit of extra work" (a redraft, a re-edit).
What does it actually do to LEAD TIME, WORK-IN-PROCESS and CAPACITY?

One-paragraph answer (baseline vs no rework, same demand 17.5/month):
rework adds ≈ 72 minutes of hands-on work but ≈ 9.7 days of lead time —
the queue cost is ~30× the work cost.  WIP rises 6 → 12 → 20 videos and the
effective capacity ceiling falls 27 → 24 → 21 videos/month (no rework →
baseline → heavy rework).  Rework does not just slow the queue; it lowers
the demand level at which the queue explodes.

Model (discrete-event simulation):
  * Poisson arrivals at demand λ (videos/month, working-day clock).
  * Two producers = ONE pooled task queue: any free producer takes the next
    task; tasks are never preempted (no preemption, as in the queue model).
  * Each video flows through the 12 steps as work tasks (producer busy)
    alternating with client-gate waits (producer free for other videos).
  * Three looping gates: clarification (loops to another round), script
    approval (loops to a 50-min rework), final approval (loops to a 70-min
    rework).  Loop probabilities define the four scenarios.
  * Work durations in effective minutes: 480 × 0.67 ≈ 322 min/producer-day
    (producers also do platform work) — the same dedication as queue_model.
  * Work-conserving dispatch ⇒ the simulated intake wait is a LOWER BOUND;
    the real 3–7-day intake queue is modeled separately (../queue_model.py).

The script, in three parts (run in order by main()):
  Part 1  Four rework scenarios at fixed demand — table + engine check +
          calibration against company-reported values [C]
  Part 2  Rework × demand sweep — mean WIP and lead time per (λ, scenario),
          plus the WIP time series at 22/month that feeds the queue chart
  Part 3  Four SVG charts (matplotlib, transparent background):
            rework-impact.svg · queue-sample-path.svg
            rework-vs-demand.svg · gantt-rework.svg

Run:      uv run rework_simulation.py
      or  ../.venv/bin/python rework_simulation.py
Output:   console tables (each with a "how to read" block) + the four SVGs.
"""

from __future__ import annotations

import heapq
import os
import random
import statistics
from collections import deque
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.patches import Patch

# ----------------------------------------------------------------------
# Parameters — the single source of truth.
# ----------------------------------------------------------------------
WD_MONTH = 22.0                       # working days per month
CAL = 30.4 / 21.7                     # calendar days per working day ≈ 1.40
DEDICATION = 0.67                     # share of paid time available for videos
MIN_PER_DAY = 480 * DEDICATION        # ≈ 322 effective producer-minutes/day

MONTHS = 28                           # horizon of a scenario run
WARMUP_MONTHS = 10                    # discarded (pipeline starts empty)
CUTOFF_MONTHS = 3                     # excluded at the end (censoring guard)
LAMBDA = 17.5                         # demand, videos/month [C]

OUT_DIR = Path(__file__).resolve().parent
PNG_DIR = os.environ.get("Q_PNG_DIR")  # optional: also write PNG previews

# Hands-on minutes per task — the first-time-right process sums to 516 min
# (company reports ~10 h ≈ 600 min including rework [C]; the loops add the
# rest, see expected_work()).
MIN = {
    "intake review": 15, "clarification reply": 8, "content brief": 45,
    "script drafting": 70, "ai refinement": 35, "script rework": 50,
    "video generation": 55, "audio generation": 30, "av sync": 140,
    "final rework": 70, "platform adaptation": 95, "delivery & admin": 23,
}
CLAR_WAIT = (1.0, 2.0)                # clarification gate wait, working days
GATE_WAIT = (1.0, 3.0)                # script/final approval waits, working days

# Loop probability per review round → scenario = rework intensity.
# Expected clarification rounds = 1/(1−p_clar): 0.75 → 4 rounds [C].
SCENARIOS = [
    ("no rework",       dict(p_clar=0.00, p_script=0.00, p_final=0.00)),
    ("rework halved",   dict(p_clar=0.50, p_script=0.15, p_final=0.15)),
    ("baseline",        dict(p_clar=0.75, p_script=0.30, p_final=0.30)),
    ("heavy rework",    dict(p_clar=0.80, p_script=0.50, p_final=0.50)),
]

NAVY, GOLD, RED, GREEN, GREY = ("#0F2A43", "#C9A227", "#C62828", "#2E7D32",
                                "#9AA5B1")
DARKRED, SLATE = "#7B1F1F", "#5C7A99"


def expected_work(p: dict) -> float:
    """Closed-form expected hands-on minutes — audits the engine:
    E[work] = first-time-right + extra rounds/loops, each a geometric mean."""
    return (MIN["intake review"]
            + MIN["clarification reply"] / (1 - p["p_clar"])
            + MIN["content brief"] + MIN["script drafting"] + MIN["ai refinement"]
            + MIN["script rework"] * p["p_script"] / (1 - p["p_script"])
            + MIN["video generation"] + MIN["audio generation"] + MIN["av sync"]
            + MIN["final rework"] * p["p_final"] / (1 - p["p_final"])
            + MIN["platform adaptation"] + MIN["delivery & admin"])


def hr(title: str) -> None:
    print("\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78)


# ----------------------------------------------------------------------
# Simulation engine — event heap + pooled producers.  (The logic here is
# behaviour-identical to the version the published numbers came from;
# only names, constants and output were reorganized.)
# ----------------------------------------------------------------------
class Sim:
    def __init__(self, params, lam_per_month, seed=7):
        self.t = 0.0
        self.events = []                        # min-heap of (time, seq, fn)
        self.seq = 0
        self.rng = random.Random(seed)
        self.params = params
        self.lam_wd = lam_per_month / WD_MONTH
        self.intake = deque()                   # requests not yet picked up
        self.work_queue = deque()               # work tasks waiting for a producer
        self.finished = []
        self.series = []                        # (t, intake_len, wip) samples
        self.next_vid = 0
        self.owners = []

    def schedule(self, delay, fn):
        self.seq += 1
        heapq.heappush(self.events, (self.t + delay, self.seq, fn))

    def run(self, until):
        while self.events and self.events[0][0] <= until:
            t, _, fn = heapq.heappop(self.events)
            self.t = t
            fn()


class Video:
    __slots__ = ("vid", "arrival", "first_work", "delivered", "work",
                 "clar_rounds", "script_loops", "final_loops", "segments")

    def __init__(self, vid, arrival):
        self.vid = vid
        self.arrival = arrival
        self.first_work = None                  # when a producer first touches it
        self.delivered = None
        self.work = 0.0                         # hands-on minutes
        self.clar_rounds = 0
        self.script_loops = 0
        self.final_loops = 0
        self.segments = []                      # (start, end, label, kind)


class Owner:
    def __init__(self):
        self.busy = False
        self.busy_days = 0.0


def dispatch(sim):
    """Start queued work on any free producer (work-conserving)."""
    while sim.work_queue:
        owner = next((o for o in sim.owners if not o.busy), None)
        if owner is None:
            return
        minutes, video, label, cb = sim.work_queue.popleft()
        owner.busy = True
        dur = minutes / MIN_PER_DAY
        owner.busy_days += dur
        video.segments.append((sim.t, sim.t + dur, label, "work"))
        if label == "intake review" and video.first_work is None:
            video.first_work = sim.t
            if video in sim.intake:
                sim.intake.remove(video)

        def done(o=owner, callback=cb):
            o.busy = False
            callback()
            dispatch(sim)

        sim.schedule(dur, done)


def request_work(sim, minutes, video, label, cb):
    sim.work_queue.append((minutes, video, label, cb))
    dispatch(sim)


# ----------------------------------------------------------------------
# One video through the 12 steps — a generator yielding work/wait actions.
# rng call order is part of the model; keep it stable.
# ----------------------------------------------------------------------
def video_steps(sim, video, p):
    def work(label):
        return ("work", MIN[label], label)

    def wait(days, label):
        return ("wait", days, label)

    yield work("intake review")
    while True:
        video.clar_rounds += 1
        yield wait(sim.rng.uniform(*CLAR_WAIT), "clarification wait")
        yield work("clarification reply")
        if sim.rng.random() >= p["p_clar"]:
            break

    yield work("content brief")
    yield work("script drafting")
    yield work("ai refinement")
    while True:
        yield wait(sim.rng.uniform(*GATE_WAIT), "script approval")
        if sim.rng.random() >= p["p_script"]:
            break
        video.script_loops += 1
        yield work("script rework")

    yield work("video generation")
    yield work("audio generation")
    yield work("av sync")
    while True:
        yield wait(sim.rng.uniform(*GATE_WAIT), "final approval")
        if sim.rng.random() >= p["p_final"]:
            break
        video.final_loops += 1
        yield work("final rework")

    yield work("platform adaptation")
    yield work("delivery & admin")


def drive(sim, video, gen):
    """Execute the next action of a video's generator; deliver when done."""
    try:
        act = next(gen)
    except StopIteration:
        video.delivered = sim.t
        sim.finished.append(video)
        return
    if act[0] == "work":
        _, minutes, label = act
        video.work += minutes
        request_work(sim, minutes, video, label,
                     lambda: drive(sim, video, gen))
    else:
        _, days, label = act
        video.segments.append((sim.t, sim.t + days, label, "wait"))
        sim.schedule(days, lambda: drive(sim, video, gen))


# ----------------------------------------------------------------------
# Scenario runner — simulate, then measure over a clean window.
# ----------------------------------------------------------------------
def run_scenario(name, params, lam=LAMBDA, months=MONTHS, seed=7,
                 warmup=WARMUP_MONTHS):
    sim = Sim(params, lam, seed)
    sim.owners = [Owner(), Owner()]

    def arrival():
        v = Video(sim.next_vid, sim.t)
        sim.next_vid += 1
        sim.intake.append(v)
        drive(sim, v, video_steps(sim, v, params))
        sim.schedule(sim.rng.expovariate(sim.lam_wd), arrival)

    def log():
        sim.series.append((sim.t, len(sim.intake),
                           sim.next_vid - len(sim.finished)))
        sim.schedule(0.5, log)

    sim.schedule(0.0, arrival)
    log()
    sim.run(months * WD_MONTH)

    # measure only videos that ARRIVE inside the clean window: after warm-up
    # (empty-start transient) and before the cutoff (undelivered at horizon)
    t0 = warmup * WD_MONTH
    cutoff = months * WD_MONTH - CUTOFF_MONTHS * WD_MONTH
    window = [v for v in sim.finished
              if t0 <= v.arrival <= cutoff and v.delivered is not None]
    window_months = months - warmup - CUTOFF_MONTHS

    leads = [(v.delivered - v.arrival) * CAL for v in window]
    intake_waits = [((v.first_work or v.arrival) - v.arrival) * CAL
                    for v in window]
    works = [v.work for v in window]
    loops = [1 if (v.clar_rounds > 1 or v.script_loops or v.final_loops) else 0
             for v in window]
    util = sum(o.busy_days for o in sim.owners) / (2 * months * WD_MONTH)

    series = [(t, wip) for (t, _q, wip) in sim.series if t >= t0]

    return dict(
        name=name, leads=leads, intake_waits=intake_waits, works=works,
        loops=loops, util=util,
        mean_wip=statistics.mean([w for _, w in series]) if series else float("nan"),
        capacity=(2 * WD_MONTH * MIN_PER_DAY / statistics.mean(works)
                  if works else float("nan")),
        throughput=len(window) / window_months,
        mean_lead=statistics.mean(leads) if leads else float("nan"),
        p90_lead=(sorted(leads)[int(0.9 * len(leads))] if leads else float("nan")),
        mean_wait=statistics.mean(intake_waits) if intake_waits else float("nan"),
        mean_work=statistics.mean(works) if works else float("nan"),
        rework_share=statistics.mean(loops) if loops else float("nan"),
        series=series, videos=window,
    )


# ======================================================================
# PART 1 — four rework scenarios at fixed demand
# ======================================================================
def part1_scenarios() -> list:
    hr(f"PART 1 · REWORK INTENSITY — demand λ = {LAMBDA}/month, "
       f"2 producers, {MONTHS} simulated months")

    results = [run_scenario(name, params) for name, params in SCENARIOS]

    print(f"  {'scenario':<16}{'lead d':>8}{'P90 d':>8}{'intake d':>10}"
          f"{'work min':>10}{'rework':>8}{'cap/mo':>8}{'util':>7}")
    for r in results:
        print(f"{r['name']:<18}{r['mean_lead']:>8.1f}{r['p90_lead']:>8.1f}"
              f"{r['mean_wait']:>10.1f}{r['mean_work']:>10.0f}"
              f"{r['rework_share']:>7.0%}{r['capacity']:>8.1f}"
              f"{r['util']:>7.0%}")

    base = next(r for r in results if r["name"] == "baseline")
    no = next(r for r in results if r["name"] == "no rework")
    print(f"""
how to read the table
  lead d      calendar days from lawyer request to delivered video
  P90 d       1 in 10 orders takes at least this long
  intake d    wait before first touch (lower bound — see model notes)
  work min    hands-on producer minutes per video (company: ~600 incl.
              rework [C])
  cap/mo      capacity ceiling = 2 × 22 × {MIN_PER_DAY:.0f} min ÷ work per video
  util        share of the video-dedicated budget that is busy
              ({base['util']:.0%} there ≈ {base['util'] * DEDICATION:.0%} of paid hours)

what the numbers say
  * no rework → baseline: +{base['mean_work'] - no['mean_work']:.0f} min of work
    (+{base['mean_work'] / no['mean_work'] - 1:.0%}) but
    +{base['mean_lead'] - no['mean_lead']:.1f} days of lead time
    (+{base['mean_lead'] / no['mean_lead'] - 1:.0%})""")
    work_cost_cal = (base["mean_work"] - no["mean_work"]) / MIN_PER_DAY * CAL
    print(f"  * the queue cost of rework is "
          f"~{(base['mean_lead'] - no['mean_lead']) / work_cost_cal:.0f}× its"
          f" work cost ({base['mean_lead'] - no['mean_lead']:.1f} d of waiting"
          f" vs {work_cost_cal:.1f} d of extra work)")
    print(f"  * removing rework cuts lead time "
          f"{1 - no['mean_lead'] / base['mean_lead']:.0%} while cutting work"
          f" only {1 - no['mean_work'] / base['mean_work']:.0%}")

    print("\nengine check — closed-form expected work vs simulated:")
    for (name, params), r in zip(SCENARIOS, results):
        ok = "  ✓" if abs(r["mean_work"] - expected_work(params)) <= 20 else "  ✗"
        print(f"  {name:<16}{expected_work(params):>7.0f} min formula"
              f"{r['mean_work']:>8.0f} min simulated{ok}")

    print(f"""
calibration (baseline vs company-reported [C])
  lead time     {base['mean_lead']:.1f} d    vs 14–28 d [C]      ✓ inside
  hands-on work {base['mean_work']:.0f} min vs ~600 min [C]     ✓ {base['mean_work'] / 600 - 1:+.0%}
  rework share  {base['rework_share']:.0%}     vs ~90% [E]         ✓
  capacity      {base['capacity']:.1f}/mo vs demand 15–20 [C] ✓ headroom""")
    return results


# ======================================================================
# PART 2 — rework × demand: the sweep and the wall
# ======================================================================
def part2_sweep():
    hr("PART 2 · REWORK × DEMAND — mean lead days / mean WIP, 3 seeds each")

    lambdas = [15.0, 17.5, 20.0, 22.0]
    levels = [("no rework", SCENARIOS[0][1]),
              ("baseline", SCENARIOS[2][1]),
              ("heavy rework", SCENARIOS[3][1])]

    print(f"  {'λ':>5}" + "".join(f"{n:>20}" for n, _ in levels))
    sweep = {}
    for lam in lambdas:
        row = []
        for name, params in levels:
            runs = [run_scenario(name, params, lam=lam, months=36, warmup=16,
                                 seed=s) for s in (11, 12, 13)]
            row.append((statistics.mean(r["mean_lead"] for r in runs),
                        statistics.mean(r["mean_wip"] for r in runs)))
        sweep[lam] = row
        print(f"{lam:>5.1f}" + "".join(f"{a:>11.1f} d /{b:>6.1f}"
                                       for a, b in row))
    print("""
how to read the table
  cell = mean lead time / mean videos-in-system (WIP) at that demand
  Little's Law: lead time ≈ WIP ÷ throughput — when WIP climbs, waits climb
  the sweep reports WIP (not only lead) because an unstable queue shows up
  honestly in WIP: it keeps growing while censored lead times look tame

what the numbers say
  * without rework the process absorbs 22/month (WIP ≈ 9, lead ≈ 12 d)
  * baseline rework degrades steeply past 20/month (WIP 16 → 23)
  * heavy rework at 22/month is PAST CAPACITY: WIP ≈ 72 and lead ≈ 100 d —
    the backlog grows without bound; no amount of effort drains it""")

    # WIP time series at 22/month for the queue chart
    queue_runs = [run_scenario(name, params, lam=22.0, months=36, warmup=14,
                               seed=13)
                  for name, params in levels]
    return lambdas, levels, sweep, queue_runs


# ======================================================================
# PART 3 — charts (matplotlib → four SVGs, transparent background)
# ======================================================================
def _save(fig: plt.Figure, name: str) -> None:
    """Save with a transparent background (for slides) — no white box."""
    fig.patch.set_alpha(0.0)
    for ax in fig.axes:
        ax.set_facecolor("none")
    path = OUT_DIR / name
    fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
    if PNG_DIR:
        fig.savefig(Path(PNG_DIR) / name.replace(".svg", ".png"), dpi=110,
                    transparent=True)
    plt.close(fig)
    print(f"  wrote {path.name}")


SCEN_COLORS = [GREY, GREEN, GOLD, RED]


def short(name: str) -> str:
    return name.replace(" (~90% rework)", "")


# Value labels: one consistent colour (black) with a thin white halo, so it
# stays readable on every bar fill and on any slide background.
LABEL_COLOR = "black"
LABEL_HALO = [patheffects.withStroke(linewidth=2.5, foreground="white")]


def chart_impact(results) -> None:
    """Left: mean lead + P90 per scenario. Right: hands-on work per video."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 5.2),
                                   width_ratios=(1.05, 1.0))
    fig.subplots_adjust(top=0.85, wspace=0.5)   # room for the right panel's labels
    ymax = max(r["p90_lead"] for r in results) * 1.15
    for i, r in enumerate(results):
        ax1.bar(i, r["mean_lead"], width=0.55, color=SCEN_COLORS[i], zorder=3)
        # whisker from the bar top up to P90, capped and labelled
        ax1.vlines(i, r["mean_lead"], r["p90_lead"], color=DARKRED, lw=2.0,
                   zorder=4)
        ax1.hlines(r["p90_lead"], i - 0.14, i + 0.14, color=DARKRED, lw=2.8,
                   zorder=4)
        ax1.text(i, r["mean_lead"] - ymax * 0.03, f"mean {r['mean_lead']:.1f}",
                 ha="center", va="top", color=LABEL_COLOR, fontsize=10,
                 weight="bold", zorder=5, path_effects=LABEL_HALO)
        ax1.text(i, r["p90_lead"] + ymax * 0.012, f"P90 {r['p90_lead']:.1f}",
                 ha="center", va="bottom", color=DARKRED, fontsize=9.5,
                 weight="bold", zorder=5)
    ax1.set_xticks(range(len(results)))
    ax1.set_xticklabels([short(r["name"]) for r in results], fontsize=10)
    ax1.set_ylim(0, ymax)
    ax1.set_ylabel("lead time (calendar days)")
    ax1.set_title("bar = mean · whisker = P90 (1 in 10 orders)", fontsize=10,
                  color="#555")
    ax1.grid(axis="y", color="#E3E6EA", lw=0.8)

    for i, r in enumerate(results):
        y = len(results) - 1 - i
        ax2.barh(y, r["mean_work"], height=0.6, color=SCEN_COLORS[i], zorder=3)
        ax2.text(r["mean_work"] - 12, y,
                 f"{r['mean_work']:.0f} min · rework {r['rework_share']:.0%}",
                 ha="right", va="center", color=LABEL_COLOR, fontsize=10,
                 weight="bold", path_effects=LABEL_HALO)
    ax2.set_yticks(range(len(results)))
    ax2.set_yticklabels([short(r["name"]) for r in reversed(results)],
                        fontsize=10)
    ax2.set_xlim(0, 720)
    ax2.axvline(600, color="#666", ls=":", lw=1.6, zorder=2)
    ax2.text(600, len(results) - 0.35, " company baseline ≈ 600 min [C]",
             fontsize=9, color="#555", va="center")
    ax2.set_xlabel("hands-on work per video (minutes)")
    ax2.grid(axis="x", color="#E3E6EA", lw=0.8)

    fig.suptitle("Rework: a little extra work, a lot of extra waiting "
                 "(same team, same demand)", weight="bold")
    _save(fig, "rework-impact.svg")


def _smooth(vals, k=4):
    return [sum(vals[max(0, i - k):min(len(vals), i + k + 1)])
            / (min(len(vals), i + k + 1) - max(0, i - k))
            for i in range(len(vals))]


def chart_queue_path(queue_runs) -> None:
    """WIP over time at 22/month — flat / climbing / runaway."""
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    colors = [GREEN, GOLD, RED]
    for r, color in zip(queue_runs, colors):
        series = r["series"]
        t0 = series[0][0]
        months_x = [(t - t0) / WD_MONTH for t, _ in series]
        ax.plot(months_x, _smooth([w for _, w in series]), color=color,
                lw=2.2, label=short(r["name"]))
    n_months = (queue_runs[0]["series"][-1][0]
                - queue_runs[0]["series"][0][0]) / WD_MONTH
    ax.set_xlabel(f"months into the {n_months:.0f}-month window "
                  "(sampled twice per working day, smoothed)")
    ax.set_ylabel("videos in the system (WIP)")
    ax.set_title("Videos in the system at 22/month — rework builds a backlog",
                 weight="bold")
    ax.legend(frameon=False, fontsize=10)
    ax.grid(axis="y", color="#E3E6EA", lw=0.8)
    _save(fig, "queue-sample-path.svg")


def chart_sweep(lambdas, levels, sweep) -> None:
    """Mean WIP vs demand — each rework level has its own breaking point."""
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    colors = [GREEN, GOLD, RED]
    for j, (name, _) in enumerate(levels):
        ys = [sweep[lam][j][1] for lam in lambdas]
        ax.plot(lambdas, ys, "o-", color=colors[j], lw=2.6, ms=6,
                label=name)
    ax.annotate("past capacity:\nWIP ≈ 72 · lead ≈ 100 d",
                xy=(22.0, sweep[22.0][2][1]), xytext=(19.0, 62),
                fontsize=10, color=RED, weight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.set_xlabel("demand λ (videos/month) — same two producers")
    ax.set_ylabel("mean videos in the system (WIP)")
    ax.set_title("Rework × demand: where work-in-process explodes",
                 weight="bold")
    ax.legend(frameon=False, fontsize=10)
    ax.grid(axis="y", color="#E3E6EA", lw=0.8)
    _save(fig, "rework-vs-demand.svg")


def chart_gantt(results) -> None:
    """Two median orders — first-time-right vs baseline with loops."""
    base = next(r for r in results if r["name"] == "baseline")
    no = next(r for r in results if r["name"] == "no rework")

    def pick(r):
        vids = sorted(r["videos"], key=lambda v: v.delivered - v.arrival)
        return vids[len(vids) // 2]

    rows = [("first-time-right (no rework)", pick(no), 1),
            ("with rework (baseline)", pick(base), 0)]
    fig, ax = plt.subplots(figsize=(11.0, 4.4))
    tmax = max((v.delivered - v.arrival) * CAL for _, v, _ in rows) + 2

    for label, v, y in rows:
        lead = (v.delivered - v.arrival) * CAL
        ax.barh(y, lead, height=0.52, color="#ECEFF3", zorder=1)  # elapsed
        intake = ((v.first_work or v.arrival) - v.arrival) * CAL
        ax.barh(y, intake, height=0.52, color=SLATE, zorder=3)
        if intake > 2:
            ax.text(intake / 2, y, "intake", ha="center", va="center",
                    fontsize=8.5, color="white", weight="bold")
        for (s, e, lab, kind) in v.segments:
            x = (s - v.arrival) * CAL
            w = (e - s) * CAL
            if kind == "work":
                color = DARKRED if "rework" in lab else GREEN
            else:
                color = GOLD if "clarification" in lab else RED
            ax.barh(y, max(w, 0.15), left=x, height=0.52, color=color,
                    zorder=4)

    ax.set_yticks([y for _, _, y in rows])
    ax.set_yticklabels([l for l, _, _ in rows], fontsize=11)
    for d in range(0, int(tmax) + 1, 5):
        ax.axvline(d, color="#E3E6EA", lw=0.8, zorder=0)
    ax.set_xlim(0, tmax)
    ax.set_xlabel("calendar days since request")
    ax.set_title("One order, two worlds — where rework time actually goes",
                 weight="bold")
    handles = [Patch(facecolor=c, label=l) for l, c in
               (("active work", GREEN), ("rework (extra work)", DARKRED),
                ("approval wait", RED), ("clarification wait", GOLD),
                ("intake queue", SLATE), ("total elapsed (grey)", "#ECEFF3"))]
    ax.legend(handles=handles, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, -0.18), frameon=False, fontsize=9)
    _save(fig, "gantt-rework.svg")


def part3_charts(results, sweep_data) -> None:
    hr("PART 3 · CHARTS → four SVGs, transparent background, next to script")
    lambdas, levels, sweep, queue_runs = sweep_data
    chart_impact(results)
    chart_queue_path(queue_runs)
    chart_sweep(lambdas, levels, sweep)
    chart_gantt(results)


def main() -> None:
    results = part1_scenarios()
    sweep_data = part2_sweep()
    part3_charts(results, sweep_data)
    print("\nDONE. Slide use: rework-impact.svg → the headline (queue cost ≈ 30×"
          " work cost) · queue-sample-path.svg → the backlog forming ·"
          " rework-vs-demand.svg → the moving capacity wall ·"
          " gantt-rework.svg → one order with vs. without loops\n")


if __name__ == "__main__":
    main()
