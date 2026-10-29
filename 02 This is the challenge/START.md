# Section 2 — This is the challenge

**Guiding question:** HiLegal wants to expand the service. What prevents it from scaling today?

**What this section must accomplish:** make the audience feel the tension *before* any process map appears. A subscription promise the process cannot keep, a costing assumption that missed the human factor, money and people being poured into a side hustle instead of the core product — and, on the other side of the counter, lawyers paying for the same queues with stalled campaigns and lost clients.

---

## The pricing of the human factor (the number everything else hangs on)

HiLegal produces videos with **two full-time producers in Shenzhen** [C]. Their fully-loaded cost — not the salary, the *whole* cost — is what every video pays for:

| Component (per producer, monthly) | Value | Basis |
|---|---:|---|
| Gross salary — bilingual video producer, Shenzhen | ¥10,000 [E] | Shenzhen market range ¥8,000–14,000 |
| Employer social insurance + housing fund (五险一金), ~35% of gross | ¥3,500 [E] | Statutory employer burden, 30–40% band |
| Equipment, software seats, office & overhead share | ¥1,500 [E] | |
| **Fully-loaded cost per producer** | **¥15,000/month** | |
| Productive hours | 176 h (22 working days × 8 h) | |
| **Fully-loaded rate** | **≈ ¥85/h** | 15,000 ÷ 176 |

So what does one video cost today?

| Cost component per video | Value | Share |
|---|---:|---:|
| Human labour: ~10 h [C] × ¥85/h | ¥850 | **90.6%** |
| Model/tool credits (ChatGPT, Seedance, TTS, stock assets) | ¥90 [E] | 9.6% |
| **Total cost per video** | **≈ ¥940 [E]** | |

**The one-liner:** this is called an *AI video service*, but **91% of its cost is people**. The money coming in from subscribers goes straight back out as payroll.

## The challenge in three layers

### Layer 1 — The economics are inverted (the money problem)

