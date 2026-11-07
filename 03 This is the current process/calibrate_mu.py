"""Calibrate mu by fitting the whole observed wait band, not one anchor.

Observed: Wq ~3 d at lambda=15, ~7 d at lambda=20 [C].
Method 1: pin each anchor separately (gives the bracket 22.0 - 23.7).
Method 2: least squares on both anchors, mu constrained to that bracket:
          min (Wq(15)-3)^2 + (Wq(20)-7)^2, solved by ternary search.
Run:   python3 calibrate_mu.py
"""

WD_PER_MONTH = 22
CAL = 1.4  # calendar days per working day
OBSERVED = {15.0: 3.0, 20.0: 7.0}  # lambda -> observed Wq [C]


def wq_days(lam: float, mu: float) -> float:
    """Expected intake wait, calendar days."""
    return lam / (mu - lam) * WD_PER_MONTH / mu * CAL


def calibrate(lam: float, target_days: float) -> float:
    """Solve wq_days(lam, mu) = target_days for mu (quadratic)."""
    b = CAL * WD_PER_MONTH * lam / target_days
    return (lam + (lam * lam + 4 * b) ** 0.5) / 2


def sse(mu: float) -> float:
    """Squared error of the predicted wait interval vs the observed band."""
    return sum((wq_days(lam, mu) - t) ** 2 for lam, t in OBSERVED.items())


def optimize(lo: float, hi: float, iters: int = 200) -> float:
    """Ternary search: minimize sse(mu) on [lo, hi]."""
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if sse(m1) <= sse(m2):
            hi = m2
        else:
            lo = m1
    return (lo + hi) / 2


def test(name: str, mu: float) -> None:
    print(f"\n{name}: mu = {mu:.2f}/month")
    observed = {15.0: "~3 d", 17.5: "3-7 d", 20.0: "~7 d"}
    for lam, obs in observed.items():
        w = wq_days(lam, mu)
        inside = 2.3 <= w <= 7.5
        print(f"  lambda={lam:<5} rho={lam/mu:.2f}  Wq={w:4.1f} d   observed {obs}  {'OK' if inside else 'OUT'}")


if __name__ == "__main__":
    # anchors -> bracket
    mu_lo = calibrate(15, 3)   # pin 3 d at lambda=15
    mu_hi = calibrate(20, 7)   # pin 7 d at lambda=20
    print(f"Bracket: pin(3,15) = {mu_lo:.2f}  <=  mu  <=  pin(7,20) = {mu_hi:.2f}")

    # optimize inside the bracket
    mu_opt = optimize(mu_lo, mu_hi)
    assert mu_lo <= mu_opt <= mu_hi
    assert sse(mu_opt) <= min(sse(mu_lo), sse(mu_hi)) + 1e-12
    test("Optimized (fit 3 d and 7 d)", mu_opt)

    print(f"\nConclusion: mu = {mu_opt:.2f}/month  (sse = {sse(mu_opt):.3f})")
    print(f"  endpoints: Wq(15) = {wq_days(15, mu_opt):.2f} d vs 3,  Wq(20) = {wq_days(20, mu_opt):.2f} d vs 7")
