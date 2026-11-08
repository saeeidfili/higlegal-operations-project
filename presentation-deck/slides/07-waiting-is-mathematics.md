# Slide 7 — Waiting is mathematics

**Speaker:** Saeed Filizadeh
**Time:** 1:15
**Figures:** `../04 These are the wastes and root causes/queue/queue-cliff.svg` (THE chart — utilization cliff; place large)
**Related appendix:** `A2-queue-model.md`

## On-slide content

- Eyebrow: `WHY THE WAIT`
- Title: `The 3–7 day wait is not a people problem — it is mathematics`
- Left column, four facts (few words, numbers bolded):
  1. `One pooled server → M/M/1` — `video held start-to-finish; the inbox is answered only when someone frees up`
  2. `μ = 23.5 videos/month, calibrated [E]` — `reproduces 2.3–7.5 d waits across demand 15–20/month [C]`
  3. `ρ = 0.64–0.85` — `demand ×1.33 → wait ×3.2  (multiplier ρ/(1−ρ))`
  4. `P90 ≈ 10 d` — `1 in 10 lawyers waits 2 weeks just to be looked at`
- Falsifiability chip (small, under the facts): `Falsifiable: the inbox should hold ≈ 2–5 parked requests — HiLegal can count them`
- Figure: `queue-cliff.svg`, placed large, right side — utilization cliff with observed 3–7 d band, demand dots, and the ρ = 1 wall
- Figure label: `calculated + company-reported — curve calculated (M/M/1, μ = 23.5 calibrated [E]); observed 3–7 d band and demand 15–20/month company-reported [C]`
- Pull quote (bottom band, the one-liner):

  > "At ρ ≈ 0.74–0.85, the 3–7 day intake wait is not a people problem — it is the mathematics of standing on the steep part of the utilization cliff."

## Layout

- **Background:** solid `#F3F4F6`, full bleed. Figure dominant: right ~62 % of slide width, vertically centered, as large as the 1.53:1 aspect allows (SVG, transparent background).
- **Eyebrow:** Inter, 24 px, all caps, letter-spacing 0.15 em, gold `#C9A86A`.
- **Title:** Momo Trust Display, ink `#101010`, ~44 px, left-aligned, three lines, top-left; occupies left column's upper third.
- **Left column** (~32 % width): title, then the four facts as a compact stack — each fact's lead number/phrase in Inter semibold 28 px text `#262626`, its one-line gloss in Inter 24 px body `#4A5565`; separated by 16 px of whitespace, no bullets, no boxes.
- **Accent red `#D92605`** used once only: the `×3.2` in fact 3 — the single number the eye should catch.
- **Falsifiability chip:** Inter 24 px, muted `#6A7282`, italic, with a 2 px wait-line `#A8823F` left rule; sits under the facts, above the quote band.
- **Figure callouts** (in the SVG, not added text): observed 3–7 d band in wait-fill `#F6EEDF` / wait-line `#A8823F`; the ρ = 1 wall rendered as the curve's vertical asymptote. Do not overlay extra text on the figure.
- **Figure label:** Inter, 24 px, muted `#6A7282`, one line directly under the figure, right-aligned to the figure's right edge.
- **Pull quote band:** full-width strip pinned ~64 px from the bottom edge, fill wait-fill `#F6EEDF`, 2 px wait-line `#A8823F` left border; quote in Inter italic 26 px text `#262626`. No attribution needed — it is the team's line.
- All text ≥ 24 px. No other decoration.

## Speaker notes

**TIME:** 1:15 — about half on the chart and the cliff, half on the tail and the falsifiable prediction. Hand off to slide 7 (rework).

**MAIN MESSAGE:** The 3–7 day intake wait is not slack people — the team stands on the steep part of the utilization cliff, and the mathematics of that position produces the wait.

**SPEAKING POINTS:**

- Bridge from slide 6: we know where the time goes — 94 % waiting; now, why the wait.
- Model choice, in one breath: each video is held start-to-finish, so the inbox is only picked up when a producer finishes one — the team behaves as one pooled server, so M/M/1 is the honest description, not two independent servers.
- μ = 23.5 videos/month is calibrated, not measured — it reproduces the observed waits, 2.3–7.5 days, across the whole demand range of 15–20/month.
- Walk the chart: ρ = 0.64–0.85 puts HiLegal on the cliff's steep part. Demand ×1.33 (15 → 20) multiplies the wait ×3.2 — that is the multiplier ρ/(1−ρ), and it is why "work harder" fails: near the wall, effort buys almost nothing.
- The tail: waits are exponential — P90 ≈ 10 days, so 1 in 10 lawyers waits two weeks just to be looked at. The "workload-dependent" complaint [C] *is* this fat tail.
- Make it falsifiable: the model says the inbox should hold ≈ 2–5 parked requests — HiLegal can simply count them. If the inbox never exceeds 1 while waits run 3–7 days, the delay is batch-review cadence, not queueing, and we model it differently.
- Land the one-liner (on-slide quote), then continue: "And on top of the queue, every failed gate adds rework — that's slide 7."

**DATA STATUS:** Numbers from the queue model summary only. Company-reported [C]: demand 15–20/month, observed 3–7 d waits, ~10 h/video, 352 h/month available, "workload-dependent" complaint. Estimate [E]: μ = 23.5 calibrated, not measured. Calculated from the model: ρ 0.64–0.85, Wq 3.8–7.5 d, Lq 2.2–4.9 (the ≈2–5 inbox prediction), P(Wait > 7 d) = 19 %, P90 ≈ 10 d, ×3.2 multiplier. Validation: a 200k-order FIFO simulation reproduces the algebra at 0.7 % (λ = 17.5) / 1.2 % (λ = 20) — internal consistency only; real-world fit rests on the calibration, the 67 % / 65 % labour cross-check, and the falsifiable inbox count. Say "calibrated model", never "measured". Detail in appendix A2.
