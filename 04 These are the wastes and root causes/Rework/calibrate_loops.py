"""Calibrate the gate loop probabilities with p_final > p_script.

Rationale: failing at the last gate (final approval, after the video is
rendered) is more likely than failing the script gate - the client sees the
actual product only at the end.

Reported anchors [C], with an estimated geometric interpretation [E]:
  - ~10 h = 600 min total work per video (incl. rework)
  - >= 4 clarification rounds -> p_clar = 0.75 (geometric mean 1/(1-p))

Given p_clar and a chosen p_script, the 600-min anchor pins p_final:
  first-time-right work        = 516 min
  extra clarification replies  = (4-1) x 8 min        = 24 min
  script loops                 = 50 x p_s/(1-p_s) min
  final loops                  = 70 x p_f/(1-p_f) min
  budget for script+final      = 600 - 516 - 24       = 60 min
  -> solve 70 r/(1-r) = C  ->  r = C/(70+C)

Run: python3 calibrate_loops.py
"""

WD = 22


def loops(p: float) -> float:
    """Expected number of loops at a gate with loop probability p."""
    return p / (1 - p)


def solve_p(loop_cost_min: float, budget_min: float) -> float:
    """Solve loop_cost_min * r/(1-r) = budget_min for r."""
    return budget_min / (loop_cost_min + budget_min)


def calibrate(p_clar: float, p_script: float, verbose: bool = True) -> dict:
    """p_clar and p_script chosen; p_final solved from the 600-min anchor."""
    ftr = 516.0                     # first-time-right minutes (12 tasks)
    clar_rounds = 1 / (1 - p_clar)  # geometric mean rounds
    clar_extra = (clar_rounds - 1) * 8
    budget = 600 - ftr - clar_extra          # minutes left for script+final loops
    script_min = 50 * loops(p_script)
    final_budget = budget - script_min
    p_final = solve_p(70, final_budget)

    work = ftr + clar_extra + script_min + 70 * loops(p_final)
    incidence = 1 - (1 - p_clar) * (1 - p_script) * (1 - p_final)

    if verbose:
        print(f"p_clar = {p_clar:.2f} -> mean {clar_rounds:.0f} rounds [E representative assumption], "
              f"extra replies {clar_extra:.0f} min")
        print(f"p_script = {p_script:.2f} -> script loops {script_min:.1f} min")
        print(f"budget for final loops = {final_budget:.1f} min "
              f"-> p_final = {p_final:.3f}")
        print(f"E[work]  = {work:.1f} min  (anchor 600 [C])")
        print(f"incidence = {incidence:.1%}  (our approximate 90% modelling estimate [E])\n")
    return dict(p_clar=p_clar, p_script=p_script, p_final=p_final,
                work=work, incidence=incidence)


if __name__ == "__main__":
    # p_final roughly 2x p_script: late-stage rejection is the likelier one
    for ps in (0.15, 0.20, 0.25):
        print(f"--- p_script = {ps:.2f} ---")
        r = calibrate(0.75, ps)
        assert abs(r["work"] - 600) < 0.1
        assert r["p_final"] > r["p_script"]
        assert 0.80 < r["incidence"] < 0.95
