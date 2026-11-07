# Section 6 — This is how we improve the process iteration by iteration (summary)

Flow from Section 5: scoreboard set, measurement plan says *simulate first* — the versions below are simulated under target-informed assumptions (each folder carries its own `iterationN_sim.py`, same engine as the Section 4 study, sanity-checked against the previous rung) before any pilot.

## The chain in one view

A **chain, not a menu** — each iteration fixes the constraint the previous one exposed, consumes the previous one's data output, adds an API layer.

| Version | Expected work min | Simulated work min | Lead cal d | P90 cal d | Rework observed | Work-content capacity/mo |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 599.17 | 597.87 | 22.05 | 35.09 | 89.4% | 23.62 |
| iteration 1 | 435.00 | 434.83 | 6.60 | 9.67 | 53.4% | 32.53 |
| iteration 2 | 349.85 | 349.61 | 3.91 | 5.21 | 27.9% | 40.45 |
| iteration 3 | 61.45 | 61.33 | 1.60 | 2.07 | 9.0% | 230.29 |

*(Target row values in kpi-data; simulated values above — target-informed scenario calculations, not independent validation.)*

## Why this order, not another

1. Iter 2's model needs structured Briefs — impossible without Iter 1's form
2. Iter 3's renderer needs machine-readable Scripts — impossible without Iter 2
3. Automating production before standardizing intake would auto-produce **the wrong video faster** — the classic automation trap
4. Theory of Constraints: **Identify** (sync = constraint) → **Exploit/Subordinate** (Iter 1–2 standardize around it) → **Elevate** (Iter 3 deletes it) → **Repeat** (new constraint = client approvals — already capped by Iter 1's SLA machinery)

## The three iterations in one line each

- **Iter 1 — the front door.** Self-serve structured form + format previews + 48 h SLA'd approvals; intake queue and clarification loop deleted at the source. No new AI — pure process design; produces the Brief JSON everything else consumes. Lead 22.05 → 6.60 calendar d (reconciled 3-seed scenario at 17.5/month) (gate-dominated: lawyer behaviour swings 5.1–8.2 d).
- **Iter 2 — the middle.** Fine-tuned legal LLM drafts from template + profile; humans edit instead of write. Compliance moves from memory to templates. Practical capacity ~38/mo — **the stated 35–40 ceiling approached in a proposed model scenario, not observed in operation**. Bonus: every edit becomes labelled fine-tuning data — the video process starts improving the core asset.
- **Iter 3 — the cliff.** One render = voice + lip-sync + video + all variants; sync/adaptation/generation ops cease to exist; consent token hard-gates every render; delivery + proposed 24 h objection window replaces the serial final approval. Lead 1.6 d, work 62 min, util 8% — **queueing remains low at the tested low-demand settings; capacity stops being the question.**

## Both benefit views, always

Every KPI chart shows incremental (what THIS change bought) and cumulative (what the CHAIN bought): cost ¥940 → ¥705 (−25%) → ¥595 (−16% incr, −37% cum) → ¥180 (−70% incr, **−81% cum**). The "small" Iter-2 step is the enabler of Iter-3's cliff — narrate it exactly that way.

## Where the constraint went

intake → scripting → sync → **lawyer approval**. After Iter 3, residual lead time substantially client-influenced, with internal render and QC still contributing (1.6 d SLA-shaped, 2.1 d if the lawyer rides the 48 h cap). Further improvement means managing the client, not more automation.

## Per-iteration folders

Each contains `START.md` (problem → change → map → API deltas → KPI effect → pilot gate → limitation → risks), `ux-flow.md` (clickable demo spec + paste-into-AI prompt), `iterationN_sim.py` (the simulation behind the numbers), `SUMMARY.md`.

Bridge to Section 7: *"That's the design. Now let's stress-test it."*

## Reconciled interpretation

Model results below use the existing two-producer event engine, 67% video dedication, 22 working days = 30.4 calendar days per month, demand 17.5/month [E], 36 months, 16-month warm-up, 3-month cutoff and seeds 11/12/13. This replaces earlier single-seed examples using a slightly different calendar conversion. The spread between seeds is not a confidence interval. Inputs for the proposed iterations were informed by targets, so matching those targets is conditional scenario analysis, not independent validation or a tested operational improvement.

Do not infer independent feasibility validation, a dead queue at every load, or actual headcount savings. The same average workload can produce different queues under M/M/1 and the two-server task simulation. Initial delivery, final acceptance and the proposed objection policy must be agreed before pilot measurement.
