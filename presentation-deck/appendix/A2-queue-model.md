# Appendix A2 — The queue model: calibrating μ and validating the math

**Appendix A2 · Q&A** — untimed backup, no speaker, no clock
**Drops on:** any queueing or model challenge — the μ = 23.5 number, the M/M/1 choice, the tail, the simulation (default backup for slides 4, 6)
**Feeds slides:** 4 (current process — one pooled server behind the 3–7 d wait) · 6 (waiting is mathematics)
**Figures:** none — compact math blocks and tables carry it (`why-one-server.svg` sits in the queue folder if the model-choice question turns visual)

## On-slide content

**Eyebrow:** APPENDIX A2 · Q&A BACKUP

**Title:** The queue model: calibrating μ and validating the math

**1 · Why M/M/1 — one pooled server, not two**

- Each video is **held start-to-finish** by a producer — no preemption, no hand-offs mid-video
- The inbox is answered only when a producer **finishes** one → two producers behave as **one pooled server**, not two independent ones
- So: ρ = λ/μ (utilization) · τ = 1/μ (one "turn" of work) · **Wq = ρ/(1−ρ) · τ** (expected wait) · Lq = λ·Wq (parked requests)
- Rates per month; 1 month = 22 working days, 1 wd ≈ 1.4 calendar days

*Label: model assumption, stated on purpose — defensible arrivals (independent lawyers, no coordination); bursts only make waits worse*

**2 · Calibrating μ — anchors → quadratics → least squares**

```
Model:  Wq(λ, μ) = ρ/(1−ρ) · τ = λ/(μ−λ) · 22/μ  [wd]   ×1.4 → calendar days

Anchor 1 — pin the heavy month (λ = 20, ~7 d):
        20/(μ−20) · 22/μ · 1.4 = 7   →  μ² − 20μ − 88 = 0    →  μ = 23.7
Anchor 2 — pin the light month (λ = 15, ~3 d):
        15/(μ−15) · 22/μ · 1.4 = 3   →  μ² − 15μ − 154 = 0   →  μ = 22.0
Bracket:        22.0 ≤ μ ≤ 23.7
Least squares (both anchors):  min (Wq(15)−3)² + (Wq(20)−7)²   →  μ = 23.66 ≈ 23.5
```

- Rejected first attempt: 100% dedication → μ = 352 h ÷ 10 h = 35.2 → predicts Wq = 0.9 d — contradicts the reported 3–7 d [C]; pickups are not instant, so the one knob μ absorbs availability, meetings and context switching
- One knob, one observation: the heavy end pins μ, because Wq grows exponentially in ρ

*Label: estimate — μ calibrated, not measured*

**3 · Verification — μ = 23.5 reproduces the whole band [C]**

| λ [C] | ρ = λ/23.5 | Wq (calculated) | Observed [C] | |
|---|---:|---:|---:|---|
| 15 | 0.64 | 2.3 d | ~3 d | ✓ |
| 17.5 | 0.74 | 3.8 d | 3–7 d | ✓ |
| 20 | 0.85 | 7.5 d | ~7 d | ✓ |

- Worked, typical month: ρ = 17.5 ÷ 23.5 = 0.745 → multiplier 2.92 → Wq = 2.92 × 0.94 wd = 2.73 wd × 1.4 = **3.8 d**
- The model reproduces the band *including its workload-dependence* — the observation HiLegal reported [C]

*Label: calculated (M/M/1, μ = 23.5) vs company-reported band*

**4 · Cross-check — 67% vs 65%, two routes to the same answer**

| Route | Arithmetic | Result |
|---|---|---:|
| μ-implied (from wait times) | 23.5 × 10 h = 235 h ÷ 352 h available | **67%** of producer time on video work |
| Independent estimate (kpi-data.md) | producers are not 100% dedicated — meetings, admin, context switching | **~65%** availability |

- 352 h = 2 producers × 22 wd × 8 h — the same input as Section 2's table
- Had calibration landed at e.g. μ = 33 (94% busy), it would contradict reality. **67 ≈ 65 → μ = 23.5 is credible**

*Label: calculated (μ-implied) vs estimate (availability)*

**5 · Predictions — countable, not just descriptive**

