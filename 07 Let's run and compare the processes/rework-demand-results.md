# Rework x demand: existing engine, three seeds

All inputs below are modelling assumptions, not measured gate rates. Capacity is expected work-content capacity. Busy utilization and WIP use the same post-warm-up time window; throughput counts departures in that window.
Working month = 22 days, calendar month = 30.4 days. Lead is the full arrival-cohort mean only when all cohort arrivals finish and offered utilization is below one. Otherwise the completed-only diagnostic is withheld from the lead column. WIP growth is a finite-horizon diagnostic, not a stationary law.

| Rework | Demand/mo | Work min/video | Workload h/mo | Capacity/mo | Offered util | Busy util | Throughput/mo | Mean WIP | WIP growth/mo | Lead cal d | Cohort completion |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| no rework | 15 | 516.00 | 129.00 | 27.42 | 54.7% | 54.3% | 14.86 | 5.17 | -0.02 | 10.56 | 100.0% |
| no rework | 17.5 | 516.00 | 150.50 | 27.42 | 63.8% | 61.8% | 16.98 | 6.16 | -0.02 | 11.03 | 100.0% |
| no rework | 20 | 516.00 | 172.00 | 27.42 | 72.9% | 72.1% | 19.71 | 7.61 | 0.10 | 11.68 | 100.0% |
| no rework | 22 | 516.00 | 189.20 | 27.42 | 80.2% | 79.8% | 21.92 | 8.88 | -0.24 | 12.33 | 100.0% |
| no rework | 25 | 516.00 | 215.00 | 27.42 | 91.2% | 95.8% | 26.16 | 22.56 | 0.43 | 25.83 | 100.0% |
| baseline | 15 | 599.17 | 149.79 | 23.62 | 63.5% | 63.6% | 15.00 | 10.25 | -0.10 | 20.87 | 100.0% |
| baseline | 17.5 | 599.17 | 174.76 | 23.62 | 74.1% | 73.3% | 17.22 | 12.65 | 0.25 | 22.05 | 100.0% |
| baseline | 20 | 599.17 | 199.72 | 23.62 | 84.7% | 85.3% | 20.08 | 15.27 | 0.02 | 23.12 | 100.0% |
| baseline | 22 | 599.17 | 219.69 | 23.62 | 93.2% | 91.8% | 21.71 | 20.39 | -0.75 | 28.52 | 100.0% |
| baseline | 25 | 599.17 | 249.65 | 23.62 | 105.9% | 99.7% | 22.86 | 72.09 | 1.71 | overload | 93.9% |
| heavy | 15 | 686.33 | 171.58 | 20.62 | 72.8% | 75.6% | 15.57 | 14.85 | -0.29 | 29.18 | 100.0% |
| heavy | 17.5 | 686.33 | 200.18 | 20.62 | 84.9% | 83.0% | 16.84 | 16.84 | 0.24 | 30.20 | 100.0% |
| heavy | 20 | 686.33 | 228.78 | 20.62 | 97.0% | 96.5% | 19.65 | 35.31 | 0.55 | censored | 99.5% |
| heavy | 22 | 686.33 | 251.66 | 20.62 | 106.7% | 100.0% | 19.63 | 81.04 | 3.76 | overload | 86.9% |
| heavy | 25 | 686.33 | 285.97 | 20.62 | 121.3% | 100.0% | 18.80 | 164.50 | 6.39 | overload | 62.3% |

Analytical link: workload = demand x E[work]; capacity = 14,150.4 / E[work]; offered utilization = demand / capacity. Rework increases both required labour and repeated client waits. At demand >= capacity, report backlog growth, not an infinite-horizon mean lead. Little law requires consistent units and a stable common boundary; it is not applied to the overloaded rows.

These simulations quantify conditional consequences of assumed rates. They do not identify real rejection rates or independently validate proposed improvements.
