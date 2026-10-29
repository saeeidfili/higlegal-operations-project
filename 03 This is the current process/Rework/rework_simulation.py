#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rework and the queue — full-process discrete-event simulation
==============================================================
Section 3 annex: "Rework" (Operations Management project, HiLegal)

Question: what does rework actually do to queues, lead time and capacity?

Model of the WHOLE content-production process (the 12 steps), not just intake:
  * Poisson arrivals (demand λ, videos/month).
  * Two producers form ONE pooled task pool (the "team as a processing unit"):
    any producer takes the next available work task; no task is preempted.
  * Every video flows independently through the 12 steps: work tasks
    (producer busy) alternating with client-gate waits (producer free).
  * Three looping gates, matching the process map:
      Gate 1 Clarification   -> loops back to intake (baseline mean ~4 rounds [C])
      Gate 2 Script approval -> loops back to drafting
      Gate 3 Final approval  -> loops back into production (partial redo)
  * Work durations are effective working days: minutes / (480 x 0.67),
    where 0.67 reflects that producers also do platform work (~33% of time).
  * The model is work-conserving: idle producers take queued work immediately.
    This means the simulated intake wait is a LOWER BOUND — the real batching
    policy (producers checking the inbox between videos) makes it longer,
    as the M/M/1 analysis in queueing-model.md shows.

Scenarios (rework intensity):
  no rework | rework halved | baseline (~90% of videos loop) | heavy rework

Outputs: console tables + four SVG charts written next to this script.

