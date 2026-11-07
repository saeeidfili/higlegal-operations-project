# HiLegal analytical reconciliation

Review date: 7 November 2026. Scope: `main` only. Reviewed starting commit: `0d24ec176270ab1f991e69033092ca7b5df67859`.

The three-iteration design, Saeed's task decomposition and proposed implementation direction are preserved. Confirmed company-reported ranges are retained. The corrections distinguish model assumptions, targets and generated results and remove unsupported claims of validation, cash savings and stationary lead times under overload. No presentation regeneration or presentation-branch write is part of this review.

## Completion report

| Item | Outcome |
|---|---|
| Files modified | Exact repository-relative paths appear in the manifest below; existing folders retained. Submitted proposal unchanged. |
| Issues identified | Mixed hour budgets; contradictory gate probabilities; conflated rounds/incidence/quality; survivor-biased finite-horizon leads; mismatched throughput and WIP windows; calendar denominator mismatch; mistaken one-server justification; publishing scope drift; incorrect staff-hours/payroll and payback claims. |
| Corrections | Shared measurement helper, explicit censor/overload diagnostics, common time units, expected-work capacity, corrected absence handling, cross-factor rework/demand output, reconciled canonical tables and dependent documents. |
| Verification | Nine existing scripts exit 0; verify_analysis.py identities and 3-seed reproduction pass; four updated SVG charts visually checked; original process parameters and proposal bytes checked against the starting commit. |
| Open questions | Empirical gate rates, time dedication, meaning of reported ceiling, actual cash-cost changes, customer usage and delivery/final-acceptance policy remain unmeasured. See questions below. |
| Presentation implications | Replace conflated capacity figures; withdraw overloaded lead-time claims; qualify target-informed simulations; correct labour/payroll/payback claims, strict under-one-hour wording and publishing boundary. No slides changed here. |

## Capacity reconciliation

| Number | Meaning and denominator |
|---|---|
| 15–20/month [C] | Reported completed output, not a measured Poisson arrival stream. |
| 19.2/month [D] | 2 x 160 h x 60% x 60 / 600 min = 11,520/600. The 60% is dedication, not observed queue utilization. |
| 23.5/month [E] | Retained calibrated serial M/M/1 intake-surrogate rate. Non-preemption/shared queuing do not prove one physical server. |
| 23.62/month [D] | Two-server task model: 2 x 176 h x 67% x 60 / 599.17 = 14,150.4/599.17. |
| 35.2/month [D] | Illustration at 100% of 352 paid staff hours and 10 h/video. |
| 35–40/month [C] | Separate company-stated ceiling, preserved; sustainability/overtime/dedication not verified. |

At retained mu=23.5, consistent units give intake waits about 2.28/3.77/7.39 calendar days at assumed arrivals 15/17.5/20. This does not exactly fit all reported endpoints. Assigning light demand to 3 d and heavy demand to 7 d is itself an assumption. The supposed independent 65% corroboration was not supported; it has been removed.

## Work, loops and measurement

Baseline first-pass work is 516 min. Expected additional work is 24 clarification +12.5 script +46.67 final =83.17 min, giving 599.17 min. The implemented model therefore does not add loops on top of an already rework-inclusive 600-minute baseline. The separate KPI waterfall decomposes the approximately 600-minute total and must not be used as a first-pass task vector.

Current baseline probabilities remain (.75,.20,.40). The .30/.30 documentation was stale. p_clar=.75 corresponds to a geometric mean of four rounds, but the reported ≥4 iterations do not identify that probability. The calibration helper, conditional on chosen p_script=.20, can solve p_final≈.404; the retained rounded .40 implementation gives 599.17 rather than exactly 600. Multiple gate-rate combinations fit the same total, so rates are not empirically identified. Iteration rates and task times are target-informed proposals, not separately validated improvements.

Order-level incidence is 1-product(1-p): baseline 88%; iterations about 55.04%,30.07%,9.97%. QAR=1-incidence is valid only for the same population/boundary and first-pass definition. It is not legal accuracy or content quality. A p=.75 stress has mean four rounds at each active gate, with unbounded possible rounds, unlike a literal exactly four-round scenario.

