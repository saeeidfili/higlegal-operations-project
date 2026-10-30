# Single source of truth — the evidence base

This folder holds the project's **evidence**: every company-reported fact and
every assumption we make, each appearing exactly once, tagged and traceable.
Everything else in the project (targets, derivations, model outputs,
implementation figures) is *computed or committed* from these — those live
with their owners, listed below.

## The files

| File | What lives there |
|---|---|
| `company-facts.md` | everything **company-reported [C]** — the canon |
| `assumptions.md` | everything **we assumed or estimated [E]** |

## Evidence tags (used project-wide)

- **[C]** company-reported — confirmed with HiLegal (visit / proposal, Sept 2026). Canon.
  The submitted proposal (`Proposal/OM-Project-Proposal-HiLegal.docx`) is the ultimate authority.
- **[E]** estimate — our assumption; plausible, sanity-checked, replace when real data arrives.
- Elsewhere you will also see **[T]** target (a commitment, not an observation) and derived
  figures labelled [E] in the section folders — this folder is where their [C]/[E] inputs live.

## The 20 most-quoted numbers (quick reference)

| Figure | Value | Tag | Home |
|---|---|---|---|
| Process steps (as-is) | 12 | [C] | `company-facts.md` |
| Labour per video | ~10 h (600 min) | [C] | `company-facts.md` |
| Lead time | 2–4 weeks (14–28 d) | [C] | `company-facts.md` |
| Intake queue wait | 3–7 days, "workload-dependent" | [C] | `company-facts.md` |
| Brief/clarification loop | ≥ 4 iterations | [C] | `company-facts.md` |
| Output / ceiling | 15–20 / month; ceiling 35–40 | [C] | `company-facts.md` |
| AV sync · platform adaptation | 2–3 h · ~2 h | [C] | `company-facts.md` |
| Subscription tier | $100/mo ≈ ¥720, promises 10 videos/mo | [C] | `company-facts.md` |
| Their cost attribution | ¥117/video (models + 30%) | [C] | `company-facts.md` |
| Producers | 2, Shenzhen | [C] | `company-facts.md` |
| Fully-loaded producer rate | ¥85/h | [E] | `assumptions.md` |
| Cost per video (true, baseline) | ¥940 — labour is ~90% | [D] | `05 .../kpi-data.md` §3 |
| Rework rate · QAR | ~90% · ~10% | [E] | `assumptions.md` |
| Work share of lead time | ≈ 6% (PCE 5–8%) | [D] | `03 .../START.md` |
| Capacity at 60% utilization | ~19/month | [D] | `05 .../kpi-data.md` §4 |
| Queue model capacity μ | ≈ 23.5/month (ρ 0.64–0.85) | [D] | `03 .../queue_model-explained.md` |
| Calculated ceiling | 352 h ÷ 10 h = 35.2/month ≈ stated 35–40 | [D] | `03 .../queue_model-explained.md` |
| Iteration 3 targets | ~1 h labour · ~1.5 d lead · ¥180/video · ~190/mo | [T] | `06 .../START.md` |
| Payroll released | ≈ ¥270k/year (~1.5 FTE) | [E] | `08 .../START.md` |
| One-time implementation | ≈ ¥105–180k, payback 5–8 months | [E] | `09 .../START.md` |

## Where the derived numbers live (their owners, not this folder)

| Content | Owner |
|---|---|
| KPI ladder, labour waterfall, cost ladder, capacity math, bleed tables | `05 These are our operational KPIs/kpi-data.md` |
| Intake queue model (μ, ρ, Wq, tail, ceiling, wall) | `03 .../queue_model-explained.md` + `queue_model.py` |
| Rework simulation (scenarios, sweep, capacity erosion, WIP) | `03 .../Rework/rework-flow.md` + `rework_simulation.py` |
| Iteration targets & mechanisms, pilot gates | `06 .../START.md` + iteration folders |
| Implementation costs, payback, monitoring | `09 .../START.md` |
| The waste/root-cause narrative that uses the models | `04 .../START.md` |

## Reconciliation — numbers that look inconsistent but aren't

All "capacities" are the same story at different assumptions — quote the one
that matches your frame:

| Figure | Value | Assumptions behind it | Home |
|---|---|---|---|
| KPI capacity (baseline) | ~19/mo | 2 × 160 h × **60%** utilization = 11,500 min ÷ **600 min** | kpi-data §4 |
| Queue-model capacity μ | ~23.5/mo | calibrated to the 3–7 d wait; 67% of 2 × 176 h | queue_model-explained.md |
| Rework-sim capacity (baseline) | ~24/mo | 2 × 22 d × 322 min (**67%**) ÷ **588 min** simulated | rework-flow.md |
| Theoretical ceiling | 35.2/mo | **100%** of 2 × 176 paid hours ÷ 10 h — ≈ stated 35–40 [C] | queue_model-explained.md |
| No-rework ceiling (sim) | ~27.4/mo | same 67% budget ÷ 516 min first-time-right | rework-flow.md |

Other deliberate differences:
- **Hours base:** 176 h = 22 d × 8 h paid (models) vs 160 h productive (KPI math) vs
  21.7 working days/month (calendar conversion).
- **Minute split of the ~10 h:** the KPI waterfall (600) and the rework simulation's
  task minutes (516 first-time-right + loops → 588) are two decompositions of the same
  [C] total — side by side in `assumptions.md`.
- **Labour share of ¥940:** ¥850/¥940 = 90.4%; some drafts say 90.6% or "91%". Use ~90%.
- **Utilization vs dedication:** 60% (KPI) and 67% (models) are the same concept at
  different granularity — never mix them inside one calculation.

## Governance

1. **Change a number here first**, then propagate to sections and scripts.
2. When HiLegal shares real data (the 10-video time-log pilot), replace the [E],
   note it in the changelog below, re-run the models.
3. This folder holds evidence, not conclusions — every derived figure must be
   recomputable from these values plus its model.

**Changelog**
- 2026-10-30 folder created; figures collected from sections 01–09 and the two models.
- 2026-10-30 trimmed to the evidence base ([C] + [E]); derived/targets/implementation
  files removed — that content stays with its owners (kpi-data.md, the model docs,
  sections 06/09).
