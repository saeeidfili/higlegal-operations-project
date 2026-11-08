# Appendix A4 — The iteration simulations: anchors, ladders, and practical capacity

**Appendix A4 · Q&A** — untimed backup, no speaker, no clock
**Drops on:** any challenge to a Section-6 simulation number — method, loop probabilities, ladder, capacity (default backup for slides 9, 10, 11, 12)
**Feeds slides:** 9 (Iteration 1) · 10 (Iteration 2) · 11 (Iteration 3) · 12 (the chain, simulated)
**Figures:** `../07 Let's run and compare the processes/timer-bars.svg` (optional)

## On-slide content

**Eyebrow:** APPENDIX A4 · Q&A BACKUP

**Title:** The iteration simulations: anchors, ladders, and practical capacity

**1 · The method — three lines**

1. **One engine, three folders.** The Section-4 rework-study engine is copied unchanged into each iteration folder (`iteration1_sim.py` · `iteration2_sim.py` · `iteration3_sim.py`) — same lineage, no per-iteration rewriting.
2. **Check the rung below first.** Every run is sanity-checked against the previous rung before its own numbers are believed: the baseline reproduces 21.8 d / 600 min / 87%; Iteration 3 is checked against all three prior rungs.
3. **Loop probabilities are solved, never picked.** Two anchors per iteration — rework incidence + E[work] — solve for ps, with pf = 2·ps (the Section-4 relation).

*Label: calculated — simulation configuration*

**2 · Per-iteration anchors — what each solve consumes**

| | Incidence anchor | E[work] anchor | → ps | → pf (2·ps) | Loop-design change modeled |
|---|---:|---:|---:|---:|---|
| **Iter 1** | 55% | 435 min | 0.214 | 0.428 | structured change requests make loops *cheaper* — script 50→25 min, final 70→35 min; previews kill clarification entirely |
| **Iter 2** | 30% | 350 min | 0.108 | 0.216 | a script loop = regenerate one scene, 10 min |
| **Iter 3** | 10% | 60 min | 0.034 | 0.068 | objection window runs in parallel — no serial wait; an objection adds a scene re-render + re-QA (15 min) inside the window |

*Label: calculated — anchors follow the Section-4 study; loop designs are design targets*

**3 · The simulated ladder**

| KPI | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|
| Lead time | 21.8 d | 6.8 d | 4.0 d | **1.6 d** |
| Human work | 600 min | 438 min | 351 min | **62 min** |
| Rework | 87% | 59% | 34% | **11%** |
| *Engine check (closed form)* | *600 ✓* | *435 ✓* | *350 ✓* | *61 ✓* |

- Simulator vs algebra at every rung: 438/435 · 351/350 · 62/61 min ✓ — engine and closed form agree.
- Rework sim vs closed form: 59/55 · 34/30 · 11/10% — seed variation, both shown, neither hidden.

*Label: simulated designs — targets, not results*

**4 · Practical capacity — the criterion validates itself first**

- **Definition:** the highest demand whose **mean lead stays ≤ 28 d** — the top of today's reported band.
- **Self-validation:** at baseline the criterion yields **~20/mo** — reproducing the company-reported output of **15–20/mo [C]**. The criterion proves itself before any iteration answer is trusted.
- The cliff is sharp: at Iter 1, 32/mo already → 45 d.

| | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|
| **Practical capacity (lead ≤ 28 d)** | ~20/mo | ~30/mo | ~38/mo | **~230/mo** |
| Work-content ceiling (67% budget basis) | 23.6/mo | 32.5/mo | 40.4/mo | 230.3/mo |

- Iter 2 lands **inside the stated 35–40/mo ceiling [C] — reached without hiring**.
- Iter 3: lead flat 1.6–2.2 d from 15 to 200/mo — **the queue is dead**; the binding ceiling is now demand, not capacity.

*Label: simulated designs — targets, not results; validation anchor company-reported*

**5 · Sensitivities — every rung is gate-dominated**

| Iter | Lawyer behaviour / channel | Gate wait | Lead | P90 |
|---|---|---|---:|---:|
| 1 | Approves in ~1 d | U(0.25–1.0) wd | 5.1 d | 7.4 |
| 1 | Typical | U(0.5–1.5) wd | **6.8 d** | 9.9 |
| 1 | Always near the 48 h cap | U(1.0–1.6) wd | 8.2 d | 12.4 |
| 2 | In-app approval (~24 h avg) | U(0.25–1.0) wd | **4.0 d** | 5.1 |
| 2 | Email fallback (v1 gates) | U(0.5–1.5) wd | 5.3 d | 7.1 |
| 3 | SLA-shaped (~24 h) | U(0.25–1.0) wd | **1.6 d** | 2.1 |
| 3 | Rides the 48 h cap | U(0.5–1.5) wd | 2.1 d | 2.7 |

- Iteration 1's lead swings **5.1–8.2 d** on lawyer behaviour alone — more than any internal production change; even the breach case stays inside the 7–12 d target.
- Iteration 2: the Script Engine **removes writing, not waiting**.
- Iteration 3: lead ≈ **100% client approval time** — the constraint has left HiLegal's building.

*Optional figure:* `../07 Let's run and compare the processes/timer-bars.svg` — where the remaining wait actually sits. *Label: calculated scenario*

*Chip: simulated designs — targets, not results*

## Layout

