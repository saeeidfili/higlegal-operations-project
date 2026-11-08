# Slide 6 — Three wastes dominate — and three root causes generate them

- **Speaker:** Dedi Li
- **Time:** 1:00
- **Figures:** none (table slide — no SVG from the manifest)
- **Related appendix:** A3 (rework simulation), A6 (assumptions & model cards)

## On-slide content

**Title:** Three wastes dominate — and three root causes generate them

**Dominant wastes (TIMWOODS, evidence-based):**

| Waste | Evidence | Severity |
|---|---|---|
| **Waiting** | Work ≈ 6% of lead time; queue model reproduces the 3–7 d band [C]; P90 ≈ 10 d | **Dominant — lead time** |
| **Overprocessing** | Sync 2–3 h [C] + adaptation ~2 h [C] ≈ 40–45% of labour [E] | **Dominant — labour/capacity** |
| **Defects** | ~90% of videos loop [E]; +84 min work → +10.8 d lead; ceiling 27.4 → 23.6 → 20.6/mo | High |
| **Skills = value-model mismatch** | ¥360k/yr [E] manual payroll inside an AI-native company | High — strategic |
| Transportation · Motion · Inventory · Overproduction | Files across 5+ tools [C]; WIP ≈ 12.7 videos in system — real but secondary | Medium/Low |

**Synthesis band (bottom, full width):**

> **Unstructured intake + no data spine + unstructured approvals → generate all three dominant wastes**

## Layout

- **Title:** Momo Trust Display, `#262626`, top-left, short-statement grammar; no subtitle.
- **Table dominates the slide** (no figure). Per source presentation tip: the **top three wastes in large type** — waste names ~32 px semibold Inter, `#0A0A0A`, left column; the mismatch row steps down to ~26 px; evidence column Inter 24–26 px, body `#4A5565`, max two lines per cell; [C]/[E] tags kept inline, muted `#6A7282`.
- **Severity tags** as small right-aligned pills: "Dominant" pills filled white with 2 px gold `#C9A86A` border + gold text; "High" pills grey-400 `#99A1AF` border, body `#4A5565`.
- **Row hierarchy:** top-3 rows separated by 1 px grey-200 `#E5E7EB` rules with extra leading (the visual "large type" beat); mismatch row slightly tighter; the secondary row compressed to a single muted line (`#6A7282`, 24 px, no pill) so it reads as a footnote to the table, not a peer.
- **Synthesis band:** white card on bg `#F3F4F6`, 1 px grey-200 `#E5E7EB` border, generous padding; three root-cause chips ("Unstructured intake", "No data spine", "Unstructured approvals") joined by `+`, then a single `→` in accent red `#D92605` (the only red on the slide) pointing to "generate all three dominant wastes" in `#0A0A0A` semibold.
- **Density check:** 1 header + 5 rows + synthesis band; evidence cells ≤ 2 lines at 24 px minimum (Inter floor per design system). No figure labels needed (no figure); [C]/[E] legend footnote one line, muted: "[C] company-reported · [E] estimate".

## Speaker notes

**TIME** — 1:00 (Dedi Li). Orientation ~5 s → ~12 s per dominant waste (36 s) → mismatch row ~8 s → secondary row ~4 s → synthesis line ~10 s. Do not walk the secondary row cell by cell.

**MAIN MESSAGE** — Three wastes account for essentially all the damage, and all three trace back to the same three root causes — so the answer is one chain of fixes aimed at root causes, not three separate war-rooms.

**SPEAKING POINTS**

1. "We scored every step of the 12-step process against TIMWOODS. Three wastes dominate — and each has a different victim."
2. **Waiting kills lead time:** work is ≈ 6% of lead time; the queue model reproduces the whole 3–7 d intake band from first principles — the wait is the mathematics of utilization, not slowness. P90 ≈ 10 days.
3. **Overprocessing eats labour:** humans draft and AI refines — the order is reversed; manual AV sync plus manual platform adaptation is roughly 40–45% of all labour.
4. **Defects multiply everything:** ~90% of videos loop at least once; each loop adds ~84 minutes of work but 10.8 days of lead — the queue cost dwarfs the work cost — and loops pull the capacity ceiling 27.4 → 23.6 → 20.6 per month.
5. **The fourth row is strategic, not operational:** producers are fully utilized but cannot cross into LLM work — ¥360k/yr of manual production payroll inside an AI-native company. What automation releases is money and management attention, not engineer-hours.
6. Transportation, motion, inventory, overproduction: real but secondary — they fall out of the same fixes, so we don't spend slide time on them.
7. **Synthesis (the point of the slide):** the Five Whys drive all three dominant wastes to three root causes — unstructured intake, no data spine, unstructured approvals. They are linked: unstructured intake puts the process on the queue cliff; unstructured approvals multiply WIP; no data spine keeps service time near 10 h, capping throughput and pushing utilization up the same cliff. The wastes are each other's causes — attacked in sequence, not one at a time.
8. Bridge out: "The next two slides take the two quantified wastes in turn — starting with waiting, because waiting is mathematics."

**DATA STATUS** — Evidence-tag discipline per A6: [C] = company-reported, [E] = estimate. Waiting: 3–7 d band is [C]; work ≈ 6% and P90 ≈ 10 d are model-calculated (queue model). Overprocessing: sync 2–3 h and adaptation ~2 h are [C]; the 40–45% labour share is [E]. Defects: ~90% loop share is [E]; the +84 min / +10.8 d ratio and the 27.4 → 23.6 → 20.6 ceiling are simulated outputs of the calibrated rework model (A3). Skills mismatch: ¥360k/yr is [E]. Nothing on this slide presents iterations as results — it is diagnosis only.

