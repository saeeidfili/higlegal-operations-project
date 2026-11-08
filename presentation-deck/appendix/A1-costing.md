# Appendix A1 — Costing and unit economics: every number derived

**Appendix A1 · Q&A** — untimed backup, no speaker, no clock
**Drops on:** any costing or unit-economics challenge (default backup for slides 2, 3, 14)
**Feeds slides:** 2 (¥940 vs ¥117) · 3 (per-customer bleed, break-even, drain) · 14 (payroll released)
**Figures:** none — tables only

## On-slide content

**Eyebrow:** APPENDIX A1 · Q&A BACKUP

**Title:** Costing and unit economics: every number derived

**1 · Fully-loaded producer rate — the ¥85/h anchor**

| Component (per producer, monthly) | Formula | Value |
|---|---|---:|
| Gross salary — bilingual video producer, Shenzhen | market rate | ¥10,000 [E] |
| Employer social insurance + housing fund (五险一金) | ¥10,000 × 35% | ¥3,500 [E] |
| Equipment, software, office & overhead | — | ¥1,500 [E] |
| **Fully-loaded cost** | ¥10,000 + ¥3,500 + ¥1,500 | **¥15,000/month [E]** |
| Productive hours | — | 176 h [E] |
| **Fully-loaded rate** | ¥15,000 ÷ 176 h = ¥85.2 | **≈ ¥85/h [E]** |

*Label: estimate*

**2 · Cost per video vs HiLegal's ¥117 attribution**

| Line | Formula | Value |
|---|---|---:|
| Human labour | 10 h [C] × ¥85/h [E] | ¥850 · 90.6% |
| Model/tool credits (ChatGPT · Seedance · TTS · stock) | — | ¥90 [E] |
| **Actual cost per video** | ¥850 + ¥90 | **≈ ¥940 [E]** |
| HiLegal's attribution | ¥90 × 1.30 (credits + 30% overhead) | **¥117 [C]** |
| **The gap** | ¥940 ÷ ¥117 | **off 8×** |
| What the buffer really covers | ¥27 overhead ÷ ¥850 human factor | **≈ 3%** |

*Label: estimate + company-reported (attribution)*
*Every video vs attribution: ¥117 − ¥940 = **−¥823***

**3 · The cost ladder — mechanism per step**

| Component | Baseline | Iter 1 [T] | Iter 2 [T] | Iter 3 [T] |
|---|---:|---:|---:|---:|
| Labour (min of work × ¥85/h) | ¥850 (600 min [C]) | ≈ ¥615 (435) | ≈ ¥495 (350) | ¥85 (60) |
| Manual tool credits | ¥90 [E] | ¥90 | ¥65 | — |
| LLM inference (self-hosted, marginal) | — | — | ¥20 | ¥20 |
| Template/pipeline dev, amortized (~500 videos) | — | — | ¥15 | ¥30 |
| Single-render avatar API (voice + lip-sync + video) | — | — | — | ¥45 |
| **COST PER VIDEO** | **¥940 [E]** | **¥705 [T]** | **¥595 [T]** | **¥180 [T]** |
| Step Δ | — | −25% | −16% | −70% |
| Cumulative Δ | — | −25% | −37% | **−81%** |
| Margin vs ¥117 attribution | −¥823 | −¥588 | −¥478 | −¥63 |

- **→ ¥705 · Iter 1 standardizes intake** — structured self-serve brief, auto-generated from form + lawyer profile; kills clarification/brief redo loops (600 → 435 min).
- **→ ¥595 · Iter 2 stops the writing** — LLM drafts from template + profile, human edits; self-hosted LLM replaces ChatGPT credits (¥90 → ¥65), adds ¥20 inference + ¥15 amortized dev (435 → 350 min).
- **→ ¥180 · Iter 3 deletes the bottom** — single render fuses voice, lip-sync, video and auto-variants, erasing A/V sync, adaptation and generation ops (350 → 60 min); adds ¥45 render API, amortization rises to ¥30.

*Chip: simulated designs — targets, not results*

**4 · Per-customer bleed (baseline) — break-even 0.77**

Tier revenue: $100/month × FX 7.2 [E] = **¥720 [C]**, promising 10 videos [C].

| Usage of the 10-video promise | Cost | Revenue | Bleed/month |
|---|---:|---:|---:|
| 1 video | 1 × ¥940 = ¥940 | ¥720 | −¥220 |
| 2 videos (typical [E]) | 2 × ¥940 = ¥1,880 | ¥720 | −¥1,160 |
| 5 videos | 5 × ¥940 = ¥4,700 | ¥720 | −¥3,980 |
| 10 videos (full entitlement) | 10 × ¥940 = ¥9,400 | ¥720 | **−¥8,680 (−$1,206)** |

- **Break-even:** ¥720 ÷ ¥940 = **0.77 videos/month** — the tier loses money on video #1
- **Aggregate:** (¥940 − ¥117) × 15–20 delivered/month [C] = −¥12–16k/month → **−¥150–195k/year [E]**

*Label: calculated — company-reported revenue × estimated cost*

**5 · The Iteration-3 flip [T]**

| Usage | Baseline bleed | Iter-3 cost | Iter-3 bleed |
|---|---:|---:|---:|
| 2 videos (typical) | −¥1,160 | 2 × ¥180 = ¥360 | **+¥360** |
| 10 videos (full entitlement) | −¥8,680 | 10 × ¥180 = ¥1,800 | −¥1,080 |