- Background `#F3F4F6`; **five white cards** in a 2 + 1 + 2 grid, 1 px `#E5E7EB` borders, generous padding — same skeleton as A1 so the appendix reads as one system. Q&A density is acceptable; hierarchy must survive it.
- Row 1: card 1 (the method, ~40%) + card 2 (anchor table, ~60% — the ps/pf columns land here).
- Row 2: card 3 **full width** — the simulated ladder, the slide's spine; its three KPI rows must be readable from the back of the room.
- Row 3: card 4 (practical capacity) + card 5 (sensitivities table, with the optional timer-bars strip).
- Card headings: Inter semibold 26 px `#262626`, numbered ("1 · The method — three lines") so the answer pattern is scannable. Thin **gold `#C9A86A` rules** under the derived rows: the ps/pf pairs in card 2, the Iter-3 finals in card 3 (**1.6 d · 62 min**), and **~230/mo** in card 4.
- Method card: three numbered lines, Inter 24 px body `#4A5565`, verbs bold in `#262626` (*copied · sanity-checked · solved, never picked*).
- Tables: numerals right-aligned, tabular figures, Inter 24 px; gate-wait distributions `U(0.25–1.0) wd` set in muted `#6A7282`. All text ≥ 24 px.
- **Accent red `#D92605` only in card 5**, on the three stress leads — **8.2 d · 5.3 d · 2.1 d** — the "what if the gate slips" answers. Everything else stays black/ink; ladder and capacity finals are bold black `#0A0A0A` with the gold underline (no green in the system).
- Design-system labels under each card: *calculated — simulation configuration* (1) · *calculated — anchors follow the Section-4 study* (2) · *simulated designs — targets, not results* (3) · *simulated designs; validation anchor company-reported* (4) · *calculated scenario* (5). Cards 3 and 4 also carry the chip "simulated designs — targets, not results".
- Optional figure: `timer-bars.svg` as a slim strip at the bottom of card 5, captioned "where the remaining wait actually sits"; omit entirely if the card runs dense.
- Title in Momo Trust Display, `#0A0A0A`, one line, short-statement grammar; eyebrow "APPENDIX A4 · Q&A BACKUP" in muted `#6A7282`, Inter 24 px, letterspaced caps. No icons, no decoration beyond the rules, labels and one chip.

## Speaker notes

**MAIN MESSAGE:** This slide answers *"why should we believe the simulation?"* with one repeated pattern: **name the two anchors → show the solve → point at the check.** Prepared answers:

1. *"Where do ps and pf come from?"* → Solved, not assumed: incidence + E[work] give ps, and pf = 2·ps. Walk card 2: 55% + 435 min → 0.214/0.428; 30% + 350 min → 0.108/0.216; 10% + 60 min → 0.034/0.068. No hand-tuning anywhere in the chain.
2. *"Is this the same model as Section 4?"* → Same engine, copied per folder — and each rung must reproduce the previous rung's published numbers before its own are read. The baseline run reproduces 21.8 d / 600 min / 87% before Iteration 1 gets quoted.
3. *"Why does the simulator disagree slightly with the closed form?"* → 438 vs 435, 351 vs 350, 62 vs 61 min; rework 59/34/11 vs 55/30/10%. Seed variation — both numbers are shown on card 3, neither is hidden.
4. *"What does practical capacity actually mean?"* → The highest demand whose mean lead stays ≤ 28 d — the top of today's reported band. And it validates itself first: at baseline it returns ~20/mo against the company-reported 15–20 [C]. Only then do we quote ~20 → ~30 → ~38 → ~230/mo.
5. *"Isn't 230/mo absurd?"* → It is the 28 d criterion dissolving, not heroics: lead stays flat at 1.6–2.2 d from 15 to 200/mo because the queue is dead. The binding ceiling is now demand — and at 40/mo the two producers spend ~4 h/month on video.
6. *"What breaks these numbers?"* → The gate, every time: Iter 1 swings 5.1–8.2 d on lawyer behaviour alone; Iter 2's email fallback costs 5.3 d; Iter 3's slow lawyer costs 2.1 d. All gate-dominated — that is the finding, not a weakness: after Iteration 3, improvement means managing the client, not the process.
7. Never call these results. Every rung is a **simulated design with a target**; the pilot gates (10 vs 10 cohorts) are where they become evidence.

**DATA STATUS:** **[C] company-reported:** 15–20 videos/month output (the self-validation anchor); the 35–40/mo stated capacity ceiling. **Section-4 study (company-anchored):** baseline 21.8 d / 600 min / 87% rework and the incidence anchors 55/30/10% — the 30% and 10% double as the Iter-2/Iter-3 rework targets [T]. **Calculated:** ps/pf (two-anchor solve, pf = 2·ps), E[work] closed forms (435/350/61 min), the 67%-basis work-content ceilings 23.6/32.5/40.4/230.3 per month (kpi files quote a 60% basis — difference documented in kpi-data §4). **Simulated designs — targets, not results:** the rung values 6.8/4.0/1.6 d lead, 438/351/62 min work, 59/34/11% rework, ~30/~38/~230/mo practical capacity, and the P90/sensitivity rows (gate-wait distributions U(0.25–1.0) / U(0.5–1.5) / U(1.0–1.6) wd are scenario assumptions). The 28 d criterion is a stated definition; its baseline output (~20/mo) is validated against [C] before use. `timer-bars.svg` is Section-7 output, labeled *calculated scenario*. Sources: Iteration 1–3 SUMMARY.md (§ KPI effect — targets vs simulation, § sensitivities), Section-4 study for the engine lineage and baseline anchors.
