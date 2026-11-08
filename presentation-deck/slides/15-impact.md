# Slide 15 — The impact: operations stops taxing the strategy and starts compounding it

- **Speaker:** Joel Wirth
- **Time:** 1:15 (starts ≈ 13:00, after slide 14; hands off to slide 16 at ≈ 14:15)
- **Figures:** none — four gain → outcome bands + one strategy strip
- **Related appendix:** A1 (`appendix/A1-costing.md` — ¥940 build-up, per-customer bleed tables), A6 (`appendix/A6-assumptions-and-models.md` — assumption ladder, model cards)

## On-slide content

**Eyebrow:** THE IMPACT · GAIN → OUTCOME

**Title:** The impact: operations stops taxing the strategy and starts compounding it

**Four gain → outcome rows (exact):**

| Gain | | Outcome | |
|---|---|---|---|
| **Capacity** — ~19 → ~190 videos/mo · same two producers | → | **The paid service can scale to every tier without hiring** — video stops being the reason to say "no" | *if* demand exceeds 19/mo and grows with subscribers **[E]** |
| **Cost** — ¥940 → ¥180 per video | → | **Typical customer flips −¥1,160 → +¥360/month** · volume burn −¥150–195k/yr → ≈ break-even | *if* the typical customer uses ~2 of 10 videos **[E]** |
| **Human time** — 10 h → 1 h per video | → | **≈ ¥270k/yr production payroll released to the core** — money and attention, not video-maker hours, fund the LLM | *if* saved payroll funds the core, not overhead **[E — management decision]** |
| **Flywheel** — every edit + change request = labelled training data (Iter 2) | → | **The video process improves the legal LLM** — service and core asset reinforce each other | *if* the fine-tuning backlog is maintained **[E]** |

**Strategy line (bottom strip):** **Strategy —** the moat is maintained by a pipeline — and the pipeline generates fine-tuning data.

## Layout

- 16:9 canvas, white background; no figure, no icons — the four arrows and one red number are the visual. Eyebrow in muted `#6A7282`, Inter, 24 px, letterspaced caps.
- Title in Momo Trust Display, `#0A0A0A`, left-aligned, two lines max; keep the colon grammar intact.
- **Four gain → outcome bands** stacked with 1 px grey-200 `#E5E7EB` rules between them; each band ~15 % of slide height, generous padding. Three zones per band on one shared sight-line:
  - **Gain (left, ~36 % width):** category label ("CAPACITY", "COST", "HUMAN TIME", "FLYWHEEL") Inter 24 px caps muted `#6A7282`; the gain figures Inter semibold 28 px ink `#101010`, with the *within-gain* arrow (~19 → ~190) in grey-400 `#99A1AF`.
  - **Arrow (center column, all four aligned on the same vertical axis):** single "→" in gold `#C9A86A`, Inter 32 px — reads left-to-right as the section's logic: gain becomes outcome.
  - **Outcome (right, ~55 % width):** lead phrase Inter semibold 26 px `#0A0A0A`; the tail after the dash Inter 24–26 px body `#4A5565`. Directly beneath, the connecting assumption: Inter italic 24 px muted `#6A7282`, with the tag **[E]** / **[E — management decision]** in grey-400 `#99A1AF` — visible at reading size, never footnote-sized.
- **Accent red `#D92605` appears exactly once: +¥360** in row 2 — the unit-economics flip is the slide's landing zone. Deliberate inversion of slide 3: there red marked the bleed (−¥1,160); here −¥1,160 stays body `#4A5565` as the "before" state, and red marks the payoff. ~190, ¥180 and ¥270k stay ink — no second red.
- **Strategy strip (bottom, full width):** gold `#C9A86A` 4 px left rule, ink `#101010`, Inter 26 px; "Strategy —" semibold, rest regular. Same thesis-strip treatment as slide 3 — a deliberate bookend: the thesis opened the fix, this closes it.
- Density check: 1 title + 4 bands + 1 strategy strip; all text ≥ 24 px; no other decoration.

## Speaker notes