The serial intake surrogate assumes exponential service. The process simulator uses two FIFO task servers, deterministic work durations, independent geometric gate draws and uniform client/machine waits. Producers do other tasks while clients wait. The 22-working-day model month now consistently equals 30.4 calendar days; it is not an explicit weekend/holiday calendar. Seeds repeat runs but do not ensure common arrival streams across changed process versions, because event and gate draws share a generator.

Measurement now integrates WIP and clips busy segments over a common window; departure throughput counts departures in that window. Arrival cohorts retain their size and unfinished count. Under overload there is no stationary mean lead; under censoring a completed-only mean is withheld. Expected work sets capacity, avoiding survivor-biased work-content capacity. `measurement-diagnostics.json` preserves per-run statuses, counts, windows, expected work and completed-cohort diagnostics, including withheld cases. Those diagnostics are not silently substituted for a complete-cohort mean.

Section 7 adds 3 rework intensities x 5 demand levels x 3 seeds using the existing process engine. At heavy rework E[work]=686.33 min and capacity=20.62/month; at demand22 offered load=106.7%, with finite-window mean WIP≈81.04 and backlog growth≈3.76 orders/month. These are conditional finite-horizon results. At stable baseline demand17.5, 3-seed mean lead=22.05 d; iterations=6.60/3.91/1.60 d. Exact snapshots and seed spread are in `single source of truth/model-results.json`; Section-7 normal comparison separately uses demand20. Three seeds are sensitivity evidence, not confidence intervals.

The service-level capacity threshold of <=28 calendar days is not the proposed 1–2-day SLA. At v3 demand230, simulated mean lead is about 10 d. Renderer concurrency is unconstrained in the model. Mean work 61.45 min including residual corrections does not demonstrate a strict <60-minute target; a 65-minute tolerance cannot certify it. Script waits, machine rendering, QC and producer queues all contribute to v3 lead, so it is not 100% client approval time.

The absence experiment now marks the same producer unavailable, finishes a current non-preemptive task and dispatches queued work on return. Two working weeks are represented as10 working days, rather than half of a 22-day month (11 days). It remains a single-seed temporary-disruption scenario, not a stationary model.

## Process and financial boundary

HiLegal produces and hands finished files to lawyers; lawyers publish and manage accounts. Proposed direct social-account publishing/API wording has been corrected to delivery. Engagement reporting would depend on optional lawyer-provided data outside production lead time. A proposed objection policy is not an implemented control: current code draws objections immediately before delivery, with no actual 24-hour post-delivery event window. That boundary needs agreement; the model does not establish the original proposal's final-approval protection under a changed policy.

At 20 videos/month, the 10 h to 1 h planning targets mean 200 to 20 staff h/month:180 h freed (1.02 paid FTE at 176 h/FTE), allocated labour value ¥183,600/year at ¥85/h. At 15/month:135 h, 0.77 FTE,¥137,700/year. At 40/month proposed work is40 h, not 4 h. Released hours, avoided future hiring and actual payroll cash are different benefits. Existing salaries do not disappear automatically; do not add allocated labour savings twice through unit cost and payroll. The earlier¥270k/1.5-FTE cash-release claim is not established at reported volume.

The¥117/video figure is an internal attribution benchmark, not observed sales revenue per video. Customer tables assume the full¥720 subscription can cover video costs and omit other bundled services, support/acquisition and implementation costs. They show conditional residuals, not actual profitability or audited company burn. Salary, burden, exchange rate and tool prices remain unverified model assumptions, not current market/regulatory advice.

At ¥760/video allocated reduction, ¥105–180k investment corresponds to 138–237 videos. At 20–35/month the full extreme range is 3.95–11.84 months (about 4–12); at reported 15–20/month it is 6.9–15.8 months. Cash payback requires an actual cash-cost change or documented avoided hire; unchanged salaries and assumed tooling rising ¥90 to ¥95/video do not demonstrate it. Pilot and implementation costs must be checked for overlapping cost allocations.