- **Lq = λ·Wq** (λ per working day): 17.5 ÷ 22 × 2.73 wd = **2.2** typical · 20 ÷ 22 × 5.35 wd = **4.9** heavy → the inbox should hold **≈ 2–5 parked requests** — *falsifiable: HiLegal can count it*
- Waits are exponential; drain rate (23.5 − 17.5)/22 = 0.273/wd → tail: 28% (>5 d) · **19% (>7 d)** · 11% (>10 d) · 5% (>14 d)
- **P90 ≈ 10 d** — solves 0.745 · e^(−0.273·t) = 0.10 → t = ln 7.45 ÷ 0.273 = 7.4 wd: 1 in 10 lawyers waits 2 weeks just to be looked at; "workload-dependent" [C] *is* this fat tail
- P(arrival waits at all) = ρ ≈ 0.745 → **3 in 4** new requests find the team busy

*Label: calculated — falsifiable prediction*

**6 · Nonlinearity — the multiplier is the villain**

| ρ | 0.64 | 0.74 | 0.85 | 0.90 | 0.95 | → 1 |
|---|---:|---:|---:|---:|---:|---:|
| ρ/(1−ρ) | 1.8 | 2.9 | 5.7 | 9.0 | 19 | ∞ |

- Demand **×1.33** (15 → 20) but wait **×3.2** (2.3 → 7.5 d) — the process climbed the multiplier ladder
- Effort moves λ or μ a little; the multiplier turns small moves into large waits — "working harder" fails, only process change moves μ
- The wall: at λ ≥ μ = 23.5, Wq → ∞. The 100%-dedication ceiling 352 h ÷ 10 h = 35.2/month ≈ stated 35–40 [C] *is* the ρ = 1 wall; a λ = 24 marketing push gives ρ = 1.02 — the queue never drains

*Label: calculated*

