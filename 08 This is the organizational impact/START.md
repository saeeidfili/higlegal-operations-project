# Section 8 — This is the organizational impact

**Guiding question:** What do the production improvements enable for HiLegal as a whole?

**What this section must accomplish:** translate operational gains into business outcomes — scale the paid service, improve customer experience, strengthen profitability, release staff capacity for other priorities — **with the assumptions connecting each operational gain to each outcome stated explicitly.** This is where the project story closes: the video process stops competing with the legal LLM and starts feeding it.

---

## The impact map (operational gain → mechanism → business outcome)

| # | Operational gain (from `single source of truth/kpi-data.md`) | Connecting assumption (state it!) | Business outcome |
|---|---|---|---|
| 1 | Capacity ~19 → ~190/mo with the same two producers | Demand for the differentiator exceeds 19/mo (marketing waitlist) and grows with subscriber base [E] | **The paid service can scale** to every subscriber tier without hiring producers — video stops being the reason to say "no" |
| 2 | Cost/video ¥940 → ¥180 | Typical customer uses ~2 of the 10 promised videos/month [E]; volumes 15–40/mo | **The assumed two-video case has a positive subscription-minus-video-cost residual**: −¥1,160 → +¥360 per customer-month; delivered-volume burn −¥150–195k/yr → ≈ break-even [E] |
| 3 | Human time target 10 h to about 1 h; 20 videos require about 20 h/month | Same demand and task scope; management finds useful work for freed time [E] | 180 h/month freed, about 1.02 paid FTE; allocated value ¥183,600/year, not automatic payroll cash |
| 4 | Training examples: every edit + change request becomes labelled fine-tuning data (Iteration 2 flywheel) | HiLegal maintains the fine-tuning backlog [E] | **The video process improves the legal LLM** — the service and the core asset reinforce each other instead of competing |
| 5 | Lead time 21 d → 1.5 d; QAR 10% → 90% | Lawyer satisfaction tracks first-pass acceptance and speed [E] | **Customer experience**: lawyers get campaign-ready video in days, in all formats, with near-zero review rounds — the differentiator becomes marketable as a proposed service-level to test ("video in 48 h") |
| 6 | SLA machinery + analytics from Iteration 1/3 | Dashboard reviewed weekly (PDCA) | **Management capability**: per-step cycle times, SLA compliance, engagement per video — the operations habit HiLegal lacks today [C] |

## The three impact stories (pick per audience)

1. **Money:** lower allocated video cost and released staff hours are two views of the same labour benefit. They are not additive cash savings. A positive subscription-minus-video-cost residual does not establish overall customer profitability.
2. **The growth story (commercial):** "video included in your subscription, delivered in 48 h" is a subscription-selling feature; capacity no longer caps pricing/packaging experiments (e.g., video-count tiers).
3. **The strategy story (leadership — our framing):** HiLegal is a software company with a legal LLM as its moat. Today the moat is maintained by hand, one video at a time. After the three iterations, the moat is maintained by a pipeline — and the same pipeline *generates* fine-tuning data. **Operations stops taxing the strategy and starts compounding it.**

## Assumption ladder (put this table on the slide — it is the section's credibility)

| Assumption | Value | Basis | Risk if wrong |
|---|---|---|---|
| Labour rate / utilization | ¥85/h [E] · 60% [E] | Shenzhen fully-loaded build-up (`single source of truth/kpi-data.md` §3); utilization back-solved from company-reported output [C] | Cost figures shift proportionally; ranking of iterations unchanged |
| Revenue attribution per video | ¥117 [C] | HiLegal's own first assumption: model costs + 30% overhead | Attribution needs re-basing; direction robust (cost falls 81%) |
| Demand at scale | 20 → 40+/mo | Marketing ambition consistent with stated ceiling 35–40 [C] | If demand stays 20/mo, gains 2–3 (profit, headcount) still hold; gain 1 partially idles |
| Staff-time redeployment | 135–180 h/month at 15–20 videos, 0.77–1.02 paid FTE | Conditional on target times and unchanged volume | Cash requires a separate staffing/avoided-hire decision; do not double-count unit-cost labour savings |
| Quality held at scale | QAR ≥ 90% | Pilot gates (Section 6) | Reputation risk with lawyers — guarded by QC steps and QAR gates |
| Vendor economics stable | render ≈ ¥45/video [E] | Current market rates, dual-vendor strategy | ±¥10/video moves cost ±6% — immaterial to conclusions |

## Risks to the organizational story (name them before the audience does)

- **Bespoke expectations:** some lawyers will want non-template work → priced escalation path keeps the standardized line clean.
- **Two people, one brain-drain risk:** cross-train both producers on the pipeline; playbooks are a Section 9 deliverable.
- **Change fatigue at HiLegal:** phased rollout (Section 9) exists precisely for this — each iteration ships value before the next begins.

## Suggested slide plan (3 slides)

1. Impact map (the 6-row table, trimmed to 4 strongest rows)
2. The money story: from −¥150–195k/yr burn to ≈ break-even + 135–180 staff h/month potentially freed, +¥360/typical customer-month [E tags visible]
3. The strategy story: "the pipeline feeds the moat" — Brief → Script → Render → **fine-tuning data → better LLM → better scripts** (the loop closes)

## Checklist

- [ ] Every business outcome traced to a specific KPI change
- [ ] Every connecting assumption visible with an [E]/[C] tag
- [ ] The payroll-reallocation story stated in one clean sentence (money and management attention fund the LLM; the producers are video makers).
- [ ] No outcome claimed without its assumption — this section is graded on rigor, not ambition

## Financial reconciliation

The ¥940 to ¥180 planning comparison includes allocated labour and tooling. At 20 videos/month, the 10 h to 1 h targets imply 200 h to 20 h of work: 180 h/month freed, worth ¥183,600/year at the model rate ¥85/h (1.02 paid FTE at 176 h/FTE). At 15/month the corresponding values are 135 h, ¥137,700/year and 0.77 FTE. The existing two salaries remain payable unless a staffing or avoided-hire decision changes cash outflows. Producers' released time is not ML engineering capacity.

¥117/video is an internal cost/revenue attribution assumption, not observed sales revenue. Comparing it with costs is not an audited margin or burn calculation. The ¥360 residual for a two-video subscription assumes all ¥720 subscription revenue is available to cover video production; other bundled services, support and acquisition costs are excluded. Do not add the allocated per-video labour reduction and released-payroll value as separate benefits.

Training-data reuse requires consent, appropriate access and an actual model-improvement evaluation. QAR measures first-pass acceptance, not legal correctness. Speed, customer satisfaction, content quality and actual contribution margin require separate pilot evidence.
