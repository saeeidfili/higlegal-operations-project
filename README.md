# HiLegal Operations Management Project — Working Structure

**Team:** Augustin · Dedi · Joel · Saeed — October 2026
**Proposal:** `Proposal/OM-Project-Proposal-HiLegal.docx` (submitted; its numbers are canon)
**Client:** HiLegal — cross-border legal-tech platform operated by FaDaDa (Shenzhen)

---

## The story in one paragraph (keep every section consistent with this)

HiLegal is a software company. Lawyers pay a subscription — the most popular tier is ≈ $100/month and promises ten videos a month [C] — and promotional videos are produced for them as a service bundled with that subscription. The service is a stated differentiator — no major competitor offers AI-video promotion for lawyers in the cross-border space — but today every video takes **twelve manual steps, ~10 hours of labour, and 2–4 weeks** to deliver. Because the subscription price is fixed, every inefficient hour is money HiLegal loses: the service bleeds margin, it cannot scale past ~15–20 videos/month with two producers, and engineering attention is diverted from HiLegal's real asset — its fine-tuned legal language model. Our proposal: **standardize and then automate the production pipeline in three chained iterations**, so videos cost almost nothing to produce, the production payroll (~1.5 FTE ≈ ¥270k/year) is released to fund the core product — the fine-tuned legal LLM — and the video service flips from a cost centre into a scalable, profitable differentiator.

**The chain logic (each iteration attacks the constraint the previous one exposed):**

```
Baseline: queues everywhere, ~10 h of manual work, 2–4 weeks lead time
   │
   ▼
Iteration 1 — Standardize briefing & approvals
   Kills the queues at the source (self-serve brief, format previews, SLA'd approvals)
   → lead time 2–4 weeks → ~9 days. Exposes: manual scripting + sync still dominate labour.
   │
   ▼
Iteration 2 — Template-based AI scripting (their fine-tuned legal LLM drafts, humans edit)
   Kills script-writing labour and script-surprise loops
   → labour 7h15 → 5h50. Exposes: audio-video sync is now THE binding constraint (~40% of labour).
   │
   ▼
Iteration 3 — Integrated audio/video generation (single-render avatar: voice + lip-sync + video)
   Kills sync, separate generation, and manual platform adaptation in one stroke
   → labour 1h, lead time 1–2 days, ~10× capacity. The remaining constraint is the
   lawyer's own approval time — which is why Iteration 1's SLA machinery matters to the end.
```

**The data-object chain (why the iterations must come in this order):**

```
Iteration 1 produces the structured Brief (JSON) ──► Iteration 2's LLM consumes the Brief
        and produces an approved Script (JSON)      ──► Iteration 3's renderer consumes the
        Script and produces the finished video (+ auto variants)
```

Each iteration's API additions consume the previous iteration's outputs. Nothing in Iteration 2 works without Iteration 1's structured brief; nothing in Iteration 3 works without Iteration 2's structured script.

---

## Folder map

| Folder | Presentation section | What belongs there |
|---|---|---|
| `01 This is HiLegal` | 1 | Company intro, business model, example video, visit photo, methodology |
| `02 This is the challenge` | 2 | Scaling problem, customer needs, consequences |
| `03 This is the current process` | 3 | As-is process map, one-order walkthrough, work vs waiting |
| `04 These are the wastes and root causes` | 4 | TIMWOODS, Five Whys, bottleneck vs lead-time drivers |
| `05 These are our operational KPIs` | 5 | KPI definitions, baselines, targets — **master data in `kpi-data.md`** |
| `06 This is how we improve the process iteration by iteration` | 6 | Chain overview + one sub-folder per iteration (each has `START.md` + `ux-flow.md`) |
| `06 .../Iteration 1 - Standardize briefing and approvals` | 6 | Front-end standardization: forms, previews, SLA approvals |
| `06 .../Iteration 2 - Template-based AI scripting` | 6 | LLM drafting from templates + lawyer profile |
| `06 .../Iteration 3 - Integrate audio and video generation` | 6 | Single-render avatar pipeline with auto variants |
| `07 Let's run and compare the processes` | 7 | Simulation/animation spec, scenarios, inputs & assumptions |
| `08 This is the organizational impact` | 8 | Scaling, profitability, released capacity, assumptions |
| `09 This is how HiLegal can implement it` | 9 | Phased rollout, responsibilities, costs, pilot, monitoring |

Each folder contains a `START.md` with suggestions, ready-to-use tables, and (where useful) Mermaid diagrams you can paste into slides or docs. Iteration folders additionally contain `ux-flow.md` — a self-contained prompt you can paste into another AI to generate a clickable software demo of that iteration.

## Data labelling legend (use it everywhere)

- **[C]** = **Company-reported** — confirmed with HiLegal (visit / proposal, September 2026). These are canon.
- **[E]** = **Estimate** — our assumption or derived figure; plausible, must be sanity-checked, replace when better data arrives.
- **[T]** = **Target** — a value we commit to for a future iteration, not an observation.

**Currency note:** all money figures are in **RMB (¥)** — HiLegal is a Shenzhen-based company. Fully-loaded producer rate **¥85/h [E]** (build-up in `05 .../kpi-data.md` §3), FX **USD/CNY 7.2 [E]** ($100 tier ≈ ¥720/month). Subscription facts [C]: most popular tier $100/month, promising 10 videos/month. HiLegal's own revenue attribution: model costs + 30% overhead ≈ ¥117/video [C].

## Master KPI snapshot (full detail and waterfall tables in `05 .../kpi-data.md`)

| KPI | Baseline | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| Lead time per video (calendar) | 14–28 d [C] | 7–12 d [T] | 3–5 d [T] | 1–2 d [T] |
| Human processing time per video | 10 h 00 [C] | 7 h 15 [T] | 5 h 50 [T] | ~1 h [T] |
| Cost per video | ¥940 [E] | ¥705 [T] | ¥595 [T] | ¥180 [T] |
| Throughput capacity, same 2 producers | ~19/mo [E] | ~26/mo [T] | ~33/mo [T] | ~190/mo [T] |
| (Company-reported actual output) | 15–20/mo, ceiling 35–40 [C] | — | — | — |
| Rework rate (≥1 rework loop) | ~90% [E] | ~55% [T] | ~30% [T] | ~10% [T] |
| Quality Acceptance Rate (zero loops, first pass) | ~10% [E] | ~45% [T] | ~70% [T] | ~90% [T] |
| Process steps | 12 [C] | 10 | 9 | 8 |

## Where to put raw materials

- Visit photo, example video, any slide images → the relevant section folder (e.g., `01 .../`)
- Any spreadsheet models (simulation, cost model) → `07 .../` or `05 .../`
- Final deck lives outside these folders; these folders are the evidence & content kitchen.
