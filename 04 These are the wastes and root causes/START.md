# Section 4 — These are the wastes and root causes

**Guiding question:** Where does work wait, repeat, or require unnecessary effort — and why?

**What this section must accomplish:** annotate the as-is map with TIMWOODS, drive each dominant waste to a root cause with Five Whys, and make the **critical distinction between the capacity constraint (what limits output) and the causes of long lead time (what limits speed)**. Those are two different diseases, and our three iterations split cleanly between them.

---

## TIMWOODS audit (evidence-based, tied to the map)

| Waste | Where on the map | Evidence | Severity |
|---|---|---|---|
| **Waiting** | Step 2 intake queue (3–7 d [C]); gates 7, 12a; loop re-queues | Work ≈ 6% of lead time; 94% is waiting; every gate can loop, brief loop runs ≥4 iterations [C] | **Dominant (lead time)** |
| **Overprocessing** | Steps 5–6 (human drafts, AI only refines — order reversed from optimal); steps 9–11 (video and audio generated **separately**, then synced **manually**); step 12b (manual platform adaptation) | Sync 2–3 h [C] + adaptation ~2 h [C] = ~40–45% of all labour [E] | **Dominant (labour/capacity)** |
| **Defects** | Rejection loops at all three gates; clarification may loop multiple times [C] | ≥4 brief iterations [C]; rework ≈ 90% of videos [E] | High |
| **Skills — strategic cost mismatch** | The two producers are video makers by trade: their skills are fully used — but they cannot cross over to the core product (LLM fine-tuning is a different discipline). The waste is the cost structure: ¥360k/year [E] of manual video production payroll inside an AI-native software company | An AI-native company should create value through software leverage; carrying agency-style human production economics — expensive people doing what the platform should produce — destroys value against that model. No amount of effort by these two people converts their hours into core-product progress | **High (strategic)** |
| **Transportation** | Files moved by copy-paste across 5+ tools (email → ChatGPT → Seedance → TTS → editor) | Manual handoffs at every green box [C — tool stack confirmed] | Medium |
| **Inventory (WIP)** | Videos sitting in queues between all steps | Queue-gated process (Little's Law); WIP hiding in inboxes, not tracked | Medium |
| **Motion** | Searching emails/Assets for brief versions, brand files, prior feedback | No single source of truth per order [E] | Medium |
| **Overproduction** | Minor — occasional unused format variants produced "just in case" | Low | Low |

**Why we reframed the "skills" waste (important).** The producers are **video makers** — competent, and their talent is fully used. They are not would-be ML engineers, and they cannot simply be pointed at the legal LLM: fine-tuning is a different discipline. So the waste is not *unused talent*; it is a **value-model mismatch** — an AI-native company paying human-agency production costs (¥360k/year [E]) for work its own automation should absorb. What automation actually releases here is **money and management attention**; those — not video-maker hours — are what can be redirected to the core. (This is why Section 8 measures the prize in payroll released, not in engineers "freed".)

**Presentation tip:** put the top three (Waiting, Overprocessing, Defects — matches the proposal) in large type; compress the rest into one summary row. Waste map = same mermaid as Section 3 with red/amber badges per box.

## Five Whys — drive the three dominant wastes to root causes

### Chain 1 — Lead time (Waiting)
1. Why does a video take 2–4 weeks? → Because orders sit in queues at intake and at three approval gates.
2. Why do orders sit in queues? → Because intake is free-form and must be clarified before work can start (3–7 days [C]).
3. Why must it be clarified? → Lawyers describe wants in prose; format, length, tone, language are undefined at request time.
4. Why are they undefined? → There is no structured intake: no form, no format previews, no profile auto-fill.
5. **Root cause: variety is absorbed manually at the front end instead of being standardized at intake** (the 4-Vs insight: high-variety demand meets an unstructured front door).

### Chain 2 — Labour / capacity (Overprocessing)
1. Why does a video take ~10 h [C]? → The three biggest blocks are manual sync (2–3 h), manual adaptation (~2 h), manual script drafting.
2. Why is sync manual? → Video and audio are generated as separate artefacts and married by hand.
3. Why separate? → The toolchain (Seedance + separate TTS + editor) was assembled ad hoc; no single-render pipeline exists.
4. Why is scripting manual? → The LLM is used only to refine a human draft — the automation order is inverted.
5. **Root cause: no standardized data spine — a brief is never captured as structured data, so no downstream step can be automated from it.**

### Chain 3 — Rework (Defects)
1. Why do ≥4 brief iterations happen [C]? → Feedback arrives as free-text email ("make it punchier").
2. Why does that cause loops? → Vague feedback is unactionable; producer guesses; next review rejects again.
3. Why is feedback vague? → Approvals happen over email with no structure, no SLA, no scene-level change requests.
4. Why no structure? → No approval workflow exists — the producer manually chases each gate.
5. **Root cause: unstructured, un-SLA'd approvals.**

**One-line synthesis for the slide:** *three root causes — unstructured intake, no data spine, unstructured approvals — generate all three dominant wastes.*

## Capacity constraint vs. lead-time causes (the distinction the brief demands)

| Lens | What limits it | Evidence | Which iteration fixes it |
|---|---|---|---|
| **Output volume (capacity)** | Manual audio-visual synchronization — largest single labour block (2–3 h [C]), serialized per video, cannot be parallelized by adding effort | Company operates at 15–20/month vs. a stated ceiling of 35–40 [C]; labour math: ~19/month at observed utilization [E] | Iterations 2–3 (scripting automation shrinks upstream labour; single render deletes sync + adaptation entirely) |
| **Lead time (speed)** | Queues: intake queue (3–7 d [C]) + three looping approval gates [C] | Work ≈ 6% of lead time; Little's Law says the process is queue-gated | **Iteration 1** (structured intake kills the intake queue and clarification loop; SLA'd mobile approvals cap gate waits) |
| **Unit economics** | Labour content per video (every manual minute is recurring cost) | ¥940/video [E] vs. ¥117 revenue attribution [C — HiLegal's own assumption: model costs + 30% overhead] | All three iterations (labour waterfall in `05 .../kpi-data.md`) |

**The key sentence to say out loud:** *"Fixing the bottleneck alone would not fix the lead time — queues, not capacity, gate this process. And fixing the queues alone would not fix the cost — the manual middle is the cost. That is why we need a chain of iterations, not one silver bullet."* This is also exactly why Iteration 1 (lead time) precedes Iterations 2–3 (capacity/cost) — and why each iteration's design assumes the previous one is already in place.

## Optional extras (if slide budget allows)

- Fishbone (Ishikawa) with the 6 Ms for the "≥4 brief iterations" defect — Machines (no tooling), Methods (no intake standard), People (producer chasing), Measurement (no cycle-time logging), Materials (vague briefs), Management (no SLA policy)
- Theory of Constraints five focusing steps mapped to our plan: **Identify** (sync = constraint) → **Exploit** (standardize around it: Iter 1) → **Subordinate** (feed it structured input: Iter 2) → **Elevate** (automate it: Iter 3) → **Repeat** (new constraint = lawyer approval time)

## Files to produce for this folder

- `waste-map.png` — Section 3 map with TIMWOODS badges
- `five-whys.md` — the three chains above (ready as speaker notes)
- `root-cause-table.png` — root causes ↔ wastes ↔ iterations mapping (one slide)

## Checklist

- [ ] Every waste claim traceable to a step number or a [C] figure
- [ ] Skills waste framed correctly: video makers, not idle ML talent — the waste is the cost structure/value model, and the released resource is payroll + management attention (Section 8 must match)
- [ ] Bottleneck (sync) explicitly separated from lead-time drivers (queues)
- [ ] Root causes phrased as process design gaps, not people failures (HiLegal's team reads this)
- [ ] Bridge sentence to Section 5: *"Before we change anything, we commit to the numbers we will be judged on."*
