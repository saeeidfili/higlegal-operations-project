"""Measurement helpers for the existing simulations, not a new process model.

All rates use 22 working days / 30.4 calendar days per model month.
Keep offered workload, realised busy time, cohort outcomes and time-window
throughput distinct. Finite-horizon completed cohorts are not steady-state
estimates when the offered workload exceeds capacity or arrivals are censored.
"""
import math
import statistics

WD_MONTH = 22.0
CAL = 30.4 / WD_MONTH

def measure(sim, start, end, horizon, expected_minutes, minutes_per_day,
            arrival_rate, owners=2, absent_days=0.0):
    videos = sim.videos
    cohort = [v for v in videos if start <= v.arrival < end]
    complete = [v for v in cohort if v.delivered is not None]
    missing = len(cohort) - len(complete)
    months = (end-start)/WD_MONTH
    budget = (owners*(end-start)-absent_days)*minutes_per_day
    def overlap(a,b): return max(0.0,min(b,end)-max(a,start))
    wip_area = sum(overlap(v.arrival,v.delivered if v.delivered is not None else horizon) for v in videos)
    busy = sum(overlap(a,b) for v in videos for a,b,_,kind in v.segments if kind=='work')
    completed_in_window = sum(v.delivered is not None and start <= v.delivered < end for v in videos)
    def count_at(t): return sum(v.arrival <= t and (v.delivered is None or v.delivered > t) for v in videos)
    capacity = owners*WD_MONTH*minutes_per_day/expected_minutes
    rho = arrival_rate/capacity
    leads=[(v.delivered-v.arrival)*CAL for v in complete]
    return dict(window_start_working_day=start, window_end_working_day=end,
                horizon_working_day=horizon, configured_arrivals_per_month=arrival_rate,
                available_minutes_in_window=budget,
                expected_work=expected_minutes, capacity=capacity,
                offered_util=rho, busy_util=busy/(owners*(end-start)),
                available_util=busy/budget if budget else math.nan,
                stable=rho < 1, censored=missing, cohort_size=len(cohort),
                cohort_completed=len(complete),
                throughput=completed_in_window/months,
                mean_wip=wip_area/(end-start),
                wip_start=count_at(start),wip_end=count_at(end),
                wip_growth=(count_at(end)-count_at(start))/months,
                completed_cohort_lead=statistics.mean(leads) if leads else math.nan,
                # Retain diagnostics, but label overload/censoring explicitly.
                lead_status='overload: no stationary mean' if rho>=1 else ('censored cohort' if missing else 'stable, complete cohort'))
