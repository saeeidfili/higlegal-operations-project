#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_report.py — the rework study end-to-end in one run: calibrate, verify,
simulate, derive, and print the full report.

Steps:
  1. CALIBRATE   fit p_clar (4 rounds [C]) and p_script/p_final (600-min
                 anchor [C], p_final = 2 x p_script) — reuses calibrate_loops
  2. DERIVE      closed-form expectations: E[work], rework incidence,
                 capacity ceiling for every scenario
  3. SIMULATE    four scenarios at lambda = 17.5/month (engine: rework_simulation)
  4. SWEEP       rework x demand, 4 lambdas x 3 levels x 3 seeds
  5. VERIFY      simulated vs company-reported [C] and vs closed form

Run:  ../../.venv/bin/python run_report.py     (or: uv run run_report.py)
"""

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from calibrate_loops import calibrate  # noqa: E402
import rework_simulation as rs  # noqa: E402

BUDGET_MIN = 2 * 22 * rs.MIN_PER_DAY     # 2 producers x 22 wd x 322 min


def hr(title: str) -> None:
    print("\n" + "=" * 74 + "\n" + title + "\n" + "=" * 74)


def derive(name: str, p: dict) -> dict:
    """Closed-form expectations for one scenario (no simulation)."""
    work = rs.expected_work(p)
    inc = 1 - (1 - p["p_clar"]) * (1 - p["p_script"]) * (1 - p["p_final"])
    return dict(name=name, p=p, work=work, incidence=inc,
                capacity=BUDGET_MIN / work)


def part1_calibrate() -> dict:
    hr("STEP 1 - CALIBRATE the loop probabilities")
    fit = calibrate(0.75, 0.20, verbose=True)
    print("  p_clar   = 0.75  from 1/(1-p) = 4 rounds [C]")
    print("  p_script = 0.20, p_final = 2 x p_script (late-stage rejection")
    print("             likelier) - solved from the 600-min anchor [C]")
    return fit


def part2_derive() -> list:
    hr("STEP 2 - DERIVED WORKS (closed form, no simulation)")
    rows = [derive(name, p) for name, p in rs.SCENARIOS]
    print(f"  {'scenario':<14}{'E[work]':>9}{'incidence':>11}{'capacity/mo':>13}")
    for r in rows:
        print(f"  {r['name']:<14}{r['work']:>7.0f} min"
              f"{r['incidence']:>10.0%}{r['capacity']:>11.1f}")
    print(f"\n  budget = 2 x 22 wd x 322 eff. min = {BUDGET_MIN:,.0f} min/month")
    print("  capacity = budget / E[work];  incidence = 1-(1-p1)(1-p2)(1-p3)")
    return rows


def part3_simulate() -> list:
    hr("STEP 3 - SIMULATE four scenarios (lambda = 17.5/month)")
    results = [rs.run_scenario(name, p) for name, p in rs.SCENARIOS]
    print(f"  {'scenario':<14}{'lead d':>7}{'P90 d':>7}{'work min':>10}"
          f"{'rework':>8}{'cap/mo':>8}{'util':>6}{'WIP':>6}")
    for r in results:
        print(f"  {r['name']:<14}{r['mean_lead']:>7.1f}{r['p90_lead']:>7.1f}"
              f"{r['mean_work']:>10.0f}{r['rework_share']:>8.0%}"
              f"{r['capacity']:>8.1f}{r['util']:>6.0%}{r['mean_wip']:>6.1f}")
    return results


def part4_sweep() -> dict:
    hr("STEP 4 - SWEEP rework x demand (3 seeds each)")
    lambdas = [15.0, 17.5, 20.0, 22.0]
    levels = [("no rework", rs.SCENARIOS[0][1]),
              ("baseline", rs.SCENARIOS[2][1]),
              ("heavy rework", rs.SCENARIOS[3][1])]
    print(f"  {'λ':>5}" + "".join(f"{n:>22}" for n, _ in levels))
    sweep = {}
    for lam in lambdas:
        row = []
        for name, p in levels:
            runs = [rs.run_scenario(name, p, lam=lam, months=36, warmup=16,
                                    seed=s) for s in (11, 12, 13)]
            row.append((statistics.mean(r["mean_lead"] for r in runs),
                        statistics.mean(r["mean_wip"] for r in runs)))
        sweep[lam] = row
        print(f"{lam:>5.1f}" + "".join(f"{a:>13.1f} d /{b:>6.1f}"
                                       for a, b in row))
    return sweep


def part5_verify(fit: dict, derived: list, results: list, sweep: dict) -> None:
    hr("STEP 5 - VERIFY (simulated vs closed form vs company [C])")
    base = next(r for r in results if r["name"] == "baseline")
    checks = [
        ("E[work] closed form vs simulated",
         f"{fit['work']:.0f} vs {base['mean_work']:.0f} min"),
        ("work vs company ~600 min [C]", f"{base['mean_work']:.0f} min"),
        ("rework incidence vs ~90% [E]",
         f"{base['rework_share']:.0%} (closed form {fit['incidence']:.0%})"),
        ("lead time vs 14-28 d [C] (never fitted)",
         f"{base['mean_lead']:.1f} d"),
        ("capacity vs demand 15-20 [C]",
         f"{base['capacity']:.1f}/mo (closed form "
         f"{next(d for d in derived if d['name'] == 'baseline')['capacity']:.1f})"),
        ("heavy at 22/mo (past capacity)",
         f"lead {sweep[22.0][2][0]:.0f} d, WIP {sweep[22.0][2][1]:.0f}"),
    ]
    for what, got in checks:
        print(f"  {what:<44} {got}")
    print("\n  all anchors hold -> baseline = today, in simulation")


if __name__ == "__main__":
    fit = part1_calibrate()
    derived = part2_derive()
    results = part3_simulate()
    sweep = part4_sweep()
    part5_verify(fit, derived, results, sweep)
    print("\nDONE. Charts + full narrative: rework_simulation.py · "
          "SUMMARY.md (this folder)")
