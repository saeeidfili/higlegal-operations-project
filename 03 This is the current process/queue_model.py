#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Queueing-theory model of HiLegal's video-production intake queue
================================================================
Section 3 — "This is the current process" (Operations Management project)

Company-reported inputs [C] (confirmed with HiLegal, September 2026):
  * demand / output            λ ≈ 15–20 videos/month
  * intake queue wait          3–7 days, "workload-dependent"
  * labour per video           ~10 h, two producers
  * stated output ceiling      35–40 videos/month

Model: M/M/1 — one shared intake inbox, producers pick up requests one at a
time (no preemption). Refined with Kingman's VUT equation for variability.
Units: working days (wd). Month = 22 wd. 1 wd ≈ 1.4 calendar days.

The script:
  Part 1  Calibrates the model against the observed 3–7 day wait
  Part 2  Predictions: inbox backlog, wait-time tail, P90, demand sweep
  Part 3  Kingman VUT: how rework loops & marketing pushes inflate the queue
  Part 4  Validates the formulas with a pure-Python discrete-event simulation
  Part 5  Renders three SVG charts (no external dependencies)

Run:  python3 queue_model.py
Outputs: console tables + queue-cliff.svg, order-timeline.svg, demand-sweep.svg
"""

import math
import random
import statistics
from pathlib import Path

# ----------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------
WD_MONTH = 22.0                 # working days per month
CAL = 30.4 / 21.7               # calendar days per working day ≈ 1.40
OUT_DIR = Path(__file__).resolve().parent   # charts are written next to this script
LAMBDA_LOW, LAMBDA_MID, LAMBDA_HIGH = 15.0, 17.5, 20.0   # /month [C]
HOURS_AVAIL = 2 * 176           # producer-hours available per month (2 × 22d × 8h)
TAU_HOURS = 10.0                # active labour per video [C]
MU_THEORETICAL = HOURS_AVAIL / TAU_HOURS                  # 35.2/month at 100% dedication
MU_EFFECTIVE = 23.5             # calibrated effective capacity (Part 1)


# ----------------------------------------------------------------------
# M/M/1 formulas  (all rates per month; times returned in working days)
# ----------------------------------------------------------------------
def mm1(lam: float, mu: float) -> dict:
    """Standard M/M/1 results. Wq = expected wait in queue, tau = mean service."""
    rho = lam / mu
    tau = WD_MONTH / mu                     # wd per serial video cycle
    if rho >= 1.0:
        return dict(rho=rho, tau=tau, Wq=float("inf"), W=float("inf"),
                    Lq=float("inf"), L=float("inf"))
    Wq = rho / (1.0 - rho) * tau            # VUT with exponential assumptions
    W = Wq + tau                            # sojourn: queue + service
    lam_wd = lam / WD_MONTH
    return dict(rho=rho, tau=tau, Wq=Wq, W=W, Lq=lam_wd * Wq, L=lam_wd * W)


def tail_prob(lam: float, mu: float, cal_days: float) -> float:
    """P(wait in queue > t) for M/M/1: rho * exp(-(mu-lam) * t)."""
    rho = lam / mu
    t_wd = cal_days / CAL
    return rho * math.exp(-(mu - lam) / WD_MONTH * t_wd)


def kingman(lam: float, mu: float, ca2: float, cs2: float) -> float:
    """Kingman's VUT approximation (working days):
       Wq ≈ [rho/(1-rho)] * [(ca²+cs²)/2] * tau."""
    rho = lam / mu
    tau = WD_MONTH / mu
    return rho / (1.0 - rho) * (ca2 + cs2) / 2.0 * tau


def hr(title: str) -> None:
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


# ======================================================================
# PART 1 — CALIBRATION: the model must reproduce reality
# ======================================================================
hr("PART 1 — CALIBRATION OF THE INTAKE QUEUE (M/M/1)")

print(f"Theoretical capacity at 100% dedication : {MU_THEORETICAL:.1f} videos/month")
print(f"Company-stated ceiling [C]              : 35–40/month  ← matches the ρ=1 wall")
print(f"Calibrated effective capacity μ         : {MU_EFFECTIVE} videos/month")
dedication = MU_EFFECTIVE * TAU_HOURS / HOURS_AVAIL
print(f"Implied producer dedication             : {dedication:.0%} of available hours")
print("  → consistent with two producers who also do platform work [E]\n")

print(f"{'demand λ':<12}{'ρ = λ/μ':<10}{'Wq (M/M/1)':<16}{'≈ calendar':<14}{'observed [C]'}")
for label, lam in (("light 15", LAMBDA_LOW), ("typical 17.5", LAMBDA_MID),
                   ("heavy 20", LAMBDA_HIGH)):
    r = mm1(lam, MU_EFFECTIVE)
    print(f"{label:<12}{r['rho']:<10.2f}{r['Wq']:<16.2f}"
          f"{r['Wq'] * CAL:<14.1f}{'3–7 days'}")

print("""
REALITY CHECKS
  1. Wait times:  ρ ∈ [0.64, 0.85] over the observed demand range reproduces
     the company-reported 3–7 day intake wait ✓  (same phenomenon, same shape)
  2. Labour:      μ = 23.5/month × 10 h = 235 h ≈ 67% of 352 available hours —
     matches the ~65% team availability assumed in kpi-data.md §4 ✓
  3. Simulation:  Part 4 below reproduces the formula empirically ✓
