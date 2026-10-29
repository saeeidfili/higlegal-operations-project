# Section 6 — This is how we improve the process iteration by iteration

**Guiding question:** Each iteration addresses a specific cause and develops the process further.

**What this section must accomplish:** present the three iterations as a **chain, not a menu** — each one fixes the constraint the previous one exposed, consumes the previous one's data output, and adds a distinct API layer on top. Never show an iteration's benefit without also showing the cumulative effect vs. the original 12-step process.

---

## The chain in one view

| | Baseline (as-is) | **Iteration 1**<br>Standardize briefing & approvals | **Iteration 2**<br>Template-based AI scripting | **Iteration 3**<br>Integrate audio/video generation |
|---|---|---|---|---|
| **Root cause attacked** | — | Unstructured intake + un-SLA'd approvals (Section 4, chains 1 & 3) | Inverted automation order: human drafts, AI refines; no data spine (chain 2) | Separate generation + manual sync + manual adaptation (chain 2) |
| **Waste killed** | — | Waiting (queues), Defects (brief loops) | Overprocessing (scripting), Defects (script loops) | Overprocessing (sync, adaptation), Transportation (tool handoffs) |
| **Data object created** | Free-text emails | **Brief JSON** (structured, validated) | **Script JSON** (scenes, generated from Brief) | **Render job** (video + variants, generated from Script) |
| **API layer added** | — | Orders + intake + approvals + SLA engine | Script engine: templates + fine-tuned legal LLM + change-request loop | Render pipeline: single-render avatar, variants, consent, analytics |
| **Steps** | 12 [C] | 10 | 9 | 8 (matches proposal's to-be) |
| **Lead time** | ~21 d | ~9 d | ~4 d | ~1.5 d |
| **Human time** | 10 h 00 | 7 h 15 | 5 h 50 | ~1 h 00 |
| **Cost/video** | ¥940 | ¥705 | ¥595 | ¥180 |
| **Capacity (2 producers)** | ~19/mo | ~26/mo | ~33/mo | ~190/mo |
| **Rework / QAR** | 90% / 10% | 55% / 45% | 30% / 70% | 10% / 90% |
| **Remaining limitation** | Everything | Manual scripting + manual sync still dominate labour | **Sync is now THE binding constraint (~40% of labour)** — but it can't be fixed until scripts are standardized | Constraint leaves HiLegal: lawyer approval time + AI-vendor dependency |
| **New capability exposed** | — | Every step timestamped (measurement habit) | Model learns from accepted/rejected edits → feeds LLM fine-tuning | Engagement analytics per video; variant matrix for every platform |

**Why this order and not another:**
1. Iteration 2's model needs structured Briefs — impossible without Iteration 1's form.
2. Iteration 3's renderer needs machine-readable approved Scripts — impossible without Iteration 2.
3. Automating production (Iter 3) before standardizing intake (Iter 1) would auto-produce *the wrong video faster* — the classic automation trap we explicitly avoid.
4. Theory of Constraints narrative: **Identify** (sync = constraint, Section 4) → **Exploit/Subordinate** (Iter 1–2 standardize everything around it) → **Elevate** (Iter 3 deletes it) → **Repeat** (new constraint = client-side approvals, which Iter 1's SLA machinery already caps).

## How each iteration folder is organized

Each iteration sub-folder contains:
- **`START.md`** — problem addressed → change introduced → updated process map → **API deltas vs. previous iteration** → KPI effect (vs. previous iteration AND vs. baseline) → **KPI-check methodology** (how to verify in a pilot, pass/fail gates) → remaining limitation → risks/guardrails
- **`ux-flow.md`** — a complete UX flow for a clickable software demo of that iteration, ending with a **self-contained prompt you can paste into another AI** to generate the demo

## Presentation flow for this section (the demo choreography)

1. Show the chain view above (one slide, the whole story)
2. Per iteration: **problem (30 s) → change & process map (60 s) → live/pictured demo (60 s) → KPI delta bar vs. previous iteration (30 s) → remaining limitation that motivates the next iteration (15 s)**
3. End with the cumulative slide: baseline vs. Iteration 3 side by side — lead time 21 d → 1.5 d, labour 10 h → 1 h, cost ¥940 → ¥180, capacity ~19 → ~190 — then hand off to Section 7: *"That's the design. Now let's stress-test it."*

## Both benefit views, always (the brief demands it)

Every KPI chart in this section shows two bars per iteration:
- **Incremental** — improvement vs. the previous iteration (what THIS change bought)
- **Cumulative** — improvement vs. the original 12-step baseline (what the CHAIN has bought so far)

Example for Cost/video: Baseline ¥940 → I1 ¥705 (−25% cumulative) → I2 ¥595 (−16% incremental, −37% cumulative) → I3 ¥180 (−70% incremental, **−81% cumulative**). The "small" Iteration-2 step is the enabler of Iteration 3's cliff — narrate it exactly that way.

## Comparison chart pack to build for the deck

- [ ] 4-bar chart × 6 KPIs (baseline + 3 iterations), incremental + cumulative labels
- [ ] Labour waterfall stacked bars (600 → 435 → 350 → 60 min; sync/adaptation visibly deleted in Iter 3)
- [ ] Process map morph: 12 → 10 → 9 → 8 boxes (animate boxes fusing)
- [ ] Constraint-movement diagram: intake → scripting → sync → lawyer approval
