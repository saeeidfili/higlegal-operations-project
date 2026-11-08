# Slide 16 — Implementation: standardize first, automate second — self-sufficient in 15 weeks

**Speaker:** Joel Wirth
**Time:** 1:00
**Figures:** none (timeline built from layout tokens — no SVG from the manifest)
**Related appendix:** `A6-assumptions-and-model-cards.md` ([C]/[E] discipline, assumption ladder, falsifiable predictions)

## On-slide content

**Title:** Implementation: standardize first, automate second — self-sufficient in 15 weeks

**Order-rule strip (one line under the title):**

> **Standardize first** (no new AI) → **automate second** — cheapest risk reduction before the most expensive capability · separate go/no-go at every gate.

**Phased rollout timeline (five segments on one horizontal spine, week-scaled):**

| Seg | Weeks | Phase | Exit gate (few words) |
|---|---|---|---|
| **P0** | 1–2 | Baseline instrumentation | baselines published · targets re-confirmed |
| **P1** | 3–6 | Standardize front end *(Iter 1)* | lead ≤ 12 d · rework ≤ 60% · QAR ≥ 35% |
| **P2a** | 7–10 | Script Engine *(Iter 2)* | lead ≤ 5 d · edit depth ≤ 20% · **0 compliance incidents** |
| **P2b** | 11–14 | Render pipeline *(Iter 3)* | lead ≤ 2 d · render ≥ 90% · consent 100% |
| **P3** | 15+ | Sustain & improve | 4 wks at target → steady state |

**Timeline caption (one line, muted):** every phase ships to 10 pilot videos vs a concurrent legacy cohort — legacy stays fallback until the gate passes.

**Cost & payback strip (full width, under the timeline):**

> **One-time ≈ ¥105–180k [E]** · payback **≈ 5–8 months** at 20–35 videos/mo

**Exit-condition band (wait-fill band, above the alerts line):**

> **EXIT CONDITION:** HiLegal runs the weekly PDCA review **without us for 3 consecutive weeks** with all gate metrics holding.

**Alerts line (bottom strip, one line):**

> `Alerts: P90 > 5 d · SLA < 85% · consent < 100% → stop-the-line`

**Legend footnote:** `[E] estimate`

## Layout

- **Background:** solid `#F3F4F6`, full bleed; no figure — the timeline is the visual.
- **Title:** Momo Trust Display, ink `#101010`, ~40 px, top-left, max two lines (break after "second —" so "self-sufficient in 15 weeks" sits on line 2); no red in the title.
- **Order-rule strip:** no card — one full-width line directly under the title. "Standardize first" and "automate second" in Inter semibold 26–28 px `#0A0A0A`; "(no new AI)" muted `#6A7282`; the arrow → and "·" separators in grey-400 `#99A1AF`; the gloss ("cheapest risk reduction before the most expensive capability · separate go/no-go at every gate") Inter 24–26 px body `#4A5565`.
- **Timeline band (the core visual, ~40 % of slide height, mid-slide):** a 2 px grey-200 `#E5E7EB` horizontal spine across the full content width; five segment cards sitting on it, widths proportional to duration (2 : 4 : 4 : 4 weeks; P3 open-ended). P3's right edge dashed grey-200 with a grey-400 `#99A1AF` arrowhead running past it — "15+" reads as open-ended. 8–12 px gaps between cards, small grey-400 chevrons in the gaps.
- **Segment card:** white fill, 1 px grey-200 `#E5E7EB` border, 12–16 px padding. Text stack top-to-bottom: header `P0 · WK 1–2` in Inter 24 px caps, letter-spacing 0.1 em, muted `#6A7282` (iteration tags `ITER 1/2/3` in gold `#C9A86A` caps 24 px, inline after the header on P1/P2a/P2b); phase name Inter semibold 26–28 px `#0A0A0A`, two lines allowed; gate line prefixed with a `GATE` tag in gold `#C9A86A` caps 24 px, gate text Inter 24 px body `#4A5565` with every metric value (≤ 12 d · ≤ 60% · ≥ 35% · ≤ 5 d · ≤ 20% · 0 incidents · ≤ 2 d · ≥ 90% · 100% · 4 wks) in Inter semibold ink `#101010` — so the lead staircase **12 → 5 → 2 d** reads left-to-right across the band. "0 compliance incidents" semibold on P2a as its hard stop.
- **Timeline caption:** under the spine, Inter 24 px, muted `#6A7282`, one line, left-aligned.
- **Cost & payback strip:** full-width white band, 1 px grey-200 `#E5E7EB` border, one centered line: label "One-time" Inter 26 px body `#4A5565`, then `≈ ¥105–180k` Inter semibold ~32 px ink `#0A0A0A` with `[E]` tag 24 px muted `#6A7282`; "payback" body; `≈ 5–8 months` Inter semibold ~32 px ink; "at 20–35 videos/mo" Inter 24–26 px body.
- **Exit-condition band:** full-width strip, fill wait-fill `#F6EEDF`, 2 px wait-line `#A8823F` left border. `EXIT CONDITION` in Inter 24 px caps muted `#6A7282`; the sentence in Inter semibold 26 px `#262626`, with "without us for 3 consecutive weeks" in semibold ink `#0A0A0A` and "with all gate metrics holding" dropping to regular body weight.
- **Alerts line:** bottom strip, one line: "Alerts:" Inter 24 px caps muted `#6A7282`; the three thresholds Inter 24–26 px `#262626` with values (5 d · 85% · 100%) semibold ink `#101010`; "→" grey-400; **"stop-the-line" in accent red `#D92605` semibold — the only red on the slide**.
- **Legend footnote:** Inter 24 px, muted `#6A7282`, bottom-left, one line: `[E] estimate`.
- **Density check:** title + order strip + 5-card timeline + caption + cost strip + exit band + alerts line + legend. All text ≥ 24 px; no other decoration.

