#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib"]
# ///
"""
compare_sim.py — Section 7: run baseline vs Iterations 1–3 through the
scenario matrix S0–S5 and build the comparison chart pack.

Engine + process configs: imported from the Iteration-3 simulation (same
lineage as the Section-4 study; all four process versions live there).

Scenarios:
  S0 normal      λ=20/mo, parameters as calibrated
  S1 demand      λ sweep 15→240/mo (saturation curves + WIP paths at 40/mo)
  S2 slow lawyers  all gate waits ×2.5 (≈3–6 calendar days)
  S3 rework stress  loop probability 0.75 at every gate (geometric high-rework sensitivity, not a finite worst case)
  S4 absence     one producer away for 10 working days from month 12
  S5 quality dip  v3 with v2-level loop rates + deeper edits (editing 30,
                 render QA 30 min)

Charts (transparent SVG, next to this script):
  ladder.svg · timer-bars.svg · saturation.svg · wip-paths.svg ·
  slow-lawyers.svg · rework-stress.svg
Also writes scenario-results.md with every table.

Run:  ../../.venv/bin/python compare_sim.py
"""

from __future__ import annotations

import statistics
import math
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent
                       / "06 This is how we improve the process iteration by iteration"
                       / "Iteration 3 - Integrate audio and video generation"))
import iteration3_sim as eng  # noqa: E402
from simulation_metrics import measure

WD, CAL, BUDGET = eng.WD_MONTH, eng.CAL, eng.BUDGET_MIN
OUT = HERE
# Colour tokens — presentation design system (STYLE.md, presentation branch)
NAVY, GOLD, RED, GREEN, GREY = ("#101010", "#C9A86A", "#D92605", "#A8823F",
                                "#99A1AF")                # ink, gold, accent, wait-line, grey-400
SLATE, BLUE, DARKRED = "#99A1AF", "#4A5565", "#D92605"    # grey-400, body, accent
VERSIONS = ["baseline", "iteration 1", "iteration 2", "iteration 3"]
SHORT = {"baseline": "baseline", "iteration 1": "v1 · standardize",
         "iteration 2": "v2 · AI scripting", "iteration 3": "v3 · single render"}
VCOLORS = {"baseline": "#99A1AF", "iteration 1": "#A8823F",
           "iteration 2": "#C9A86A", "iteration 3": "#101010"}
MEASUREMENT_LOG = []
TOOLS = {"baseline": 90, "iteration 1": 90, "iteration 2": 100, "iteration 3": 95}


def cfg_for(name, **over):
    cfg = dict(eng.CONFIGS[name])
    minutes = dict(cfg["minutes"])
    for k, v in over.pop("_minutes", {}).items():
        minutes[k] = v
    cfg["minutes"] = minutes
    cfg.update(over)
    return cfg


def scale_waits(cfg, f):
    cfg = dict(cfg)
    cfg["gate_wait"] = tuple(w * f for w in cfg["gate_wait"])
    if cfg.get("clar_wait"):
        cfg["clar_wait"] = tuple(w * f for w in cfg["clar_wait"])
    return cfg