Ten-video pilots are screens, not adequate independent verification of rare compliance events, a P90 guarantee or long-run capacity. Concurrent cohorts sharing producers still face learning, queue-interference and order-mix confounding. The 14+ week rollout is a documented refinement of the proposal's 10-week plan, not evidence implementation has happened.

## Open questions for Saeed and HiLegal

1. Does ≥4 iterations describe a typical mean, minimum observed example, total rounds or rejections? Supply per-gate timestamp/outcome logs before estimating probabilities.
2. What are real arrivals, unfinished orders, paid hours, daily video dedication and other platform work? Which conditions support the 35–40 ceiling?
3. Are final acceptance and delivery the same event? Would HiLegal accept an objection window, and what happens to late objections? Publishing remains the lawyer's responsibility.
4. What is actual subscription usage, bundled revenue allocation, tool usage and loaded staff cost? Which payroll/overtime/contractor or avoided-hire outflows could actually change?
5. What are renderer concurrency, retry delays, human QC/edit distributions and quality criteria? Is strict under 60 min still a commitment or should a revised target be agreed?
6. Which speaker made each interview statement? Our team identified the visit contact as the product lead; individual CEO attribution is not established in the repository.
7. What pilot sample, matched/randomized comparison and uncertainty criteria are acceptable before selling an SLA or claiming quality gains?

## Verification and reproduction

Python 3.12, Matplotlib 3.11.2 and NumPy 2.5.4 were used in an isolated task dependency folder. Run the original scripts from their folders (their existing dependency declarations remain), and `python verify_analysis.py` from the root for identities and the normal snapshot. All 9 existing scripts completed with exit 0. Checks cover baseline parameter identity across copies, work formulas/incidence, calendar units, exact toy WIP/busy-time/departure/censoring cases and a 3-seed reproducible snapshot. Original task/wait/probability/dedication dictionaries were compared with Git objects; no fit-to-target input changes were made. Updated analytical SVGs are regenerated by their original scripts, not presentation slides.

