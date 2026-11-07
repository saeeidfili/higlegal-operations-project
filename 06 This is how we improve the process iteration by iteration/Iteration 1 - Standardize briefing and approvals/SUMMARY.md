# Iteration 1 — Standardize briefing and approvals (summary)

Flow from Section 5: scoreboard set — first iteration attacks the front door. Pure process design, no new AI. Cheapest, fastest, and produces the structured Brief data Iterations 2–3 are built on. Demo: *HiLegal Studio v1 — Intake & Approvals*.

## Problem (with numbers)

| Symptom | Evidence |
|---|---|
| 3–7 d before work starts | Intake queue [C] — free-form requests clarified by email |
| Brief loop ≥4 iterations [C] | No format previews; free-text feedback |
| ~90% rework [E] | Un-SLA'd email approvals, manual chasing |
| 21 d lead, ~94% waiting | Three looping gates + intake queue |

## The change (5 pieces)

1. **Structured self-serve intake form** — 12 fields, 5-format catalogue with **30 s format previews** (lawyer sees the end-shape before requesting)
2. **Profile auto-fill** from platform profile (9 of 12 fields pre-filled; ~3 manual)
3. **Auto completeness check + routing** — incomplete briefs bounce instantly with named missing fields; complete briefs route straight to a producer. **Intake queue and clarification loop deleted at the source**
4. **SLA'd mobile approvals** — approve / request change; change requests tied to **scene + reason code**; 48 h SLA, reminders 24 h/40 h, phone escalation
5. **Order state machine + timestamps** — every transition logged (the PDCA measurement habit, free)

## Process map: 12 → 10 steps

Intake queue + clarification collapse into form + auto-check; approvals become instrumented SLA gates. **Deliberately untouched: the manual production middle** (drafting, generation, sync) — Iterations 2–3's job. `POST /v1/requests` stores **Brief JSON** — the input contract Iteration 2 consumes.

## KPI effect — targets vs simulation

Simulation: `iteration1_sim.py` in this folder (engine copied from the Section 4 rework study, baseline sanity-checked: reproduces 21.8 d / 600 min / 87%). Loop probabilities solved the Section-4 way — two anchors: rework incidence 55% and E[work] = 435 min → ps ≈ 0.214, pf ≈ 0.428; structured change requests make loops *cheaper* (script 50→25, final 70→35 min), previews kill clarification entirely.

| KPI | Baseline | Target [T] | **Simulated** | Note |
|---|---|---|---|---|
| Lead time | 21.8 d | ~9 d (7–12) | **6.8 d** (P90 9.9) | target holds with headroom |
| Human time | 600 min | 435 min | **438 min** | engine check 435 closed form ✓ |
| Cost/video | ¥940 | ¥705 | **¥710** (labour 438 min ≈ ¥620 + tools ¥90) | |
| Work-content ceiling | 23.6/mo | 26/mo (kpi 60% basis) | **32.5/mo** (sim 67% basis) | basis difference documented in kpi-data §4 |
| **Practical capacity** | **~20/mo** | — | **~30/mo** | criterion: lead ≤ 28 d; 32/mo → 45 d |
| Rework | 87% | ~55% | **59%** | closed form 55%, seed variation |
| QAR | ~13% | ~45% | **~41%** | 1 − rework |

**The self-validation:** baseline's simulated practical capacity (~20/mo) reproduces the company-reported output 15–20 [C] — the criterion proves itself before we trust its Iter-1 answer.

## SLA sensitivity (what the lead time actually depends on)

| Lawyer behaviour | Gate wait | Lead | P90 |
|---|---|---:|---:|
| Approves in ~1 d | U(0.25–1.0) wd | 5.1 d | 7.4 |
| Typical | U(0.5–1.5) wd | 6.8 d | 9.9 |
| Always near 48 h cap | U(1.0–1.6) wd | 8.2 d | 12.4 |

**Iteration 1's lead time is gate-dominated** — lawyer behaviour swings it more than any internal production change. Even the breach case stays inside the 7–12 d target range.

## Pilot gate (pass = all hold)

10 videos v1 vs 10 legacy, same weeks/producers; state machine gives lead/gate-wait/loops automatically.
- Lead ≤ 12 d · clarification loops 0 on ≥8/10 · human time ≤ 8 h · rework ≤ 60% · QAR ≥ 35%
- **Guardrail: no quality drop** — faster but worse = fail

## Bridge to Iteration 2

Labour still ~7 h 20, ~6 h 40 of it the manual middle (drafting 50 + editing 22 + video 60 + audio 35 + sync 130 + adaptation 85). Front end fixed, middle untouched. **Manual scripting is the next constraint — and it needs structured Briefs, which now exist.**

*"We standardized what the client sends us. Now let's make the machine do the writing."*

Risks covered: adoption (pre-filled form, ≤3 manual fields), SLA breach by lawyer (reminders + escalation + terms), rigidity (free-text alongside codes), bypass (system IS the delivery channel).
