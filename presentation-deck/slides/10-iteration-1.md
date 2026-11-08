# Slide 10 — Iteration 1 — standardize briefing and approvals: the front door

- **Speaker:** Saeed Filizadeh
- **Time:** 1:15
- **Figures:** none (text + small KPI table — no SVG from the manifest)
- **Related appendix:** A4 (`appendix/A4-iteration-simulations.md` — per-iteration config anchors, ladder results, practical-capacity criterion, SLA sensitivities)

## On-slide content

**Title:** Iteration 1 — standardize briefing and approvals: the front door

**Status chip (top-right, persistent):** `simulated design with targets — not tested results`

**The change in one line:**

> Structured self-serve form + 30 s format previews + 48 h SLA'd approvals — intake queue and clarification loop **deleted at the source**. No new AI.

**KPI table — targets vs simulated:**

| KPI | Baseline | Target [T] | Simulated |
|---|---|---|---|
| Lead time | 21.8 d | ~9 d (7–12) | **6.8 d** (P90 9.9) |
| Human time | 600 min | 435 min | **438 min** |
| Rework | 87% | ~55% | **59%** |
| QAR | ~13% | ~45% | **~41%** |

*Table footnote:* `Target [T] = design target · Simulated = output of the calibrated engine (baseline sanity-check reproduces 21.8 d / 600 min / 87%)`

**Self-validation (small band under the table):**

> Baseline's simulated practical capacity **~20/mo** reproduces the company-reported **15–20/mo [C]** — the criterion proves itself before we trust its Iter-1 answer.

**Sensitivity note (one line):** Gate-dominated — lead swings **5.1–8.2 d** on lawyer behaviour (approves in ~1 d → near the 48 h cap); even the breach case stays inside the 7–12 d target.

**Bridge (bottom band):** Front door fixed — manual scripting is the next constraint (labour still ~7 h 20, ~6 h 40 of it the manual middle).

## Layout

- **Background:** solid `#F3F4F6`, full bleed; no figure — the table and the change line carry the slide.
- **Title:** Momo Trust Display, black `#0A0A0A`, top-left, one line if it fits, two max; short-statement grammar.
- **Status chip:** Inter 24 px, muted `#6A7282`, 2 px grey-400 `#99A1AF` border pill, top-right aligned with the title baseline — the "never present as results" rule made visible.
- **Change line:** white card, 1 px grey-200 `#E5E7EB` border, generous padding, Inter 26–28 px text `#262626`; the three mechanisms (form · previews · SLA'd approvals) set as semibold; **accent red `#D92605` used once on the slide** for "deleted at the source"; "No new AI." as a short muted `#6A7282` tail on the same line.
- **KPI table:** dominant block, center-left, ~55 % width; header row Inter 24 px muted `#6A7282`; baseline column body `#4A5565`; Target [T] column ink `#101010` with `[T]` tag in gold `#C9A86A`; **Simulated** column Inter semibold ~30 px ink `#101010` (the eye's landing zone); 1 px grey-200 `#E5E7EB` row rules, no vertical rules. P90 glosses in 24 px muted.
- **Table footnote:** Inter 24 px, muted `#6A7282`, one line directly under the table — carries the *target / simulated* data-status labelling for the slide.
- **Self-validation band:** wait-fill `#F6EEDF` strip, 2 px wait-line `#A8823F` left border (echoes the falsifiability chip of slide 6), Inter italic 24–26 px text `#262626`; the two numbers (~20/mo, 15–20/mo [C]) in semibold.
- **Sensitivity note:** Inter 24 px body `#4A5565`, one line full width under the validation band; "Gate-dominated" lead word semibold `#262626`; the 5.1–8.2 d range in ink semibold.
- **Bridge band:** bottom strip pinned ~64 px from the bottom edge, white fill, 1 px grey-200 `#E5E7EB` border; Inter 26 px, "manual scripting is the next constraint" semibold `#0A0A0A`; numbers muted.
- All text ≥ 24 px. No other decoration.

## Speaker notes

**TIME** — 1:15 (Saeed Filizadeh). Setup/bridge ~10 s → the change ~15 s → KPI table ~20 s → self-validation ~10 s → gate sensitivity ~10 s → bridge to Iteration 2 ~10 s. Do not read the table cell by cell — lead with lead time, gesture at the rest.

**MAIN MESSAGE** — The cheapest iteration goes first and fixes the front door: pure process design, no new AI, and it deletes the intake queue and clarification loop at the source — simulated to land at 6.8 days against a 9-day target.

**SPEAKING POINTS**

1. Bridge from slide 9: the KPI scoreboard is set — the first iteration attacks the front door. It is the cheapest, fastest change, it is pure process design (no new AI), and it produces the structured Brief data Iterations 2 and 3 are built on.
2. The problem, in numbers: 3–7 days before work starts [C], a brief loop of ≥4 iterations [C], ~90% rework [E] under un-SLA'd email approvals — 21 d lead, ~94% waiting.
3. The change: a structured self-serve intake form (12 fields, 5-format catalogue with 30 s previews so the lawyer sees the end-shape before requesting), auto completeness check and routing — **the intake queue and clarification loop are deleted at the source**, not accelerated — plus mobile approvals on a 48 h SLA with 24 h/40 h reminders and escalation, change requests tied to scene + reason code. Process map drops 12 → 10 steps; the manual production middle is deliberately untouched.
4. Walk the table once, honestly: these are **targets and simulations, not tested results**. Lead 21.8 d → ~9 d target, **6.8 d simulated** (P90 9.9); human time 600 → 435 target, **438 simulated** (engine check against the 435 closed form ✓); rework 87% → 55 target, **59 simulated** (closed form says 55; seed variation); QAR ~13% → ~45 target, **~41 simulated**.
5. Why trust the engine — self-validation: run the same criterion on the baseline and it gives practical capacity ~20/mo, which reproduces the company-reported 15–20/mo [C]. The criterion proves itself on the baseline before we trust its Iter-1 answer.
6. Gate-dominated: lead swings 5.1–8.2 d depending on lawyer behaviour — approves in ~1 d versus always near the 48 h cap. Iteration 1's lead time depends on the lawyers, not on internal production; even the breach case stays inside the 7–12 d target.
7. Bridge: the front end is fixed, but labour is still ~7 h 20, ~6 h 40 of it the manual middle — **manual scripting is the next constraint**, and it needs structured Briefs, which now exist. "We standardized what the client sends us. Now let's make the machine do the writing." Hand off to slide 10.

**DATA STATUS** — Iteration 1 is a **simulated design with targets — never presented as tested results** (status chip on-slide; per design-system rule). Baseline column: 21.8 d / 600 min / 87% are the calibrated baseline model's outputs (engine sanity-checked: reproduces 21.8 d, 600 min, 87%). Target [T] column: design targets. Simulated column: outputs of `iteration1_sim.py` (Section-4 engine; loop probabilities from two anchors — rework incidence 55% and E[work] = 435 min → ps ≈ 0.214, pf ≈ 0.428; structured change requests make loops cheaper, previews kill clarification entirely). Self-validation: baseline practical capacity ~20/mo is model-calculated against company-reported 15–20/mo [C]. Sensitivity: gate waits U(0.25–1.0) / U(0.5–1.5) / U(1.0–1.6) working days → 5.1 / 6.8 / 8.2 d, P90 7.4 / 9.9 / 12.4. Problem framing: 3–7 d [C], brief loop ≥4 [C], ~90% rework [E]. Detail in appendix A4.
