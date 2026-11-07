# Section 5 — These are our operational KPIs (summary)

Flow from Section 4: root causes named — now the scoreboard. Master numbers: `../single source of truth/kpi-data.md`.

## Two primary KPIs — the value, both sides of the counter

| KPI | Whose value | Baseline |
|---|---|---|
| **Cost per Video** | **Company's** — every manual minute is recurring cost | ¥940 [E] |
| **Lead Time per Video** | **Customer's** — the lawyer's campaign calendar pays for every queued day | 14–28 d [C] (~21) |

Cost says whether the service stops bleeding; lead time says whether the lawyer stops waiting. Orthogonal — every iteration must move both.

## Auxiliary KPIs — what changes inside the black box

| KPI | Makes visible | Baseline |
|---|---|---|
| Human time per video | The labour waterfall behind cost | ~10 h [C] |
| Throughput (demand / output / capacity separate) | The scaling question | output 15–20 [C]; capacity ~19 [E] |
| Rework rate | Whether the loop families are dying | ~90% [E] |
| **QAR** (first-pass at every gate) | First-time correctness; catches "faster but worse" | ~10% [E] |

Primaries say *whether* an iteration worked; auxiliaries say *why*.

## Measurement plan — simulate, then pilot

1. **Simulate first:** each iteration's targets validated in the process simulation (Section 7) before implementation — models carry baseline and to-be scenarios.
2. **Pilot in the company:** contained pilot per iteration (Section 9); order state machine timestamps every transition → all KPIs auto-computed per order from Iter 1 on (PDCA).
3. **Gate rule:** pass = primary KPIs hit target AND no auxiliary regresses.

Every figure tagged [C]/[E]/[T]; targets as ranges with mechanisms (justification table in `kpi-data.md`).
