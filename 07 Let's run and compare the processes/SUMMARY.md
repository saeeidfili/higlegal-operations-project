# Section 7: compare and stress-test the proposed process

The existing Section-4 event engine is retained through the Iteration-3 lineage. Proposed task times, rejection probabilities and waits remain assumptions, not measured improvements. Results are generated in `scenario-results.md`; the joint workload/queue experiment is in `rework-demand-results.md` with machine-readable records in `rework-demand-results.json`.

## Common measurement basis

Two producers share a FIFO task queue. A producer is free for other videos during client waits. Work tasks have deterministic durations; client/machine waits use uniform ranges, and arrivals are Poisson. The month has 22 working days and 30.4 calendar days. Weekend and holiday scheduling is not explicitly modelled.

WIP is integrated exactly over the same post-warm-up time window used to count departures. Throughput counts departures in that window, not completed arrival-cohort members divided by the arrival-window length. The arrival cohort retains its completion count; uncompleted arrivals are flagged, not silently discarded. Work-content capacity uses expected work including rework rather than completed-survivor work. Offered utilization is demand/capacity; observed busy utilization is reported separately.

The main comparison uses 36 months, 16 months warm-up, a 3-month cutoff and seeds 11/12/13. S4 remains a single-seed disruption experiment. Three seeds show sensitivity, not a confidence interval or external validation. Stable means below the analytical work-content limit; it does not guarantee that a short run has converged.

## Scenarios and interpretation

| Scenario | Retained experiment | Interpretation |
|---|---|---|
| S0 | Baseline and three versions at 20 arrivals/month | Conditional normal-operation comparison; source of the generated KPI table |
| S1 | Demand sweep 15–240/month | Overloaded/censored cases have no reported stationary mean lead; show backlog instead |
| S2 | Gate waits x2.5 | Client-response sensitivity, not a mathematical worst case; a censored baseline is reported unavailable |
| S3 | p=.75 per active gate | Mean four geometric rounds, with unbounded possible rounds; not exactly four rounds or a finite worst case |
| S4 | One producer unavailable for half a model month | Existing task finishes without preemption; the same producer resumes and queued work is dispatched immediately; recovery cohort is distinct from stationary operation |
| S5 | Higher proposed v3 correction rates and deeper edits | Conditional quality/workload sensitivity; not proof that legal quality is protected |
| Rework x demand | Existing baseline process, 3 rework intensities x 5 demands x 3 seeds | Joint effects on workload, capacity, offered/busy utilization, throughput, WIP, backlog growth and lead |

## Main findings that survive review

Baseline E[work]=599.17 min and rework incidence=88% under p=(.75,.20,.40). Removing loops gives 516 min; heavy rework gives 686.33 min. At the same 14,150.4-minute monthly budget, capacities are 27.42, 23.62 and 20.62/month respectively. Heavy rework at 22/month is over capacity. The finite completed-only lead seen in an overloaded run is not a stationary mean and has been withdrawn from decision tables.

At 20/month, the corrected comparison gives approximately 23.1, 7.1, 3.9 and 1.6 calendar days from baseline to v3. These are simulations of proposed configurations. Iteration 3 retains work and renderer waits; client approval is not 100% of its lead time. The engine currently treats objections as immediate rework before delivery, so a real 24-hour post-delivery objection window is not validated.

Practical-capacity figures based on <=28 calendar days are grid-dependent scenario thresholds. They must not be sold as a 1–2-day SLA: at 230/month v3 lead is about 10 days. A mean 1.6-day result does not guarantee every customer delivery within 48 hours.

## Evidence still required

Arrival timestamps, per-gate outcomes, task-time distributions, daily video dedication, producer assignments, approved final-delivery boundary and renderer concurrency. Calibration to the reported baseline and matching target-informed inputs are not independent operational validation. The direction of the proposed improvement remains plausible; its size and service commitments require the Section-9 pilot.
