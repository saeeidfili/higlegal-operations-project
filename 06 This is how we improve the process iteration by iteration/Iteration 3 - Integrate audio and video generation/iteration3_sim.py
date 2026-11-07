#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
iteration3_sim.py — Iteration 3 (single-render avatar pipeline) simulated
==========================================================================
A modified copy of ../Iteration 2/iteration2_sim.py (same engine lineage:
event heap, two pooled producers, no preemption — Section 4 study).

What changed vs Iteration 2's config:
  * Video + audio generation, manual sync, and platform adaptation are
    DELETED — one automated render (machine time, producers free) emits
    all variants. Modelled as a machine wait U(0.1–0.5) wd + a 25-min
    human render-QA pass (20 min checklist + ~5 min retry allowance).
  * The serial final approval is REPLACED by auto-delivery with a 24 h
    objection window running in PARALLEL: no blocking wait; an objection
    (prob p_final) triggers a scene re-render + re-QA (15 min) inside the
    window.
  * Only one serial client gate remains: script approval, U(0.25–1.0) wd.

Iteration-3 loop probabilities, solved the Section-4 way (two anchors):
  * rework incidence 1−(1−ps)(1−pf) = 10%  (kpi-data §5 target)
  * pf = 2·ps → (1−s)(1−2s) = 0.90 → s = (3−√8.2)/4 ≈ 0.034
  * E[work] = 60 FTR + 10·ps/(1−ps) + 15·pf/(1−pf) ≈ 61.5 ≈ 60 min [T]

Outputs: sanity check (baseline/Iter1/Iter2 reproduced), the four-rung
ladder at λ=17.5, demand sweep → practical capacity (highest λ with mean
lead ≤ 28 d), script-approval SLA sensitivity.

