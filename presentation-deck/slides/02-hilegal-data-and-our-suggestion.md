# Slide 2 — What HiLegal told us — and what we suggest

**Speaker:** Augustin Dulon
**Time:** 0:45
**Figures:** process flowchart (12-step as-is map, reused from the presentation deck's slide 4 — see Layout)
**Related appendix:** A1 (costing inputs), A6 (label discipline)

## On-slide content

**Left column — "Given by HiLegal" (every row tagged company-reported [C], Sept 2026):**

| What they reported | Value |
|---|---|
| Intake queue wait | 3–7 days, "workload-dependent" |
| Lead time, request → delivery | 14–28 days |
| Active labour per video | ~10 h |
| Brief iterations before approval | ≥4 rounds |
| Videos reworked at least once | ~90% (estimate on their report) |
| Monthly output / stated ceiling | 15–20 / 35–40 videos |
| Subscription tier | $100/month ≈ ¥720, promising 10 videos |
| Manual A/V sync | 2–3 h per video |
| Platform adaptation | ~2 h per video |
| Their own cost attribution | ¥117/video (model credits + 30% overhead) |

**Center/right — the 12-step process flowchart** (the confirmed as-is map): request → intake queue → clarify → brief → draft → AI refine → script approval → video + audio generation → manual sync → final approval → publish. Work boxes white, waiting boxes wait-fill, approval gates pills, three dashed rework loops. Footer: "process map confirmed with HiLegal, Sep 2026; times reported by the HiLegal team."

**Bottom strip — "What we suggest" (first appearance, one line each):**
- **Thesis:** automate and optimize the process — AI-aided QC for speed — to produce more videos at the same quality, for less money.
- **Iteration 1:** standardize briefing & approvals (kill the queues at the source)
- **Iteration 2:** let the fine-tuned legal LLM draft; humans edit (kill script loops)
- **Iteration 3:** one render = voice + video + all variants (kill the manual middle)

## Layout

- Light slide, header band + gold rule; eyebrow `THE FACTS → OUR SUGGESTION`.
- **Flowchart center-right, dominant:** copy the geometry from the presentation deck's slide 4 (`slides/current.html`, presentation branch): 6-column grid, boxes at x = 128/413/698/983/1268/1553, width 239, rows y = 270 and 446 (stacked half-boxes 52+50 px at 446/506); work = white fill + 2 px ink `#101010` border, radius 8; waiting = `#F6EEDF` fill + `#A8823F` border; gates = same fill/border but pill radius 56; start/end = ink fill, white text, pill; rework loops = dashed 3 px `#262626` above row 1 (y 246) and below row 2 (y 590) with `bg`-backed labels ("Not clarified", "Rejected"); connectors 2 px ink. Optional: reuse the moving-dot animation (`animations/...Slide04.html`) in the web deck — label "one possible path; not to scale".
- **Data table left**, Inter 24 px, white card, tag column in gold.
- **Suggestion strip bottom:** white band, 2 px accent-red `#D92605` top rule — the only red on the slide; three iteration chips in a row, gold rules between.
- Flow unit / boundary caption under the flowchart: "one video order · request received → sent for publishing".

## Speaker notes

TIME: 0:45 (facts 20 s → flowchart walk 15 s → suggestion 10 s)
MAIN MESSAGE: everything we build on comes from HiLegal's own numbers; our answer is a three-step process redesign, not a reorganization.
SPEAKING POINTS: (1) this table is the company-reported baseline — the wait, the lead time, the 10 hours, the four clarification rounds, the tier promise; nothing here is our estimate. (2) The flowchart is their process, confirmed with them in September: white = work, amber = waiting, dark dashed = rework loops. (3) Given these facts, we suggest three iterations: standardize the front door, let the LLM draft, fuse generation into one render — details and simulated numbers come in the next sections. (4) Hand off: "first, let's see where the time actually goes" → slide 5.
DATA STATUS: table 100% company-reported [C] (Sept 2026), one derived estimate flagged (~90% rework); flowchart confirmed with HiLegal [C]; suggestion strip = our proposal, no numbers claimed here.
