# Section 6 — This is how we improve the process iteration by iteration (summary)

Flow from Section 5: scoreboard set, measurement plan says *simulate first* — every iteration below is simulated (each folder carries its own `iterationN_sim.py`, same engine as the Section 4 study, sanity-checked against the previous rung) before any pilot.

## The chain in one view

A **chain, not a menu** — each iteration fixes the constraint the previous one exposed, consumes the previous one's data output, adds an API layer.

| | Baseline | **Iter 1** — Standardize briefing & approvals | **Iter 2** — Template-based AI scripting | **Iter 3** — Integrate audio/video generation |
|---|---|---|---|---|
| Root cause attacked | — | Unstructured intake + un-SLA'd approvals | Inverted automation order (human drafts, AI refines); no data spine | Separate generation + manual sync + adaptation |
| Waste killed | — | Waiting, Defects (brief loops) | Overprocessing (scripting), Defects (script loops) | Overprocessing (sync, adaptation), Transportation |
| **Data object created** | Free-text emails | **Brief JSON** | **Script JSON** (from Brief) | **Render job** (from Script) |
| Steps | 12 [C] | 10 | 9 | 8 |
| Lead time | 21.8 d | 6.8 d | 4.0 d | 1.6 d |
| Human time | 600 min | 438 min | 351 min | 62 min |
| Cost/video | ¥940 | ¥705 | ¥595 | ¥180 (sim ¥183) |
| Practical capacity (sim) | ~20/mo | ~30/mo | ~38/mo | **~230/mo** |
| Rework / QAR | 87% / 13% | 59% / 41% | 34% / 66% | 11% / 89% |
| Remaining limitation | Everything | Manual scripting + sync dominate labour | **Sync is THE binding constraint (~40% of labour)** | Constraint leaves HiLegal: lawyer approval time + AI-vendor dependency |
| New capability | — | Every step timestamped (PDCA habit) | Edits → LLM fine-tuning data (the flywheel) | Engagement analytics; variant matrix per platform |

*(Target row values in kpi-data; simulated values above — every target validated end-to-end.)*

## Why this order, not another

1. Iter 2's model needs structured Briefs — impossible without Iter 1's form
2. Iter 3's renderer needs machine-readable Scripts — impossible without Iter 2
3. Automating production before standardizing intake would auto-produce **the wrong video faster** — the classic automation trap
4. Theory of Constraints: **Identify** (sync = constraint) → **Exploit/Subordinate** (Iter 1–2 standardize around it) → **Elevate** (Iter 3 deletes it) → **Repeat** (new constraint = client approvals — already capped by Iter 1's SLA machinery)

## The three iterations in one line each

- **Iter 1 — the front door.** Self-serve structured form + format previews + 48 h SLA'd approvals; intake queue and clarification loop deleted at the source. No new AI — pure process design; produces the Brief JSON everything else consumes. Lead 21.8 → 6.8 d (gate-dominated: lawyer behaviour swings 5.1–8.2 d).
- **Iter 2 — the middle.** Fine-tuned legal LLM drafts from template + profile; humans edit instead of write. Compliance moves from memory to templates. Practical capacity ~38/mo — **the stated 35–40 ceiling reached for real, without hiring**. Bonus: every edit becomes labelled fine-tuning data — the video process starts improving the core asset.
- **Iter 3 — the cliff.** One render = voice + lip-sync + video + all variants; sync/adaptation/generation ops cease to exist; consent token hard-gates every render; publish + 24 h parallel objection window replaces the serial final approval. Lead 1.6 d, work 62 min, util 8% — **the queue is dead; capacity stops being the question.**

## Both benefit views, always

Every KPI chart shows incremental (what THIS change bought) and cumulative (what the CHAIN bought): cost ¥940 → ¥705 (−25%) → ¥595 (−16% incr, −37% cum) → ¥180 (−70% incr, **−81% cum**). The "small" Iter-2 step is the enabler of Iter-3's cliff — narrate it exactly that way.

## Where the constraint went

intake → scripting → sync → **lawyer approval**. After Iter 3, residual lead time ≈ 100% client-side (1.6 d SLA-shaped, 2.1 d if the lawyer rides the 48 h cap). Further improvement means managing the client, not more automation.

## Per-iteration folders

Each contains `START.md` (problem → change → map → API deltas → KPI effect → pilot gate → limitation → risks), `ux-flow.md` (clickable demo spec + paste-into-AI prompt), `iterationN_sim.py` (the simulation behind the numbers), `SUMMARY.md`.

Bridge to Section 7: *"That's the design. Now let's stress-test it."*
