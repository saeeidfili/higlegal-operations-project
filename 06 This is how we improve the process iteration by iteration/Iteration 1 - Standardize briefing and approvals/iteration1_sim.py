#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
iteration1_sim.py — Iteration 1 (standardized briefing & approvals) simulated
================================================================================
A modified copy of ../../04 .../Rework/rework_simulation.py (same engine:
event heap, two pooled producers, no preemption, geometric gate loops).

What changed vs the Section-4 study:
  * CONFIGS carry task minutes + gate-wait ranges + loop probabilities per
    process version (baseline vs Iteration 1) — the 04 script hardcodes one
    task set.
  * Iteration 1 flow: no clarification gate (structured form + previews kill
    it at source); approval waits SLA-capped at 48 h → U(0.5–1.5) wd;
    structured change requests (scene + reason code) make each loop CHEAPER
    (script 50→25 min, final 70→35 min) rather than rarer.

Iteration-1 loop probabilities are solved the 04 way (two anchors):
  * rework incidence 1−(1−ps)(1−pf) = 55% (kpi-data §5 target)
  * E[work] = 402 first-time-right + loop costs = 435 min (kpi-data §1)
  → ps ≈ 0.214, pf ≈ 0.428 (pf = 2·ps, as calibrated in Section 4)

Outputs (console): baseline sanity check, baseline vs Iter 1 at λ=17.5,
demand sweep (practical capacity = highest λ with mean lead ≤ 28 d, the top
of the company-reported band [C]), SLA-compliance sensitivity.

Run:  ../../.venv/bin/python iteration1_sim.py   (or: python3 — stdlib only)
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
# Shared constants — identical to the Section-4 simulation.
# ----------------------------------------------------------------------
WD_MONTH = 22.0
CAL = 30.4 / 22.0                    # calendar days per working day ≈ 1.40
DEDICATION = 0.67
MIN_PER_DAY = 480 * DEDICATION       # ≈ 321.6 effective producer-minutes/day
BUDGET_MIN = 2 * WD_MONTH * MIN_PER_DAY   # ≈ 14,150 min/month (67% budget)

MONTHS = 28
WARMUP_MONTHS = 10
CUTOFF_MONTHS = 3
LAMBDA = 17.5                        # arrival-rate assumption [E], midpoint of reported output

# ----------------------------------------------------------------------
# Process versions.  "minutes" = hands-on task minutes; the engine check
# (expected_work) audits each config against its own arithmetic.
# ----------------------------------------------------------------------
BASE_MIN = {   # as-is 12-step process (Section 4; sums to 516 FTR)
    "intake review": 15, "clarification reply": 8, "content brief": 45,
    "script drafting": 70, "ai refinement": 35, "script rework": 50,
    "video generation": 55, "audio generation": 30, "av sync": 140,
    "final rework": 70, "platform adaptation": 95, "delivery & admin": 23,
}
ITER1_MIN = {  # 10-step v1: form+previews, no clarification task; FTR 402
    "brief review": 10, "script drafting": 50, "script editing": 22,
    "script rework": 25,                      # structured change: scene+code
    "video generation": 60, "audio generation": 35, "av sync": 130,
    "final rework": 35,                       # targeted re-edit + re-sync
    "platform adaptation": 85, "delivery & admin": 10,
}

CONFIGS = {
    "baseline": dict(
        flow="baseline", minutes=BASE_MIN,
        clar_wait=(1.0, 2.0), gate_wait=(1.0, 3.0),
        p_clar=0.75, p_script=0.20, p_final=0.40),
    "iteration 1": dict(
        flow="iter1", minutes=ITER1_MIN,
        clar_wait=None, gate_wait=(0.5, 1.5),     # 48 h SLA both gates
        p_clar=0.00, p_script=0.214, p_final=0.428),
    "iteration 1 · fast lawyer": dict(
        flow="iter1", minutes=ITER1_MIN,
        clar_wait=None, gate_wait=(0.25, 1.0),    # approves in ~1 cal day
        p_clar=0.00, p_script=0.214, p_final=0.428),
    "iteration 1 · SLA breached": dict(
        flow="iter1", minutes=ITER1_MIN,
        clar_wait=None, gate_wait=(1.0, 1.6),     # always near the 48 h cap
        p_clar=0.00, p_script=0.214, p_final=0.428),
}


def expected_work(cfg: dict) -> float:
    """Closed-form E[work] — audits the engine per config."""
    m, p = cfg["minutes"], cfg
    if cfg["flow"] == "baseline":
        return (m["intake review"]
                + m["clarification reply"] / (1 - p["p_clar"])
                + m["content brief"] + m["script drafting"] + m["ai refinement"]
                + m["script rework"] * p["p_script"] / (1 - p["p_script"])
                + m["video generation"] + m["audio generation"] + m["av sync"]
                + m["final rework"] * p["p_final"] / (1 - p["p_final"])
                + m["platform adaptation"] + m["delivery & admin"])
    return (m["brief review"] + m["script drafting"] + m["script editing"]
            + m["script rework"] * p["p_script"] / (1 - p["p_script"])
            + m["video generation"] + m["audio generation"] + m["av sync"]
            + m["final rework"] * p["p_final"] / (1 - p["p_final"])
            + m["platform adaptation"] + m["delivery & admin"])


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
    """One video through its process version. rng call order is part of
    the model: baseline keeps the 04 stream; iter1 has no clar draw."""
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
    else:
        yield work("brief review")          # complete Brief JSON, 10 min check
        yield work("script drafting")
        yield work("script editing")

    while True:
        yield ("wait", sim.rng.uniform(*cfg["gate_wait"]), "script approval")
        if sim.rng.random() >= cfg["p_script"]:
            break
        video.script_loops += 1
        yield work("script rework")

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
    hr("PART 0 · SANITY — copied engine must reproduce the Section-4 baseline")
    r = run_scenario("baseline", CONFIGS["baseline"])
    checks = [("lead time", r["mean_lead"], 21.8, 1.5),
              ("work min", r["mean_work"], 600, 25),
              ("rework", r["rework_share"], 0.87, 0.05),
              ("capacity", r["capacity"], 23.6, 0.5)]
    for what, got, want, tol in checks:
        ok = "✓" if abs(got - want) <= tol else "✗"
        print(f"  {what:<10} {got:>7.1f}  vs 04 published {want:>6.1f}   {ok}")
    print("  (tolerances: ±run-to-run seed noise; seed 7 as in 04)")


