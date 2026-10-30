#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib"]
# ///
"""
queue_model.py — the HiLegal intake queue, modelled end-to-end in one file
==========================================================================
Section 3, "This is the current process" (Operations Management project).

Company-reported inputs [C] (confirmed with HiLegal, September 2026):
  * demand / output        λ = 15–20 videos/month
  * intake queue wait      3–7 calendar days, "workload-dependent"
  * labour per video       ~10 h, two producers
  * stated output ceiling  35–40 videos/month

Model: M/M/1 — one intake inbox; the two producers act as ONE pooled pickup
function because videos are held start-to-finish (no preemption), so a slot
frees only at a completion boundary.  Units: working days (wd);
1 month = 22 wd; 1 wd ≈ 1.4 calendar days.

The script, in four parts (each is one function, run in order by main()):
  Part 1  Calibrate the one unknown μ against the observed 3–7 day wait, and
          calculate the company's 35–40/month ceiling from first principles
  Part 2  Predictions: backlog, wait tail, P90, nonlinearity, the ρ = 1 wall
  Part 3  Validate every formula with a discrete-event simulation
  Part 4  Render the three SVG charts with matplotlib (transparent
            backgrounds, for slides):
            queue-cliff.svg (utilization cliff + demand sweep, merged)
            order-timeline.svg · why-one-server.svg

Run:      uv run queue_model.py            (auto-installs matplotlib)
      or  .venv/bin/python queue_model.py  (project venv, matplotlib installed)
Output:   console tables + the three SVG files, written next to this script.
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
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

# ----------------------------------------------------------------------
# Parameters — the single source of truth; every table and chart flows
# from these values.
# ----------------------------------------------------------------------
WD_MONTH = 22.0                    # working days per month
CAL = 30.4 / 21.7                  # calendar days per working day ≈ 1.40
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
    ("12b Publish + adapt",     17.8,  1.0, "work"),
]

NAVY, GOLD, RED, GREEN = "#0F2A43", "#C9A227", "#C62828", "#2E7D32"
AMBER, BLUE, GREY = "#F9A825", "#1565C0", "#9AA5B1"


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
    print("  ✓ reproduces the whole observed band, incl. its workload-dependence")

    print("\nReality check — labour")
    print(f"  {MU} × 10 h = {MU * TAU_HOURS:.0f} h = {DEDICATION:.0%}"
          f" of the {HOURS_AVAIL:.0f} h available  (≈ the 65% in kpi-data.md)")

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
    print(f"  the wall:  the calculated ceiling {MU_THEORETICAL:.1f} (Part 1)"
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
    print("  → the formulas are what actually happens when you run the process.")


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
            fontsize=10.5, color="#8a6d1a")

    # the three observed demand points
    for lam, lab, col in ((LAMBDA_LOW, "light 15/mo", GREEN),
                          (LAMBDA_MID, "typical 17.5/mo", "#8a6d1a"),
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
    ax.text(1.01, 21.6, "calculated ceiling 35.2 [C]", fontsize=9.5,
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
    ax.grid(axis="y", color="#E3E6EA", lw=0.8)
    _save(fig, "queue-cliff.svg")


def chart_order_timeline() -> None:
    """One order through the 12 steps — work vs. wait."""
    colors = {"work": GREEN, "wait": RED, "mixed": AMBER, "client": BLUE}
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
        ax.axvline(d, color="#E3E6EA", lw=0.8, zorder=1)
    ax.set_xlim(0, 19.5)
    ax.set_ylim(-0.7, n - 0.3)
    ax.set_xlabel("calendar days")
    ax.set_xticks(range(0, 20, 2))
    ax.set_title("active work ≈ 10 h ≈ 6% of elapsed time — everything red is waiting",
                 fontsize=11, color="#555")
    fig.suptitle("Lawyer Chen's video — 18.8 days end-to-end (reported: 2–4 weeks [C])",
                 weight="bold")

    handles = [Patch(facecolor=c, label=l) for l, c in
               (("waiting", RED), ("active work", GREEN),
                ("mostly waiting", AMBER), ("lawyer (client)", BLUE))]
    ax.legend(handles=handles, ncol=4, loc="upper center",
              bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=10)
    _save(fig, "order-timeline.svg")


def chart_why_one_server() -> None:
    """The model-choice slide: textbook M/M/c vs HiLegal's order rail."""
    fig = plt.figure(figsize=(11.2, 7.0))
    gs = fig.add_gridspec(2, 2, height_ratios=(2.6, 1), hspace=0.34,
                          wspace=0.14, top=0.90, bottom=0.04)

    def rbox(ax, x, y, w, h, text, fc="white", ec=NAVY, tc="#222",
             fs=9.5, weight="normal", lw=1.6):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.10",
                                    fc=fc, ec=ec, lw=lw))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=tc, weight=weight)

    def arrow(ax, p1, p2, color=NAVY, dashed=False):
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                     color=color, lw=1.4,
                                     linestyle="--" if dashed else "-"))

    # ---- left panel: textbook M/M/c -----------------------------------
    axl = fig.add_subplot(gs[0, 0])
    axl.set_xlim(0, 10); axl.set_ylim(0, 10)
    axl.axis("off")
    axl.set_title("Textbook M/M/c — tills & call centres",
                  color=NAVY, weight="bold", fontsize=12)
    for i, x in enumerate((0.8, 1.7, 2.6)):           # the shared line
        axl.add_patch(FancyBboxPatch((x, 4.6), 0.7, 0.7,
                                     boxstyle="round,pad=0.04",
                                     fc="#ECEFF3", ec=GREY, lw=1.2))
    axl.text(2.05, 3.7, "one shared line", ha="center", fontsize=9.5,
             color="#555")
    for y, name in ((7.2, "Server 1"), (4.5, "Server 2"), (1.8, "Server 3")):
        rbox(axl, 5.0, y, 4.5, 1.7,
             f"{name}\ntakes the next customer\nthe instant it is free")
        arrow(axl, (3.8, 4.95), (5.0, y + 0.85), dashed=True)
    axl.text(5.0, 0.35, "jobs take minutes · handover is free → M/M/c fits",
             ha="center", fontsize=10, color="#555", style="italic")

    # ---- right panel: HiLegal's order rail ----------------------------
    axr = fig.add_subplot(gs[0, 1])
    axr.set_xlim(0, 10); axr.set_ylim(0, 10)
    axr.axis("off")
    axr.set_title("HiLegal — the order rail (no preemption)",
                  color=NAVY, weight="bold", fontsize=12)
    rbox(axr, 0.3, 7.0, 3.2, 1.9, "INTAKE INBOX\nrequests wait\n3–7 days [C]",
         fc=RED, ec=RED, tc="white", weight="bold")
    rbox(axr, 4.5, 7.0, 3.4, 1.9,
         "PICKUP GATE\nonly at a completion\nboundary — no preemption",
         fc="#FFF8E1", ec=AMBER, tc="#6d5300", weight="bold")
    arrow(axr, (3.5, 7.95), (4.5, 7.95))
    rbox(axr, 0.6, 2.2, 4.3, 1.2, "Producer A\nvideo in hands:\nstart → finish",
         fc=GREEN, ec=GREEN, tc="white", fs=9)
    rbox(axr, 5.1, 2.2, 4.3, 1.2, "Producer B\nvideo in hands:\nstart → finish",
         fc=GREEN, ec=GREEN, tc="white", fs=9)
    arrow(axr, (6.2, 7.0), (2.75, 3.4))
    arrow(axr, (6.2, 7.0), (7.25, 3.4))
    axr.text(0.35, 4.55, "a slot frees only\nwhen a video finishes",
             ha="left", fontsize=9, color="#555")
    axr.text(5.0, 0.6, "both mid-video → nobody answers  ⇒  ONE pooled server (M/M/1)",
             ha="center", fontsize=10, color=RED, weight="bold")

    # ---- bottom band: the claim, tied to the calibration fit -----------
    axb = fig.add_subplot(gs[1, :])
    axb.set_xlim(0, 1); axb.set_ylim(0, 1)
    axb.axis("off")
    axb.add_patch(FancyBboxPatch((0.01, 0.02), 0.98, 0.96,
                                 boxstyle="round,pad=0.01",
                                 fc="#F5F6F8", ec="#D8DCE2", lw=1.2))
    axb.text(0.5, 0.78, "One queue, one pooled answering function — that is M/M/1",
             ha="center", fontsize=11.5, color=NAVY, weight="bold")
    axb.text(0.5, 0.50, "A video is held start-to-finish, so a slot frees only"
                        " when one finishes —\nthe inbox cannot be answered by"
                        " “the other producer” mid-video.",
             ha="center", fontsize=10.5, color="#333")
    axb.text(0.5, 0.15, "And it fits: M/M/1 at μ ≈ 23.5 gives 2.3 / 3.8 / 7.5"
                        " days across the demand range 15–20 — the reported"
                        " 3–7 days [C].",
             ha="center", fontsize=10.5, color=RED, weight="bold")

    fig.suptitle("Why one server?  Two waiting lines, different physics",
                 fontsize=13, weight="bold")
    _save(fig, "why-one-server.svg")


def part4_charts() -> None:
    hr("PART 4 · CHARTS → three SVGs, transparent background, next to script")
    chart_cliff_sweep()
    chart_order_timeline()
    chart_why_one_server()


def main() -> None:
    part1_calibration()
    part2_predictions()
    part3_simulation()
    part4_charts()
    print("\nDONE. Slide use:  queue-cliff.svg → THE chart (cliff + demand"
          " sweep, one curve) · order-timeline.svg → work vs wait ·"
          " why-one-server.svg → the model-choice slide\n")


if __name__ == "__main__":
    main()