# ----------------------------------------------------------------------
# Full runner — like eng.run_scenario but keeps per-video records + WIP
# series, so the timer bars and WIP paths can be drawn.
# ----------------------------------------------------------------------
def run_full(name, cfg, lam=20.0, months=36, warmup=16, seed=7,
             owners=None, absence=None):
    sim = eng.Sim(cfg, lam, seed)
    n_own = owners if owners else 2
    sim.owners = [eng.Owner() for _ in range(n_own)]

    if absence:                       # S4: drop to 1 owner for a window
        t_drop, t_back = absence

        def drop():
            sim.owners[-1].available = False  # finish any current non-preemptive task

        def restore():
            sim.owners[-1].available = True
            eng.dispatch(sim)

        sim.schedule(t_drop, drop)
        sim.schedule(t_back, restore)

    def arrival():
        v = eng.Video(sim.next_vid, sim.t)
        sim.next_vid += 1
        sim.videos.append(v)
        sim.intake.append(v)
        eng.drive(sim, v, eng.video_steps(sim, v, cfg))
        sim.schedule(sim.rng.expovariate(sim.lam_wd), arrival)

    def log():
        sim.series.append((sim.t, len(sim.intake),
                           sim.next_vid - len(sim.finished)))
        sim.schedule(0.5, log)

    sim.schedule(0.0, arrival)
    log()
    sim.run(months * WD)

    t0 = warmup * WD
    cutoff = months * WD - eng.CUTOFF_MONTHS * WD
    window = [v for v in sim.finished
              if t0 <= v.arrival <= cutoff and v.delivered is not None]
    leads = [(v.delivered - v.arrival) * CAL for v in window]
    works = [v.work for v in window]
    loops = [1 if (v.clar_rounds > 1 or v.script_loops or v.final_loops) else 0
             for v in window]
    absent_days = max(0.0, min(absence[1], cutoff)-max(absence[0], t0)) if absence else 0.0
    metrics = measure(sim, t0, cutoff, months*WD, eng.expected_work(cfg), eng.MIN_PER_DAY,
                      lam, owners=n_own, absent_days=absent_days)
    valid = metrics['stable'] and metrics['censored'] == 0
    MEASUREMENT_LOG.append(dict(name=name,demand=lam,seed=seed,months=months,warmup=warmup,absence=absence,
                                gate_probabilities={key:cfg[key] for key in ['p_clar','p_script','p_final']},metrics=metrics))
    return dict(
        metrics=metrics, completed_cohort_lead=metrics['completed_cohort_lead'],
        name=name, videos=window, leads=leads, works=works, loops=loops,
        series=[(t, w) for (t, _q, w) in sim.series if t >= t0],
        mean_lead=statistics.mean(leads) if leads and valid else float("nan"),
        p90_lead=(sorted(leads)[int(0.9 * len(leads))] if leads and valid else float("nan")),
        mean_work=statistics.mean(works) if works else float("nan"),
        rework=statistics.mean(loops) if loops else float("nan"),
        cost=(statistics.mean(works) / 60 * 85 + TOOLS[name.split(" · ")[0]]
              if works else float("nan")),
        capacity=metrics["capacity"],
    )


def multi(name, cfg, lam, seeds=(11, 12, 13), **kw):
    runs = [run_full(name, cfg, lam=lam, seed=s, **kw) for s in seeds]
    return dict(
        name=name, runs=runs, metrics=runs[0]["metrics"],
        mean_lead=statistics.mean(r["mean_lead"] for r in runs),
        p90_lead=statistics.mean(r["p90_lead"] for r in runs),
        mean_work=statistics.mean(r["mean_work"] for r in runs),
        rework=statistics.mean(r["rework"] for r in runs),
        cost=statistics.mean(r["cost"] for r in runs),
        capacity=statistics.mean(r["capacity"] for r in runs),
        series=runs[0]["series"], videos=runs[0]["videos"],
        leads=runs[0]["leads"],
    )


def hr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


