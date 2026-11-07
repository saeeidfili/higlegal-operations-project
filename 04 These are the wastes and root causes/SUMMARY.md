# Section 4 — These are the wastes and root causes (summary)

Flow from Section 3: showed *where* the time goes — this explains *why*, drives each dominant waste to a root cause, and splits capacity limits from lead-time causes. The two model folders — `queue/` and `Rework/` — are the quantitative explanation of two of the wastes: **Waiting** and **Defects**.

## The dominant wastes (TIMWOODS, evidence-based)

| Waste | Evidence | Severity |
|---|---|---|
| **Waiting** | Work ≈ 6% of lead time. Queue model reproduces the whole 3–7 d intake band from first principles: μ ≈ 23.5, demand 15–20 → ρ = 0.64–0.85, expected wait 2.3–7.5 d. The wait is *the mathematics of utilization*, not slowness. P90 ≈ 10 d; demand ×1.33 → wait ×3.2 | **Dominant (lead time)** |
| **Overprocessing** | Human drafts, AI only refines (order reversed); video + audio generated separately then synced by hand; manual platform adaptation. Sync 2–3 h [C] + adaptation ~2 h [C] ≈ 40–45% of all labour [E] | **Dominant (labour/capacity)** |
| **Defects** | ≥4 brief iterations [C]; ~90% of videos loop [E]. Simulated: loops add **84 min of work but 10.8 days of lead** (~29×) and pull the ceiling 27.4 → 23.6 → 20.6/month | High |
| **Skills = value-model mismatch** | Producers are video makers, fully used, can't cross to LLM work. The waste is the cost structure: ¥360k/yr [E] of manual production payroll inside an AI-native company. What automation releases is money + management attention, not engineer-hours | High (strategic) |
| Transportation · Motion · Inventory · Overproduction | Files copy-pasted across 5+ tools [C]; no single source of truth per order [E]; WIP ≈ 12.7 videos in system at typical demand; unused format variants rare | Medium/Low — real but secondary; fix falls out of the same iterations |

## Five Whys — three root causes

1. **Waiting → unstructured intake.** 2–4 weeks because orders queue; queue because prose briefs need clarifying; undefined format/length/tone; no form, no previews, no auto-fill. *Variety absorbed manually at the front end instead of standardized at intake.*
2. **Overprocessing → no data spine.** 10 h because sync/adaptation/drafting are manual; separate artefacts from an ad-hoc toolchain; LLM refines instead of writes. *A brief is never captured as structured data, so nothing downstream can be automated from it.*
3. **Defects → unstructured, un-SLA'd approvals.** Vague email feedback → producer guesses → rejected again; no approval workflow.

*Three root causes — unstructured intake, no data spine, unstructured approvals — generate all three dominant wastes.*

## The quantitative narrative (the two models)

**Beat 1 — Waiting is mathematics (`queue/`).** One pooled server (video held start-to-finish), μ = 23.5 calibrated → predicts 2.3–7.5 d across demand 15–20 [C], including the "workload-dependent" behaviour. At typical ρ = 0.74, 3 of 4 arrivals find the team busy. Congestion multiplier ρ/(1−ρ) turns +33% demand into 3.2× wait. Falsifiable prediction: inbox holds ≈ 2–5 parked requests — count it.

**Beat 2 — Rework is a queue problem wearing a work costume (`Rework/`).** Full 12-step simulation calibrated to today (21.8 d lead inside 14–28 [C], 600 min work, 87% rework). Loops off: lead 11.0 d, ceiling 27.4/mo. **+84 min buys +10.8 days**; the ceiling is a property of the team *plus its rework* (27.4 → 23.6 → 20.6).

**Beat 3 — One identity binds them.** Little's Law: lead time = WIP ÷ throughput. Unstructured intake puts the process on the cliff (Waiting); unstructured approvals multiply WIP (Defects); no data spine keeps τ ≈ 10 h, capping μ and pushing ρ up the same cliff (Overprocessing). The wastes are each other's causes — attacked in sequence, not one at a time.

## Capacity constraint vs. lead-time causes (two diseases)

| Lens | What limits it | Fixed by |
|---|---|---|
| **Output volume (capacity)** | Manual AV sync — largest labour block, serialized — plus rework inflating everything; ceiling 23.6/mo at baseline rework | Iterations 2–3 |
| **Lead time (speed)** | Queues: intake (3–7 d [C]) + three looping gates; work ≈ 6% of lead | Iteration 1 |
| **Unit economics** | Labour content per video: ¥940 [E] vs ¥117 attribution [C] | All three |

**Key sentence:** *"Fixing the bottleneck alone would not fix the lead time — queues, not capacity, gate this process. And fixing the queues alone would not fix the cost — the manual middle is the cost. That is why we need a chain of iterations, not one silver bullet."*

## Charts

`queue/queue-cliff.svg` (THE waiting slide), `queue/order-timeline.svg` (work ≈ 6%), `Rework/rework-impact.svg` (+84 min ↔ +10.8 d headline), `Rework/rework-vs-demand.svg` (three rework levels, three walls), `Rework/queue-sample-path.svg` + `Rework/gantt-rework.svg` (backups).

Bridge to Section 5: *"Before we change anything, we commit to the numbers we will be judged on."*
