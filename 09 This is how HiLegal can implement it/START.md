# Section 9 — This is how HiLegal can implement it

**Guiding question:** Which improvements should HiLegal introduce first, and how will it sustain them?

**What this section must accomplish:** a phased rollout mapped to our three iterations, with owners, costs, pilot gates, monitoring, and an explicit path to **self-sufficiency within months** — HiLegal's stated requirement [C]. Order rule: **standardize first (no new technology), automate second** — the cheapest risk reduction comes before the most expensive capability.

---

## Phased rollout (extends the proposal's roadmap)

| Phase | Weeks | Scope (= our iteration) | Deliverables | Exit gate (from Section 6 KPI-checks) |
|---|---|---|---|---|
| **0 — Baseline instrumentation** | 1–2 | Measure the current process | Time-log for 10 legacy videos; replace [E] baselines with observations; freeze the KPI dashboard spec | Observed baselines published; targets re-confirmed or adjusted |
| **1 — Standardize front end** | 3–6 | **Iteration 1** (no new AI tech — forms, previews, SLA approvals, order state machine) | HiLegal Studio v1; 5 format previews; SLA terms text; producer training (½ day) | Lead time ≤ 12 d · 0 clarification loops on ≥8/10 · rework ≤ 60% · QAR ≥ 35% · no quality drop |
| **2a — Script Engine** | 7–10 | **Iteration 2** (fine-tuned LLM + templates; human edit-QC) | v2 templates with compliance constraints; versioning; training-example export | Lead ≤ 5 d · edit depth ≤ 20% · rework ≤ 35% · **0 compliance incidents** |
| **2b — Render pipeline** | 11–14 | **Iteration 3** (single-render avatar, variants, consent registry, publish + objection window) | v3 render integration; consent/e-sign flow; QA checklist; analytics dashboard | Lead ≤ 2 d · render success ≥ 90% · consent coverage 100% · QAR ≥ 85% |
| **3 — Sustain & improve** | 15+ | PDCA at full run-rate | Weekly ops review; quarterly target refresh; vendor cost review; backlog grooming | KPIs at target for 4 consecutive weeks → declare steady state |

*(The proposal's "Phase 2 weeks 5–10" is split here into 2a/2b because our iteration gates showed different risk profiles — scripting automation and render automation fail differently and deserve separate go/no-go decisions.)*

## Responsibilities (small company — hats, not departments)

| Workstream | Owner (HiLegal) | Supported by |
|---|---|---|
| Process design, training, playbooks | Production lead (one of the two producers) | Our team during weeks 1–10 |
| Forms/templates content, SLA policy | Marketing/content owner | Production lead |
| LLM integration, prompt/template engineering, render API | Engineer (the person who would otherwise be fine-tuning the LLM — weeks 7–14 only, ~30% capacity, then hands off) | Our team: architecture + code reviews |
| Consent/legal wording (likeness, voice, disclaimers) | Legal/compliance (FaDaDa resources) | Our team: requirement specs |
| Dashboard, KPI reporting, weekly PDCA chair | Production lead | — |
| Go/no-go at each gate | COO/founder | All |

**Our team's exit condition:** HiLegal runs the weekly PDCA review without us for 3 consecutive weeks and all gate metrics hold. (Self-sufficiency, stated as a testable condition — matches their requirement [C].)

## Costs of implementation (one-time, [E] — keep honest and small)

| Item | Estimate | Note |
|---|---:|---|
| Forms/approvals build (v1) | ¥35–65k internal eng time | 2–3 weeks part-time; or no-code stack first |
| Template library + prompt engineering (v2) | ¥25–40k | Mostly content work, not engineering |
| Render/LLM integration (v3) | ¥45–75k | Includes dual-vendor abstraction layer |
| Producer training | 2 × ½ day per phase | Playbooks are the deliverable |
| Run-rate tooling (already in KPI cost) | ¥65–95/video | See `kpi-data.md` §3 |
| **Total one-time** | **≈ ¥105–180k [E]** | Payback at ¥760/video saving ≈ **140–240 videos ≈ 5–8 months** at 20–35 videos/month |

## Pilot validation (the evidence engine — reuse Section 6 gates)

- Every phase ships to **10 pilot videos** before becoming default; legacy path stays available as fallback until the gate passes (reversibility = adoption insurance).
- Concurrent cohorts (pilot vs. legacy, same weeks and producers) isolate the process effect from demand mix.
- Gates are **quantitative and pre-registered** (see table above): if a gate fails, we do not proceed — we diagnose, fix, and re-run. A gate pass is a decision, not a celebration.
- Steady-state declaration (Phase 3): 4 consecutive weeks at target → lock the standard, archive the legacy path.

## Ongoing monitoring (the PDCA habit, concretely)

| Cadence | Ritual | Metrics reviewed | Actions if off-target |
|---|---|---|---|
| **Weekly** (30 min, production lead) | Ops review | Lead time (median + P90), SLA compliance, rework loops by reason code, render success, edit depth | Reason-code Pareto → template/form fix next week (this IS the P in PDCA) |
| **Monthly** | KPI review vs. targets | All six KPIs + cost/render price drift | Adjust SLA terms, reminder timing, vendor mix |
| **Quarterly** | Strategic check | Volume vs. capacity headroom, training-example flow to LLM backlog, payroll-savings audit (is the ≈ ¥270k actually funding the core?) | Rebalance staffing; refresh targets; renegotiate vendors |

**Alert thresholds (automated from the dashboard):** lead-time P90 > 5 d (v3 steady state) · SLA compliance < 85% · render success < 90% · QAR < 80% · consent coverage < 100% (stop-the-line).

## Sustaining the change (why this survives after we leave)

1. **The system is the process** — the pipeline is the only path to delivery (no shadow email route), so compliance is structural, not disciplinary.
2. **Playbooks per role** — intake, script QC, render QA: one page each, versioned like code.
3. **The flywheel keeps paying** — training examples accumulate automatically; every month the LLM drafts better and edit depth falls (visible in the edit-depth trend — a KPI that gamifies itself).
4. **Vendor discipline** — dual-source renders, interchangeable via the Script JSON contract; quarterly price review (the lock-in risk the proposal flagged [C], managed continuously).
5. **Self-sufficiency is scheduled, not hoped for** — see our exit condition above; weeks 15+ have no external dependency.

## Suggested slide plan (3 slides)

1. Roadmap timeline (phases, gates, our-exit marker)
2. Ownership + costs + payback (≤ ¥180k one-time, ~5–8-month payback [E])
3. Monitoring: weekly/monthly/quarterly cadence + alert thresholds — "the improvement machine stays after the project ends"

## Checklist

- [ ] Standardize-before-automate rationale stated (it is the roadmap's thesis)
- [ ] Every phase has a quantitative exit gate (copy from Section 6 tables)
- [ ] HiLegal's self-sufficiency requirement [C] answered with a testable exit condition
- [ ] Costs and payback labelled [E]
- [ ] Closing line of the deck: *"You don't need a bigger video team. You need your video team back."*