## Speaker notes

**TIME:** 1:00 — bridge ~5 s · order rule ~5 s · timeline walk ~30 s (≈ 6 s per phase) · cost & payback ~10 s · exit condition + alerts ~10 s.

**MAIN MESSAGE:** The rollout is ordered cheapest-risk-first — standardize before automating — five phases over 15 weeks, each closed by a pre-registered quantitative gate; one-time cost ≈ ¥105–180k [E] pays back in ≈ 5–8 months at 20–35 videos/mo; and self-sufficiency is a test, not a hope: HiLegal runs the weekly PDCA review without us for 3 consecutive weeks with all gate metrics holding.

**SPEAKING POINTS:**

- Bridge from slide 15: the plan fits the org we just showed — hats, not departments (one engineer at ~30 % capacity, weeks 7–14 only). Here is the same plan on a calendar.
- The order rule: **standardize first, automate second** — take the cheapest risk reduction before buying the most expensive capability. Phase 1 ships with no new AI at all, and every phase is a separate go/no-go.
- Walk the spine, left to right — the lead-time gate stairs down 12 → 5 → 2 d:
  - **P0, weeks 1–2:** time-log 10 legacy videos, replace the [E] baselines with observed ones, freeze the dashboard spec. Gate: baselines published, targets re-confirmed.
  - **P1, weeks 3–6** (= Iteration 1): forms, previews, SLA approvals, the order state machine. Full gate: lead ≤ 12 d · 0 clarification loops ≥ 8/10 · rework ≤ 60% · QAR ≥ 35% · no quality drop.
  - **P2a, weeks 7–10** (= Iteration 2): the Script Engine — fine-tuned LLM + templates, edit-QC. Gate: lead ≤ 5 d · edit depth ≤ 20% · rework ≤ 35% · **0 compliance incidents**.
  - **P2b, weeks 11–14** (= Iteration 3): single render, variants, consent registry, delivery + objection window. Gate: lead ≤ 2 d · render success ≥ 90% · consent 100% · QAR ≥ 85%.
  - **P3, weeks 15+:** PDCA at run-rate — 4 consecutive weeks at target → steady state.
- Why 2a/2b and not one Phase 2: scripting and render automation fail differently — separate go/no-go decisions. You can stop after 2a and still keep the gains.
- Reversibility is adoption insurance: every phase ships to 10 pilot videos against a concurrent legacy cohort, and the legacy path stays as fallback until the gate passes. A gate pass is a decision, not a celebration; a failure means diagnose, fix, re-run.
- Costs [E]: forms/approvals build ¥35–65k, template library + prompts ¥25–40k, render/LLM integration ¥45–75k, training 2 × ½ day per phase — **≈ ¥105–180k one-time**. At ¥760/video saving that is ≈ 140–240 videos, i.e. **≈ 5–8 months** at 20–35 videos/mo.
- The exit condition, said as a test: HiLegal runs the weekly PDCA review **without us for 3 consecutive weeks**, all gate metrics holding. Weeks 15+ carry no external dependency — self-sufficiency is scheduled, not wished for.
- Alerts that stop the line: P90 > 5 d · SLA < 85% · consent < 100%. The weekly 30-min review (lead median + P90, SLA, rework by reason code, render success, edit depth) feeds a reason-code Pareto that sets next week's fix.
- Handoff to slide 17 (closing): "You don't need a bigger video team. You need your video team back."

**DATA STATUS:** All numbers from the Section 9 summary (phased rollout, gates, costs, exit condition, alerts). Costs are [E] estimates — build-up ¥35–65k + ¥25–40k + ¥45–75k → ≈ ¥105–180k one-time; payback derived at ¥760/video saving ≈ 140–240 videos ≈ 5–8 months at 20–35 videos/mo — a calculated scenario on simulated savings, never presented as observed results. Gates are pre-registered thresholds from the Section 6 / iteration designs; on-slide gates are quoted in few words, full gates in these notes. The iterations themselves remain **simulated designs, not results** (design-system rule) — the 10-video pilot per phase is the evidence engine. Self-sufficiency within months is HiLegal's stated requirement [C]. Full alert set (adds render < 90%, QAR < 80%) and monitoring cadence per Section 9; tag discipline, assumption ladder, and model cards in appendix A6.
