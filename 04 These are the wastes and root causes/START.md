# Section 4 — These are the wastes and root causes

**Guiding question:** Where does work wait, repeat, or require unnecessary effort — and why?

**What this section must accomplish:** annotate the as-is map with TIMWOODS, drive each dominant waste to a root cause with Five Whys, and make the **critical distinction between the capacity constraint (what limits output) and the causes of long lead time (what limits speed)**. Those are two different diseases, and our three iterations split cleanly between them. This section also carries the **quantitative evidence**: the two Section-3 models — the intake-queue model and the whole-process rework simulation — turn every dominant waste claim into a number. Deep dives: `../03 This is the current process/queue_model-explained.md` and `../03 This is the current process/Rework/rework-flow.md`.

---

## TIMWOODS audit (evidence-based, tied to the map and the models)

| Waste | Where on the map | Evidence | Severity |
|---|---|---|---|
| **Waiting** | Step 2 intake queue (3–7 d [C]); gates 7, 12a; loop re-queues | Work ≈ 6% of lead time. The queue model reproduces the whole intake band from first principles: at μ ≈ 23.5/month the observed demand 15–20 gives ρ = 0.64–0.85 and an expected wait of 2.3–7.5 days — the reported 3–7 d is *the mathematics of utilization*, not slowness; P90 ≈ 10 d, and demand ×1.33 makes the wait ×3.2 | **Dominant (lead time)** |
| **Overprocessing** | Steps 5–6 (human drafts, AI only refines — order reversed from optimal); steps 9–11 (video and audio generated **separately**, then synced **manually**); step 12b (manual platform adaptation) | Sync 2–3 h [C] + adaptation ~2 h [C] = ~40–45% of all labour [E]; the rework simulation confirms these blocks dominate every scenario untouched by loops | **Dominant (labour/capacity)** |
| **Defects** | Rejection loops at all three gates; clarification may loop multiple times [C] | ≥4 brief iterations [C]; rework ≈ 90% of videos [E]. Simulated: the loops add **72 minutes of work but 9.7 days of lead time** — the queue cost is ~30× the work cost — and they pull the capacity ceiling down 27.4 → 24.0 → 20.7/month | High |
| **Skills — strategic cost mismatch** | The two producers are video makers by trade: their skills are fully used — but they cannot cross over to the core product (LLM fine-tuning is a different discipline). The waste is the cost structure: ¥360k/year [E] of manual video production payroll inside an AI-native software company | An AI-native company should create value through software leverage; carrying agency-style human production economics — expensive people doing what the platform should produce — destroys value against that model. No amount of effort by these two people converts their hours into core-product progress | **High (strategic)** |
| **Transportation** | Files moved by copy-paste across 5+ tools (email → ChatGPT → Seedance → TTS → editor) | Manual handoffs at every green box [C — tool stack confirmed] | Medium |
| **Inventory (WIP)** | Videos sitting in queues between all steps | Queue-gated process (Little's Law). The models make the invisible inventory countable: the intake inbox should hold **≈ 2–5 parked requests** (falsifiable — go count it), and the whole system ≈ 12.5 videos in process at typical demand, rising to 20+ with heavy rework | Medium |
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

*The model agrees:* nothing in the queue math is about effort — the 3–7 d wait falls out of ρ ≈ 0.74 and the multiplier ρ/(1−ρ) ≈ 2.9. Standing slightly left of a cliff is not a people problem.

### Chain 2 — Labour / capacity (Overprocessing)
1. Why does a video take ~10 h [C]? → The three biggest blocks are manual sync (2–3 h), manual adaptation (~2 h), manual script drafting.
2. Why is sync manual? → Video and audio are generated as separate artefacts and married by hand.
3. Why separate? → The toolchain (Seedance + separate TTS + editor) was assembled ad hoc; no single-render pipeline exists.
4. Why is scripting manual? → The LLM is used only to refine a human draft — the automation order is inverted.
5. **Root cause: no standardized data spine — a brief is never captured as structured data, so no downstream step can be automated from it.**

*The model agrees:* these 250 minutes survive every rework scenario unchanged — loops only stack on top of them. They are the τ in Wq = ρ/(1−ρ) · τ: cutting them is the only lever that moves the whole curve.

### Chain 3 — Rework (Defects)
1. Why do ≥4 brief iterations happen [C]? → Feedback arrives as free-text email ("make it punchier").
2. Why does that cause loops? → Vague feedback is unactionable; producer guesses; next review rejects again.
3. Why is feedback vague? → Approvals happen over email with no structure, no SLA, no scene-level change requests.
4. Why no structure? → No approval workflow exists — the producer manually chases each gate.
5. **Root cause: unstructured, un-SLA'd approvals.**

*The model agrees — loudly:* a loop looks like 50–70 minutes of extra work, but each one also plants a fresh 1–3-day gate wait and another turn in the work queue while every other video waits behind it (Little's Law). 72 minutes bought 9.7 days.

**One-line synthesis for the slide:** *three root causes — unstructured intake, no data spine, unstructured approvals — generate all three dominant wastes.*

## The quantitative narrative — two models, one overloaded system

This is the story the charts tell. It runs in three beats; each beat is one
model result, and together they explain why this process cannot be fixed by
effort.

### Beat 1 — The waiting is mathematics, not slowness (intake queue model)

Model the team as one pooled processing unit (a video is held start-to-finish;
the inbox is answered only when a producer finishes one — `why-one-server.svg`),
and the reported 3–7-day wait stops being mysterious: calibrate the one
unknown capacity to μ ≈ 23.5/month and the model predicts **2.3–7.5 days
across the observed demand range 15–20/month [C]** — including the
"workload-dependent" behaviour HiLegal described. At typical demand
ρ = 0.74: three out of four arrivals find the team busy. Nobody is slacking;
the process simply sits on the steep part of the utilization cliff, where the
congestion multiplier ρ/(1−ρ) turns a 33% demand increase into a **3.2× wait
increase**, and 1 in 5 lawyers waits over a week (P90 ≈ 10 d) *before
production even starts*.

The same arithmetic exposes the ceiling. 2 producers × 176 h ÷ 10 h = **35.2
videos/month at 100% dedication — which is precisely the company-stated
ceiling of 35–40 [C].** The "ceiling" is not a target; it is the ρ = 1 wall,
where waiting goes infinite. "Pushing to the ceiling" is a mathematical
promise of unbounded queues.

One falsifiable prediction to offer the room: **the intake inbox should hold
≈ 2–5 parked requests at any moment** (Little's Law). If it never holds more
than one, the delay is batch-review cadence instead — and Iteration 1's
self-serve intake kills either mechanism.

### Beat 2 — Rework is a queue problem wearing a work costume (whole-process simulation)

Simulate the entire 12-step process — two pooled producers, three looping
gates, arrivals at 17.5/month — and calibrate it to today (it reproduces the
reported lead time 20.7 d inside 14–28 [C], the work 588 min ≈ 600 [C], and
the ~90% rework incidence [E]). Then switch the loops off and compare:

| | no rework | baseline (today) | heavy rework |
|---|---:|---:|---:|
| Lead time | 11.0 d | **20.7 d** | 28.8 d (P90 47.8) |
| Hands-on work | 516 min | **588 min** | 684 min |
| Videos in system | 6.2 | **12.5** | 20.4 |
| Capacity ceiling | 27.4/mo | **24.0/mo** | 20.7/mo |

Read the gap between the columns: going from no-rework to today adds **72
minutes of work but 9.7 days of lead time** — the queue cost of rework is
~30× its work cost. The mechanism is Little's Law: every loop parks the video
at a gate for 1–3 days, adds another turn in the work queue, and holds it in
the system while everything else waits behind it. And because loops inflate
work content, they also **eat the ceiling**: 27.4 → 24.0 → 20.7/month as
rework grows. The ceiling is not a property of the team; it is a property of
**the team plus its rework**. At 22/month with heavy rework — a level the
company wants to reach — the simulation's queue grows without bound (WIP ≈ 72,
lead ≈ 100 days): past the wall, every month adds permanent backlog.

### Beat 3 — One system, three wastes, one accounting identity

Put the two models side by side and the three dominant wastes stop being
separate complaints:

- **Unstructured intake** (root cause 1) puts the process on the steep part of
  the utilization cliff — the *Waiting* waste is that cliff's shadow.
- **Unstructured approvals** (root cause 3) multiply the videos in the system
  — the *Defects* waste is mostly WIP wearing a work costume.
- **No data spine** (root cause 2) keeps τ ≈ 10 h of manual work per video,
  which caps μ and pushes ρ up the same cliff — the *Overprocessing* waste
  pays rent to the other two.

Little's Law — lead time = WIP ÷ throughput — is the identity that binds
them: the wastes *are* each other's causes, which is why they must be
attacked in sequence rather than one at a time. That is the entire logic of
the iteration chain in Section 6, and it is why the key sentence below is
true.

## Capacity constraint vs. lead-time causes (the distinction the brief demands)

| Lens | What limits it | Evidence | Which iteration fixes it |
|---|---|---|---|
| **Output volume (capacity)** | Manual audio-visual synchronization — largest single labour block (2–3 h [C]), serialized per video, cannot be parallelized by adding effort — **plus the rework that inflates every other task** | Company operates at 15–20/month vs. a stated ceiling of 35–40 [C]; labour math ~19/month at observed utilization [E]; simulation: rework pulls the ceiling 27.4 → 24.0 → 20.7/month; the stated ceiling equals the calculated 100%-dedication wall 35.2 | Iterations 2–3 (scripting automation shrinks upstream labour; single render deletes sync + adaptation entirely) |
| **Lead time (speed)** | Queues: intake queue (3–7 d [C]) + three looping approval gates [C] | Work ≈ 6% of lead time; queue model: expected wait 2.3–7.5 d, P90 ≈ 10 d, ×3.2 nonlinearity; simulation: loops are worth +9.7 d of waiting | **Iteration 1** (structured intake kills the intake queue and clarification loop; SLA'd mobile approvals cap gate waits) |
| **Unit economics** | Labour content per video (every manual minute is recurring cost) | ¥940/video [E] vs. ¥117 revenue attribution [C — HiLegal's own assumption: model costs + 30% overhead] | All three iterations (labour waterfall in `05 .../kpi-data.md`) |

**The key sentence to say out loud:** *"Fixing the bottleneck alone would not fix the lead time — queues, not capacity, gate this process. And fixing the queues alone would not fix the cost — the manual middle is the cost. That is why we need a chain of iterations, not one silver bullet."* This is also exactly why Iteration 1 (lead time) precedes Iterations 2–3 (capacity/cost) — and why each iteration's design assumes the previous one is already in place.

## Optional extras (if slide budget allows)

- Fishbone (Ishikawa) with the 6 Ms for the "≥4 brief iterations" defect — Machines (no tooling), Methods (no intake standard), People (producer chasing), Measurement (no cycle-time logging), Materials (vague briefs), Management (no SLA policy)
- Theory of Constraints five focusing steps mapped to our plan: **Identify** (sync = constraint) → **Exploit** (standardize around it: Iter 1) → **Subordinate** (feed it structured input: Iter 2) → **Elevate** (automate it: Iter 3) → **Repeat** (new constraint = lawyer approval time)

## Charts — already built in Section 3, reuse them here

Don't regenerate; link or copy from `../03 This is the current process/`:

| Chart | Use in this section as |
|---|---|
| `queue-cliff.svg` | THE waiting-waste slide: the utilization cliff with the observed 3–7 d band and the ρ = 1 wall = the "ceiling" |
| `why-one-server.svg` | the modeling-choice sidebar (why the team counts as one pooled unit) |
| `order-timeline.svg` | work ≈ 6% — red dominates Lawyer Chen's 18.8 days |
| `Rework/rework-impact.svg` | the defects-waste headline: +72 min ↔ +9.7 d, whiskers show the P90 tail |
| `Rework/rework-vs-demand.svg` | capacity erosion: three rework levels, three different walls |
| `Rework/queue-sample-path.svg` · `Rework/gantt-rework.svg` | backup slides: the backlog forming at 22/mo; one order's loops |

## Files to produce for this folder

- `waste-map.png` — Section 3 map with TIMWOODS badges
- `five-whys.md` — the three chains above (ready as speaker notes)
- `root-cause-table.png` — root causes ↔ wastes ↔ iterations mapping (one slide)

## Checklist

- [ ] Every waste claim traceable to a step number or a [C] figure
- [ ] Model numbers quoted with their homes (queue model / rework sim docs) — not from memory
- [ ] The falsifiable prediction stated once (inbox holds ≈ 2–5 parked requests)
- [ ] The ceiling = ρ = 1 wall connection said aloud (35.2 calculated ≈ 35–40 stated [C])
- [ ] Skills waste framed correctly: video makers, not idle ML talent — the waste is the cost structure/value model, and the released resource is payroll + management attention (Section 8 must match)
- [ ] Bottleneck (sync) explicitly separated from lead-time drivers (queues)
- [ ] Root causes phrased as process design gaps, not people failures (HiLegal's team reads this)
- [ ] Bridge sentence to Section 5: *"Before we change anything, we commit to the numbers we will be judged on."*
