# Slide 12 — Iteration 3 — one render: the queue dies

**Speaker:** Saeed Filizadeh
**Time:** 1:15
**Figures:** none (no SVG from the manifest — table + stat slide)
**Related appendix:** `A4-iteration-simulations.md` (per-iteration config anchors, ladder results, practical-capacity criterion, SLA sensitivities)

## On-slide content

**Title:** Iteration 3 — one render: the queue dies

**The change in one line (strip under the title):**

> **Single render = voice + lip-sync + video + all variants** (16:9 / 9:16 / 1:1) — sync · adaptation · generation **deleted** · consent token **hard-gates every render** · delivery + 24 h **parallel** objection window replaces the serial final approval

**Targets vs simulated (left column, the core table):**

| KPI | Target [T] | Simulated |
|---|---|---|
| Lead time | ~1.5 d | **1.6 d** (P90 2.1) |
| Human time | 60 min | **62 min** |
| Cost / video | ¥180 | **¥183** |
| Rework | ~10% | **11%** |
| Utilization (video budget) | — | **8%** |

**Capacity block (right column):**

- **~230/mo** practical capacity (Iteration 2: ~38/mo)
- Lead flat **1.6–2.2 d** from 15 to 200/mo
- **The queue is dead**

**Constraint band (bottom, full width):**

> Residual lead ≈ **100% client approval** — the constraint has left HiLegal's building. Further improvement = managing the client, not more internal automation.

**Guardrail chip (in the constraint band):** `consent on file = zero-tolerance guardrail`

**Footnote (bottom edge, muted):** Iterations are simulated designs, not tested results — pilot gate before any rollout.

## Layout

- **Background:** solid `#F3F4F6`, full bleed; no figure.
- **Title:** Momo Trust Display, ink `#101010`, ~40 px, top-left, one line.
- **Change strip:** full-width white card, 1 px grey-200 `#E5E7EB` border, generous padding, directly under the title. Lead phrase "Single render = voice + lip-sync + video + all variants" in Inter semibold 26–28 px `#0A0A0A`; "deleted" applied to sync · adaptation · generation as strikethrough in grey-400 `#99A1AF`; consent-token and objection-window clauses in Inter 24 px body `#4A5565` with the words "hard-gates" and "parallel" in `#262626` semibold. Variants "(16:9 / 9:16 / 1:1)" muted `#6A7282`.
- **Two columns below the strip:** table left (~55% width), capacity block right (~45%).
- **Table:** Inter ≥ 24 px; KPI column body `#4A5565`; Target column with small gold `[T]` tag (`#C9A86A`); Simulated column Inter semibold ink `#101010`; the utilization target cell an em-dash in muted `#6A7282`; 1 px grey-200 `#E5E7EB` row rules, no vertical rules, no zebra.
- **Capacity block:** "~230/mo" as the slide's largest stat (Momo Trust Display or Inter semibold ~48 px, ink `#101010`); gloss "practical capacity (Iteration 2: ~38/mo)" muted `#6A7282` 24 px; "Lead flat 1.6–2.2 d from 15 to 200/mo" Inter 24–26 px `#262626`; "The queue is dead" in accent red `#D92605` semibold — **the only red on the slide**.
- **Constraint band:** full-width strip pinned near the bottom, fill wait-fill `#F6EEDF`, 2 px wait-line `#A8823F` left border. "Residual lead ≈ 100% client approval" and "the constraint has left HiLegal's building" in Inter semibold 26 px `#262626`; the gloss ("managing the client, not more internal automation") 24 px body `#4A5565`. Guardrail chip to the right inside the band: white pill, 2 px gold `#C9A86A` border, gold text, 24 px.
- **Footnote:** Inter 24 px, muted `#6A7282`, bottom edge, one line, right-aligned. All text ≥ 24 px; no other decoration.

## Speaker notes

**TIME:** 1:15 — ~10 s bridge + the change in one line · ~25 s targets vs simulated · ~15 s capacity · ~15 s constraint band + consent · ~10 s honesty line + handoff to slide 12 (the chain, simulated).

**MAIN MESSAGE:** One render replaces the last four heavy manual steps, every target is validated in simulation — and the queue dies: practical capacity ~230/month with lead time flat from 15 to 200 videos. What remains of lead time is ≈ 100% client approval — the constraint has left HiLegal's building.

**SPEAKING POINTS:**

- Bridge from Iteration 2: the script is already data — now let the data render itself.
- The change in one line: **one render** produces voice + lip-sync + video together and emits all platform variants (16:9 / 9:16 / 1:1). The separate audio track, the 2–3 h manual sync — 134 min, ~40% of all labour — the ~75–80 min manual adaptation, and the 70 min of generation ops cease to exist: four steps, ~280 min, collapse into one automated render plus a deliberate 20-min human QA pass. Nine steps become eight.
- Two governance moves travel with it: the consent token hard-gates every render — compliance by construction, zero tolerance, stop-the-line — and publish plus a 24 h objection window runs in **parallel**, so the last serial wait disappears. An objection costs a 15-min scene re-render inside the window, not a new cycle.
- Walk the table, left to right — every target validated: lead 1.6 d vs the ~1.5 d target, P90 2.1, inside the 1–2 d range; human time 62 min vs 60; cost ¥183 vs ¥180 (down from ¥595 at Iteration 2); rework 11% vs ~10% — the residual is avatar glitches and pronunciation, not process. Utilization of the video budget falls 45% → 8%: capacity stops being the question.
- Capacity block: practical capacity ~230/mo, up from ~38/mo at Iteration 2 — and lead time stays flat at 1.6–2.2 d as demand runs from 15 to 200/mo. **The queue is dead.** This is the whole point of the slide.
- Constraint band: after Iteration 3, residual lead ≈ 100% client approval. The constraint has left HiLegal's building — further improvement means managing the client (SLAs in subscription terms, reminders, escalation), not more internal automation.
- Honesty line, said out loud: these iterations are simulated designs, not tested results — a pilot gate (10 videos, v3 vs v2 cohort) must hold before any rollout.

**DATA STATUS:** Iteration-3 numbers are **simulated targets, never presented as results** (design-system rule). Simulation: `iteration3_sim.py`, same engine lineage, sanity-checked against all three prior rungs; loop probabilities solved from anchors (10% incidence + 60-min work → ps 0.034, pf 0.068); objection window modeled as parallel, no serial wait. Targets are [T]: lead ~1.5 d (1–2), work 60 min, cost ¥180, rework ~10%. Simulated: lead 1.6 d (P90 2.1), work 62 min, cost ¥183 (labour ¥88 + render ¥45 + LLM ¥20 + amort ¥30), rework 11%, QAR ~89%, utilization 8%, work-content ceiling 230/mo (sim 67% basis), practical capacity ~230/mo with lead flat 1.6–2.2 d from 15 to 200/mo. Iteration-2 baselines [C]/model: lead 4.0 d, work 351 min, cost ¥595, rework 34%, capacity ~38/mo, sync 134 min, adaptation ~75–80 min/video, generation ops 70 min. Config anchors, ladder results, and the practical-capacity criterion are in appendix A4.
