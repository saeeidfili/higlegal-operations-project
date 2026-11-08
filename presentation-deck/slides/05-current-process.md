# Slide 5 — The current process: ~10 hours of work spread over 2–4 weeks

- **Speaker:** Augustin Dulon
- **Time:** 1:15
- **Figures:** `../04 These are the wastes and root causes/queue/order-timeline.svg` — Lawyer Chen's order through the 12 steps: green = work, red = waiting; 18.8 d end-to-end, work ≈ 6%. Label: **company-reported / calculated**.
- **Related appendix:** A2 (`appendix/A2-queue-model.md` — μ calibration, M/M/1 predictions, nonlinearity, 200k-order validation, 67/65% cross-check)

## On-slide content

**Title:** The current process: ~10 hours of work spread over 2–4 weeks

**Punchline numbers (stat band, left column):**

| 12 steps | ~10 h work | 14–28 d lead | work ≈ 6% of lead | PCE ≈ 5–8% |
|---|---|---|---|---|
| [C] | [C] | [C] | calculated | [E] |

**Three rejection loops** (clarify → intake · approval → drafting · final approval → script) drive rework.

**One-line process summary (bottom strip, small type):**

request → intake queue 3–7 d → clarify ×2–4 → brief → draft → AI refine → approvals → generate video+audio → manual sync 2–3 h → publish/adapt ~2 h

**Figure (main visual, right, large):** `order-timeline.svg` — Lawyer Chen's order, 18.8 d end-to-end, work ≈ 6%. Caption: *One real order through all 12 steps — green is work, red is waiting. **company-reported / calculated***

## Layout

- **Text left (~40%):** title, then the punchline number band as five stacked/large stats (12 steps · ~10 h · 14–28 d · ≈ 6% · PCE 5–8%), rejection-loops line, source tags `[C]`/`[E]`/calculated in muted small type under each stat.
- **Figure right (~60%), dominant:** `order-timeline.svg` at native aspect ≈ 1.6:1, largest box that fits the right column. Red waiting dominates the bar — let it carry the message; no extra decoration.
- **Bottom strip full-width:** one-line process summary in Inter, small, muted `#6A7282`; arrows in grey-400 `#99A1AF`. The two waits (intake 3–7 d) and bottleneck (sync 2–3 h) may be set in accent red `#D92605`.
- **Tokens:** title Momo Trust Display, black `#0A0A0A`; body Inter ≥ 24 px, body `#4A5565`; stats in ink `#101010` with `≈ 6%` allowed one accent-red hit; figure caption Inter small, muted, with data-status label. Background `#F3F4F6`; figure is transparent-background SVG, no border box.

## Speaker notes

**TIME** — 1:15. ~20 s process walk, ~30 s figure, ~25 s punchline numbers + handoff.

**MAIN MESSAGE** — The time is not spent making the video; it is spent waiting. ~10 hours of real work stretched across 2–4 weeks — the process is queue-gated, not work-gated.

**SPEAKING POINTS**
- Walk the one-liner once, fast: request → 3–7 days just sitting in the intake queue → 2–4 clarification rounds → brief, draft, AI refine → approvals → video + audio generation → 2–3 h of *manual* AV sync → publish and adapt (~2 h).
- Point at the figure: this is one real order — Lawyer Chen's — 18.8 days end-to-end. The green slivers are work; everything red is waiting. Work is ≈ 6% of lead time.
- Hit the stat band: 12 steps, ~10 hours of work, 14–28 days of lead time — all company-reported. Work ≈ 6% means ~94% is waiting; Process Cycle Efficiency ≈ 5–8% is our single most quotable baseline.
- Name the three rejection loops — clarify-back-to-intake, script approval back to drafting, final approval back to script — they are where the rework lives. Dedi takes the wastes and root causes next.

**DATA STATUS** — 12 steps [C] (confirmed with HiLegal Sept 2026), ~10 h work [C], 14–28 d lead [C], intake wait 3–7 d [C], manual AV sync 2–3 h [C], publishing/adaptation ~2 h [C]. Work ≈ 6% of lead time: calculated from ~10 h vs 14–28 d. PCE ≈ 5–8% [E]. Figure mixes company-reported step times with calculated percentages — hence the dual label *company-reported / calculated*. The μ calibration behind the queue numbers is in A2.
