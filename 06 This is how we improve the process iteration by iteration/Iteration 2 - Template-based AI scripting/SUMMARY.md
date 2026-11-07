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

## KPI effect — targets vs simulation

Simulation: `iteration2_sim.py` in this folder (same engine lineage; sanity-checked against baseline and Iteration-1 published numbers). Loop probabilities solved from two anchors — incidence 30% + E[work] 350 min → ps 0.108, pf 0.216 (pf = 2·ps); script loops cost 10 min (regenerate one scene).

| KPI | Iter 1 | Target [T] | **Simulated** | Note |
|---|---|---|---|---|
| Lead time | 6.8 d | ~4 d (3–5) | **4.0 d** (P90 5.1) | target hit exactly |
| Human time | 438 min | 350 min | **351 min** | engine check 350 closed form ✓ |
| Cost/video | ¥705 | ¥595 | ¥600 (labour ¥498 + tools ¥65 + LLM ¥20 + amort ¥15) | |
| Work-content ceiling | 32.3/mo | 33/mo (kpi basis) | **40.4/mo** (sim 67% basis) | |
| **Practical capacity** | ~30/mo | — | **~38/mo** | **inside the stated 35–40 ceiling [C] — reached without hiring** |
| Rework | 59% | ~30% | **34%** | closed form 30%, seed variation |
| QAR | ~41% | ~70% | **~66%** | 1 − rework |

**Honest framing for the modest cost step:** Iteration 2's payoff is not mainly labour minutes — it is (a) killing script-loop rework, (b) reaching the stated capacity ceiling for real, (c) creating the Script JSON that makes Iteration 3's cliff possible, and (d) starting the fine-tuning flywheel.

## Approval-channel sensitivity

| Approval channel | Gate wait | Lead | P90 |
|---|---|---:|---:|
| In-app (~24 h avg) | U(0.25–1.0) wd | 4.0 d | 5.1 |
| Email fallback (v1 gates) | U(0.5–1.5) wd | 5.3 d | 7.1 |

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