M/M/1 single-server assumptions and the matched-boundary Little-law identity were checked against the [MIT primary teaching note](https://www.ocw.mit.edu/courses/2-854-introduction-to-manufacturing-systems-fall-2016/927056a1af54772a587fd84ad4951e71_MIT2_854F16_Mm1Queue.pdf). Algebra/engine verification and calibration are explicitly distinguished from empirical validation.

The remote presentation reference observed before publishing this review was `2bdd4761f69e243a65bcf24ac1bf79520a48c156`. This task edits and pushes main only; the only push target used was refs/heads/main. The post-push remote read observed presentation at 034b91adfd171536ec41a280854f846b80d5094d, so the reference advanced separately during the review. This review did not edit, merge or push presentation; its remote ref cannot truthfully be described as unchanged across the entire elapsed interval. The earlier presentation work in this chat is separate from this reconciliation.

## Exact file manifest

- `01 This is HiLegal/START.md`
- `02 This is the challenge/START.md`
- `02 This is the challenge/SUMMARY.md`
- `03 This is the current process/START.md`
- `03 This is the current process/SUMMARY.md`
- `03 This is the current process/calibrate_mu.py`
- `04 These are the wastes and root causes/Rework/START.md`
- `04 These are the wastes and root causes/Rework/SUMMARY.md`
- `04 These are the wastes and root causes/Rework/calibrate_loops.py`
- `04 These are the wastes and root causes/Rework/gantt-rework.svg`
- `04 These are the wastes and root causes/Rework/queue-sample-path.svg`
- `04 These are the wastes and root causes/Rework/rework-explained.md`
- `04 These are the wastes and root causes/Rework/rework-flow.md`
- `04 These are the wastes and root causes/Rework/rework-impact.svg`
- `04 These are the wastes and root causes/Rework/rework-vs-demand.svg`
- `04 These are the wastes and root causes/Rework/rework_simulation.py`
- `04 These are the wastes and root causes/Rework/run_report.py`
- `04 These are the wastes and root causes/queue/SUMMARY.md`
- `04 These are the wastes and root causes/queue/order-timeline.svg`
- `04 These are the wastes and root causes/queue/queue-cliff.svg`
- `04 These are the wastes and root causes/queue/queue_model-explained.md`
- `04 These are the wastes and root causes/queue/queue_model.py`
- `05 These are our operational KPIs/SUMMARY.md`
- `06 This is how we improve the process iteration by iteration/Iteration 1 - Standardize briefing and approvals/START.md`
- `06 This is how we improve the process iteration by iteration/Iteration 1 - Standardize briefing and approvals/SUMMARY.md`
- `06 This is how we improve the process iteration by iteration/Iteration 1 - Standardize briefing and approvals/iteration1_sim.py`
- `06 This is how we improve the process iteration by iteration/Iteration 2 - Template-based AI scripting/START.md`
- `06 This is how we improve the process iteration by iteration/Iteration 2 - Template-based AI scripting/SUMMARY.md`
- `06 This is how we improve the process iteration by iteration/Iteration 2 - Template-based AI scripting/iteration2_sim.py`
- `06 This is how we improve the process iteration by iteration/Iteration 3 - Integrate audio and video generation/START.md`
- `06 This is how we improve the process iteration by iteration/Iteration 3 - Integrate audio and video generation/SUMMARY.md`
- `06 This is how we improve the process iteration by iteration/Iteration 3 - Integrate audio and video generation/iteration3_sim.py`
- `06 This is how we improve the process iteration by iteration/Iteration 3 - Integrate audio and video generation/ux-flow.md`
- `06 This is how we improve the process iteration by iteration/SUMMARY.md`
- `07 Let's run and compare the processes/START.md`
- `07 Let's run and compare the processes/SUMMARY.md`
- `07 Let's run and compare the processes/compare_sim.py`
- `07 Let's run and compare the processes/ladder.svg`
- `07 Let's run and compare the processes/measurement-diagnostics.json`
- `07 Let's run and compare the processes/rework-demand-results.json`
- `07 Let's run and compare the processes/rework-demand-results.md`
- `07 Let's run and compare the processes/rework-stress.svg`
- `07 Let's run and compare the processes/saturation.svg`
- `07 Let's run and compare the processes/scenario-results.md`
- `07 Let's run and compare the processes/slow-lawyers.svg`
- `07 Let's run and compare the processes/timer-bars.svg`
- `07 Let's run and compare the processes/wip-paths.svg`
- `08 This is the organizational impact/START.md`
- `08 This is the organizational impact/SUMMARY.md`
- `09 This is how HiLegal can implement it/START.md`
- `09 This is how HiLegal can implement it/SUMMARY.md`
- `README.md`
- `RECONCILIATION.md`
- `simulation_metrics.py`
- `single source of truth/README.md`
- `single source of truth/assumptions.md`
- `single source of truth/company-facts.md`
- `single source of truth/kpi-data.md`
- `single source of truth/model-results.json`
- `verify_analysis.py`

Submitted proposal SHA256 (unchanged): `1dff8cafa36e78291d7d7aa900b1a6250e87aaab36f9c7f435efe463190a707b`.

Existing scripts verified:

- `03 This is the current process/calibrate_mu.py`: exit 0
- `07 Let's run and compare the processes/compare_sim.py`: exit 0
- `04 These are the wastes and root causes/queue/queue_model.py`: exit 0
- `04 These are the wastes and root causes/Rework/calibrate_loops.py`: exit 0
- `04 These are the wastes and root causes/Rework/rework_simulation.py`: exit 0
- `04 These are the wastes and root causes/Rework/run_report.py`: exit 0
- `06 This is how we improve the process iteration by iteration/Iteration 1 - Standardize briefing and approvals/iteration1_sim.py`: exit 0
- `06 This is how we improve the process iteration by iteration/Iteration 2 - Template-based AI scripting/iteration2_sim.py`: exit 0
- `06 This is how we improve the process iteration by iteration/Iteration 3 - Integrate audio and video generation/iteration3_sim.py`: exit 0
