#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib"]
# ///
"""
queue_model.py — the HiLegal intake queue, modelled end-to-end in one file
==========================================================================
Section 4, "These are the wastes and root causes" (Operations Management
project). The queueing model is the quantitative evidence for the Waiting
waste; it was originally developed alongside the Section-3 process map.

Company-reported inputs [C] (confirmed with HiLegal, September 2026):
  * demand / output        λ = 15–20 videos/month
  * intake queue wait      3–7 calendar days, "workload-dependent"
  * labour per video       ~10 h, two producers
  * stated output ceiling  35–40 videos/month

Model: M/M/1 — an assumed aggregate serial intake surrogate. A shared inbox
and non-preemption do not imply a literal single server for two producers.
The separate whole-process model uses two pooled task servers.  Units: working days (wd);
1 month = 22 wd; 1 wd ≈ 1.4 calendar days.

The script, in four parts (each is one function, run in order by main()):
  Part 1  Calibrate the one unknown μ against the observed 3–7 day wait, and
          calculate the company's 100%-dedication illustration alongside the reported 35–40/month ceiling
  Part 2  Predictions: backlog, wait tail, P90, nonlinearity, the ρ = 1 wall
  Part 3  Validate every formula with a discrete-event simulation
  Part 4  Render the two SVG charts with matplotlib (transparent
            backgrounds, for slides):
            queue-cliff.svg (utilization cliff + demand sweep, merged)
            order-timeline.svg

Run:      uv run queue_model.py            (auto-installs matplotlib)
      or  .venv/bin/python queue_model.py  (project venv, matplotlib installed)
Output:   console tables + the two SVG files, written next to this script.
"""

from __future__ import annotations

import math
import os
import random
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# ----------------------------------------------------------------------
# Parameters — the single source of truth; every table and chart flows
# from these values.
# ----------------------------------------------------------------------
WD_MONTH = 22.0                    # working days per month
CAL = 30.4 / 22.0                  # calendar days per working day ≈ 1.40
OUT_DIR = Path(__file__).resolve().parent
PNG_DIR = os.environ.get("Q_PNG_DIR")   # optional: also write PNG previews

LAMBDA_LOW, LAMBDA_MID, LAMBDA_HIGH = 15.0, 17.5, 20.0    # demand /month [C]
HOURS_AVAIL = 2 * 176              # producer-hours available per month
TAU_HOURS = 10.0                   # active labour per video [C]
MU_THEORETICAL = HOURS_AVAIL / TAU_HOURS      # 35.2/month at 100% dedication
MU = 23.5                          # calibrated effective capacity (Part 1)
DEDICATION = MU * TAU_HOURS / HOURS_AVAIL     # ≈ 0.67 of available hours

# One order through the 12 steps ( Lawyer Chen trace, see START.md ):
# (step name, start day, duration in days, kind)
STEPS = [
    ("1  Request submitted",     0.0,  0.2, "client"),
    ("2  INTAKE QUEUE",          0.2,  5.0, "wait"),
    ("3  Clarification ×3",      5.2,  3.0, "mixed"),
    ("4  Content brief",         8.2,  0.6, "work"),
    ("5  Script drafting",       8.8,  1.5, "work"),
    ("6  AI refinement",        10.3,  0.5, "work"),
    ("7  Script approval",      10.8,  2.0, "wait"),
    ("9  Video generation",     12.8,  1.0, "work"),
    ("10 Audio generation",     13.8,  0.5, "work"),
    ("11 AV sync (bottleneck)", 14.3,  1.5, "work"),
    ("12a Final approval",      15.8,  2.0, "wait"),
    ("12b Adapt + deliver",     17.8,  1.0, "work"),
]

# Colour tokens — presentation design system (STYLE.md, presentation branch)
NAVY, GOLD, RED, GREEN = ("#101010", "#C9A86A", "#D92605", "#A8823F")  # ink, gold, accent, wait-line
AMBER, BLUE = "#C9A86A", "#6A7282"


# ----------------------------------------------------------------------
# Queueing-theory kernel — every number the script prints comes from here.
# ----------------------------------------------------------------------
def mm1(lam: float, mu: float) -> dict:
    """Standard M/M/1 results. Rates per month; times returned in working days."""
    rho = lam / mu
    tau = WD_MONTH / mu                       # wd per serial video cycle
    if rho >= 1.0:
        return dict(rho=rho, tau=tau, Wq=float("inf"), W=float("inf"),
                    Lq=float("inf"), L=float("inf"))
    Wq = rho / (1.0 - rho) * tau              # expected wait in queue
    W = Wq + tau                              # sojourn: queue + service
    lam_wd = lam / WD_MONTH
    return dict(rho=rho, tau=tau, Wq=Wq, W=W, Lq=lam_wd * Wq, L=lam_wd * W)