def save(fig, name):
    fig.patch.set_alpha(0.0)
    for ax in fig.axes:
        ax.set_facecolor("none")
    fig.savefig(OUT / name, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(f"  wrote {name}")


RESULTS: dict[str, dict] = {}


# ======================================================================
# S0 — normal conditions (λ = 20)
# ======================================================================
def s0():
    hr("S0 · NORMAL CONDITIONS — λ = 20/mo, 3 seeds")
    res = {v: multi(v, eng.CONFIGS[v], 20.0) for v in VERSIONS}
    RESULTS["S0"] = {v: res[v] for v in VERSIONS}
    print(f"  {'version':<16}{'lead d':>8}{'P90 d':>8}{'work min':>10}"
          f"{'¥/video':>9}{'cap/mo':>8}{'rework':>8}{'QAR':>7}")
    for v in VERSIONS:
        r = res[v]
        print(f"  {SHORT[v]:<16}{r['mean_lead']:>8.1f}{r['p90_lead']:>8.1f}"
              f"{r['mean_work']:>10.0f}{r['cost']:>9.0f}{r['capacity']:>8.0f}"
              f"{r['rework']:>8.0%}{1 - r['rework']:>7.0%}")
    # chart 3 — the ladder: six KPI panels
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 7.2))
    panels = [
        ("lead time (days)", [res[v]["mean_lead"] for v in VERSIONS], None),
        ("P90 lead (days)", [res[v]["p90_lead"] for v in VERSIONS], None),
        ("human work (min)", [res[v]["mean_work"] for v in VERSIONS], None),
        ("cost (¥/video)", [res[v]["cost"] for v in VERSIONS], None),
        ("work-content capacity (/mo)", [res[v]["capacity"] for v in VERSIONS], None),
        ("rework rate", [res[v]["rework"] for v in VERSIONS], None),
    ]
    for ax, (title, vals, _) in zip(axes.flat, panels):
        colors = [VCOLORS[v] for v in VERSIONS]
        bars = ax.bar(range(4), vals, color=colors, width=0.62)
        if "rework" in title:
            import numpy as np
            ticks = ax.get_yticks()
            ax.set_yticks(ticks)
            ax.set_yticklabels([f"{t:.0%}" for t in ticks])
        for b, val in zip(bars, vals):
            txt = f"{val:.0%}" if "rework" in title else (
                f"{val:.0f}" if val >= 10 else f"{val:.1f}")
            ax.text(b.get_x() + b.get_width() / 2, val, txt, ha="center",
                    va="bottom", fontsize=9, weight="bold")
        ax.set_xticks(range(4))
        ax.set_xticklabels(["base", "v1", "v2", "v3"], fontsize=9)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", color="#E5E7EB", lw=0.8)
        if "capacity" in title:
            ax.set_yscale("log")
    fig.suptitle("S0 · normal conditions (λ = 20/mo) — the four process versions",
                 weight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "ladder.svg")

    # chart 1 — timer bars: median order per version, work vs wait
    fig, ax = plt.subplots(figsize=(11.0, 6.0))
    for i, v in enumerate(VERSIONS):
        vids = sorted(res[v]["videos"], key=lambda x: x.delivered - x.arrival)
        vd = vids[len(vids) // 2]
        y = len(VERSIONS) - 1 - i
        intake = ((vd.first_work or vd.arrival) - vd.arrival) * CAL
        if intake > 0.05:
            ax.barh(y, intake, height=0.55, color=SLATE, zorder=3)
        for (s, e, lab, kind) in vd.segments:
            x, w = (s - vd.arrival) * CAL, (e - s) * CAL
            if w <= 0:
                continue
            if kind == "work":
                c = DARKRED if "rework" in lab or "objection" in lab else NAVY
            elif "clarification" in lab:
                c = GOLD
            elif "render" in lab:
                c = BLUE
            else:
                c = RED
            ax.barh(y, max(w, 0.12), left=x, height=0.55, color=c, zorder=4)
        lead = (vd.delivered - vd.arrival) * CAL
        ax.text(lead + 0.4, y, f"{lead:.1f} d", va="center", fontsize=10,
                weight="bold", color=NAVY)
    ax.set_yticks(range(len(VERSIONS)))
    ax.set_yticklabels([SHORT[v] for v in reversed(VERSIONS)], fontsize=10.5)
    ax.set_xlabel("calendar days since request")
    ax.set_xlim(0, max(res[v]["mean_lead"] for v in VERSIONS) * 1.15)
    ax.set_title("One median order per version — where the time goes",
                 weight="bold")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=c, label=l) for l, c in
                       (("active work", NAVY), ("rework / objection", DARKRED),
                        ("approval wait", RED), ("clarification wait", GOLD),
                        ("machine render", BLUE), ("intake queue", SLATE))],
              ncol=6, loc="upper center", bbox_to_anchor=(0.5, -0.09),
              frameon=False, fontsize=9)
    ax.grid(axis="x", color="#E5E7EB", lw=0.8)
    save(fig, "timer-bars.svg")