def part1_compare() -> list:
    hr(f"PART 1 · BASELINE vs ITERATION 1 — λ = {LAMBDA}/month, 2 producers")
    results = [run_scenario(n, c) for n, c in CONFIGS.items()]
    print(f"  {'config':<26}{'lead d':>8}{'P90 d':>8}{'work min':>10}"
          f"{'rework':>8}{'wc-cap/mo':>10}{'util':>6}{'WIP':>6}")
    for r in results:
        print(f"  {r['name']:<26}{r['mean_lead']:>8.1f}{r['p90_lead']:>8.1f}"
              f"{r['mean_work']:>10.0f}{r['rework_share']:>8.0%}"
              f"{r['capacity']:>10.1f}{r['util']:>6.0%}{r['mean_wip']:>6.1f}")
    print("""
  wc-cap = work-content ceiling = 14,150 min budget ÷ work/video (the
  division number — assumes no queueing). Practical capacity: Part 2.
  targets [T] from kpi-data: lead 9 d · work 435 min · rework 55%""")
    print("  engine check (closed form vs simulated):")
    for n, c in CONFIGS.items():
        r = next(x for x in results if x["name"] == n)
        ok = "✓" if abs(r["mean_work"] - expected_work(c)) <= 20 else "✗"
        print(f"    {n:<26}{expected_work(c):>6.0f} vs {r['mean_work']:>5.0f} min  {ok}")
    print(f"  incidence check: iter1 closed form "
          f"{expected_incidence(CONFIGS['iteration 1']):.0%} (target 55%)")
    return results


def part2_sweep() -> dict:
    hr("PART 2 · DEMAND SWEEP — practical capacity (3 seeds each)")
    lambdas = [15.0, 17.5, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0]
    levels = ["baseline", "iteration 1"]
    print(f"  {'λ':>5}{'baseline':>22}{'iteration 1':>22}")
    sweep = {}
    for lam in lambdas:
        row = []
        for name in levels:
            runs = [run_scenario(name, CONFIGS[name], lam=lam, months=36,
                                 warmup=16, seed=s) for s in (11, 12, 13)]
            row.append((statistics.mean(r["mean_lead"] for r in runs),
                        statistics.mean(r["mean_wip"] for r in runs)))
        sweep[lam] = row
        print(f"{lam:>5.1f}" + "".join(f"{a:>13.1f} d /{b:>6.1f}" for a, b in row))
    print("""
  practical capacity (this study) = highest λ with mean lead ≤ 28 d —
  staying inside the top of today's reported band [C]. (A '≤14 d' bar
  would be a to-be standard the baseline can never meet; 28 d asks only
  'no worse than the client's worst experience today'.)""")
    for j, name in enumerate(levels):
        ok = [lam for lam in lambdas if lam < BUDGET_MIN / expected_work(CONFIGS[name]) and sweep[lam][j][0] <= 28.0]
        cap = max(ok) if ok else 0.0
        nxt = min((lam for lam in lambdas if lam > cap), default=None)
        print(f"  {name:<12} practical capacity ≈ {cap:.0f}/mo "
              f"(work-content ceiling {BUDGET_MIN / expected_work(CONFIGS[name]):.1f}/mo)"
              + (f" — next step {nxt:.0f}/mo: {sweep[nxt][j][0]:.0f} d, WIP {sweep[nxt][j][1]:.0f}"
                 if nxt else ""))
    return sweep


def part3_sensitivity(results: list) -> None:
    hr("PART 3 · SLA-COMPLIANCE SENSITIVITY — lead time vs lawyer behaviour")
    base = next(r for r in results if r["name"] == "iteration 1")
    fast = next(r for r in results if "fast" in r["name"])
    slow = next(r for r in results if "breached" in r["name"])
    print(f"  {'lawyer behaviour':<26}{'gate wait':>16}{'lead d':>8}{'P90 d':>8}")
    for label, r in (("approves in ~1 d", fast),
                     ("typical (SLA shape)", base),
                     ("always near 48 h cap", slow)):
        lo, hi = CONFIGS[r["name"]]["gate_wait"]
        print(f"  {label:<26}{f'U({lo}–{hi}) wd':>16}"
              f"{r['mean_lead']:>8.1f}{r['p90_lead']:>8.1f}")
    print("  → Iteration 1's lead time is gate-dominated: lawyer behaviour\n"
          "    swings it more than any production change inside HiLegal.")


if __name__ == "__main__":
    part0_sanity()
    results = part1_compare()
    part2_sweep()
    part3_sensitivity(results)
    print("\nDONE. Numbers feed kpi-data.md (single source of truth) and the "
          "Iteration-1 summary.")