- Typical customer flips positive: ¥720 − ¥360 = **+¥360/customer-month**
- Full-entitlement loss: −¥8,680 → −¥1,080 = **−88%** — closable by tier design and volume render pricing
- Even fully automated, ¥117 − ¥180 = **−¥63/video** → the attribution itself was built wrong and needs re-basing
- Aggregate at Iter 3: (¥180 − ¥117) × 15–20/month ≈ **−¥1.0–1.3k/month** ≈ break-even, before customer-mix upside
- People: 2 producers × ¥15,000 × 12 = **¥360k/year** fully loaded [E]; Iter 3 releases ~1.5 FTE ≈ **¥270k/year** for the legal-LLM core

*Label: targets, not results*

## Layout

- Background `#F3F4F6`; **five white cards** in a 2 + 1 + 2 grid, 1 px `#E5E7EB` borders, generous padding. Q&A density is acceptable; hierarchy must survive it.
- Row 1: card 1 (¥85/h build-up, ~46% width) + card 2 (¥940 vs ¥117, ~54% — the 8× line lands here).
- Row 2: card 3 **full width** — the ladder table with the three mechanism lines beneath. This is the slide's spine; give it the most height.
- Row 3: card 4 (per-customer bleed) + card 5 (Iter-3 flip).
- Card headings: Inter semibold 26 px `#262626`, numbered ("1 · Fully-loaded producer rate…") so the answer pattern is scannable. Thin **gold `#C9A86A` rules** under every derived row: ¥15,000, ≈ ¥85/h, ≈ ¥940, the ladder total row, break-even, +¥360.
- **Formula column** set in Inter 24 px muted `#6A7282`; results in `#262626` semibold; numerals right-aligned, tabular figures. All text ≥ 24 px.
- **Accent red `#D92605` reserved for negative money and the 8×**: −¥823, the bleed column, −¥150–195k, and "off 8×". The **+¥360** is the one highlighted positive: bold black `#0A0A0A` with a gold `#C9A86A` underline (no green in the system).
- Design-system labels under each card: *estimate* (1) · *estimate + company-reported* (2) · *estimate (baseline) + targets, not results* (3) · *calculated from company-reported revenue × estimated cost* (4) · *targets, not results* (5). Card 3 also carries the chip "simulated designs — targets, not results".
- Title in Momo Trust Display, `#0A0A0A`, one line, short-statement grammar; eyebrow "APPENDIX A1 · Q&A BACKUP" in muted `#6A7282`, Inter 24 px, letterspaced caps.
- Mechanism lines: Inter 24 px body `#4A5565`, mechanism verb bold in `#262626` (*standardizes · stops the writing · deletes the bottom*).
- No figure on this slide; the tables carry it. No icons, no decoration beyond the rules and labels.

## Speaker notes

**MAIN MESSAGE:** This slide exists to end costing debates in one move. Every number on slides 2, 3 and 14 divides down to two anchors — the **¥85/h fully-loaded rate [E]** and the **¥720/month tier revenue [C]**. Use the same answer pattern every time: **name the anchor → show the division → tag the provenance.** Prepared answers:

1. *"Is ¥85/h a real number?"* → Walk card 1: ¥10,000 + 35% 五险一金 + ¥1,500 = ¥15,000 ÷ 176 h ≈ ¥85. Conservative Shenzhen mid-market figure — and it back-solves: 2 producers × 160 h × 60% utilization ≈ 11,500 min ÷ 600 min/video = 19/month ≈ the company-reported 15–20 [C]. The utilization is derived from their own output, not invented.
2. *"8× sounds like hyperbole"* → ¥940 ÷ ¥117 = 8.0. And the sting is structural: the ¥27 overhead buffer was meant to cover the human factor — it covers 3% of the actual ¥850.
3. *"Where does 0.77 come from?"* → ¥720 ÷ ¥940. There is no usage level at which the tier profits — the incentive is inverted.
4. *"Does Iteration 3 fix the business?"* → The typical customer flips to +¥360/month; full entitlement still −¥1,080, an 88% smaller loss, closable by tier design and volume render pricing. And note −¥63/video vs the attribution: even a fully automated video exceeds ¥117 — the attribution needs re-basing, not just the cost.
5. *"Why is Iteration 2's step so small (−16%)?"* → By design: it fixes the middle (script quality, data structure) so Iteration 3 can delete the bottom (sync, adaptation, generation ops). Say it before someone else does.
6. Never defend a number without naming its tag. Baseline figures are [C] or [E]; every iteration rung is a [T] target — simulated designs, never presented as results.

**DATA STATUS:** **[C] company-reported:** ~10 h labour/video; $100/month ≈ ¥720 tier promising 10 videos; ¥117 attribution (¥90 credits + 30% overhead); 15–20 videos/month output. **[E] estimates:** salary ¥10,000; 35% 五险一金 = ¥3,500; ¥1,500 equipment/overhead; 176 productive hours → ¥85/h; ¥90 tool credits; FX 7.2; typical usage 2 videos/customer-month; −¥150–195k/year drain; ¥360k → ¥270k payroll figures. **[T] targets:** the ¥705/¥595/¥180 ladder and everything derived from it (+¥360, −¥1,080, −88%, −¥1.0–1.3k/month) — the Section-7 simulation reproduces the ladder (¥709/¥595/¥182, quoted on slide 12). Baseline ¥940 is calculated: [C] hours × [E] rate. Arithmetic on-slide is exact except the two ≈ labour rows (435 min → ¥615, 350 min → ¥495, kept at the source figures). Sources: kpi-data §3 (rate + cost build-up), §6 (unit economics), §7 (live sanity checks); Section-2 summary for the slide-2/3 wording this appendix backs up.