# ======================================================================
# S1 — demand surge (saturation + WIP paths)
# ======================================================================
def s1():
    hr("S1 · DEMAND SURGE — λ sweep 15→240/mo, 3 seeds")
    lambdas = [15, 20, 25, 30, 40, 60, 80, 120, 160, 200, 240]
    sweep = {}
    for lam in lambdas:
        sweep[lam] = {v: multi(v, eng.CONFIGS[v], float(lam)) for v in VERSIONS}
        row = " ".join(f"{sweep[lam][v]['mean_lead']:>7.1f}" for v in VERSIONS)
        print(f"  λ={lam:>3}   lead d: {row}")
    RESULTS["S1"] = {lam: {v: sweep[lam][v]["mean_lead"] for v in VERSIONS}
                     for lam in lambdas}

    fig, ax = plt.subplots(figsize=(10.2, 5.8))
    for v in VERSIONS:
        ys = [min(sweep[lam][v]["mean_lead"], 65) for lam in lambdas]
        ax.plot(lambdas, ys, "o-", color=VCOLORS[v], lw=2.4, ms=5,
                label=SHORT[v])
    ax.axhline(28, color=RED, ls="--", lw=1.2)
    ax.text(238, 29.5, "top of today's reported band [C]", ha="right",
            fontsize=9, color=RED)
    ax.set_xlabel("demand λ (videos/month) — same two producers")
    ax.set_ylabel("mean lead time (calendar days, clipped at 65)")
    ax.set_title("S1 · demand surge — where each version saturates", weight="bold")
    ax.legend(frameon=False, fontsize=10)
    ax.grid(color="#E5E7EB", lw=0.8)
    save(fig, "saturation.svg")

    # WIP paths at 40/mo
    paths = {v: run_full(v, eng.CONFIGS[v], lam=40.0, seed=13) for v in VERSIONS}
    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    for v in VERSIONS:
        s = paths[v]["series"]
        t0 = s[0][0]
        ax.plot([(t - t0) / WD for t, _ in s], [w for _, w in s],
                color=VCOLORS[v], lw=2.0, label=SHORT[v])
    ax.set_xlabel("months into the window (sampled twice per working day)")
    ax.set_ylabel("videos in the system (WIP)")
    ax.set_title("S1 · WIP at 40 videos/month — backlog spiral vs flat line",
                 weight="bold")
    ax.legend(frameon=False, fontsize=10)
    ax.grid(color="#E5E7EB", lw=0.8)
    save(fig, "wip-paths.svg")
    stable = {v: sweep[200][v]["mean_lead"] for v in VERSIONS}
    print(f"  at 200/mo: " + " · ".join(
        f"{SHORT[v]} {'unstable' if stable[v] != stable[v] else f'{stable[v]:.1f} d'}"
        for v in VERSIONS))