- **Their first costing assumption [C]:** a video costs *model credits + 30% overhead* — ¥90 × 1.3 ≈ **¥117 per video** — with the 30% (¥27) meant to cover the human factor. Revenue per video was allocated on exactly this basis.
- **Reality:** ¥940 per video, of which the human factor is ¥850. The 30% buffer covers **3% of it** (¥27 vs ¥850). The assumption wasn't slightly off — it was off by **8×** on the total.
- Every delivered video burns **−¥823** against HiLegal's own revenue allocation.
- And the popular tier makes it worse, not better (Layer 2's numbers): at **$100/month ≈ ¥720 (USD/CNY 7.2 [E])** with a promise of 10 videos, the tier funds **¥72 per video at full usage** — one video costs ¥940. **The most popular tier doesn't pay for one video, let alone ten.**

### Layer 2 — The process cannot scale (and the promise breaks)

- Two producers, ~15–20 videos/month, company-stated ceiling of 35–40 [C].
- **The tier promises 10 videos per month per lawyer [C].** One fully-using customer = 10 × 10 h = 100 producer hours = **57% of one producer**. The entire two-person team can keep that promise for **at most ~2 customers** today — and for no more than 3–4 customers even at the stated ceiling (35–40 ÷ 10).
- The three biggest manual blocks — audio-video sync (2–3 h), platform adaptation (~2 h), script drafting — are all **linear in volume**: 2× videos = 2× hours. No amount of effort fixes that; only a process change does.
- Demand for the cross-border differentiator exceeds what the process can serve; marketing sells the perk, operations cannot deliver it.

### Layer 3 — The side hustle is eating the company (money and resources, not just hours)

HiLegal is a legal-tech software company; video production is a side hustle attached to the subscription. Right now that side hustle consumes:

- **Cash:** −¥823 per video × 15–20 videos/month ≈ **−¥12–16k/month ≈ −¥150–195k/year [E]** of burn on delivered videos alone — before counting the promises they can't deliver.
- **People:** two full-time producers ≈ **¥360k/year** fully loaded [E], plus management attention spent chasing approvals — and a churn spiral that removes capacity and knowledge at the same time (see "The human toll" below).
- **Engineering:** scarce builder time goes to gluing the manual pipeline (files copy-pasted across five tools) instead of fine-tuning the legal LLM.
- **Core starvation:** HiLegal's durable advantage is its **fine-tuned legal language model** [C]. Every RMB burned producing videos by hand is a RMB not invested in that moat. For a startup, the side hustle competes with R&D for the same cash and the same management attention. **The video service isn't just losing money — it is draining the resources the core business runs on.**

## The human toll: burnout, churn, and knowledge walkout (CEO-reported)

Money is not the only thing this process burns. Asked what the pipeline costs beyond cash, the CEO was blunt [C]: the video team **works around the clock**, **people keep resigning**, and re-hiring makes the company **less agile** — because **the knowledge of how to run the process leaves with every resignation**.

The mechanism is a spiral, and the queue is its engine (the math lives in Section 3):

```
queue pressure (ρ ≈ 0.74–0.85, Section 3) → overtime is the only relief valve
→ burnout → resignation → a 2-person team loses up to half its capacity overnight
→ the queue lands on the survivor → deeper overtime → repeat
```

What each turn of the spiral costs:

| Cost | Mechanism | Tag |
|---|---|---|
| **Capacity whiplash** | a team of two has a bus factor of ~2 (arguably 1); one resignation removes up to 50% of throughput overnight while demand stays put | [E] |
| **Months of ramp-up** | the 12-step pipeline is undocumented — it lives in people's heads — so a replacement needs weeks-to-months while the queue keeps growing and the survivor burns | [E] (undocumented process [C]) |
| **Lost agility** | a startup's edge is redeploying people fast; churn + retraining lock the team into a rebuilding loop, consuming cash and management attention the core product needs | [C — CEO] |
| **Knowledge walkout** | no playbooks, no templates, no system state: institutional memory is 100% human-stored — every resignation is a *process-design* loss, not just a headcount loss | [C] |
| **Hidden utilization** | the reported 15–20/month output may itself be propped up by unpaid evening work — meaning true load is even closer to the ρ = 1 wall than Section 3's model shows | [E] |

**The line for the slide:** *the process doesn't just lose money — it consumes the people who run it, and loses their knowledge on the way out.*

(Note for later: this is why Section 9's playbooks and the "the system is the process" principle are not nice-to-haves — they are the HR fix as much as the operations fix. And it is one more reason Section 3 models the team conservatively: with people resigning, the "two producers" are not reliably two.)

## Why wasn't this automated already? (we asked the CEO)

A software company that automates e-signature workflows for a living, running its own flagship service by hand — we asked the CEO why. His answer [C]:

> *"We assumed automation was redundant — that it kills creativity and might lower the quality."* — CEO, HiLegal, September 2026

Four things about that answer:

1. **They were right — at the time.** When the promotion service launched, delegating production to AI end-to-end *did* mean a quality drop: early-generation video and language models could not hold legal-marketing quality, and keeping a human in every step was the rational choice [C — their reasoning]. The decision made sense when it was made.
2. **The world changed under the assumption.** AI capability has been improving on an exponential scale — single-render avatar video with voice and lip-sync in one pass, LLMs fine-tuned to write in a specific voice, speech synthesis that handles names and bilingual scripts: none of that existed at launch; all of it is commodity today. HiLegal has even proved it to itself — the company runs its own fine-tuned legal LLM [C]. The technology barrier expired; the belief just hasn't been re-tested since. **Today the barrier is the belief, not the technology.**
3. **The time log agrees.** Of the ~10 hours a video takes [C], under 3 touch the creative content (briefing 50 + drafting 80 + refining 40 = 170 min of the waterfall). The majority — chasing clarifications, operating generation tools, manually synchronizing audio and video (150 min), re-formatting per platform (100 min) — is mechanical assembly. **There is no creativity in queue-jumping and lip-sync alignment for automation to kill.**
4. **It contradicts their own costing.** The ¥117/video attribution priced the humans as nearly absent (models + 30%), while the operating philosophy treated them as irreplaceable. The process pays for the first belief — and with ≥4 rework loops per video [C] and ~10% first-pass acceptance [E], doesn't even deliver on the second.

**How we answer it (and why we take the fear seriously):** every iteration of our design keeps the creative judgment human — producers *edit* instead of write, humans QC every render — while the machines take the queues and the synchronization. The CEO's test was run on yesterday's AI; this project simply re-runs it on today's — and we committed a KPI specifically to score it: **Quality Acceptance Rate** (Section 5). If automation still kills quality, that number will say so.

## How much does one customer bleed? (the money slide)

Popular tier: **$100/month ≈ ¥720**, promising **10 videos/month** [C]. Against a true cost of ¥940/video:

| Actual usage (of 10 promised) | Monthly cost | Monthly revenue | Bleed per month | Bleed per year |
|---|---:|---:|---:|---:|
| 1 video | ¥940 | ¥720 | −¥220 | −¥2,640 |
| 2 videos (typical [E]) | ¥1,880 | ¥720 | −¥1,160 | −¥13,920 |
| 5 videos | ¥4,700 | ¥720 | −¥3,980 | −¥47,760 |
| 10 videos (full entitlement) | ¥9,400 | ¥720 | **−¥8,680 (−$1,206)** | **−¥104,160 (−$14,470)** |

- Break-even usage: ¥720 ÷ ¥940 = **0.77 videos/month** — the tier loses money on the *first* video and every one after it.
- A single fully-using customer consumes over half a producer. The more successful the tier is, the faster the company bleeds — **the incentive is inverted.**

## The lawyer's perspective: the wait costs them money too

The bleed so far is HiLegal's. But the subscription has another side, and the lawyer pays for the same queues in a different currency.

**The facts of their experience [C]:** publishing and account management sit with the *lawyer*, not HiLegal — the company delivers finished files; the lawyer owns the channels and runs the campaign. So every internal queue lands directly on the lawyer's campaign calendar:

- 3–7 days in the intake queue before anyone even looks at the request [C]
- ≥4 clarification rounds they must personally answer [C]
- three approval gates, each of which can loop [C]
- 2–4 weeks total from request to file-in-hand [C] — and only then does *their* work begin: publishing, promoting, managing the account

**What the wait does to a campaign [E — mechanisms, standard platform behavior]:**

1. **Momentum collapses.** Platform algorithms reward consistent posting; a 2–4 week gap mid-campaign collapses reach. The first videos build an audience; the gap loses it.
2. **The content expires.** Legal marketing is event-driven — regulatory changes, compliance deadlines, a firm launch, a practice-area push. A script pitched for this month's news is delivered as last month's news.
3. **Their own hours are consumed.** The lawyer is the reviewer in every loop. Cross-border lawyers bill at $200–500/h [E]; hours spent re-explaining a brief are hours not sold to clients.
4. **The inbound never arrives.** The video's job is to win cross-border clients. A stalled campaign is weeks of missing inbound leads — and a single engagement won through the video is worth multiples of the annual subscription (¥8.6k) [E].

**The renewal risk:** the perk sold as a growth engine is experienced as a waiting room. A lawyer who cannot get campaigns out the door does not renew the $100 subscription — the video service's queues threaten churn on the *entire* platform relationship, not just the perk.

**The line to say on stage:** *HiLegal measures these queues in payroll; the lawyer measures them in lost clients. Same queues — two bills.*

## The startup framing (why they tolerate it — and why that has to end)

HiLegal knowingly runs the service as a **marketing campaign**: video is the differentiator that wins lawyers onto the platform, and the burn is treated as customer-acquisition spend. As a startup, they don't mind — for now [C].

But a marketing campaign has a budget and an endpoint. This one:

1. **scales with every new subscriber** (up to −¥8.7k/month each),
2. **hits a hard capacity ceiling at ~2 fully-served customers**, and
3. **eats the cash and the management attention that should be funding the legal LLM.**

A campaign with a growing budget, a capacity ceiling, and a drain on the core product is not a campaign — it's a leak.

**What we told them (the thesis of this project):** you can stop the bleed, turn the service slightly positive, and point every freed RMB — and the management attention it buys — at the core of the business, the legal LLM. A preview of the math: at ~¥180/video after the three iterations (Section 6), the *typical* 2-video customer flips from −¥1,160 to **+¥360/month**, and the full-entitlement loss shrinks by 88%. The details are Sections 5–9; first, where exactly does the time go?

## Customer needs (what lawyers experience today)

| Lawyer's need | Today's reality | Consequence |
|---|---|---|
| Fast turnaround (marketing momentum) | 2–4 weeks request → delivery [C] | Campaigns stall; lawyers disengage |
| Predictability ("when will I get it?") | Intake queue alone is 3–7 days, workload-dependent [C] | No date can be promised |
| Getting it right in one round | Brief loop alone runs ≥4 iterations [C] | Lawyers spend time reviewing instead of practising law |
| Multi-platform presence | Manual platform adaptation ~2 h [C], done case-by-case | Inconsistent or missing formats (16:9 / 9:16 / 1:1) |
| The 10 videos they were promised | Team capacity ≈ 15–20/month in total [C] | The entitlement exists on paper, not in practice |
| Run campaigns on their own channels | Publishing & account management sit with the lawyer [C]; delivery date = campaign start date | Every queued day inside HiLegal slips the lawyer's campaign outside it |

## Consequences of the current limitations (build the burn here)

- **Commercial:** the differentiator is sold as a subscription perk but delivered as artisanal labour — tiers are capped by production capacity, not demand.
- **Financial:** −¥823/video → ≈ −¥150–195k/year on delivered volume [E], and up to −¥104k/year per fully-using customer — financed out of the same pocket that funds product development.
- **Operational:** producers are saturated at 50–65% of the stated ceiling; the queue (not the work) drives lead time — the process is queue-gated.
- **Strategic:** the legal LLM — the actual moat — is chronically under-resourced because the side hustle eats the money, the people, and the engineering attention.
- **Customer-side:** lawyers absorb the queues as stalled campaigns and missed content windows — the differentiator is experienced as a waiting room, putting renewal of the whole subscription at risk, not just the video perk.
- **Human:** the queue runs on overtime; churn removes capacity and undocumented knowledge simultaneously, forcing a rebuilding loop after every resignation (CEO-reported [C]) — the process is structurally dependent on the very people it burns out.

## Suggested slide plan (6 slides)

1. One-line challenge statement + the three layers + the CEO's answer to "why not automate?" — right at the time, expired by AI's exponential improvement [C]
2. The human-factor pricing table + the ¥940 build-up ("91% of an 'AI video service' is people")
3. The per-customer bleed table ("the tier loses money on the first video")
4. The lawyer's side: two bills, one queue — momentum, expiry, billable hours, lost inbound → renewal risk
5. The human toll: the burnout → churn → knowledge-walkout spiral (CEO-reported [C])
6. The startup framing + our counter-thesis teaser → transition: *"So where exactly does the time go? Let's follow one video."* → Section 3

## Evidence checklist

- [ ] CEO quote tagged [C] with date — first validated as correct-at-the-time (AI quality then), then overturned by the exponential improvement; answered with evidence (170 of 600 min are creative), never mocked
- [ ] Publishing & account management on the lawyer's side tagged [C]; lawyer-side economics (billable rates, engagement values) tagged [E] and kept illustrative — no invented precision
- [ ] CEO's HR report (around-the-clock work, resignations, agility loss, knowledge walkout) tagged [C]; churn/ramp cost mechanics tagged [E]; the spiral diagram shown before any fix is mentioned
- [ ] Tier price ($100/month) and the 10-video promise tagged [C]
- [ ] The attribution assumption (models + 30% overhead) presented as *their* first assumption [C], then contrasted with the ¥940 reality
- [ ] The per-customer bleed table shown before any solution appears
- [ ] The startup/marketing-campaign framing stated fairly (they *do* tolerate it) before our counter-thesis
- [ ] No detailed solutions in this section — preview hooks only (~¥180/video, the QAR KPI pointer)