Run:  ../../.venv/bin/python iteration3_sim.py   (or: python3 — stdlib only)
"""

from __future__ import annotations

import heapq
import random
import statistics
from collections import deque
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from simulation_metrics import measure

# ----------------------------------------------------------------------
# Shared constants — identical across the simulation lineage.
# ----------------------------------------------------------------------
WD_MONTH = 22.0
CAL = 30.4 / 22.0
DEDICATION = 0.67
MIN_PER_DAY = 480 * DEDICATION
BUDGET_MIN = 2 * WD_MONTH * MIN_PER_DAY   # ≈ 14,150 min/month (67% budget)

MONTHS = 28
WARMUP_MONTHS = 10
CUTOFF_MONTHS = 3
LAMBDA = 17.5

BASE_MIN = {
    "intake review": 15, "clarification reply": 8, "content brief": 45,
    "script drafting": 70, "ai refinement": 35, "script rework": 50,
    "video generation": 55, "audio generation": 30, "av sync": 140,
    "final rework": 70, "platform adaptation": 95, "delivery & admin": 23,
}
ITER1_MIN = {
    "brief review": 10, "script drafting": 50, "script editing": 22,
    "script rework": 25, "video generation": 60, "audio generation": 35,
    "av sync": 130, "final rework": 35, "platform adaptation": 85,
    "delivery & admin": 10,
}
ITER2_MIN = {
    "brief review": 15, "ai param & gen check": 5, "script editing": 25,
    "script rework": 10, "video generation": 45, "audio generation": 25,
    "av sync": 134, "final rework": 35, "platform adaptation": 80,
    "delivery & admin": 10,
}
ITER3_MIN = {  # FTR 60: the manual bottom is deleted; QC remains
    "brief exceptions": 10, "ai param check": 5, "script editing": 15,
    "script rework": 10,                      # regenerate one scene
    "render QA": 25,                          # checklist 20 + retries ~5
    "objection re-render": 15,                # scene re-render + re-QA
    "delivery & admin": 5,
}

CONFIGS = {
    "baseline": dict(
        flow="baseline", minutes=BASE_MIN,
        clar_wait=(1.0, 2.0), gate_wait=(1.0, 3.0),
        p_clar=0.75, p_script=0.20, p_final=0.40),
    "iteration 1": dict(
        flow="iter1", minutes=ITER1_MIN,
        clar_wait=None, gate_wait=(0.5, 1.5),
        p_clar=0.00, p_script=0.214, p_final=0.428),
    "iteration 2": dict(
        flow="iter2", minutes=ITER2_MIN,
        clar_wait=None, gate_wait=(0.25, 1.0),
        p_clar=0.00, p_script=0.108, p_final=0.216),
    "iteration 3": dict(
        flow="iter3", minutes=ITER3_MIN,
        clar_wait=None, gate_wait=(0.25, 1.0),   # script approval only
        render_wait=(0.1, 0.5),                  # machine render, producers free
        p_clar=0.00, p_script=0.034, p_final=0.068),
    "iteration 3 · slow lawyer": dict(
        flow="iter3", minutes=ITER3_MIN,
        clar_wait=None, gate_wait=(0.5, 1.5),    # rides the 48 h SLA cap
        render_wait=(0.1, 0.5),
        p_clar=0.00, p_script=0.034, p_final=0.068),
}


def expected_work(cfg: dict) -> float:
    m, p = cfg["minutes"], cfg
    if cfg["flow"] == "baseline":
        return (m["intake review"]
                + m["clarification reply"] / (1 - p["p_clar"])
                + m["content brief"] + m["script drafting"] + m["ai refinement"]
                + m["script rework"] * p["p_script"] / (1 - p["p_script"])
                + m["video generation"] + m["audio generation"] + m["av sync"]
                + m["final rework"] * p["p_final"] / (1 - p["p_final"])
                + m["platform adaptation"] + m["delivery & admin"])
    if cfg["flow"] == "iter1":
        return (m["brief review"] + m["script drafting"] + m["script editing"]
                + m["script rework"] * p["p_script"] / (1 - p["p_script"])
                + m["video generation"] + m["audio generation"] + m["av sync"]
                + m["final rework"] * p["p_final"] / (1 - p["p_final"])
                + m["platform adaptation"] + m["delivery & admin"])
    if cfg["flow"] == "iter2":
        return (m["brief review"] + m["ai param & gen check"] + m["script editing"]
                + m["script rework"] * p["p_script"] / (1 - p["p_script"])
                + m["video generation"] + m["audio generation"] + m["av sync"]
                + m["final rework"] * p["p_final"] / (1 - p["p_final"])
                + m["platform adaptation"] + m["delivery & admin"])
    return (m["brief exceptions"] + m["ai param check"] + m["script editing"]
            + m["script rework"] * p["p_script"] / (1 - p["p_script"])
            + m["render QA"]
            + m["objection re-render"] * p["p_final"] / (1 - p["p_final"])
            + m["delivery & admin"])


def expected_incidence(cfg: dict) -> float:
    if cfg["flow"] == "baseline":
        return 1 - ((1 - cfg["p_clar"]) * (1 - cfg["p_script"])
                    * (1 - cfg["p_final"]))
    return 1 - (1 - cfg["p_script"]) * (1 - cfg["p_final"])


def hr(title: str) -> None:
    print("\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78)


# ----------------------------------------------------------------------
# Engine — behaviour-identical to rework_simulation.py.
# ----------------------------------------------------------------------
class Sim:
    def __init__(self, cfg, lam_per_month, seed=7):
        self.t = 0.0
        self.events = []
        self.seq = 0
        self.rng = random.Random(seed)
        self.cfg = cfg
        self.lam_wd = lam_per_month / WD_MONTH
        self.intake = deque()
        self.work_queue = deque()
        self.videos = []
        self.finished = []
        self.series = []
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
        self.first_work = None
        self.delivered = None
        self.work = 0.0
        self.clar_rounds = 0
        self.script_loops = 0
        self.final_loops = 0
        self.segments = []


class Owner:
    def __init__(self):
        self.busy = False
        self.busy_days = 0.0


def dispatch(sim):
    while sim.work_queue:
        owner = next((o for o in sim.owners if not o.busy and getattr(o, "available", True)), None)
        if owner is None:
            return
        minutes, video, label, cb = sim.work_queue.popleft()
        owner.busy = True
        dur = minutes / MIN_PER_DAY
        owner.busy_days += dur
        video.segments.append((sim.t, sim.t + dur, label, "work"))
        if video.first_work is None:
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


def video_steps(sim, video, cfg):
    m = cfg["minutes"]

    def work(label):
        return ("work", m[label], label)

    if cfg["flow"] == "baseline":
        yield work("intake review")
        while True:
            video.clar_rounds += 1
            yield ("wait", sim.rng.uniform(*cfg["clar_wait"]), "clarification wait")
            yield work("clarification reply")
            if sim.rng.random() >= cfg["p_clar"]:
                break
        yield work("content brief")
        yield work("script drafting")
        yield work("ai refinement")
    elif cfg["flow"] == "iter1":
        yield work("brief review")
        yield work("script drafting")
        yield work("script editing")
    elif cfg["flow"] == "iter2":
        yield work("brief review")
        yield work("ai param & gen check")
        yield work("script editing")
    else:  # iter3 — exceptions + params + edit-QC only
        yield work("brief exceptions")
        yield work("ai param check")
        yield work("script editing")

    while True:  # script approval — the only serial client gate left
        yield ("wait", sim.rng.uniform(*cfg["gate_wait"]), "script approval")
        if sim.rng.random() >= cfg["p_script"]:
            break
        video.script_loops += 1
        yield work("script rework")

    if cfg["flow"] == "iter3":
        # single render: machine time, producers free; variants included
        yield ("wait", sim.rng.uniform(*cfg["render_wait"]), "render (machine)")
        yield work("render QA")
        # objection window runs in PARALLEL: no serial wait; an objection
        # adds a re-render + re-QA inside the window
        while True:
            if sim.rng.random() >= cfg["p_final"]:
                break
            video.final_loops += 1
            yield work("objection re-render")
        yield work("delivery & admin")
        return

    yield work("video generation")
    yield work("audio generation")
    yield work("av sync")
    while True:
        yield ("wait", sim.rng.uniform(*cfg["gate_wait"]), "final approval")
        if sim.rng.random() >= cfg["p_final"]:
            break
        video.final_loops += 1
        yield work("final rework")

    yield work("platform adaptation")
    yield work("delivery & admin")


def drive(sim, video, gen):
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


def run_scenario(name, cfg, lam=LAMBDA, months=MONTHS, seed=7,
                 warmup=WARMUP_MONTHS):
    sim = Sim(cfg, lam, seed)
    sim.owners = [Owner(), Owner()]

    def arrival():
        v = Video(sim.next_vid, sim.t)
        sim.next_vid += 1
        sim.videos.append(v)
        sim.intake.append(v)
        drive(sim, v, video_steps(sim, v, cfg))
        sim.schedule(sim.rng.expovariate(sim.lam_wd), arrival)

    def log():
        sim.series.append((sim.t, len(sim.intake),
                           sim.next_vid - len(sim.finished)))
        sim.schedule(0.5, log)

    sim.schedule(0.0, arrival)
    log()
    sim.run(months * WD_MONTH)

    t0 = warmup * WD_MONTH
    cutoff = months * WD_MONTH - CUTOFF_MONTHS * WD_MONTH
    window = [v for v in sim.finished
              if t0 <= v.arrival <= cutoff and v.delivered is not None]
    leads = [(v.delivered - v.arrival) * CAL for v in window]
    works = [v.work for v in window]
    loops = [1 if (v.clar_rounds > 1 or v.script_loops or v.final_loops) else 0
             for v in window]
    util = sum(o.busy_days for o in sim.owners) / (2 * months * WD_MONTH)
    series = [(t, wip) for (t, _q, wip) in sim.series if t >= t0]

    metrics = measure(sim, t0, cutoff, months*WD_MONTH, expected_work(cfg), MIN_PER_DAY, lam)
    return dict(
        metrics=metrics, name=name, leads=leads, works=works, loops=loops, util=metrics["busy_util"],
        mean_wip=metrics["mean_wip"],
        capacity=metrics["capacity"],
        mean_lead=statistics.mean(leads) if leads and metrics["stable"] and not metrics["censored"] else float("nan"),
        p90_lead=(sorted(leads)[int(0.9 * len(leads))] if leads and metrics["stable"] and not metrics["censored"] else float("nan")),
        mean_work=statistics.mean(works) if works else float("nan"),
        rework_share=statistics.mean(loops) if loops else float("nan"),
    )


# ======================================================================
# Parts
# ======================================================================
def part0_sanity() -> None:
    hr("PART 0 · SANITY — engine must reproduce the published numbers")
    checks = [("baseline", run_scenario("baseline", CONFIGS["baseline"]),
               dict(lead=21.8*21.7/22, work=600)),
              ("iteration 1", run_scenario("iteration 1", CONFIGS["iteration 1"]),
               dict(lead=6.8*21.7/22, work=438)),
              ("iteration 2", run_scenario("iteration 2", CONFIGS["iteration 2"]),
               dict(lead=4.0*21.7/22, work=351))]
    for name, r, want in checks:
        ok = "✓" if abs(r["mean_lead"] - want["lead"]) < 0.15 else "✗"
        print(f"  {name:<12} lead {r['mean_lead']:>5.1f} vs {want['lead']:>5.1f}"
              f" · work {r['mean_work']:>5.0f} vs {want['work']:>5.0f}   {ok}")


def part1_ladder() -> list:
    hr(f"PART 1 · THE LADDER — baseline → Iter 1 → 2 → 3, λ = {LAMBDA}/month")
    results = [run_scenario(n, c) for n, c in CONFIGS.items()]
    print(f"  {'config':<28}{'lead d':>8}{'P90 d':>8}{'work min':>10}"
          f"{'rework':>8}{'wc-cap/mo':>10}{'util':>6}{'WIP':>6}")
    for r in results:
        print(f"  {r['name']:<28}{r['mean_lead']:>8.1f}{r['p90_lead']:>8.1f}"
              f"{r['mean_work']:>10.0f}{r['rework_share']:>8.0%}"
              f"{r['capacity']:>10.1f}{r['util']:>6.0%}{r['mean_wip']:>6.1f}")
    print("""
  wc-cap = work-content ceiling (14,150 min ÷ work/video; assumes no queueing)
  targets [T] from kpi-data: Iter 3 lead 1.5 d (1–2) · work 60 min · rework 10%""")
    print("  engine check (closed form vs simulated):")
    for n, c in CONFIGS.items():
        r = next(x for x in results if x["name"] == n)
        ok = "✓" if abs(r["mean_work"] - expected_work(c)) <= 20 else "✗"
        print(f"    {n:<28}{expected_work(c):>6.0f} vs {r['mean_work']:>5.0f} min  {ok}")
    print(f"  incidence check: iter3 closed form "
          f"{expected_incidence(CONFIGS['iteration 3']):.0%} (target 10%)")
    return results


def part2_sweep() -> dict:
    hr("PART 2 · DEMAND SWEEP — practical capacity (3 seeds each)")
    lambdas = [15.0, 20.0, 22.0, 26.0, 30.0, 34.0, 38.0, 40.0,
               80.0, 120.0, 160.0, 200.0, 230.0, 250.0]
    levels = ["baseline", "iteration 2", "iteration 3"]
    print(f"  {'λ':>6}{'baseline':>16}{'iteration 2':>16}{'iteration 3':>16}")
    sweep = {}
    for lam in lambdas:
        row = []
        for name in levels:
            runs = [run_scenario(name, CONFIGS[name], lam=lam, months=36,
                                 warmup=16, seed=s) for s in (11, 12, 13)]
            row.append((statistics.mean(r["mean_lead"] for r in runs),
                        statistics.mean(r["mean_wip"] for r in runs)))
        sweep[lam] = row
        print(f"{lam:>6.1f}" + "".join(f"{a:>10.1f} d /{b:>5.1f}" for a, b in row))
    print("""
  practical capacity = highest λ with mean lead ≤ 28 d (top of today's
  reported band [C]). For Iteration 3 the ceiling stops being capacity at
  all — it becomes demand: at any plausible demand queueing is low under the tested low-demand assumptions.""")
    for j, name in enumerate(levels):
        ok = [lam for lam in lambdas if lam < BUDGET_MIN / expected_work(CONFIGS[name]) and sweep[lam][j][0] <= 28.0]
        cap = max(ok) if ok else 0.0
        print(f"  {name:<12} practical capacity ≈ {cap:.0f}/mo "
              f"(work-content ceiling {BUDGET_MIN / expected_work(CONFIGS[name]):.1f}/mo)")
    return sweep


def part3_sensitivity(results: list) -> None:
    hr("PART 3 · SCRIPT-APPROVAL SENSITIVITY — the last serial wait")
    base = next(r for r in results if r["name"] == "iteration 3")
    slow = next(r for r in results if "slow" in r["name"])
    print(f"  {'lawyer behaviour':<26}{'gate wait':>16}{'lead d':>8}{'P90 d':>8}")
    for label, r in (("SLA-shaped (~24 h)", base),
                     ("rides the 48 h cap", slow)):
        lo, hi = CONFIGS[r["name"]]["gate_wait"]
        print(f"  {label:<26}{f'U({lo}–{hi}) wd':>16}"
              f"{r['mean_lead']:>8.1f}{r['p90_lead']:>8.1f}")
    print("  → after Iteration 3, client approval is a major lead-time component; machine render and human QC remain.\n"
          "    The constraint has left HiLegal's building.")


if __name__ == "__main__":
    part0_sanity()
    results = part1_ladder()
    part2_sweep()
    part3_sensitivity(results)
    print("\nDONE. Numbers feed kpi-data.md and the Iteration-3 summary.")