def tail_prob(lam: float, mu: float, cal_days: float) -> float:
    """P(wait in queue > t) for M/M/1: rho · exp(−(mu−lam) · t)."""
    rho = lam / mu
    t_wd = cal_days / CAL
    return rho * math.exp(-(mu - lam) / WD_MONTH * t_wd)


def p90_wait(lam: float, mu: float) -> float:
    """Solve rho·exp(−rate·t) = 0.10 for t; return calendar days."""
    rho = lam / mu
    rate_wd = (mu - lam) / WD_MONTH
    return math.log(rho / 0.10) / rate_wd * CAL


def simulate_mm1(lam: float, mu: float, n: int = 200_000, warmup: int = 20_000,
                 seed: int = 7) -> float:
    """Pure-Python discrete-event simulation of a FIFO M/M/1 queue.
    Returns the mean wait in queue (working days)."""
    rng = random.Random(seed)
    lam_wd, mu_wd = lam / WD_MONTH, mu / WD_MONTH
    clock = 0.0
    server_free = 0.0
    waits = []
    for _ in range(n):
        clock += rng.expovariate(lam_wd)      # next arrival
        service = rng.expovariate(mu_wd)      # its serial service time
        start = max(clock, server_free)       # FIFO: waits for the server
        waits.append(start - clock)
        server_free = start + service
    return statistics.mean(waits[warmup:])


def hr(title: str) -> None:
    print("\n" + "=" * 74 + "\n" + title + "\n" + "=" * 74)


# ======================================================================
# PART 1 — CALIBRATION: fit the one unknown μ to the one observation
# ======================================================================
def part1_calibration() -> None:
    hr("PART 1 · CALIBRATION — find the one unknown, μ")

    bad = mm1(LAMBDA_MID, MU_THEORETICAL)
    print(f"Attempt 1 · 100% dedication   μ = 352 h ÷ 10 h = {MU_THEORETICAL:.1f}/month")
    print(f"  ρ = {bad['rho']:.2f} → Wq = {bad['Wq'] * CAL:.1f} calendar days"
          "   ✗  (observed: 3–7 d) — pickups are not instant\n")

    print(f"Attempt 2 · calibrated        μ = {MU}/month")
    print(f"  {'λ':>6}  {'ρ':>5}  {'Wq':>6}  {'vs observed [C]':<14}")
    for lam, obs in ((LAMBDA_LOW, "~3 d"), (LAMBDA_MID, "3–7 d"),
                     (LAMBDA_HIGH, "~7 d")):
        r = mm1(lam, MU)
        print(f"  {lam:>6.1f}  {r['rho']:>5.2f}  {r['Wq'] * CAL:>4.1f} d"
              f"  {obs:<14}")
    print("  Approximate calibration only: endpoints are about 2.3 and 7.4 d, outside the reported 3–7 d band.")

    print("\nReality check — labour")
    print(f"  {MU} × 10 h = {MU * TAU_HOURS:.0f} h = {DEDICATION:.0%}"
          f" of the {HOURS_AVAIL:.0f} h available  (distinct from the KPI scenario: 60% of 160 h, not an independent 65% estimate)")

    print("\nThe company's output ceiling, calculated from first principles:")
    print(f"  2 producers × 22 working days × 8 h = {HOURS_AVAIL:.0f}"
          " producer-hours/month")
    print(f"  {HOURS_AVAIL:.0f} h ÷ {TAU_HOURS:g} h of labour per video"
          f"        = {MU_THEORETICAL:.1f} videos/month at 100% dedication")
    print("  ≈ the company-stated ceiling of 35–40 videos/month [C]")
    print(f"  → the ceiling IS the ρ = 1 wall: at λ ≥ {MU_THEORETICAL:.1f}"
          " the queue can only grow —\n    'pushing to the ceiling' is a"
          " mathematical promise of unbounded waiting")