# ======================================================================
# S2 — slow lawyers (gate waits ×2.5)
# ======================================================================
def s2():
    hr("S2 · SLOW LAWYERS — all gate waits ×2.5 (≈3–6 calendar days), λ=20")
    res = {}
    for v in VERSIONS:
        normal = multi(v, eng.CONFIGS[v], 20.0)
        slow = multi(v, scale_waits(eng.CONFIGS[v], 2.5), 20.0)
        res[v] = (normal, slow)
        print(f"  {SHORT[v]:<16} normal {normal['mean_lead']:>5.1f} d"
              f" (P90 {normal['p90_lead']:>5.1f})   slow {slow['mean_lead']:>5.1f} d"
              f" (P90 {slow['p90_lead']:>5.1f})")
    RESULTS["S2"] = {v: dict(normal=res[v][0]["mean_lead"],
                             slow=res[v][1]["mean_lead"]) for v in VERSIONS}

    import numpy as np
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    x = np.arange(len(VERSIONS))
    w = 0.36
    ax.bar(x - w / 2, [res[v][0]["mean_lead"] for v in VERSIONS], w,
           color=NAVY, label="normal gates")
    ax.bar(x + w / 2, [res[v][1]["mean_lead"] for v in VERSIONS], w,
           color=RED, label="gates ×2.5 (slow lawyers)")
    for i, v in enumerate(VERSIONS):
        ax.text(x[i] - w / 2, res[v][0]["mean_lead"], f"{res[v][0]['mean_lead']:.1f}",
                ha="center", va="bottom", fontsize=9, weight="bold")
        ax.text(x[i] + w / 2, res[v][1]["mean_lead"], f"{res[v][1]['mean_lead']:.1f}",
                ha="center", va="bottom", fontsize=9, weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([SHORT[v] for v in VERSIONS], fontsize=10)
    ax.set_ylabel("mean lead time (calendar days)")
    ax.set_title("S2 · slow lawyers — slow-response sensitivity, not a worst-case bound",
                 weight="bold")
    ax.legend(frameon=False, fontsize=10)
    ax.grid(axis="y", color="#E5E7EB", lw=0.8)
    save(fig, "slow-lawyers.svg")


# ======================================================================
# S3 — rework stress (loop probability 0.75 at every gate)
# ======================================================================
def s3():
    hr("S3 · REWORK STRESS — loop p = 0.75 at every gate (geometric high-rework sensitivity, not a finite worst case), λ=20")
    res = {}
    for v in VERSIONS:
        cfg = cfg_for(v, p_script=0.75, p_final=0.75)
        r = multi(v, cfg, 20.0)
        res[v] = r
        print(f"  {SHORT[v]:<16} lead {r['mean_lead']:>6.1f} d (P90 {r['p90_lead']:>6.1f})"
              f"   work {r['mean_work']:>5.0f} min   rework {r['rework']:.0%}")
    RESULTS["S3"] = {v: dict(lead=res[v]["mean_lead"], p90=res[v]["p90_lead"],
                             rework=res[v]["rework"]) for v in VERSIONS}

    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    for i, v in enumerate(VERSIONS):
        r = res[v]
        if math.isfinite(r['mean_lead']):
            ax.bar(i, r['mean_lead'], color=VCOLORS[v], width=0.6)
            ax.errorbar(i, r['mean_lead'], yerr=[[0],[max(0,r['p90_lead']-r['mean_lead'])]],
                        fmt='none', ecolor=DARKRED, capsize=5)
            ax.text(i, r['p90_lead']+1, f"P90 {r['p90_lead']:.1f} d", ha='center')
        else:
            ax.text(i, 1, 'No stationary mean\n(overload/censored)', ha='center', color=RED)
    ax.set_xticks(range(len(VERSIONS)))
    ax.set_xticklabels([SHORT[v] for v in VERSIONS], fontsize=10)
    ax.set_ylabel("mean lead time (calendar days)")
    ax.set_title("S3 · mean four rounds at each active gate; overload has no stationary lead",
                 weight="bold")
    ax.grid(axis="y", color="#E5E7EB", lw=0.8)
    save(fig, "rework-stress.svg")


# ======================================================================
# S4 — producer absence (1 producer for 2 weeks)
# ======================================================================
def s4():
    hr("S4 · PRODUCER ABSENCE — one producer away for 10 working days from month 12, λ=20")
    t_drop, t_back = 12 * WD, 12 * WD + 10.0
    res = {}
    for v in VERSIONS:
        r = run_full(v, eng.CONFIGS[v], lam=20.0, months=36, warmup=11,
                     seed=13, absence=(t_drop, t_back))
        # videos arriving in the 3 months after the absence: recovery cohort
        cohort = [x for x in r["videos"] if t_drop <= x.arrival <= t_drop + 3 * WD]
        leads = [(x.delivered - x.arrival) * CAL for x in cohort]
        mean = statistics.mean(leads) if leads else float("nan")
        peak_wip = max(w for _, w in r["series"] if t_drop <= _ <= t_drop + 4 * WD)
        res[v] = dict(lead=mean, peak_wip=peak_wip)
        print(f"  {SHORT[v]:<16} cohort lead {mean:>6.1f} d   peak WIP during/after absence {peak_wip:>5.1f}")
    RESULTS["S4"] = res


# ======================================================================
# S5 — quality dip (v3 with v2-level loops + deeper edits)
# ======================================================================
def s5():
    hr("S5 · QUALITY DIP — v3 model regresses (loops → v2 level, edits deeper), λ=20")
    dip = cfg_for("iteration 3", p_script=0.108, p_final=0.216,
                  _minutes={"script editing": 30, "render QA": 30})
    v3 = multi("iteration 3", eng.CONFIGS["iteration 3"], 20.0)
    v2 = multi("iteration 2", eng.CONFIGS["iteration 2"], 20.0)
    d = multi("iteration 3 · quality dip", dip, 20.0)
    print(f"  v3 normal     lead {v3['mean_lead']:>4.1f} d · work {v3['mean_work']:>4.0f} min"
          f" · rework {v3['rework']:.0%} · ¥{v3['cost']:.0f}")
    print(f"  v3 dipped     lead {d['mean_lead']:>4.1f} d · work {d['mean_work']:>4.0f} min"
          f" · rework {d['rework']:.0%} · ¥{d['cost']:.0f}")
    print(f"  v2 normal     lead {v2['mean_lead']:>4.1f} d · work {v2['mean_work']:>4.0f} min"
          f" · rework {v2['rework']:.0%} · ¥{v2['cost']:.0f}")
    RESULTS["S5"] = dict(v3=v3, dipped=d, v2=v2)


# ----------------------------------------------------------------------
# scenario-results.md
# ----------------------------------------------------------------------
def write_results_md():
    L = ["# Section 7 — scenario results (generated by compare_sim.py)", ""]
    L.append("Model results under stated assumptions, not observed improvements. 22 working days = 30.4 calendar days. Work durations are deterministic; waits and arrivals are stochastic. Each comparison uses 3 seeds unless a single-seed absence path is specified.")
    L.append("Lead/P90 are unavailable if offered workload exceeds capacity or the arrival cohort remains censored. Such cases have no defensible stationary lead estimate; completed-only diagnostics are not substituted. Capacity is analytical work-content capacity, not throughput.")
    L.append("## S0 · normal conditions (λ = 20/mo)")
    L.append("| version | lead d | P90 d | work min | ¥/video | cap/mo | rework | QAR |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for v in VERSIONS:
        r = RESULTS["S0"][v]
        L.append(f"| {SHORT[v]} | {r['mean_lead']:.1f} | {r['p90_lead']:.1f} |"
                 f" {r['mean_work']:.0f} | {r['cost']:.0f} | {r['capacity']:.0f} |"
                 f" {r['rework']:.0%} | {1 - r['rework']:.0%} |")
    L.append("\n## S1 · demand surge — mean lead (d) by λ")
    lams = sorted(RESULTS["S1"])
    L.append("| λ/mo | " + " | ".join(SHORT[v] for v in VERSIONS) + " |")
    L.append("|---:|" + "---:|" * 4)
    for lam in lams:
        cells = [f"{RESULTS['S1'][lam][v]:.1f}" if RESULTS["S1"][lam][v] == RESULTS["S1"][lam][v]
                 else "unavailable (overload/censored)" for v in VERSIONS]
        L.append(f"| {lam} | " + " | ".join(cells) + " |")
    L.append("\n## S2 · slow lawyers (gates ×2.5)")
    L.append("| version | normal d | slow d |")
    L.append("|---|---:|---:|")
    for v in VERSIONS:
        L.append(f"| {SHORT[v]} | {RESULTS['S2'][v]['normal']:.1f} |"
                 f" {RESULTS['S2'][v]['slow']:.1f} |")
    L.append("\n## S3 · rework stress (p = 0.75 per active gate; mean four rounds, not a maximum)")
    L.append("| version | lead d | P90 d | rework |")
    L.append("|---|---:|---:|---:|")
    for v in VERSIONS:
        L.append(f"| {SHORT[v]} | {RESULTS['S3'][v]['lead']:.1f} |"
                 f" {RESULTS['S3'][v]['p90']:.1f} | {RESULTS['S3'][v]['rework']:.0%} |")
    L.append("\n## S4 · producer absence (1 of 2 away, 2 weeks)")
    L.append("| version | cohort lead d (3 mo after) | peak WIP |")
    L.append("|---|---:|---:|")
    for v in VERSIONS:
        L.append(f"| {SHORT[v]} | {RESULTS['S4'][v]['lead']:.1f} |"
                 f" {RESULTS['S4'][v]['peak_wip']:.1f} |")
    s5 = RESULTS["S5"]
    L.append("\n## S5 · quality dip (v3 regresses to v2-level loops + deeper edits)")
    L.append("| config | lead d | work min | rework | ¥/video |")
    L.append("|---|---:|---:|---:|---:|")
    for k, lab in (("v3", "v3 normal"), ("dipped", "v3 dipped"),
                   ("v2", "v2 normal")):
        r = s5[k]
        L.append(f"| {lab} | {r['mean_lead']:.1f} | {r['mean_work']:.0f} |"
                 f" {r['rework']:.0%} | {r['cost']:.0f} |")
    (OUT / "scenario-results.md").write_text(re.sub(r"\bnan\b", "unavailable (overload/censored)", "\n".join(L)) + "\n", encoding="utf-8")
    print("  wrote scenario-results.md")


if __name__ == "__main__":
    s0()
    s1()
    s2()
    s3()
    s4()
    s5()
    write_results_md()
    print("\nDONE. Six SVGs + scenario-results.md in this folder.")


def rework_demand_report():
    """Section 7 cross-factor extension: same Section-4/6 event engine."""
    levels = {'no rework': (0,0,0), 'baseline': (.75,.20,.40), 'heavy': (.80,.40,.60)}
    lines=['# Rework x demand: existing engine, three seeds', '',
           'All inputs below are modelling assumptions, not measured gate rates. Capacity is expected work-content capacity. Busy utilization and WIP use the same post-warm-up time window; throughput counts departures in that window.',
           'Working month = 22 days, calendar month = 30.4 days. Lead is the full arrival-cohort mean only when all cohort arrivals finish and offered utilization is below one. Otherwise the completed-only diagnostic is withheld from the lead column. WIP growth is a finite-horizon diagnostic, not a stationary law.', '',
           '| Rework | Demand/mo | Work min/video | Workload h/mo | Capacity/mo | Offered util | Busy util | Throughput/mo | Mean WIP | WIP growth/mo | Lead cal d | Cohort completion |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|']
    import json
    records=[]
    for label,(pc,ps,pf) in levels.items():
        cfg=cfg_for('baseline',p_clar=pc,p_script=ps,p_final=pf)
        work=eng.expected_work(cfg)
        for lam in [15,17.5,20,22,25]:
            runs=[run_full('baseline',cfg,lam=lam,months=36,warmup=16,seed=seed) for seed in (11,12,13)]
            ms=[r['metrics'] for r in runs]
            avg=lambda key:statistics.mean(m[key] for m in ms)
            valid=all(m['stable'] and not m['censored'] for m in ms)
            lead=f"{statistics.mean(r['mean_lead'] for r in runs):.2f}" if valid else ('overload' if not ms[0]['stable'] else 'censored')
            completion=sum(m['cohort_completed'] for m in ms)/sum(m['cohort_size'] for m in ms)
            lines.append(f"| {label} | {lam} | {work:.2f} | {lam*work/60:.2f} | {avg('capacity'):.2f} | {avg('offered_util'):.1%} | {avg('busy_util'):.1%} | {avg('throughput'):.2f} | {avg('mean_wip'):.2f} | {avg('wip_growth'):.2f} | {lead} | {completion:.1%} |")
            records.append(dict(rework=label,demand=lam,work=work,lead=lead,metrics=ms))
    lines+=['', 'Analytical link: workload = demand x E[work]; capacity = 14,150.4 / E[work]; offered utilization = demand / capacity. Rework increases both required labour and repeated client waits. At demand >= capacity, report backlog growth, not an infinite-horizon mean lead. Little law requires consistent units and a stable common boundary; it is not applied to the overloaded rows.', '',
            'These simulations quantify conditional consequences of assumed rates. They do not identify real rejection rates or independently validate proposed improvements.']
    (OUT/'rework-demand-results.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/'rework-demand-results.json').write_text(json.dumps(records,indent=2),encoding='utf-8')

if __name__ == '__main__':
    rework_demand_report()

if __name__ == '__main__':
    (OUT/'measurement-diagnostics.json').write_text(json.dumps(MEASUREMENT_LOG,indent=2)+'\n',encoding='utf-8')
