# Slide 11 — Iteration 2: the LLM drafts, humans edit

- **Speaker:** Saeed Filizadeh
- **Time:** 1:00
- **Figures:** none (one-line change + targets-vs-simulation table + capacity banner — no SVG from the manifest)
- **Related appendix:** A4 (iteration simulations)

## On-slide content

**Title:** Iteration 2 — the LLM drafts, humans edit

**The change in one line (directly under the title):**

> **Reverses today's order:** the fine-tuned legal LLM drafts from template + lawyer profile — humans **edit instead of write**. Compliance is encoded in the templates, and every edit becomes labelled fine-tuning data — the flywheel.

**Targets vs simulated (table, left ~55 %):**

| KPI | Target [T] | Simulated | Verdict |
|---|---|---|---|
| Lead time | ~4 d (3–5) | **4.0 d** (P90 5.1) | target hit exactly |
| Human work | 350 min | **351 min** | engine check 350 ✓ |
| Rework | ~30 % | **34 %** | closed form 30 %, seed variation |
| Cost/video | ¥595 | **¥600** | labour ¥498 + tools ¥65 + LLM ¥20 + amort ¥15 |

**Headline banner (right ~45 %, the hero element):**

> **Simulated practical capacity ~38 videos/mo — inside the company-stated ceiling of 35–40 [C] — reached without hiring**

**Honest-framing strip (bottom, full width):**

> **The payoff is not mainly labour minutes:** loops killed **+** ceiling reached **+** Script JSON created (the enabler of Iteration 3) **+** flywheel started

**Status caption (under the table, one line):**

`Simulated design — targets vs simulation, not tested results`

## Layout

- **Background:** solid `#F3F4F6`, full bleed. No figure; the slide is one line, one table, one banner, one strip.
- **Title:** Momo Trust Display, `#262626`, top-left, short-statement grammar; no subtitle. The one-line change sits directly beneath in Inter 26 px text `#262626`, with "edit instead of write" semibold and the flywheel clause after an em dash in body `#4A5565` — max two lines.
- **Table (left ~55 % width):** KPI column Inter 26 px `#0A0A0A`; Target column Inter 24 px muted `#6A7282`; Simulated column Inter 28 px semibold `#0A0A0A` (the anchor of each row); Verdict column Inter 24 px body `#4A5565`. Rows separated by 1 px grey-200 `#E5E7EB` rules; no zebra fill.
- **Headline banner (right ~45 %):** white card, 2 px gold `#C9A86A` border, generous padding, vertically centered against the table. "~38 videos/mo" in accent red `#D92605` semibold — the **only red on the slide**; "reached without hiring" semibold `#0A0A0A`; the ceiling phrase with its [C] tag in body `#4A5565`, tag muted `#6A7282`.
- **Honest-framing strip:** full-width band pinned near the bottom, fill white, 1 px grey-200 `#E5E7EB` border; lead-in "The payoff is not mainly labour minutes:" in Inter italic 24 px body `#4A5565`; the four payoffs as chips ("loops killed", "ceiling reached", "Script JSON created (the enabler of Iteration 3)", "flywheel started") in Inter 24 px `#262626`, joined by gold `#C9A86A` `+`.
- **Status caption:** Inter 24 px, muted `#6A7282`, italic, 2 px wait-line `#A8823F` left rule, directly under the table — the "iterations are simulated designs, not results" discipline made visible.
- **Density check:** 1 title + 1 line + 4 table rows + 1 banner + 1 strip + 1 caption; all text ≥ 24 px (Inter floor per design system). No figure label needed (no figure).

## Speaker notes

**TIME** — 1:00 (Saeed Filizadeh). One-line change ~15 s → table walk ~20 s → capacity banner ~10 s → honest framing ~10 s → constraint moves + hand-off ~5 s. Do not read the cost breakdown aloud.

**MAIN MESSAGE** — Iteration 2 reverses the writing order — the fine-tuned legal LLM drafts from a template plus the lawyer's profile, and humans edit instead of write — and the simulation says that alone puts HiLegal inside its company-stated capacity ceiling of 35–40 videos/month, without hiring.

**SPEAKING POINTS**

1. Bridge from Iteration 1: the brief is now standardized data — Brief JSON is the Script Engine's input contract, so Iteration 1 is not optional infrastructure.
2. **The change in one line:** today humans draft and AI only refines — the order is inverted. From here the LLM drafts against a fixed template enriched with the lawyer's profile (credentials, case highlights, past accepted edits as few-shot examples); the producer edits in a scene editor. Drafting + AI refinement (80 min: 55 + 25) collapses into ~1 min generation + 30 min edit-QC; the process map goes 10 → 9 steps.
3. **Compliance moves from memory to system:** the templates (5 formats) carry the legal-marketing constraints — no outcome guarantees, disclaimer handling — so template constraints plus human QC give two layers.
4. **The flywheel — say this one out loud:** every change request and every producer edit is a labelled training example. The video process *generates* the asset HiLegal most wants to improve — its fine-tuned legal LLM.
5. **Targets vs simulated:** lead 4.0 d against the ~4 d target, hit exactly (P90 5.1); human work 351 min against the 350 target — the engine cross-check closes at 350 ✓; rework 34 % against ~30 % (closed form gives 30 %, seed variation); cost ¥600 against ¥595. For scale: Iteration 1 left us at 6.8 d, 438 min, 59 % rework, ¥705.
6. **The headline:** simulated practical capacity ~38 videos/month — *inside* the company-stated 35–40 ceiling [C], reached without hiring.
7. **Honest framing:** the cost step is modest and that is fine — the payoff is (a) script-loop rework killed, (b) the capacity ceiling reached for real, (c) Script JSON created — the single source of truth that becomes Iteration 3's render input contract, and (d) the flywheel started.
8. Constraint moves, as Theory of Constraints predicts: sync is now 134 of ~350 min ≈ 40 % of all labour — the Script Engine removes writing, not waiting (email-fallback approvals would push lead back to 5.3 d). Hand off: "The script is now data — so let the data render itself. Iteration 3."

**DATA STATUS** — All Iteration-2 numbers are **simulated designs, not tested results**: outputs of `iteration2_sim.py` (same engine lineage as the baseline and Iteration-1 simulations, sanity-checked against their published numbers). Loop probabilities are solved from two anchors — incidence 30 % + E[work] 350 min → ps 0.108, pf 0.216 (pf = 2·ps); script loops cost 10 min (regenerate one scene). Lead 4.0 d assumes in-app approval (~24 h avg); email fallback gives 5.3 d (P90 7.1). The **only [C] number is the 35–40 videos/month ceiling** (company-stated); ~38/mo is simulated against it. [T] = team-set targets. Never say "we reached 38/month" — say "the simulation reaches". Section-7 comparison is labelled *calculated scenario*. Detail in appendix A4.