# ======================================================================
# PART 2 — PREDICTIONS
# ======================================================================
def part2_predictions() -> None:
    hr("PART 2 · PREDICTIONS — what the model says beyond the average")
    rt, rh = mm1(LAMBDA_MID, MU), mm1(LAMBDA_HIGH, MU)
    print(f"  {'metric':<42}{'typical 17.5':>13}{'heavy 20':>10}")
    print(f"  {'utilization ρ':<42}{rt['rho']:>13.2f}{rh['rho']:>10.2f}")
    print(f"  {'expected intake wait Wq':<42}{rt['Wq'] * CAL:>11.1f} d"
          f"{rh['Wq'] * CAL:>8.1f} d")
    print(f"  {'pending requests in inbox Lq = λ·Wq':<42}{rt['Lq']:>13.1f}"
          f"{rh['Lq']:>10.1f}   ← falsifiable: count the inbox")
    print(f"  {'videos inside the system L = λ·W':<42}{rt['L']:>13.1f}"
          f"{rh['L']:>10.1f}")

    print("\n  tail of the intake wait (typical month) — exponential:")
    print("  " + " · ".join(f"P(> {d} d) = {tail_prob(LAMBDA_MID, MU, d):.0%}"
                            for d in (5, 7, 10, 14)))
    print(f"  P90 ≈ {p90_wait(LAMBDA_MID, MU):.0f} calendar days"
          " — before production even starts")

    rl = mm1(LAMBDA_LOW, MU)
    mult_l = rl["rho"] / (1 - rl["rho"])
    mult_h = rh["rho"] / (1 - rh["rho"])
    print(f"\n  nonlinearity:  demand ×{LAMBDA_HIGH / LAMBDA_LOW:.2f} (15→20)"
          f"  ⇒  multiplier ρ/(1−ρ) {mult_l:.1f} → {mult_h:.1f}"
          f"  ⇒  wait ×{rh['Wq'] / rl['Wq']:.1f}"
          f" ({rl['Wq'] * CAL:.1f} → {rh['Wq'] * CAL:.1f} d)")
    print(f"  the wall:  the effective ceiling {MU:.1f} for this scenario (Part 1)"
          f" IS ρ = 1;  at λ = 24 → ρ = {24 / MU:.2f} > 1,"
          " backlog grows forever")


# ======================================================================
# PART 3 — SIMULATION VALIDATION
# ======================================================================
def part3_simulation() -> None:
    hr("PART 3 · VALIDATION — discrete-event simulation (FIFO, 200k orders)")
    for lam in (LAMBDA_MID, LAMBDA_HIGH):
        theory = mm1(lam, MU)["Wq"] * CAL
        sim = simulate_mm1(lam, MU) * CAL
        print(f"  λ = {lam:>5.1f}/month   formula {theory:4.1f} d   "
              f"simulation {sim:4.1f} d   diff {abs(sim - theory) / theory:.1%}")
    print("  → the simulation verifies the algebra under identical assumptions; it does not validate HiLegal operations.")


# ======================================================================
# PART 6 — CHARTS (matplotlib → four SVGs)
# ======================================================================
def _save(fig: plt.Figure, name: str) -> None:
    """Save with a transparent background (for slides) — no white box."""
    fig.patch.set_alpha(0.0)
    for ax in fig.axes:
        ax.set_facecolor("none")
    path = OUT_DIR / name
    fig.savefig(path, format="svg", bbox_inches="tight", transparent=True)
    if PNG_DIR:                                   # optional QA previews
        fig.savefig(Path(PNG_DIR) / name.replace(".svg", ".png"), dpi=110,
                    transparent=True)
    plt.close(fig)
    print(f"  wrote {path.name}")


