# Iteration 3 — Integrate audio and video generation (summary)

Flow from Iteration 2: the script is data — now let the data render itself. **One render produces voice + lip-sync + video together** and emits all platform variants — deleting the separate audio track, the **2–3 h manual sync [C]**, and the **~2 h manual adaptation [C]**. The cliff: labour under an hour, cost −70% in one step, the constraint leaves HiLegal's building. Demo: *HiLegal Studio v3 — Render Pipeline*.

## Problem (as left by Iteration 2)

| Symptom | Root cause (Section 4, chain 2) |
|---|---|
| Sync = 134 min ≈ **40% of all labour** — binding constraint | Video and audio are separate artefacts married by hand |
| Adaptation still ~75–80 min/video | Manual resize/caption per platform |
| Generation ops 70 min (two tools, two retry sets) | Two tool handoffs |
| Cost ¥595, capacity ~38/mo vs demand ambition 40+ | Labour-bound process |

**Prerequisite:** the renderer consumes **approved Script JSON** (v2) — rendering from documents is impossible; from data it's one API call. Brief JSON (v1) → Script JSON (v2) → Render (v3): each layer consumes the previous one's output.

## The change (6 pieces)

1. **Single-render avatar pipeline** (`POST /v3/renders`): Script JSON + consent token → voice + lip-sync + video in one render (batch queue, ~20–30 min wall-clock, near-zero human attention). TTS and sync steps **cease to exist**
2. **Auto variants from the same render**: 16:9 / 9:16 / 1:1 — manual adaptation → zero; cross-platform consistency becomes structural
3. **Avatar & consent registry**: written likeness + voice consent per lawyer, **hard-gates** every render (compliance by construction; fits the e-signature DNA)
4. **Human QC stays, deliberately**: ~20-min render-QA pass (likeness, name pronunciation, captions, brand frames) — the quality guardrail
5. **Delivery + proposed 24 h objection window replaces serial final approval** — runs in parallel; the last serial wait disappears
6. **Engagement analytics** feed the unified dashboard; per-step cycle-time logging covers the whole pipeline (PDCA)

## Process map: 9 → 8 steps

Video gen + audio gen + sync + adaptation (4 steps, ~280 min) collapse into one automated render + a 20-min QA pass. **What remains human: brief exceptions, script edit/QC, render QA — by design.**

## KPI effect: targets and model results kept separate

Model results below use the existing two-producer event engine, 67% video dedication, 22 working days = 30.4 calendar days per month, demand 17.5/month [E], 36 months, 16-month warm-up, 3-month cutoff and seeds 11/12/13. This replaces earlier single-seed examples using a slightly different calendar conversion. The spread between seeds is not a confidence interval. Inputs for the proposed iterations were informed by targets, so matching those targets is conditional scenario analysis, not independent validation or a tested operational improvement.

| Version | Expected work min | Simulated work min | Lead cal d | P90 cal d | Rework observed | Work-content capacity/mo |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 599.17 | 597.87 | 22.05 | 35.09 | 89.4% | 23.62 |
| iteration 1 | 435.00 | 434.83 | 6.60 | 9.67 | 53.4% | 32.53 |
| iteration 2 | 349.85 | 349.61 | 3.91 | 5.21 | 27.9% | 40.45 |
| iteration 3 | 61.45 | 61.33 | 1.60 | 2.07 | 9.0% | 230.29 |

The proposed mean-work targets remain 435/350/60 minutes, costs approximately ¥705/595/180 and lead ranges 7–12/3–5/1–2 calendar days. The model consumes target-informed proposed task times and gate probabilities. It explores feasibility under those inputs; it does not independently validate them. Work-content ceilings differ from the KPI budget. The 28-day practical-capacity criterion must not be presented as the proposed fast-delivery SLA.

## Script-approval sensitivity — the last serial wait

| Scenario (seed 7, 28 months) | Gate wait working days | Lead cal d | P90 cal d |
|---|---|---:|---:|
| iteration 3 | (0.25, 1.0) | 1.56 | 2.06 |
| iteration 3 · slow lawyer | (0.5, 1.5) | 2.10 | 2.67 |

**After Iteration 3, lead time substantially affected by client approvals, with machine render and human QC still contributing.** The constraint has left HiLegal's building — further improvement means managing the client (SLAs in subscription terms, reminders, escalation), not more internal automation.

## Pilot gate (pass = all hold)

10 videos v3 vs v2 cohort + technical-QC log.
- Median lead ≤ 2 business days · human time ≤ 1 h 30 pilot / ≤ 1 h 05 steady (video 10+) · render success ≥ 90% first-pass / ≥ 98% after auto-retry · 3/3 variants on 100% · rework ≤ 12%
- **Guardrails: consent on file = 100% of avatar renders (zero tolerance, stop-the-line) · 0 compliance incidents · satisfaction ≥ v2 cohort**
- Steady-state rule: after 50 videos re-baseline; ≤ 1 h 05 is a 65-minute tolerance, not an under-one-hour standard; a strict <60 min target remains unproven

## The honest close of Section 6

- The constraint is now the lawyer's own approval time — the process is as fast as its slowest client
- AI-vendor dependency → dual-vendor evaluation; the Script JSON layer keeps the pipeline renderer-agnostic
- Volume ceiling is now **demand, not capacity**: at 40/mo the two producers spend ~40 h/month on video → Section 8: what should the company do with the payroll and attention that no longer go into video? Fund the legal LLM.

Risks: uncanny renders/mispronunciation (QA checklist + test render + retry), consent exposure (token hard-gates, registry with expiry), vendor lock-in (dual-vendor, renderer-agnostic contract), quality dilution (QAR + satisfaction guardrails, human QC never removed), bespoke requests (priced separately).

Review note: all pilot figures are proposed decision gates, not pilot results. Ten videos provide an initial screen, not reliable evidence for a tail SLA, rare safety events or long-run capacity.
