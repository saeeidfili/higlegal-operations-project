# Iteration 3 — UX flow for the software demo

**Product name:** HiLegal Studio v3 — Render Pipeline
**Demo goal:** show one click turning the approved Script JSON into a finished avatar video with voice, lip-sync, and all three platform variants — no TTS step, no sync step, no manual resizing — plus the consent gate and the engagement dashboard that close the loop.
**Continuity:** same shell as v1/v2. Open on the v2 screen where the last demo ended (approved script) so the chain is visible: *form → script → render*.

---

## Screen inventory (deltas vs. v2)

| # | Screen | Role | What it shows / does |
|---|---|---|---|
| 1 | Consent gate | Producer/Lawyer | Order card shows consent status; missing consent → one-tap consent request to lawyer (written likeness + voice consent, e-sign style — fits FaDaDa's e-signature DNA); render button **disabled** until token exists |
| 2 | Render launch | Producer | "Render video" on the approved Script JSON; options pre-set: avatar (lawyer's), voice (brand voice per language), variants 16:9 / 9:16 / 1:1 (all pre-checked); batch queue picker |
| 3 | Render monitor | Producer | Job card: progress ("Scene 3/4 rendering… voice track embedded… lip-sync pass… exporting variants"), ETA ~20 min, auto-retry badge on failure; webhook feed visible |
| 4 | Render QA checklist | Producer | The finished video player + digitized checklist: likeness ✓, name pronunciation ✓, captions ✓, brand frames ✓, disclaimer ✓; fail any item → reason code → auto-re-render or manual flag |
| 5 | Variants view | Producer/Lawyer | Same video in 16:9, 9:16, 1:1 side by side — rendered from one job, structurally consistent |
| 6 | Delivery & objection window | Lawyer | "Your video is live" card: published links per platform, 24 h objection window countdown ("Request a change — 19 h left"), changes during window trigger a scene-level re-render only |
| 7 | Engagement dashboard | Producer/Admin | Per-video views/watch-time by platform; cohort table; per-step cycle-time chart (the PDCA dashboard — to-be step 8) |
| 8 | Full-chain view | all | Vertical pipeline diagram: Brief JSON → Script JSON → Render → Variants → Analytics, with the v1/v2/v3 badges on the segments — the "chain" slide made interactive |
| 9 | Version toggles | all | Header switches "v1 ↔ v2 ↔ v3" replaying ONE order through all three process shapes (the cumulative-improvement money shot) |

## Demo click-path (≈ 2 minutes)

1. Open order at "Script approved" (end state of the v2 demo) → **Consent gate**: token missing → one-tap consent request → lawyer approves in-app (show the e-sign moment) → token appears
2. Click **Render video** → queue animation (~30 s demo time) → variants appear
3. **Render QA**: play the video (placeholder player), tick the checklist — total human time stamp shows "18 min"
4. Auto-delivery fires → cut to Lawyer: "Your video is live" + **19 h objection countdown** (no serial approval wait — say this line)
5. **Engagement dashboard**: views ticking up per platform; per-step cycle-time chart showing 21 d → 9 d → 4 d → 1.5 d across versions
6. Full-chain view: Brief → Script → Render badges light up in sequence
7. Toggle v1 ↔ v2 ↔ v3 on the same order: watch steps fuse 12 → 10 → 9 → 8 and the labour meter fall 10 h → 7 h 15 → 5 h 50 → 1 h

## Data the demo must be seeded with

- Same order as v1/v2 demos (Mei Chen — Practice-Area Explainer, approved script from v2)
- Placeholder rendered video (any 60–90 s avatar-style clip is fine for the demo)
- Consent record: "Likeness + voice consent — signed 12 Oct 2026, valid 12 months"
- Objection window: "19 h left"
- Engagement: 3 platforms, ~1.2k views combined after 48 h
- Stats bar (must match `05 .../kpi-data.md`): lead time 4 d → 1.5 d · labour 5h50 → 1h00 · cost ¥595 → ¥180 · capacity 33 → ~190/mo · rework 30% → 10% · QAR 70% → 90% · steps 9 → 8

## API surface the UI exercises

`POST /v3/renders` · `GET /v3/renders/{id}` + webhooks · `GET /v3/renders/{id}/variants` · `POST /v3/avatars/{id}/consent` · `GET /v3/voices` · `POST /v3/videos/{id}/publish` · `POST /v3/videos/{id}/engagement` · v1/v2 endpoints visible in the dev drawer for the full-chain view

---

## PASTE THIS INTO YOUR DEMO AI

> Build a single-file clickable web prototype (HTML+Tailwind or React, no backend, mocked data) called **"HiLegal Studio — Render Pipeline (v3)"**. Professional SaaS design: white background, deep-navy primary (#0F2A43), gold accent (#C9A227), Inter font. Roles: Lawyer / Producer tabs. This version adds an automated single-render video pipeline on top of an existing intake + AI-scripting system. The full chain must be visible in the UI: structured Brief → AI-generated approved Script → one-click Render → published video with analytics.
>
> **Producer flow:** open order "Mei Chen — Practice-Area Explainer" at stage "Script approved". A **consent gate banner** shows "Avatar consent: missing" with the Render button disabled; clicking "Request consent" switches to the Lawyer role showing an e-signature-style card ("I consent to the use of my likeness and voice in AI-generated videos, valid 12 months") with a signature input and Approve. Back as Producer, the consent token badge turns green and **Render** enables. Clicking it opens a render monitor: staged progress list ("Queued → Scene 1/4 → Scene 4/4 → voice embedded → lip-sync pass → exporting variants") with an ETA "~20 min" that completes in ~8 seconds of demo time, then shows **three video players side by side labeled 16:9, 9:16, 1:1** (use any placeholder video or styled div with a play button). Then a **QA checklist screen**: video player plus checklist items each with a checkbox — likeness matches, name pronunciation, captions, brand frames, disclaimer — a header stamp "Human time: 18 min", and a "Publish" button. Failing any item reveals a reason-code dropdown and a "Re-render scene only" button.
>
> **Lawyer flow:** after publish, a card "Your video is live" showing platform links (Website, YouTube, LinkedIn) and a **24-hour objection window countdown reading "19 h left"** with a "Request a change" button that opens the same scene + reason-code modal from earlier versions. A note under the countdown: "No approval meeting needed — changes during the window re-render only the affected scene."
>
> **Analytics dashboard (Producer/Admin):** a page with per-platform view counts ticking upward, a small line chart of watch time, and a **per-step cycle-time bar chart comparing four process versions**: baseline 12 steps / 21 days, v1 10 steps / 9 days, v2 9 steps / 4 days, v3 8 steps / 1.5 days.
>
> **The centerpiece — full-chain view:** a vertical pipeline diagram with four nodes — "Brief JSON (v1)", "Script JSON (v2)", "Render job (v3)", "Variants + analytics" — connected by animated flowing lines, each node clickable to reveal the JSON payload it passes downstream (mock a small realistic JSON for each).
>
> **Header version switcher "v1 ↔ v2 ↔ v3"** replaying one order through all three process shapes as an animated stepper where steps visibly fuse (12 → 10 → 9 → 8 boxes) beside a labour meter falling 10h00 → 7h15 → 5h50 → 1h00. Persistent footer stats bar: lead time 4 d → 1.5 d, cost ¥595 → ¥180, capacity 33 → ~190 videos/month, rework 30% → 10%, first-pass acceptance 70% → 90%. Dev drawer listing: POST /v3/renders, GET /v3/renders/:id, GET /v3/renders/:id/variants, POST /v3/avatars/:id/consent, GET /v3/voices, POST /v3/videos/:id/publish, POST /v3/videos/:id/engagement. English throughout; every button works; no dead ends.