def chart_cliff_sweep() -> None:
    """The merged chart: Wq vs ρ (bottom axis) = Wq vs λ (top axis).
    The utilization cliff and the demand sweep are the same curve —
    ρ = λ/μ — so one figure with two x-axes tells both stories."""
    tau = WD_MONTH / MU
    fig, ax = plt.subplots(figsize=(10.2, 5.8))

    # the curve, in utilization terms (stops where it exits the top)
    rho = np.linspace(0.05, 0.949, 1400)
    wq = rho / (1 - rho) * tau * CAL
    ax.plot(rho, np.where(wq <= 26, wq, np.nan), color=NAVY, lw=2.6, zorder=3)

    # the demand axis on top: λ = μ·ρ (same horizontal position)
    secax = ax.secondary_xaxis("top", functions=(lambda r: r * MU,
                                                 lambda l: l / MU))
    secax.set_xticks([5, 10, 15, 20, 25])
    secax.set_xlabel("monthly demand λ (videos/month, constant team)",
                     fontsize=10)
    secax.tick_params(labelsize=9.5)

    # observed band
    ax.axhspan(3, 7, color=GOLD, alpha=0.35, zorder=1)
    ax.text(0.06, 7.45, "company-reported intake wait: 3–7 days [C]",
            fontsize=10.5, color="#6B5223")

    # the three observed demand points
    for lam, lab, col in ((LAMBDA_LOW, "light 15/mo", GREEN),
                          (LAMBDA_MID, "typical 17.5/mo", "#6B5223"),
                          (LAMBDA_HIGH, "heavy 20/mo", RED)):
        r = mm1(lam, MU)
        ax.plot(r["rho"], r["Wq"] * CAL, "o", color=col, ms=7, zorder=4)
        ax.annotate(f"{lab}  ρ={r['rho']:.2f}", (r["rho"], r["Wq"] * CAL),
                    textcoords="offset points", xytext=(0, 10), ha="center",
                    fontsize=10.5, color=col, weight="bold")

    # the wall and, right of it, the unstable region (ρ > 1)
    ax.axvline(1.0, color=RED, ls="--", lw=2)
    ax.text(1.01, 24.6, "ρ = 1  ⇒  wait → ∞", fontsize=11, color=RED,
            weight="bold")
    ax.text(1.01, 23.1, "capacity λ = μ ≈ 23.5/mo", fontsize=9.5, color=RED)
    ax.text(1.01, 21.6, "100%-dedication ceiling 35.2 [D]", fontsize=9.5,
            color=RED)
    ax.axvspan(1.0, 1.25, color=RED, alpha=0.08, zorder=1)
    ax.text(1.125, 9.4, "unstable (ρ > 1)", ha="center", va="center",
            fontsize=11, color=RED, weight="bold")
    ax.text(1.125, 7.2, "backlog grows forever —\nevery month adds debt",
            ha="center", va="center", fontsize=9, color=RED)
    ax.text(1.125, 3.2, "marketing push\nλ = 24 → ρ = 1.02", ha="center",
            va="center", fontsize=9.5, color=RED)

    ax.set_xlim(0.05, 1.25)
    ax.set_ylim(0, 26)
    ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
    ax.set_xlabel("server utilization ρ = λ/μ")
    ax.set_ylabel("expected intake wait (calendar days)")
    ax.set_title("The utilization cliff = the demand sweep — one curve,"
                 " two axes (μ ≈ 23.5/month)", weight="bold")
    ax.grid(axis="y", color="#E5E7EB", lw=0.8)
    _save(fig, "queue-cliff.svg")


def chart_order_timeline() -> None:
    """One order through the 12 steps — work vs. wait."""
    colors = {"work": NAVY, "wait": RED, "mixed": GOLD, "client": BLUE}
    n = len(STEPS)
    fig, ax = plt.subplots(figsize=(10.8, 6.4))

    for i, (name, start, dur, kind) in enumerate(STEPS):
        y = n - 1 - i                                  # step 1 at the top
        ax.barh(y, dur, left=start, height=0.64, color=colors[kind], zorder=3)
        if dur >= 0.9:                                 # label wide bars only
            ax.text(start + dur / 2, y, f"{dur:g} d", ha="center", va="center",
                    fontsize=9.5, color="white", weight="bold")

    ax.set_yticks(range(n))
    ax.set_yticklabels([s[0] for s in reversed(STEPS)], fontsize=10.5)
    for lab, (name, _, _, kind) in zip(ax.get_yticklabels(), reversed(STEPS)):
        if kind == "wait":
            lab.set_color(RED)
            lab.set_weight("bold")
        else:
            lab.set_color(NAVY)

    for d in range(0, 20, 2):
        ax.axvline(d, color="#E5E7EB", lw=0.8, zorder=1)
    ax.set_xlim(0, 19.5)
    ax.set_ylim(-0.7, n - 0.3)
    ax.set_xlabel("calendar days")
    ax.set_xticks(range(0, 20, 2))
    ax.set_title("illustrative timeline: 10 h staff effort; calendar spans do not measure value-added PCE",
                 fontsize=11, color="#6A7282")
    fig.suptitle("Lawyer Chen's video — 18.8 days end-to-end (reported: 2–4 weeks [C])",
                 weight="bold")

    handles = [Patch(facecolor=c, label=l) for l, c in
               (("waiting", RED), ("active work", NAVY),
                ("mostly waiting", AMBER), ("lawyer (client)", BLUE))]
    ax.legend(handles=handles, ncol=4, loc="upper center",
              bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=10)
    _save(fig, "order-timeline.svg")


def part4_charts() -> None:
    hr("PART 4 · CHARTS → two SVGs, transparent background, next to script")
    chart_cliff_sweep()
    chart_order_timeline()


def main() -> None:
    part1_calibration()
    part2_predictions()
    part3_simulation()
    part4_charts()
    print("\nDONE. Slide use:  queue-cliff.svg → THE chart (cliff + demand"
          " sweep, one curve) · order-timeline.svg → work vs wait\n")


if __name__ == "__main__":
    main()
