# Iteration 1 — Standardize briefing and approvals (summary)

Flow from Section 5: scoreboard set — first iteration attacks the front door. Pure process design, no new AI. Cheapest, fastest, and produces the structured Brief data Iterations 2–3 are built on. Demo: *HiLegal Studio v1 — Intake & Approvals*.

## Problem (with numbers)

| Symptom | Evidence |
|---|---|
| 3–7 d before work starts | Intake queue [C] — free-form requests clarified by email |
| Brief loop ≥4 iterations [C] | No format previews; free-text feedback |
| ~90% rework [E] | Un-SLA'd email approvals, manual chasing |
| 21 d lead, mostly waiting | Three looping gates + intake queue |

## The change (5 pieces)

1. **Structured self-serve intake form** — 12 fields, 5-format catalogue with **30 s format previews** (lawyer sees the end-shape before requesting)
2. **Profile auto-fill** from platform profile (9 of 12 fields pre-filled; ~3 manual)
3. **Auto completeness check + routing** — incomplete briefs bounce instantly with named missing fields; complete briefs route straight to a producer. **Intake queue and clarification loop deleted at the source**
4. **SLA'd mobile approvals** — approve / request change; change requests tied to **scene + reason code**; 48 h SLA, reminders 24 h/40 h, phone escalation
5. **Order state machine + timestamps** — every transition logged (the PDCA measurement habit, free)

## Process map: 12 → 10 steps

Intake queue + clarification collapse into form + auto-check; approvals become instrumented SLA gates. **Deliberately untouched: the manual production middle** (drafting, generation, sync) — Iterations 2–3's job. `POST /v1/requests` stores **Brief JSON** — the input contract Iteration 2 consumes.

## KPI effect: targets and model results kept separate

Model results below use the existing two-producer event engine, 67% video dedication, 22 working days = 30.4 calendar days per month, demand 17.5/month [E], 36 months, 16-month warm-up, 3-month cutoff and seeds 11/12/13. This replaces earlier single-seed examples using a slightly different calendar conversion. The spread between seeds is not a confidence interval. Inputs for the proposed iterations were informed by targets, so matching those targets is conditional scenario analysis, not independent validation or a tested operational improvement.

| Version | Expected work min | Simulated work min | Lead cal d | P90 cal d | Rework observed | Work-content capacity/mo |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 599.17 | 597.87 | 22.05 | 35.09 | 89.4% | 23.62 |
| iteration 1 | 435.00 | 434.83 | 6.60 | 9.67 | 53.4% | 32.53 |
| iteration 2 | 349.85 | 349.61 | 3.91 | 5.21 | 27.9% | 40.45 |
| iteration 3 | 61.45 | 61.33 | 1.60 | 2.07 | 9.0% | 230.29 |

The proposed mean-work targets remain 435/350/60 minutes, costs approximately ¥705/595/180 and lead ranges 7–12/3–5/1–2 calendar days. The model consumes target-informed proposed task times and gate probabilities. It explores feasibility under those inputs; it does not independently validate them. Work-content ceilings differ from the KPI budget. The 28-day practical-capacity criterion must not be presented as the proposed fast-delivery SLA.

## SLA sensitivity (what the lead time actually depends on)

| Scenario (seed 7, 28 months) | Gate wait working days | Lead cal d | P90 cal d |
|---|---|---:|---:|
| iteration 1 | (0.5, 1.5) | 6.68 | 9.80 |
| iteration 1 · fast lawyer | (0.25, 1.0) | 5.07 | 7.31 |
| iteration 1 · SLA breached | (1.0, 1.6) | 8.06 | 12.18 |

**Iteration 1's lead time is gate-dominated** — lawyer behaviour swings it more than any internal production change. Even the breach case stays inside the 7–12 d target range.

## Pilot gate (pass = all hold)

10 videos v1 vs 10 legacy, same weeks/producers; state machine gives lead/gate-wait/loops automatically.
- Lead ≤ 12 d · clarification loops 0 on ≥8/10 · human time ≤ 8 h · rework ≤ 60% · QAR ≥ 35%
- **Guardrail: no quality drop** — faster but worse = fail

## Bridge to Iteration 2

Labour still ~7 h 20, ~6 h 40 of it the manual middle (drafting 50 + editing 22 + video 60 + audio 35 + sync 130 + adaptation 85). Front end fixed, middle untouched. **Manual scripting is the next constraint — and it needs structured Briefs, which now exist.**

*"We standardized what the client sends us. Now let's make the machine do the writing."*

Risks covered: adoption (pre-filled form, ≤3 manual fields), SLA breach by lawyer (reminders + escalation + terms), rigidity (free-text alongside codes), bypass (system IS the delivery channel).

Review note: all pilot figures are proposed decision gates, not pilot results. Ten videos provide an initial screen, not reliable evidence for a tail SLA, rare safety events or long-run capacity.
