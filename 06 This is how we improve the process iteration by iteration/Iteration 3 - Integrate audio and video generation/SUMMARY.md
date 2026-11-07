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
5. **Publish + 24 h objection window replaces serial final approval** — runs in parallel; the last serial wait disappears
6. **Engagement analytics** feed the unified dashboard; per-step cycle-time logging covers the whole pipeline (PDCA)

## Process map: 9 → 8 steps

Video gen + audio gen + sync + adaptation (4 steps, ~280 min) collapse into one automated render + a 20-min QA pass. **What remains human: brief exceptions, script edit/QC, render QA — by design.**

## KPI effect — targets vs simulation

Simulation: `iteration3_sim.py` in this folder (same engine lineage; sanity-checked against all three prior rungs). Loop probabilities solved from anchors: 10% incidence + 60-min work → ps 0.034, pf 0.068 (pf = 2·ps). Objection window modeled as parallel — no serial wait; an objection adds a scene re-render + re-QA (15 min) inside the window.

| KPI | Iter 2 | Target [T] | **Simulated** | Note |
|---|---|---|---|---|
| Lead time | 4.0 d | ~1.5 d (1–2) | **1.6 d** (P90 2.1) | range holds |
| Human time | 351 min | 60 min | **62 min** | engine check 61 closed form ✓ |
| Cost/video | ¥595 | ¥180 | **¥183** (labour ¥88 + render ¥45 + LLM ¥20 + amort ¥30) | |
| Work-content ceiling | 40.4/mo | 190/mo (kpi 60% basis) | **230/mo** (sim 67% basis) | |
| **Practical capacity** | ~38/mo | — | **~230/mo** | lead flat 1.6–2.2 d from 15 to **200/mo** — the queue is dead |
| Rework | 34% | ~10% | **11%** | residual = avatar glitches, pronunciation |
| QAR | ~66% | ~90% | **~89%** | 1 − rework |
| Utilization (video budget) | 45% | — | **8%** | capacity stops being the question |

**The ladder, simulated:** lead 21.8 → 6.8 → 4.0 → **1.6 d** · work 600 → 438 → 351 → **62 min** · practical capacity 20 → 30 → 38 → **230/mo**. Every target validated end-to-end.

## Script-approval sensitivity — the last serial wait

| Lawyer behaviour | Gate wait | Lead | P90 |
|---|---|---:|---:|
| SLA-shaped (~24 h) | U(0.25–1.0) wd | 1.6 d | 2.1 |
| Rides the 48 h cap | U(0.5–1.5) wd | 2.1 d | 2.7 |

**After Iteration 3, lead time ≈ 100% client approval time.** The constraint has left HiLegal's building — further improvement means managing the client (SLAs in subscription terms, reminders, escalation), not more internal automation.

## Pilot gate (pass = all hold)

10 videos v3 vs v2 cohort + technical-QC log.
- Median lead ≤ 2 business days · human time ≤ 1 h 30 pilot / ≤ 1 h 05 steady (video 10+) · render success ≥ 90% first-pass / ≥ 98% after auto-retry · 3/3 variants on 100% · rework ≤ 12%
- **Guardrails: consent on file = 100% of avatar renders (zero tolerance, stop-the-line) · 0 compliance incidents · satisfaction ≥ v2 cohort**
- Steady-state rule: after 50 videos re-baseline; ≤ 1 h 05 locks the "under one hour" standard

## The honest close of Section 6

- The constraint is now the lawyer's own approval time — the process is as fast as its slowest client
- AI-vendor dependency → dual-vendor evaluation; the Script JSON layer keeps the pipeline renderer-agnostic
- Volume ceiling is now **demand, not capacity**: at 40/mo the two producers spend ~4 h/month on video → Section 8: what should the company do with the payroll and attention that no longer go into video? Fund the legal LLM.

Risks: uncanny renders/mispronunciation (QA checklist + test render + retry), consent exposure (token hard-gates, registry with expiry), vendor lock-in (dual-vendor, renderer-agnostic contract), quality dilution (QAR + satisfaction guardrails, human QC never removed), bespoke requests (priced separately).