**TIME** — 1:15 (Joel Wirth). Bridge ~5 s → four rows ~60 s (≈ 13–15 s each, walk top-down) → strategy strip ~7 s → hand-off ~3 s. Not on the compress list (only slides 8 and 12 are) — but if badly over, rows 1 and 4 compress to one sentence each; never cut row 2.

**MAIN MESSAGE** — The headroom is worth something concrete: scale without hiring, a typical customer that flips from −¥1,160 to +¥360 a month, ≈ ¥270k/yr of payroll released to the core, and a process that feeds the legal LLM. Operations stops taxing the strategy and starts compounding it.

**SPEAKING POINTS**

1. Bridge from slide 14: the design held up under stress — so the process now has headroom. The question HiLegal's leadership actually asks is: **what is that headroom worth?** Four answers, each with its assumption stated on the slide.
2. **Capacity** — same two producers, ~19 → ~190 videos/month. *If* demand exceeds 19/mo and grows with subscribers [E], the paid service scales to every tier **without hiring** — video stops being the reason to say "no", and capacity stops capping pricing and packaging experiments.
3. **Money** — cost ¥940 → ¥180 per video. *If* the typical customer uses ~2 of their 10 videos [E], that customer flips from −¥1,160 to **+¥360 a month** (the red number), and the volume burn of −¥150–195k/yr goes to ≈ break-even — before any revenue growth. Add the payroll below and the finance story closes itself.
4. **Payroll** — human time 10 h → 1 h per video; at 20 videos/month the whole team load is ~4 h/month. That is ≈ ¥270k/yr of production payroll released — *if* management explicitly redirects it to the core [E — management decision]; absorbed as overhead, the strategic gain deflates. Section 9 makes that budget decision explicit. Money and attention fund the LLM — not video-maker hours.
5. **Flywheel** — every edit and change request is labelled training data (Iteration 2). *If* the fine-tuning backlog is maintained [E], the video process improves the legal LLM: the service and the core asset reinforce each other. This is the row that changes what the process *is*.
6. Strategy close — read the strip, slowly: today the moat is maintained by hand, one video at a time. After three iterations, the moat is maintained by a pipeline — and the pipeline generates fine-tuning data. That is the title of this slide: operations stops taxing the strategy and starts compounding it.
7. Credibility beat: every claim on this slide carries its [E]/[C] tag; the assumption ladder behind them — ¥85/h at 60 % utilization, ¥117 revenue attribution, demand 20 → 40+/mo, QAR ≥ 90 % held — is in A6. Risks we named before you do: bespoke expectations (priced escalation path), two people / one brain-drain risk (cross-train both; playbooks in Section 9), change fatigue (phased rollout).
8. Hand-off: "So what does it cost, and when does it pay back?" → slide 16.

**DATA STATUS** — Rows are the Section-8 impact map verbatim, tags on-slide: capacity ~19 → ~190/mo, same two producers, conditional on demand > 19/mo growing with subscribers [E]; cost ¥940 → ¥180/video with typical usage ~2 of 10 videos [E] → −¥1,160 → +¥360 per typical customer-month and −¥150–195k/yr → ≈ break-even [E]; human time 10 h → 1 h (~4 h/mo team load at 20 videos) → ≈ ¥270k/yr (≈ 1.5 FTE) released, conditional on a management reallocation decision [E]; flywheel conditional on the fine-tuning backlog being maintained [E]. Cross-deck consistency: slide 12's scoreboard quotes the Section-7 ladder figures ~230/mo and ¥182/video; this slide follows the Section-8 map's ~190/mo and ¥180 — same Iteration-3 design, different rounding/source run; if challenged, quote both and attribute each. Ladder beneath the numbers: labour ¥85/h · 60 % utilization [E] (utilization back-solved from output [C]); revenue attribution ¥117 [C] (direction robust at −81 %); demand at scale 20 → 40+/mo consistent with the stated 35–40 ceiling [C] — at 20/mo gains 2–3 still hold, gain 1 partially idles; quality held at QAR ≥ 90 % via pilot gates; render ≈ ¥45 [E] (±¥10 → ±6 %, immaterial). Detail in A1 (costing) and A6 (assumption ladder, model cards).
