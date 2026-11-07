# Iteration 2 — Template-based AI scripting (summary)

Flow from Iteration 1: the client's input is standardized — now automate what the employees write. **Reverses the automation order**: today humans draft and AI refines; from here the fine-tuned legal LLM drafts from template + lawyer profile, humans **edit instead of write**. Strategic pivot: the video process becomes a training-ground and usage engine for HiLegal's core asset. Demo: *HiLegal Studio v2 — Script Engine*.

## Problem (as left by Iteration 1)

| Symptom | Root cause (Section 4, chain 2) |
|---|---|
| Script work still 80 min/video (drafting 55 + editing 25) | Human writes first draft; AI only refines — order inverted |
| Script-surprise loops remain (~55% rework) | Lawyer approves structure only after reading a bespoke draft |
| Labour 7 h 15 — manual middle dominates | No structured data spine downstream of the brief |

**Prerequisite:** the engine consumes **Brief JSON** — Iteration 1 is not optional infrastructure, it is the input contract.

## The change (5 pieces)

1. **Script Engine** (`POST /v2/scripts/generate`): Brief JSON + profile → full draft via the fine-tuned legal LLM against a fixed template, ~1 min
2. **Template library** (5 formats): scene skeleton, tone rules, pacing, **built-in legal-marketing compliance constraints** (no outcome guarantees, disclaimer handling) — compliance moves from memory to system
3. **Profile-enriched drafting**: credentials, case highlights, **past accepted edits** as few-shot examples — the model writes like this lawyer's approved videos
4. **Edit-not-write QC**: producer reviews in a scene editor → **approved Script JSON** (`scenes[], voiceover_text, on_screen_text[], duration, prompt hints`) — single source of truth downstream
5. **The fine-tuning flywheel**: every change request + producer edit is a labelled training example — the video process *generates* the asset HiLegal most wants to improve. Say this one out loud.

## Process map: 10 → 9 steps

Drafting + AI refinement (80 min) collapse into generation (5 min) + edit-QC (30 min). **Untouched: generation + sync + adaptation** — Iteration 3's target, now fatter than ever. Approved **Script JSON** is Iteration 3's render input contract — "a script" becomes data.

## KPI effect: targets and model results kept separate

Model results below use the existing two-producer event engine, 67% video dedication, 22 working days = 30.4 calendar days per month, demand 17.5/month [E], 36 months, 16-month warm-up, 3-month cutoff and seeds 11/12/13. This replaces earlier single-seed examples using a slightly different calendar conversion. The spread between seeds is not a confidence interval. Inputs for the proposed iterations were informed by targets, so matching those targets is conditional scenario analysis, not independent validation or a tested operational improvement.

| Version | Expected work min | Simulated work min | Lead cal d | P90 cal d | Rework observed | Work-content capacity/mo |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 599.17 | 597.87 | 22.05 | 35.09 | 89.4% | 23.62 |
| iteration 1 | 435.00 | 434.83 | 6.60 | 9.67 | 53.4% | 32.53 |
| iteration 2 | 349.85 | 349.61 | 3.91 | 5.21 | 27.9% | 40.45 |
| iteration 3 | 61.45 | 61.33 | 1.60 | 2.07 | 9.0% | 230.29 |

The proposed mean-work targets remain 435/350/60 minutes, costs approximately ¥705/595/180 and lead ranges 7–12/3–5/1–2 calendar days. The model consumes target-informed proposed task times and gate probabilities. It explores feasibility under those inputs; it does not independently validate them. Work-content ceilings differ from the KPI budget. The 28-day practical-capacity criterion must not be presented as the proposed fast-delivery SLA.

## Approval-channel sensitivity

| Scenario (seed 7, 28 months) | Gate wait working days | Lead cal d | P90 cal d |
|---|---|---:|---:|
| iteration 2 | (0.25, 1.0) | 3.90 | 5.07 |
| iteration 2 · email fallback | (0.5, 1.5) | 5.22 | 6.97 |

**The Script Engine removes writing, not waiting** — the gate remains the swing factor; Iteration 3 attacks what remains.

## Pilot gate (pass = all hold)

10 videos v2 (AI-drafted) vs 10 v1 (human-drafted), same producers/weeks.
- Median lead ≤ 5 d · human time ≤ 6 h 15 · **edit depth ≤ 20% of generated words** (the model-quality KPI) · rework ≤ 35% · QAR ≥ 65%
- **Guardrails: 0 compliance incidents** (template constraints + human QC = two layers); edit-time trend flat or falling
- **Strategic KPI:** ≥25 labelled training examples per 10 videos → LLM fine-tuning backlog

## Bridge to Iteration 3

Sync is now **134 of ~350 min ≈ 40% of all labour** — the single binding constraint, exactly as Theory of Constraints predicts: elevate one constraint, the next surfaces. Generation is still two separate artefacts married by hand, then adapted by hand.

*"The script is now data. So let the data render itself."*

Risks: heavy-correction drafts (edit-depth KPI, graceful degradation to v1), compliance errors (constraints in templates + QC), lawyer distrust (few-shot from their own approved style), model drift (versioned registry + 20 golden briefs re-scored weekly).

Review note: all pilot figures are proposed decision gates, not pilot results. Ten videos provide an initial screen, not reliable evidence for a tail SLA, rare safety events or long-run capacity.