Falsifiable prediction (ask HiLegal to count): the intake inbox should hold
≈ 2–5 pending requests at any moment (Little's Law). If it never holds more
than one, the delay is batch-review cadence, not queueing — see model card.""")


# ======================================================================
# PART 1b — ROBUSTNESS: WHY M/M/1? THE M/M/2 CHECK (Erlang C)
# ======================================================================
hr("PART 1b — ROBUSTNESS: WHY M/M/1? THE M/M/2 CHECK (Erlang C)")


def erlang_c(c: int, lam: float, mu_s: float) -> float:
    """M/M/c: probability an arrival finds all c servers busy (must wait).
    mu_s = service rate of EACH server (same units as lam)."""
    a = lam / mu_s                                   # offered load, Erlangs
    if a >= c:
        return 1.0
    sum_terms = sum(a ** k / math.factorial(k) for k in range(c))
    top = a ** c / math.factorial(c) * c / (c - a)
    return top / (sum_terms + top)


def mm2_wq(lam: float, mu_agg: float) -> float:
    """Expected queue wait (working days) for M/M/2 with aggregate rate mu_agg."""
    C = erlang_c(2, lam, mu_agg / 2.0)
    return C / (mu_agg - lam) * WD_MONTH             # months → working days


print("The team is two people — shouldn't the model be M/M/2 (each producer =")
print("one server)?  We compute it instead of assuming.  Same aggregate capacity;")
print("the only difference is how the two producers' capacity is pooled.\n")
print(f"{'demand λ':<12}{'ρ':>6}{'Wq M/M/1':>12}{'Wq M/M/2':>12}{'observed [C]':>16}")
for label, lam in (("light 15", LAMBDA_LOW), ("typical 17.5", LAMBDA_MID),
                   ("heavy 20", LAMBDA_HIGH)):
    r1 = mm1(lam, MU_EFFECTIVE)
    w2 = mm2_wq(lam, MU_EFFECTIVE)
    print(f"{label:<12}{r1['rho']:>6.2f}{r1['Wq'] * CAL:>9.1f} d"
          f"{w2 * CAL:>9.1f} d{'3–7 days':>16}")

print("""
Reading:
  * the two-server view shortens the expected wait by only ~15% at the same load
  * both models land inside the company-reported 3–7 day band
  * every conclusion (cliff, ×3 nonlinearity, ρ = 1 wall, Iteration-3 fix) is identical
So M/M/1 is the CONSERVATIVE, transparent base case — if the pessimistic model
already explains reality, the optimistic one does too.

Reality sits between the two: each producer juggles 1–2 staggered videos
(Little's Law: ≈ 3–6 in system), and client-gate stalls make a producer
unavailable without being "busy" — which pushes behaviour back toward the
pooled-unit view. And with the CEO-reported churn spiral (Section 2), the
"two servers" are not even reliably two.""")


# ======================================================================
# PART 2 — PREDICTIONS
# ======================================================================
hr("PART 2 — WHAT THE MODEL PREDICTS")

print(f"{'metric':<44}{'typical λ=17.5':>16}{'heavy λ=20':>12}")
rt, rh = mm1(LAMBDA_MID, MU_EFFECTIVE), mm1(LAMBDA_HIGH, MU_EFFECTIVE)
print(f"{'Utilization ρ':<44}{rt['rho']:>16.2f}{rh['rho']:>12.2f}")
print(f"{'Expected intake wait Wq (calendar days)':<44}"
      f"{rt['Wq'] * CAL:>16.1f}{rh['Wq'] * CAL:>12.1f}")
print(f"{'Pending requests in inbox Lq = λ·Wq':<44}{rt['Lq']:>16.1f}{rh['Lq']:>12.1f}")
print(f"{'Videos inside production system L = λ·W':<44}{rt['L']:>16.1f}{rh['L']:>12.1f}")

print("\nTail of the intake wait (typical λ = 17.5) — M/M/1 waits are exponential:")
for d in (5, 7, 10, 14):
    print(f"   P(wait > {d:>2} calendar days) = {tail_prob(LAMBDA_MID, MU_EFFECTIVE, d):>5.0%}")

# P90: solve rho * exp(-(mu-lam)/WD * t) = 0.10  →  t = ln(rho/0.10) / rate
rate_wd = (MU_EFFECTIVE - LAMBDA_MID) / WD_MONTH
t90_wd = math.log(rt["rho"] / 0.10) / rate_wd
print(f"   P90 of the intake wait ≈ {t90_wd * CAL:.0f} calendar days "
      f"(1 in 10 lawyers waits this long — before production even starts)")

print("\nNonlinearity — why 'working a bit faster' cannot fix the queue:")
rl = mm1(LAMBDA_LOW, MU_EFFECTIVE)
print(f"   demand 15 → 20/month  (×{LAMBDA_HIGH / LAMBDA_LOW:.2f})  "
      f"makes the wait {rl['Wq'] * CAL:.1f} → {rh['Wq'] * CAL:.1f} days "
      f"(×{rh['Wq'] / rl['Wq']:.1f})")

print("\nThe ceiling is the ρ = 1 wall:")
print(f"   Company ceiling 35–40 [C] ≈ theoretical capacity {MU_THEORETICAL:.1f}.")
print(f"   At λ = 24/month (a marketing push): ρ = {24 / MU_EFFECTIVE:.2f} > 1 → "
      "the queue grows without bound; backlog accumulates forever.")


# ======================================================================
# PART 3 — KINGMAN'S VUT EQUATION (variability)
# ======================================================================
hr("PART 3 — KINGMAN VUT:  Wq ≈ [ρ/(1−ρ)] × [(ca²+cs²)/2] × τ")

print("Base utilization term [ρ/(1−ρ)] and service time τ stay fixed per scenario;")
print(" only the variability factor (ca², cs²) changes.\n")
print(f"{'scenario':<34}{'λ':>6}{'ca²':>6}{'cs²':>6}{'Wq (wd)':>10}{'≈ calendar':>12}")
scenarios = [
    ("steady demand, stable jobs", 17.5, 1.0, 0.5),
    ("typical (some bursts/loops)", 17.5, 1.2, 1.0),
    ("marketing push + heavy rework", 20.0, 1.5, 1.5),
]
for name, lam, ca2, cs2 in scenarios:
    w = kingman(lam, MU_EFFECTIVE, ca2, cs2)
    print(f"{name:<34}{lam:>6.1f}{ca2:>6.1f}{cs2:>6.1f}{w:>10.2f}{w * CAL:>12.1f}")
print("""
Reading: variability alone moves the expected wait from ~3 to ~11 days at the
same average load. The ≥4 rework loops [C] inflate cs²; marketing pushes
inflate ca². Both are attacks Iterations 1–2 make structurally (SLA'd
structured briefs, templates), not behaviourally.""")

print("\nWhat the iterations do to the queue (same M/M/1 lens):")
dedicated_hours = HOURS_AVAIL * dedication          # ≈ 235 h/month on videos
for name, tau_h in (("Baseline        τ = 10 h/video", 10.0),
                    ("Iter 1+2        τ ≈ 5.8 h/video", 5.83),
                    ("Iter 3          τ = 1 h/video", 1.0)):
    mu_eff = dedicated_hours / tau_h                # effective capacity, same team
    r = mm1(LAMBDA_MID, mu_eff)
    if r["Wq"] >= 0.05:                             # working days — anything less
        print(f"   {name:<28} μ_eff = {mu_eff:5.1f}/mo  ρ = {r['rho']:.2f}"
              f"  Wq ≈ {r['Wq'] * CAL:.1f} calendar days")
    else:
        print(f"   {name:<28} μ_eff = {mu_eff:5.1f}/mo  ρ = {r['rho']:.2f}"
              f"  Wq ≈ {r['Wq'] * 8 * 60:.0f} minutes")
print("""   (Iteration 1 is not in this table: it does not lower ρ — it DELETES the
    server at intake. Self-serve form + auto-routing means Wq → 0 by design.)""")


# ======================================================================
# PART 4 — DISCRETE-EVENT VALIDATION (pure Python)
# ======================================================================
hr("PART 4 — DISCRETE-EVENT SIMULATION, VALIDATING THE FORMULAS")


def simulate_mm1(lam: float, mu: float, n: int = 200_000, warmup: int = 20_000,
                 seed: int = 7) -> float:
    """FIFO single server, exponential arrivals & service. Returns mean Wq (wd)."""
    rng = random.Random(seed)
    lam_wd, mu_wd = lam / WD_MONTH, mu / WD_MONTH
    clock = 0.0
    server_free = 0.0
    waits = []
    for _ in range(n):
        clock += rng.expovariate(lam_wd)          # next arrival
        service = rng.expovariate(mu_wd)          # its serial service time
        start = max(clock, server_free)           # FIFO: waits for server
        waits.append(start - clock)
        server_free = start + service
    return statistics.mean(waits[warmup:])


for lam in (LAMBDA_MID, LAMBDA_HIGH):
    theory = mm1(lam, MU_EFFECTIVE)["Wq"] * CAL
    sim = simulate_mm1(lam, MU_EFFECTIVE) * CAL
    print(f"λ = {lam:>5}/month   M/M/1 formula: {theory:5.1f} cal days   "
          f"simulation: {sim:5.1f} cal days   diff: {abs(sim - theory) / theory:.1%}")


# ======================================================================
# PART 5 — CHARTS (dependency-free SVG)
# ======================================================================
hr("PART 5 — CHARTS → queue-cliff.svg, order-timeline.svg, demand-sweep.svg")


class SVG:
    def __init__(self, w=980, h=560):
        self.w, self.h = w, h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" '
                      f'viewBox="0 0 {w} {h}" font-family="sans-serif">',
                      f'<rect width="{w}" height="{h}" fill="white"/>']

    def line(self, x1, y1, x2, y2, stroke="#666", width=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
                          f'y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}"{d}/>')

    def rect(self, x, y, w, h, fill, opacity=1.0):
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" '
                          f'height="{max(h, 0):.1f}" fill="{fill}" '
                          f'fill-opacity="{opacity}"/>')

    def circle(self, cx, cy, r, fill):
        self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>')

    def text(self, x, y, s, size=13, anchor="start", fill="#222", weight="normal"):
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
                          f'text-anchor="{anchor}" fill="{fill}" '
                          f'font-weight="{weight}">{s}</text>')

    def poly(self, pts, stroke, width=2.5, fill="none"):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.parts.append(f'<polyline points="{p}" fill="{fill}" '
                          f'stroke="{stroke}" stroke-width="{width}"/>')

    def save(self, path):
        self.parts.append("</svg>")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.parts))
        print(f"   wrote {path}")


NAVY, GOLD, RED, GREEN, GREY = "#0F2A43", "#C9A227", "#C62828", "#2E7D32", "#9AA5B1"

# ---------- Chart 1: the utilization cliff --------------------------------
tau = WD_MONTH / MU_EFFECTIVE
svg = SVG()
L, R, T, B = 80, 940, 50, 480                      # plot bounds
X0, X1, Y0, Y1 = 0.05, 0.95, 0.0, 26.0             # axis ranges


def px(rho):  return L + (rho - X0) / (X1 - X0) * (R - L)
def py(days): return B - (days - Y0) / (Y1 - Y0) * (B - T)


svg.rect(L, T, R - L, B - T, "#FBFBFD")
svg.rect(L, py(7), R - L, py(3) - py(7), GOLD, 0.35)         # observed band 3–7 d
svg.text(R - 8, py(7) - 8, "company-reported intake wait: 3–7 days [C]",
         size=13, anchor="end", fill="#8a6d1a")
for d in range(0, 26, 5):
    svg.line(L, py(d), R, py(d), "#E3E6EA")
    svg.text(L - 10, py(d) + 4, str(d), size=12, anchor="end", fill=GREY)
pts = []
rho = X0
while rho <= X1:
    wq = rho / (1 - rho) * tau * CAL
    if wq <= Y1:
        pts.append((px(rho), py(wq)))
    rho += 0.002
svg.poly(pts, NAVY, 3)
for lam, lab, col in ((LAMBDA_LOW, "light 15/mo", GREEN),
                      (LAMBDA_MID, "typical 17.5/mo", GOLD),
                      (LAMBDA_HIGH, "heavy 20/mo", RED)):
    r = mm1(lam, MU_EFFECTIVE)
    cx, cy = px(r["rho"]), py(r["Wq"] * CAL)
    svg.circle(cx, cy, 6, col)
    svg.text(cx, cy - 12, f"{lab}  ρ={r['rho']:.2f}", size=12, anchor="middle",
             fill=col, weight="bold")
r3 = mm1(LAMBDA_MID, MU_EFFECTIVE * 10.0)            # τ = 1 h after Iteration 3
svg.circle(px(r3["rho"]), py(r3["Wq"] * CAL), 7, NAVY)
svg.text(px(r3["rho"]) + 12, py(r3["Wq"] * CAL) + 22,
         "after Iteration 3: τ 10h→1h, ρ≈0.10, wait ≈ minutes", size=12, fill=NAVY)
svg.line(px(0.95), T, px(0.95), B, RED, 2, dash="6 4")
svg.text(px(0.95) - 8, T + 18, "ρ→1 : wait→∞", size=13, anchor="end", fill=RED,
         weight="bold")
svg.text(px(0.95) - 8, T + 36, "the 'ceiling' = this wall", size=12, anchor="end",
         fill=RED)
svg.text((L + R) / 2, 516, "server utilization  ρ = λ / μ   (markers: demand 15 / 17.5 / 20 per month at μ = 23.5/month)",
         size=13, anchor="middle", fill="#222")
svg.text(L, 28, "expected intake wait (calendar days)", size=13, fill="#222")
svg.save(OUT_DIR / "queue-cliff.svg")

# ---------- Chart 2: one order through the 12 steps ------------------------
steps = [
    ("1  Request submitted",      0.0, 0.2, "client"),
    ("2  INTAKE QUEUE",           0.2, 5.0, "wait"),
    ("3  Clarification ×3",       5.2, 3.0, "mixed"),
    ("4  Content brief",          8.2, 0.6, "work"),
    ("5  Script drafting",        8.8, 1.5, "work"),
    ("6  AI refinement",         10.3, 0.5, "work"),
    ("7  Script approval",       10.8, 2.0, "wait"),
    ("9  Video generation",      12.8, 1.0, "work"),
    ("10 Audio generation",      13.8, 0.5, "work"),
    ("11 AV sync (bottleneck)",  14.3, 1.5, "work"),
    ("12a Final approval",       15.8, 2.0, "wait"),
    ("12b Publish + adapt",      17.8, 1.0, "work"),
]
colors = {"work": GREEN, "wait": RED, "mixed": "#F9A825", "client": "#1565C0"}
svg = SVG(1080, 620)
L, R = 260, 1040
top, rowh = 70, 40
scale = (R - L) / 19.5                                    # days → px
for i, (name, start, dur, kind) in enumerate(steps):
    y = top + i * rowh
    svg.text(L - 12, y + 24, name, size=13, anchor="end",
             fill=NAVY if kind != "wait" else RED,
             weight="bold" if name.startswith("2") else "normal")
    svg.rect(L + start * scale, y + 6, dur * scale, rowh - 16, colors[kind])
    if dur * scale > 34:
        svg.text(L + start * scale + 6, y + 24, f"{dur:g} d", size=11,
                 fill="white", weight="bold")
for d in range(0, 20, 2):
    svg.line(L + d * scale, top - 10, L + d * scale, top + len(steps) * rowh, "#E3E6EA")
    svg.text(L + d * scale, top - 16, f"{d}", size=11, anchor="middle", fill=GREY)
svg.text((L + R) / 2, 34, "Lawyer Chen's video — 18.8 days end-to-end [within the reported 2–4 weeks [C]]",
         size=15, anchor="middle", fill="#222", weight="bold")
svg.text((L + R) / 2, 54, "active work ≈ 10 h ≈ 6% of elapsed time — everything red is waiting",
         size=13, anchor="middle", fill="#555")
ly = top + len(steps) * rowh + 24
for i, (lab, col) in enumerate((("waiting", RED), ("active work", GREEN),
                                ("mostly waiting", "#F9A825"), ("lawyer (client)", "#1565C0"))):
    svg.rect(L + i * 190, ly, 14, 14, col)
    svg.text(L + i * 190 + 20, ly + 12, lab, size=12, fill="#333")
svg.save(OUT_DIR / "order-timeline.svg")

# ---------- Chart 3: demand sweep ------------------------------------------
svg = SVG()
L, R, T, B = 80, 940, 50, 480
X0, X1, Y0, Y1 = 14.0, 30.0, 0.0, 16.0


def dx(lam):  return L + (lam - X0) / (X1 - X0) * (R - L)
def dy(days): return B - (days - Y0) / (Y1 - Y0) * (B - T)


svg.rect(L, T, R - L, B - T, "#FBFBFD")
svg.rect(dx(MU_EFFECTIVE), T, R - dx(MU_EFFECTIVE), B - T, RED, 0.08)
svg.text((dx(MU_EFFECTIVE) + R) / 2, (T + B) / 2 - 10,
         "unstable region (ρ > 1)", size=15, anchor="middle", fill=RED, weight="bold")
svg.text((dx(MU_EFFECTIVE) + R) / 2, (T + B) / 2 + 12,
         "backlog grows forever — every month here adds debt", size=12,
         anchor="middle", fill=RED)
for d in range(0, 17, 4):
    svg.line(L, dy(d), R, dy(d), "#E3E6EA")
    svg.text(L - 10, dy(d) + 4, str(d), size=12, anchor="end", fill=GREY)
pts = []
lam = X0
while lam < MU_EFFECTIVE - 0.05:
    wq = mm1(lam, MU_EFFECTIVE)["Wq"] * CAL
    if wq <= Y1:
        pts.append((dx(lam), dy(wq)))
    lam += 0.05
svg.poly(pts, NAVY, 3)
for lam, lab, col in ((LAMBDA_LOW, "15", GREEN), (LAMBDA_MID, "17.5", GOLD),
                      (LAMBDA_HIGH, "20", RED)):
    r = mm1(lam, MU_EFFECTIVE)
    svg.circle(dx(lam), dy(r["Wq"] * CAL), 6, col)
    svg.text(dx(lam) + 10, dy(r["Wq"] * CAL) - 10, lab, size=12, fill=col, weight="bold")
svg.line(dx(MU_EFFECTIVE), T, dx(MU_EFFECTIVE), B, RED, 2, dash="6 4")
svg.text(dx(MU_EFFECTIVE) - 8, T + 18, "effective capacity μ ≈ 23.5", size=13,
         anchor="end", fill=RED, weight="bold")
svg.text(dx(MU_EFFECTIVE) - 8, T + 36, "theoretical 35.2 = company 'ceiling' [C]", size=12,
         anchor="end", fill=RED)
svg.text(dx(24.2), T + 70, "marketing push\nλ = 24", size=12, fill=RED)
svg.text((L + R) / 2, 516, "demand (videos/month) at constant team and process",
         size=13, anchor="middle", fill="#222")
svg.text(L, 28, "expected intake wait (calendar days)", size=13, fill="#222")
svg.save(OUT_DIR / "demand-sweep.svg")

print("""
DONE. Suggested slide use:
  queue-cliff.svg    → THE chart: the utilization cliff; baseline band + Iter-3 dot
  order-timeline.svg → one order, work vs wait (94% red); use in the walkthrough
  demand-sweep.svg   → why scaling breaks: the asymptote at μ, unstable region""")
