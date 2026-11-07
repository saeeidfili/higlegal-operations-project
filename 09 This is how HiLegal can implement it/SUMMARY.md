# Section 9 — This is how HiLegal can implement it (summary)

Flow from Section 8: the headroom is worth having — here is how to get it and keep it. Order rule: **standardize first (no new technology), automate second** — cheapest risk reduction before the most expensive capability. Self-sufficiency within months is HiLegal's stated requirement [C], answered with a testable exit condition.

## Phased rollout

| Phase | Weeks | Scope | Exit gate (Section 6) |
|---|---|---|---|
| **0 — Baseline instrumentation** | 1–2 | Time-log 10 legacy videos; replace [E] baselines; freeze dashboard spec | Observed baselines published; targets re-confirmed |
| **1 — Standardize front end** | 3–6 | **Iter 1** — forms, previews, SLA approvals, state machine; no new AI | Lead ≤ 12 d · 0 clarification loops ≥8/10 · rework ≤ 60% · QAR ≥ 35% · no quality drop |
| **2a — Script Engine** | 7–10 | **Iter 2** — fine-tuned LLM + templates, edit-QC | Lead ≤ 5 d · edit depth ≤ 20% · rework ≤ 35% · **0 compliance incidents** |
| **2b — Render pipeline** | 11–14 | **Iter 3** — single render, variants, consent registry, delivery + objection window | Lead ≤ 2 d · render success ≥ 90% · consent 100% · QAR ≥ 85% |
| **3 — Sustain & improve** | 15+ | PDCA at run-rate | 4 consecutive weeks at target → steady state |

The proposal's Phase 2 is split 2a/2b because scripting and render automation fail differently — separate go/no-go decisions.

## Ownership (small company — hats, not departments)

Production lead owns process + dashboard; marketing owns form/template content; **one engineer at ~30% capacity weeks 7–14 only** (the person who would otherwise be fine-tuning the LLM — then hands off); legal/compliance owns consent wording (FaDaDa resources); COO/founder holds go/no-go.

**Our exit condition:** HiLegal runs the weekly PDCA review without us for 3 consecutive weeks with all gate metrics holding — self-sufficiency as a test, not a hope.

## Costs and payback [E]

| Item | Estimate |
|---|---:|
| Forms/approvals build (v1) | ¥35–65k |
| Template library + prompts (v2) | ¥25–40k |
| Render/LLM integration (v3) | ¥45–75k |
| Training | 2 × ½ day per phase |
| **Total one-time** | **≈ ¥105–180k** |

Payback at ¥760/video saving ≈ 140–240 videos ≈ **4–12 months** at 20–35 videos/month.

## Pilot validation (the evidence engine)

Every phase ships to **10 pilot videos** vs concurrent legacy cohort; legacy path stays as fallback until the gate passes (reversibility = adoption insurance). Gates are quantitative and pre-registered — a gate pass is a decision, not a celebration; a failure means diagnose, fix, re-run.

## Monitoring (PDCA, concretely)

- **Weekly (30 min):** lead median + P90, SLA compliance, rework by reason code, render success, edit depth → reason-code Pareto drives next week's fix
- **Monthly:** all six KPIs + cost/render price drift
- **Quarterly:** volume vs headroom, training-example flow to the LLM backlog, **payroll-savings audit** (is the ≈ ¥270k actually funding the core?)
- **Alerts:** P90 > 5 d · SLA < 85% · render < 90% · QAR < 80% · consent < 100% (stop-the-line)

## Why it survives after we leave

1. **The system is the process** — the pipeline is the only delivery path; compliance is structural
2. **Playbooks per role** — one page each, versioned like code
3. **The flywheel keeps paying** — edit depth falls visibly as the LLM learns (a KPI that gamifies itself)
4. **Vendor discipline** — dual-source renders, interchangeable via Script JSON; quarterly price review
5. **Self-sufficiency is scheduled** — weeks 15+ have no external dependency

Closing line: *"You don't need a bigger video team. You need your video team back."*
