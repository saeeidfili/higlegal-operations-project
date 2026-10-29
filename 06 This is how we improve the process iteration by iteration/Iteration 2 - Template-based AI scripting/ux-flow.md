# Iteration 2 — UX flow for the software demo

**Product name:** HiLegal Studio v2 — Script Engine
**Demo goal:** show a script appearing in ~1 minute from the structured brief (Iteration 1's form), a human editing rather than writing, and every change request automatically becoming a labelled training example for the legal LLM — the fine-tuning flywheel visible in the UI.
**Continuity:** same product shell as v1 (same roles, same brand). The demo should open with the v1 form already filled — the audience saw that screen last section — and then show what's new.

---

## Screen inventory (deltas vs. v1)

| # | Screen | Role | What it shows / does |
|---|---|---|---|
| 1 | Order detail — "Generate script" | Producer | The Brief JSON from v1; button "Generate draft with [HiLegal Legal LLM]" + template already inferred from the brief's format field |
| 2 | Generation view | Producer | ~1-minute progress animation: "Reading brief… selecting template (Practice-Area Explainer)… loading lawyer profile (14 yrs, EN/中文, 3 jurisdictions)… drafting scene 3/4… applying compliance checks ✓" |
| 3 | Script scene editor | Producer | Draft as scene cards (Hook / Credentials / Practice focus / CTA), voiceover text + on-screen text per scene, compliance badges per scene ("disclaimer included", "no outcome guarantee"), inline editing, word-count and duration estimate; **"Edit depth: 8%" meter** comparing edits vs. draft |
| 4 | Version history & diff | Producer | Every regeneration/edit as versions; diff highlighting; each lawyer change request shown as the scene-level edit it triggered |
| 5 | Approval link (mobile-style) | Lawyer | Same v1 approval card, now rendering the AI draft scene-by-scene with the template's structure visible ("based on your Intro format — the structure you picked"); Request change → same scene + reason-code modal as v1 |
| 6 | Training examples feed | Producer/Admin | **The flywheel screen**: list of labelled examples auto-generated this week (original text → edited text, reason code, accepted/rejected) with a button "Export 27 examples to LLM fine-tuning backlog" |
| 7 | KPI dashboard (updated) | Producer | Tiles now compare v1 vs. v2: human time/video, script edit depth, rework loops, QAR; capacity meter showing "33/month — at your stated ceiling" |
| 8 | Version toggle | both | Header switch "v1 manual drafting ↔ v2 Script Engine" replaying the same brief through both paths side by side |

## Demo click-path (≈ 2 minutes)

1. Open order "Mei Chen — Practice-Area Explainer" at stage "Brief confirmed" (v1 machinery visible: the brief form data, timestamps)
2. Click **Generate script** → generation animation (~30 s in demo time) → draft appears
3. In the scene editor: change one phrase; the **edit-depth meter ticks from 6% to 8%** — "I edited 8% of what the machine wrote; last month I wrote 100%"
4. Send to lawyer → cut to Lawyer: approval card shows the structured draft → "Request change" on Scene 2 ("wrong emphasis") → submit
5. Cut to Producer: the change arrives as a structured card; regenerate **only scene 2** in ~10 s; version diff highlights the single scene change; lawyer approves
6. Open the **Training examples feed**: both the producer edit and the lawyer change request appear as labelled pairs → "Export 27 examples to fine-tuning backlog"
7. Version toggle: split-screen of the same order in v1 (80 min of writing, 2 loop rounds) vs. v2 (35 min total, 1 structured round)

## Data the demo must be seeded with

- Same lawyer and brief as the v1 demo (Mei Chen, Practice-Area Explainer, EN/中文)
- One complete generated script (4 scenes, ~200 words, 90 s duration) with per-scene compliance badges
- One version diff pre-populated + the change request that caused it
- Training-feed counter: 27 examples this week
- v1→v2 comparison stats (must match `05 .../kpi-data.md`): script work 80 → 35 min · labour 7h15 → 5h50 · lead time 9 → 4 days · rework 55% → 30% · QAR 45% → 70% · capacity 26 → 33/month

## API surface the UI exercises

`POST /v2/scripts/generate` · `GET /v2/templates/{id}` · `GET /v2/profiles/{lawyerId}` (extended with accepted edits) · `POST /v2/scripts/{id}/versions` + `GET .../diff` · `POST /v2/scripts/{id}/change-requests` (+ training-example export) · all v1 endpoints unchanged underneath

---

## PASTE THIS INTO YOUR DEMO AI

> Extend a single-file clickable web prototype (HTML+Tailwind or React, no backend, mocked data) called **"HiLegal Studio — Script Engine (v2)"**. Same professional SaaS design language as before: white background, deep-navy primary (#0F2A43), gold accent (#C9A227), Inter font. Two role tabs: **Lawyer** and **Producer**. This version adds AI script generation on top of an existing intake system.
>
> **Producer flow:** open an order card "Mei Chen — Practice-Area Explainer — Brief confirmed". The order page shows the structured brief as clean JSON (format: practice-area-explainer, tone: professional-warm, languages: EN + 中文, length: 90 s, key messages: cross-border M&A, 3 jurisdictions). A primary button **"Generate script"** runs a ~5-second staged progress animation ("Reading brief… selecting template… loading lawyer profile (14 yrs, PwC alumni, EN/中文)… drafting scene 3/4… compliance checks ✓"). The result opens in a **scene editor**: four scene cards (Hook / Credentials / Practice focus / Call-to-action), each with voiceover text, on-screen text, duration, and a green compliance badge ("disclaimer included", "no outcome guarantee"). Inline-edit any text; a live meter labeled **"Edit depth"** shows the % of generated words changed (start at 6%, tick to 8% after an edit). Buttons: "Request lawyer approval" and "Version history" — a diff view highlighting word-level changes between versions.
>
> **Lawyer flow:** the approval card renders the script scene-by-scene with a note "Based on the Practice-Area Explainer structure you selected". Buttons **Approve** / **Request change**; the change modal picks a scene + reason code (unclear wording / wrong emphasis / too formal / missing credential / other) + optional note. After a change request, switching to Producer shows a structured change card and a **"Regenerate scene 2 only"** button that re-drafts just that scene in ~3 seconds, creating a new version in the diff history. The lawyer then approves.
>
> **The centerpiece screen — "Training feed":** a navigation item showing a table of labelled example pairs auto-collected this week (original text → edited text, source: producer edit or lawyer change request, reason code, accepted/rejected label), a header stat "27 examples this week", and a gold button **"Export to LLM fine-tuning backlog"** with a small toast confirmation. Add a caption under the button: "Every edit improves the next draft — and the legal LLM."
>
> **Version toggle in the header:** "v1 manual drafting ↔ v2 Script Engine" showing a split-screen comparison card for the same order: v1 = 80 min writing, 2 rework rounds; v2 = 35 min total, 1 structured round. Footer stats bar: script work 80→35 min, labour 7h15→5h50, lead time 9→4 days, rework 55%→30%, first-pass acceptance 45%→70%, capacity 26→33 videos/month. Dev drawer listing endpoints: POST /v2/scripts/generate, GET /v2/templates/:id, GET /v2/profiles/:id, POST /v2/scripts/:id/versions, GET /v2/scripts/:id/diff, POST /v2/scripts/:id/change-requests. English throughout; every button functional; no dead ends.