**7 · Validation — what the 200k-order simulation checks (and what it can't)**

```
200 000 random orders · strict FIFO single server
exponential arrivals at λ · exponential service at μ
Wq, Lq, ρ re-derived from events alone — no formulas

match: 0.7% (λ = 17.5) · 1.2% (λ = 20)
```

- **Validates the algebra:** the formulas are exactly what happens when you run the modeled process — no slip, no wrong plug-in
- **Does not validate the assumptions:** the simulation draws from the same assumptions as the formulas (Poisson, exponential service, one server) — internal consistency, not real-world fit
- Real-world fit is carried by: the **calibration** (μ reproduces the 3–7 d band across the demand range [C]) + the **67 ≈ 65 cross-check** + the **falsifiable inbox count**

*Label: validation — internal consistency only*

## Layout

- Background `#F3F4F6`; **seven white cards** in a 2 + 3 + 2 grid, 1 px `#E5E7EB` borders, generous padding. Q&A density is acceptable; the numbered headings keep the answer pattern scannable.
- Row 1: card 1 (why M/M/1, ~38%) + card 2 (calibration, ~62% — **the spine**; give it the most height, the math block is the slide's centerpiece).
- Row 2: card 3 (verification, ~36%) + card 4 (67/65 cross-check, ~28%) + card 5 (predictions, ~36%).
- Row 3: card 6 (nonlinearity, ~46%) + card 7 (validation, ~54%).
- Card headings: Inter semibold 26 px `#262626`, numbered ("1 · Why M/M/1 — …") so each likely question maps to one card. Thin **gold `#C9A86A` rules** under every derived result: μ = 23.7, μ = 22.0, μ = 23.66 ≈ 23.5, the ✓ column, 67% ≈ 65%, ≈ 2–5 parked requests, P90 ≈ 10 d, the 0.7%/1.2% match line.
- **Math blocks** (cards 2 and 7) on wait-fill `#F6EEDF` panels with a 2 px wait-line `#A8823F` left rule — the queue's signature banding, echoing slide 6's quote band. Set in Inter 24 px `#262626`, tabular figures, aligned on the `=` signs; derived roots (μ = 23.7, μ = 22.0, μ = 23.66 ≈ 23.5) semibold.
- Tables: Inter 24 px; numerals right-aligned, tabular figures; ρ and Wq columns in `#262626`, observed column in muted `#6A7282`; header row muted caps.
- **Accent red `#D92605` used twice only:** the **×3.2** and the **∞** cell — the two numbers that carry "why working harder fails" (consistent with slide 6, where ×3.2 is also the one red element). Bold black `#0A0A0A` with gold underline for **≈ 2–5 parked requests** — the falsifiable prediction is the slide's one highlighted positive.
- Design-system labels under each card as listed; card 2 also carries the chip "calibrated, not measured".
- Title in Momo Trust Display, `#0A0A0A`, one line, short-statement grammar; eyebrow "APPENDIX A2 · Q&A BACKUP" in muted `#6A7282`, Inter 24 px, letterspaced caps.
- Body lines: Inter 24 px body `#4A5565`, key phrases bold in `#262626`. All text ≥ 24 px. No icons, no decoration beyond the rules, bands and labels.

## Speaker notes

**MAIN MESSAGE:** This slide exists so that any queueing challenge is answered in one move, always the same pattern: **name the model choice → show the calibration → point at the falsifiable prediction.** Never defend μ without saying "calibrated [E], not measured." Prepared answers:

1. *"Why one server? There are two producers."* → Card 1: a video is held start-to-finish, no preemption, so the inbox is only picked up when a producer *finishes* one — the pickup process behaves as one pooled unit. Two independent servers would require instant dispatch, which nobody does.
2. *"Where does 23.5 come from?"* → Card 2, in order: pin the heavy month (7 d, λ = 20) → quadratic μ² − 20μ − 88 = 0 → μ = 23.7; pin the light month (3 d, λ = 15) → μ = 22.0; that brackets μ; least squares on both anchors → 23.66 ≈ 23.5. One knob, one observation — then verified three independent ways.
3. *"Couldn't μ be anything, since you fitted it?"* → Card 3 + 4: μ = 23.5 reproduces the *whole* observed band across the *whole* demand range, and its implied labour (67%) agrees with the independently reasoned availability (~65%). A wrong μ (e.g. 33, 94% busy) would have contradicted one of the two.
4. *"Is the simulation proof the model is right?"* → Card 7, and say it crisply: the 200k-order simulation validates the **algebra** — that the formulas are what actually happens when you run the modeled process (0.7–1.2% match). It does **not** validate the assumptions — it shares them. Real-world fit comes from calibration + the labour cross-check + the inbox count.
5. *"What would change your mind?"* → The falsifiable prediction: the inbox should hold ≈ 2–5 parked requests. If it never exceeds 1 while waits still run 3–7 days, the delay is batch-review cadence (producers checking intake twice a week), not queueing — and we model it differently. Either way the fix starts with intake.
6. *"How bad does one lawyer's wait get?"* → The tail: P(> 7 d) = 19% — 1 in 5 waits over a week before production starts; P90 ≈ 10 d — 1 in 10 waits two weeks just to be looked at. "Workload-dependent" [C] is this fat tail.
7. *"What about the ceiling they state, 35–40/month?"* → That is 352 h ÷ 10 h = 35.2 — the ρ = 1 wall at 100% dedication, not an operational target. Pushing toward it is a mathematical promise of unbounded waiting; at λ = 24, ρ = 1.02 and the queue never drains.
8. Scope guard: this models the **intake queue only** — client approval-gate waits sit on top of it. With churn/overtime (Section 2), reality is likely worse than modeled.

**DATA STATUS:** **[C] company-reported:** demand 15–20/month; observed intake wait 3–7 d; ~10 h labour/video; 352 h/month available (2 × 22 wd × 8 h); "workload-dependent" complaint; stated ceiling 35–40/month. **[E] estimates:** μ = 23.5 calibrated (the one knob); ~65% producer availability (kpi-data.md, single source of truth). **Calculated from the model:** quadratics μ² − 20μ − 88 = 0 → 23.7 and μ² − 15μ − 154 = 0 → 22.0 (exact roots); least-squares optimum 23.66, rounded to 23.5; ρ 0.64/0.74/0.85; Wq 2.3/3.8/7.5 d; 67% = 235/352 h; Lq 2.2–4.9 (the ≈ 2–5 inbox prediction); tail 28/19/11/5% at 5/7/10/14 d; P90 ≈ 10 d; multiplier ladder 1.8 → 2.9 → 5.7 → 9.0 → 19 → ∞; ×3.2 vs ×1.33; ceiling 35.2. **Validation:** 200k-order FIFO discrete-event simulation, 0.7% (λ = 17.5) / 1.2% (λ = 20) — internal consistency only. Arithmetic on-slide is exact; 22.0 is an exact root (√841 = 29), 23.7 and 23.66 rounded as in the source. Say "calibrated model", never "measured". Sources: Section-3 summary calibration block (`calibrate_mu.py`), queue folder (`queue_model.py`, `queue_model-explained.md`, SUMMARY.md); kpi-data.md for the 65% availability. This appendix backs up slides 4 and 6.
