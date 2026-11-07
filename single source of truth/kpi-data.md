# KPI Master Data — single source of truth

Team: Augustin · Dedi · Joel · Saeed — HiLegal project, October 2026
Legend: **[C]** company-reported (confirmed with HiLegal, Sept 2026) · **[E]** estimate/assumption (ours) · **[T]** target
Key assumptions: **fully-loaded producer rate ¥85/h [E] (build-up in §3) · utilization 60% [E] · FX USD/CNY 7.2 [E] · subscription: most popular tier $100/month ≈ ¥720, promising 10 videos/month [C] · revenue attribution = model costs ¥90 + 30% overhead ≈ ¥117/video (HiLegal's own first assumption [C])**.

---

## 1. Labour waterfall — minutes of producer time per delivered video (monthly average, incl. rework rounds)

| Activity | Baseline | Iter 1 | Iter 2 | Iter 3 | Mechanism of change |
|---|---:|---:|---:|---:|---|
| Intake & clarification handling | 60 [E] | 15 | 15 | 10 | Iter 1: structured self-serve brief + auto completeness check replaces email ping-pong |
| Content brief creation / review | 50 [E] | 10 | 10 | 5 | Iter 1: brief auto-generated from form + lawyer profile; producer only reviews |
| Script drafting (human) | 80 [E] | 55 | 0 | 0 | Iter 1: correct brief → fewer redo rounds; Iter 2: LLM drafts, human stops writing |
| AI generation parameter check | — | — | 5 | 5 | Iter 2: select template/params, trigger generation |
| Script editing & QC (human) | 40 [E] | 25 | 30 | 15 | Iter 1: fewer loops; Iter 2: edit-not-write (slightly up per pass, loops fewer); Iter 3: mature templates + model feedback from accepted edits |
| Video generation ops | 60 [E] | 60 | 45 | 0 | Iter 2: scene-level prompt hints generated with script; Iter 3: fused into single render |
| Audio generation ops | 35 [E] | 35 | 25 | 0 | Iter 3: voice generated inside the single render |
| Audio-visual synchronization | **150 [C 2–3 h]** | 135 | 135 | 0 | Iter 1–2: only rework-reduction effect; **Iter 3: deleted by single-render avatar pipeline** |
| Render batch setup & QA | — | — | — | 20 | Iter 3: human watches output, checks likeness/names/captions (retries add ~5 min avg) |
| Platform adaptation | **100 [C ~2 h]** | 90 | 75 | 0 | Iter 3: auto variants 16:9 / 9:16 / 1:1 from same render |
| Delivery & publishing | 25 [E] | 10 | 10 | 5 | Iter 1: auto-notify + structured delivery; Iter 3: auto-publish + objection window |
| **TOTAL** | **600 min = 10 h 00 [C]** | **435 = 7 h 15** | **350 = 5 h 50** | **60 = 1 h 00** | |
| Δ vs previous | — | −28% | −20% | −83% | |
| Δ vs baseline | — | −28% | −42% | −90% | |

*Sums check: 600 = 60+50+80+40+60+35+150+100+25 · 435 = 15+10+55+25+60+35+135+90+10 · 350 = 15+10+5+30+45+25+135+75+10 · 60 = 10+5+5+15+20+5.*

*Iteration 3 note: 60 min is the steady-state target after ~50 videos of template/model maturation; expect 75–90 min during pilot phase [E]. The proposal's "under one hour" is met at steady state.*

## 2. Lead time build-up — calendar days, midpoint (range)

| Component | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| Intake queue | 3–7 d [C] | 0 (auto-route) | 0 | 0 |
| Clarification loop | 2–4 d [E] | 0 (format previews at intake) | 0 | 0 |
| Script production (draft+refine / AI+edit) | 2–3 d [E] | 1–2 d | same day | same day |
| Script approval wait | 1–3 d [E] | ≤2 d (48 h SLA, reminders) | ~1 d (in-app mobile) | ~1 d (24–48 h) |
| Video+audio production | 2–3 d [E] | 2 d | 1–2 d | 0.5 d (batch render ~30 min + queue) |
| Final approval wait | 1–3 d [E] | ≤2 d (SLA) | ~1 d | 0 d (objection window runs parallel — no serial wait) |
| Delivery/publishing | 1 d [E] | same day | same day | automatic |
| **LEAD TIME (midpoint, range)** | **~21 d (14–28) [C]** | **~9 d (7–12) [T]** | **~4 d (3–5) [T]** | **~1.5 d (1–2) [T]** |

Little's Law framing: baseline WIP sits in untracked queues (inboxes); from Iteration 1 every queue is visible and SLA-capped. **After Iteration 3 the residual lead time is ~100% lawyer approval time — the constraint leaves HiLegal's building.** That sentence is the Section 6→8 pivot.

## 3. Cost per video build-up

**Human-factor pricing (Shenzhen, per producer):** gross salary ¥10,000 [E] + employer social insurance & housing fund (五险一金, ~35%) ¥3,500 [E] + equipment/software/office share ¥1,500 [E] → **¥15,000/month fully loaded ÷ 176 productive hours = ≈ ¥85/h**.

| Component | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|
| Labour (h × ¥85/h) | ¥850 (10 h [C]) | ¥615 (7¼ h) | ¥495 (5 h 50) | ¥85 (1 h) |
| Manual tool credits (ChatGPT/Seedance/TTS/stock) | ¥90 [E] | ¥90 | ¥65 (ChatGPT credits replaced by self-hosted LLM) | — |
| LLM inference (self-hosted legal LLM, marginal) | — | — | ¥20 [E] | ¥20 |
| Template/pipeline dev amortized (~500 videos) | — | — | ¥15 [E] | ¥30 |
| Single-render avatar API (voice + lip-sync + video) | — | — | — | ¥45 [E] |
| **COST PER VIDEO** | **¥940 [E]** | **¥705 [T]** | **¥595 [T]** | **¥180 [T]** |
| Δ vs previous | — | −25% | −16% | −70% |
| Δ vs baseline | — | −25% | −37% | **−81%** |

Labour is **90.6% of the baseline cost of an "AI video service"** — the frame for Section 2's money story.

## 4. Throughput & capacity (same two producers, constant team)

Assumptions [E]: 2 producers × 160 h/month × 60% effective utilization on this service ≈ **11,500 productive minutes/month**.

| | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---:|---:|---:|---:|
| Capacity = 11,500 ÷ min/video | ~19/mo | ~26/mo | ~33/mo | ~190/mo |
| Company-reported actual output | 15–20/mo [C] | — | — | — |
| Company-stated ceiling | 35–40/mo [C] | — | — | — |
| Consistency check | 19 ≈ reported 15–20 ✓ | — | 33 ≈ stated ceiling 35–40 ✓ | ~10× baseline ✓ (matches proposal's "tenfold" claim) |
| Team time spent if demand = 40/mo | n/a (can't serve) | ~29 h/mo | ~23 h/mo | ~4 h/mo |
| Production FTE no longer required (at 20/mo demand) | 0 | ~0.2 FTE | ~0.4 FTE | **~1.5 FTE** |

**Read on the ceiling:** Iteration 2 alone roughly *reaches* the ceiling HiLegal stated (33 vs 35–40 [C]) — without new hires. Iteration 3 *breaks* it by ~5×, and at realistic demand the team's remaining effort is hours per week, not headcount. This is the quantitative bridge to Section 8's "release staff capacity to the LLM."

## 5. Rework rate & Quality Acceptance Rate

Definitions: **Rework rate** = % of delivered videos with ≥1 rework loop at any client gate. **QAR** = % accepted first-pass at *every* gate (zero loops). QAR ≈ 1 − rework rate under these definitions.

| | Baseline | Iter 1 | Iter 2 | Iter 3 | Loop family killed |
|---|---:|---:|---:|---:|---|
| Rework rate | ~90% [E] | ~55% [T] | ~30% [T] | ~10% [T] | |
| QAR | ~10% [E] | ~45% [T] | ~70% [T] | ~90% [T] | |

- Baseline anchor: brief approval loop alone runs **≥4 iterations [C]** → first-pass acceptance is near-zero; 90% rework [E] is conservative.
- Iter 1 kills **clarification/brief loops** (structured brief + previews; lawyer sees the format before anything is produced).
- Iter 2 kills **script-surprise loops** (template structure + lawyer profile; lawyer approves a structure they already chose).
- Iter 3 kills **production-defect loops** (single render from the approved script — no transcription/sync errors, auto-consistent variants; residual = avatar glitches, name mispronunciation).
- Worst case per proposal (all gates × 4 iterations [C]): Iteration 1's structured change requests + reason codes keep even this scenario inside the SLA'd windows; simulate in `07`.

## 6. Unit economics of the service (the Section 2/8 money story)

**Revenue side [C]:** most popular tier **$100/month ≈ ¥720 (FX 7.2 [E])**, promising **10 videos/month**. HiLegal's internal revenue attribution — their first costing assumption: **model costs ¥90 + 30% overhead ≈ ¥117/video [C]**, where the 30% (¥27) was meant to cover the human factor (actual human factor: ¥850 — the buffer covers 3% of it).

**Per video (vs. their ¥117 attribution):** margin = 117 − cost → **−¥823 / −¥588 / −¥478 / −¥63** (baseline → Iter 3). Even fully automated, one video slightly exceeds the attribution — the attribution itself was built on the wrong assumption and needs re-basing.

**Per customer per month (the tier reality):**

| Usage of the 10-video promise | Baseline cost | Iter 3 cost | Revenue | Bleed, baseline | Bleed, Iter 3 |
|---|---:|---:|---:|---:|---:|
| 1 video | ¥940 | ¥180 | ¥720 | −¥220 | +¥540 |
| 2 videos (typical [E]) | ¥1,880 | ¥360 | ¥720 | −¥1,160 | **+¥360** |
| 5 videos | ¥4,700 | ¥900 | ¥720 | −¥3,980 | −¥180 |
| 10 (full entitlement) | ¥9,400 | ¥1,800 | ¥720 | **−¥8,680 (−$1,206)** | −¥1,080 |

→ Baseline break-even at **0.77 videos** — the tier loses money on the first video. **Iteration 3: the typical customer flips positive (+¥360/month) and the full-entitlement loss shrinks 88%** (−¥8.7k → −¥1.1k, closable by tier design and volume render pricing). This is the "stop the bleed, make a little money, point it at the core" thesis.

**Aggregate (delivered volume 15–20/mo):** baseline burn vs attribution ≈ **−¥12–16k/month ≈ −¥150–195k/year [E]**; at Iter 3 ≈ −¥1.0–1.3k/month (≈ break-even) before the customer-mix upside.

**People:** two producers ≈ **¥360k/year** fully loaded [E]; after Iter 3 ~1.5 FTE of production payroll (≈ **¥270k/year**) is released for reallocation to the core — LLM fine-tuning budget and ML hires [E]. (The producers are video makers; the released resource is money, not ML capacity.)

## 7. Sanity checks (do these live if challenged)

1. **Capacity:** 11,500 min ÷ 600 min = 19.2 ≈ company-reported 15–20 [C] ✓ — the utilization assumption is back-solved from their own output, not invented.
2. **Labour waterfall sums** to the company-reported ~10 h [C] ✓ (see row sums under table 1).
3. **Little's Law spot check:** 21 d lead × (19 videos/month ÷ 21.7 working days) ≈ 18–19 videos in system ≈ plausible WIP sitting in intake + gates + producer queues ✓ direction & magnitude.
4. **Sync + adaptation** (250 min) = 42% of baseline labour — consistent with the proposal naming them the largest blocks [C] ✓.
5. **Cost curve shape:** −25% → −37% → −81%. Iteration 2's step looks small *by design* — it fixes the middle so Iteration 3 can delete the bottom. Say this before someone else does.

## 8. Change log

- 2026-10-29 initial dataset created from proposal Table 1 [C] + derived [E] estimates; targets [T] set per iteration. Update this log whenever a baseline number is replaced by observed pilot data.
- 2026-10-29 currency switched to RMB: fully-loaded rate ¥85/h (Shenzhen build-up in §3), FX 7.2. Revenue side rebuilt on company facts: $100/month tier promising 10 videos/month, attribution = model costs + 30% overhead ≈ ¥117/video [C]. Cost curve recomputed: ¥940 → ¥705 → ¥595 → ¥180 (tool lines now persist correctly through Iter 2: Seedance/TTS credits remain until the single render replaces them in Iter 3).