Run:  python3 rework_simulation.py
"""

import heapq
import random
import statistics
from collections import deque
from pathlib import Path

OUT = Path(__file__).resolve().parent

WD_MONTH = 22.0           # working days per month
MIN_PER_DAY = 480 * 0.67  # effective owner-minutes per day (~322; 33% platform work)
CAL = 30.4 / 21.7         # calendar days per working day (~1.40)
MONTHS = 28
WARMUP_MONTHS = 10

# ----------------------------------------------------------------------
# Simulation engine
# ----------------------------------------------------------------------
class Sim:
    def __init__(self, params, lam_per_month, seed=7):
        self.t = 0.0
        self.events = []
        self.seq = 0
        self.rng = random.Random(seed)
        self.params = params
        self.lam_wd = lam_per_month / WD_MONTH
        self.intake = deque()        # requests not yet picked up (first task)
        self.work_queue = deque()    # work tasks waiting for a producer
        self.finished = []
        self.series = []             # (t, intake_len, wip)
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
                 "waits", "clar_rounds", "script_loops", "final_loops",
                 "segments")

    def __init__(self, vid, arrival):
        self.vid = vid
        self.arrival = arrival
        self.first_work = None
        self.delivered = None
        self.work = 0.0
        self.waits = 0.0
        self.clar_rounds = 0
        self.script_loops = 0
        self.final_loops = 0
        self.segments = []          # (start, end, label, kind)


class Owner:
    def __init__(self, sim):
        self.sim = sim
        self.busy = False
        self.busy_days = 0.0
        self.work_minutes = 0.0


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
        owner.work_minutes += minutes
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
# One video through the 12 steps (generator of work/wait actions)
# ----------------------------------------------------------------------
def video_steps(sim, video, p):
    def work(minutes, label):
        return ("work", minutes, label)

    def wait(days, label):
        return ("wait", days, label)

    yield work(15, "intake review")
    while True:
        video.clar_rounds += 1
        yield wait(sim.rng.uniform(1, 2), "clarification wait")
        yield work(8, "clarification reply")
        if sim.rng.random() >= p["p_clar"]:
            break

    yield work(45, "content brief")
    while True:
        yield work(70, "script drafting")
        yield work(35, "AI refinement")
        yield wait(sim.rng.uniform(1, 3), "script approval")
        if sim.rng.random() >= p["p_script"]:
            break
        video.script_loops += 1
        yield work(50, "script rework")

    yield work(55, "video generation")
    yield work(30, "audio generation")
    yield work(140, "AV sync")
    while True:
        yield wait(sim.rng.uniform(1, 3), "final approval")
        if sim.rng.random() >= p["p_final"]:
            break
        video.final_loops += 1
        yield work(70, "final rework")

    yield work(95, "platform adaptation")
    yield work(23, "delivery & admin")


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
        video.waits += days
        video.segments.append((sim.t, sim.t + days, label, "wait"))
        sim.schedule(days, lambda: drive(sim, video, gen))


# ----------------------------------------------------------------------
# Scenario runner
# ----------------------------------------------------------------------
def run_scenario(name, params, lam=17.5, months=MONTHS, seed=7,
                 warmup=WARMUP_MONTHS):
    sim = Sim(params, lam, seed)
    sim.owners = [Owner(sim), Owner(sim)]

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

    t0 = warmup * WD_MONTH
    window = [v for v in sim.finished
              if v.arrival >= t0 and v.delivered is not None]
    window_months = months - warmup

    leads = [(v.delivered - v.arrival) * CAL for v in window]
    intake_waits = [((v.first_work or v.arrival) - v.arrival) * CAL
                    for v in window]
    works = [v.work for v in window]
    loops = [1 if (v.clar_rounds > 1 or v.script_loops or v.final_loops) else 0
             for v in window]
    util = sum(o.busy_days for o in sim.owners) / (2 * months * WD_MONTH)

    series = [(t, wip) for (t, _q, wip) in sim.series if t >= t0]
    mean_wip = statistics.mean([w for _, w in series]) if series else float("nan")

    return dict(
        name=name, leads=leads, intake_waits=intake_waits, works=works,
        loops=loops, util=util, mean_wip=mean_wip,
        throughput=len(window) / window_months,
        mean_lead=statistics.mean(leads) if leads else float("nan"),
        p90_lead=(sorted(leads)[int(0.9 * len(leads))] if leads else float("nan")),
        mean_wait=statistics.mean(intake_waits) if intake_waits else float("nan"),
        mean_work=statistics.mean(works) if works else float("nan"),
        rework_share=statistics.mean(loops) if loops else float("nan"),
        series=series,
        videos=window,
    )


SCENARIOS = [
    ("no rework", dict(p_clar=0.0, p_script=0.0, p_final=0.0)),
    ("rework halved", dict(p_clar=0.50, p_script=0.15, p_final=0.15)),
    ("baseline (~90% rework)", dict(p_clar=0.75, p_script=0.30, p_final=0.30)),
    ("heavy rework", dict(p_clar=0.80, p_script=0.50, p_final=0.50)),
]


def main():
    print("=" * 80)
    print("REWORK AND THE QUEUE — full-process discrete-event simulation")
    print("=" * 80)
    print(f"Demand λ = 17.5 videos/month · 2 producers (pooled) · {MONTHS} months, "
          f"last {MONTHS - WARMUP_MONTHS} measured\n")

    results = []
    header = (f"{'scenario':<26}{'lead d':>8}{'P90 d':>8}{'intake d':>10}"
              f"{'work min':>10}{'rework':>8}{'out/mo':>8}{'util':>7}")
    print(header)
    print("-" * len(header))
    for name, params in SCENARIOS:
        r = run_scenario(name, params)
        results.append(r)
        print(f"{name:<26}{r['mean_lead']:>8.1f}{r['p90_lead']:>8.1f}"
              f"{r['mean_wait']:>10.1f}{r['mean_work']:>10.0f}"
              f"{r['rework_share']:>7.0%}{r['throughput']:>8.1f}"
              f"{r['util']:>7.0%}")

    print("\nInterpretation:")
    base = next(r for r in results if "baseline" in r["name"])
    no = next(r for r in results if "no rework" in r["name"])
    print(f"  * removing rework cuts lead time {base['mean_lead']:.1f} -> "
          f"{no['mean_lead']:.1f} days and work {base['mean_work']:.0f} -> "
          f"{no['mean_work']:.0f} min")
    print(f"  * baseline rework incidence {base['rework_share']:.0%} — worth "
          f"~{base['mean_lead'] - no['mean_lead']:.1f} days of waiting")

    # ------------------------------------------------------------------
    # Demand sweep: rework x demand interaction
    # ------------------------------------------------------------------
    print("\nDemand sweep (mean lead time days / mean WIP videos):")
    lambdas = [15.0, 17.5, 20.0, 22.0]
    levels = [("no rework", SCENARIOS[0][1]),
              ("baseline", SCENARIOS[2][1]),
              ("heavy", SCENARIOS[3][1])]
    sweep = {}
    print(f"{'λ':>5}" + "".join(f"{n:>18}" for n, _ in levels))
    for lam in lambdas:
        row = []
        for name, params in levels:
            runs = [run_scenario(name, params, lam=lam, months=36, warmup=16,
                                 seed=s) for s in (11, 12, 13)]
            row.append((statistics.mean(r["mean_lead"] for r in runs),
                        statistics.mean(r["mean_wip"] for r in runs)))
        sweep[lam] = row
        print(f"{lam:>5.1f}" + "".join(f"{a:>10.1f} /{b:>6.1f}" for a, b in row))

    # WIP sample paths at 22/month (past the current ceiling)
    queue_runs = [run_scenario(name, params, lam=22.0, months=36, warmup=14,
                               seed=13)
                  for name, params in ((levels[0][0], levels[0][1]),
                                       (levels[1][0], levels[1][1]),
                                       (levels[2][0], levels[2][1]))]

    make_impact_chart(results)
    make_queue_chart(queue_runs)
    make_sweep_chart(lambdas, levels, sweep)
    make_gantt_chart(results)
    print("\nCharts written: rework-impact.svg, queue-sample-path.svg, "
          "rework-vs-demand.svg, gantt-rework.svg")


# ----------------------------------------------------------------------
# SVG helpers
# ----------------------------------------------------------------------
class SVG:
    def __init__(self, w=1000, h=560):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'font-family="Arial, Helvetica, sans-serif">',
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>']

    def line(self, x1, y1, x2, y2, stroke="#666", width=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
                          f'y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}"{d}/>')

    def rect(self, x, y, w, h, fill, opacity=1.0, stroke=None):
        s = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" '
                          f'height="{max(h, 0):.1f}" fill="{fill}" '
                          f'fill-opacity="{opacity}"{s}/>')

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

    def save(self, name):
        self.parts.append("</svg>")
        (OUT / name).write_text("\n".join(self.parts), encoding="utf-8")
        print(f"   wrote {name}")


NAVY, GOLD, RED, GREEN, GREY, DARKRED = ("#0F2A43", "#C9A227", "#C62828",
                                         "#2E7D32", "#9AA5B1", "#7B1F1F")


def make_impact_chart(results):
    svg = SVG(1020, 560)
    svg.text(40, 40, "Rework vs. lead time and work content", 19, fill=NAVY,
             weight="bold")
    svg.text(40, 62, "same process, same two producers, same demand "
             "(17.5 videos/month)", 13, fill="#6B7785")

    L, R, T, B = 60, 480, 110, 470
    ymax = max(r["p90_lead"] for r in results) * 1.15
    svg.text(60, T - 14, "lead time (calendar days)", 13, fill="#222")
    for i in range(0, int(ymax) + 1, 10):
        y = B - i / ymax * (B - T)
        svg.line(L - 6, y, L, y, "#C9CED6")
        svg.text(L - 10, y + 4, str(i), 11, anchor="end", fill=GREY)
    bw = (R - L) / len(results) * 0.55
    for i, r in enumerate(results):
        x = L + (i + 0.5) * (R - L) / len(results) - bw / 2
        h = r["mean_lead"] / ymax * (B - T)
        color = [GREY, GREEN, GOLD, RED][i]
        svg.rect(x, B - h, bw, h, color)
        svg.text(x + bw / 2, B - h - 8, f"{r['mean_lead']:.1f}", 12,
                 anchor="middle", fill="#222", weight="bold")
        svg.line(x, B - r["p90_lead"] / ymax * (B - T), x + bw,
                 B - r["p90_lead"] / ymax * (B - T), DARKRED, 2)
        svg.text(x + bw / 2, B + 34 + (i % 2) * 16,
                 r["name"].replace(" (~90% rework)", ""), 11,
                 anchor="middle", fill="#333")
    svg.text(L, B + 78, "bar = mean lead time · tick = P90", 11, fill=GREY)

    L2, R2 = 560, 980
    wmax = 820
    svg.text(L2, T - 14, "hands-on work per video (minutes)", 13, fill="#222")
    for i, r in enumerate(results):
        y = T + 30 + i * 78
        w = r["mean_work"] / wmax * (R2 - L2)
        color = [GREY, GREEN, GOLD, RED][i]
        svg.rect(L2, y, w, 30, color)
        svg.text(L2 + 8, y + 20,
                 f"{r['mean_work']:.0f} min · rework {r['rework_share']:.0%}",
                 12, fill="white", weight="bold")
        svg.text(L2, y - 8, r["name"].replace(" (~90% rework)", ""), 12,
                 fill="#333")
    svg.text(L2, 474, "10 h ≈ 600 min (company-reported baseline [C])", 11,
             fill=GREY)
    svg.text(L2, 496, "rework adds minutes AND loops that add waits —", 11,
             fill=GREY)
    svg.text(L2, 514, "the queue cost is larger than the work cost", 11,
             fill=GREY)
    svg.save("rework-impact.svg")


def make_queue_chart(runs):
    svg = SVG(1020, 500)
    svg.text(40, 36, "Videos in the system (WIP) at 22 per month — rework builds a backlog",
             16.5, fill=NAVY, weight="bold")
    svg.text(40, 58, "last 20 simulated months · videos in process, sampled every "
             "half working day · smoothed", 12, fill="#6B7785")

    L, R, T, B = 70, 980, 100, 410
    colors = [GREEN, GOLD, RED]
    ymax = max(max(q for _, q in r["series"]) for r in runs) * 1.08 or 1
    step = 10 if ymax < 80 else 20
    for i in range(0, int(ymax) + 1, step):
        y = B - i / ymax * (B - T)
        svg.line(L, y, R, y, "#E9ECEF")
        svg.text(L - 10, y + 4, str(i), 11, anchor="end", fill=GREY)
    tmin = runs[0]["series"][0][0]
    tmax = runs[0]["series"][-1][0]
    for (r, color) in zip(runs, colors):
        vals = [q for _, q in r["series"]]
        pts = r["series"]
        smooth = []
        for i in range(len(vals)):
            lo, hi = max(0, i - 4), min(len(vals), i + 5)
            smooth.append((pts[i][0], sum(vals[lo:hi]) / (hi - lo)))
        poly = [(L + (t - tmin) / (tmax - tmin) * (R - L),
                 B - min(v, ymax) / ymax * (B - T)) for t, v in smooth]
        svg.poly(poly, color, 2.2)
    ly = 440
    for i, (r, color) in enumerate(zip(runs, colors)):
        x = 70 + i * 310
        svg.rect(x, ly, 16, 16, color)
        svg.text(x + 24, ly + 13, r["name"].replace(" (~90% rework)", ""), 12,
                 fill="#333")
    total_months = (tmax - tmin) / WD_MONTH
    for m in range(0, int(total_months) + 1, 4):
        x = L + m / total_months * (R - L)
        svg.line(x, B, x, B + 6, "#9AA5B1")
        svg.text(x, B + 22, f"{m}", 11, anchor="middle", fill=GREY)
    svg.text(70, B + 62, "months into the 20-month window →", 12, fill="#222")
    svg.text(70, T - 12, "videos in the system (work in progress)", 12, fill="#222")
    svg.save("queue-sample-path.svg")


def make_sweep_chart(lambdas, levels, sweep):
    svg = SVG(1020, 540)
    svg.text(40, 38, "Rework × demand: where work-in-process explodes", 18,
             fill=NAVY, weight="bold")
    svg.text(40, 60, "mean videos in the system over the last 12 months · same "
             "two producers", 12, fill="#6B7785")
    L, R, T, B = 80, 960, 110, 440
    ymax = max(b for lam in lambdas for (_a, b) in sweep[lam]) * 1.1
    step = 10 if ymax < 80 else 20
    for d in range(0, int(ymax) + 1, step):
        y = B - d / ymax * (B - T)
        svg.line(L, y, R, y, "#E9ECEF")
        svg.text(L - 10, y + 4, str(d), 11, anchor="end", fill=GREY)
    colors = [GREEN, GOLD, RED]
    for j, (name, _) in enumerate(levels):
        pts = []
        for lam in lambdas:
            v = min(sweep[lam][j][1], ymax)
            pts.append((L + (lam - 14) / (23 - 14) * (R - L),
                        B - v / ymax * (B - T)))
        svg.poly(pts, colors[j], 2.6)
        for lam, (x, y) in zip(lambdas, pts):
            svg.circle(x, y, 5, colors[j])
        svg.text(940, 120 + j * 22, name, 13, anchor="end", fill=colors[j],
                 weight="bold")
    svg.text((L + R) / 2, B + 46, "demand λ (videos/month)", 13,
             anchor="middle", fill="#222")
    svg.text(L, T - 16, "mean videos in the system (WIP)", 12, fill="#222")
    svg.text(L, B + 78, "Interpretation: without rework the process absorbs "
             "22/month; baseline degrades steeply past ~20;", 12, fill="#333")
    svg.text(L, B + 96, "heavy rework hits the capacity wall early — demand "
             "that was manageable becomes a backlog.", 12, fill="#333")
    svg.save("rework-vs-demand.svg")


def make_gantt_chart(results):
    base = next(r for r in results if "baseline" in r["name"])
    no = next(r for r in results if "no rework" in r["name"])

    def pick(r):
        vids = sorted(r["videos"], key=lambda v: v.delivered - v.arrival)
        return vids[len(vids) // 2]

    v_base = pick(base)
    v_no = pick(no)
    svg = SVG(1120, 480)
    svg.text(40, 40, "One order, two worlds — where rework time actually goes",
             18, fill=NAVY, weight="bold")
    svg.text(40, 62, "median order of each scenario · coloured blocks = elapsed "
             "time per step (work vs waiting) · calendar days", 12, fill="#6B7785")

    rows = [("first-time right (no rework)", v_no, 110),
            ("with rework (baseline)", v_base, 250)]
    L, R = 300, 1080
    tmax = max((v.delivered - v.arrival) * CAL for _, v, _ in rows) + 2

    for label, v, y in rows:
        svg.text(L - 16, y + 22, label, 13, anchor="end", fill="#333",
                 weight="bold")
        intake = ((v.first_work or v.arrival) - v.arrival) * CAL
        svg.rect(L, y, intake / tmax * (R - L), 30, "#5C7A99")
        if intake > 2:
            svg.text(L + 6, y + 20, "intake queue", 11, fill="white")
        for (s, e, lab, kind) in v.segments:
            x = L + (s - v.arrival) * CAL / tmax * (R - L)
            w = (e - s) * CAL / tmax * (R - L)
            if kind == "work":
                color = DARKRED if "rework" in lab else GREEN
            else:
                color = GOLD if "clarification" in lab else RED
            svg.rect(x, y, max(w, 1.5), 30, color, 0.92)
    for d in range(0, int(tmax) + 1, 5):
        x = L + d / tmax * (R - L)
        svg.line(x, 90, x, 320, "#E3E6EA")
        svg.text(x, 88, str(d), 11, anchor="middle", fill=GREY)
    ly = 370
    for i, (lab, col) in enumerate((("active work", GREEN),
                                    ("rework (extra work)", DARKRED),
                                    ("approval wait", RED),
                                    ("clarification wait", GOLD),
                                    ("intake queue", "#5C7A99"))):
        x = 70 + i * 200
        svg.rect(x, ly, 16, 16, col)
        svg.text(x + 24, ly + 13, lab, 12, fill="#333")
    svg.text(70, ly + 44, "Same process, same product — rework adds loops that "
             "each bring their own waiting.", 12, fill="#333")
    svg.save("gantt-rework.svg")


if __name__ == "__main__":
    main()
