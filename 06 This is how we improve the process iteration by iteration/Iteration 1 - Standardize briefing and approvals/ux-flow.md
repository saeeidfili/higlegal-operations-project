# Iteration 1 — UX flow for the software demo

**Product name:** HiLegal Studio v1 — Intake & Approvals
**Demo goal:** show a lawyer requesting a video with zero back-and-forth, and a producer picking up a complete, validated brief with SLA-capped approvals — the intake queue and clarification loop visibly gone.
**Roles in the demo:** Lawyer (client) · Producer (HiLegal staff) · System (automations, timers, notifications)

---

## Screen inventory

| # | Screen | Role | What it shows / does |
|---|---|---|---|
| 1 | Login / role switcher | both | Tabs: "I'm a Lawyer" / "I'm a Producer" (demo convenience) |
| 2 | Dashboard (Lawyer) | Lawyer | "Your videos" list with status chips + SLA countdown badges; "Request a video" CTA |
| 3 | Format catalogue | Lawyer | 5 format cards — Lawyer Intro · Practice-Area Explainer · Client Testimonial · FAQ · Case Study — each with a 30 s animated preview, typical length, best-for note |
| 4 | Structured brief form | Lawyer | 12 fields, ~9 pre-filled from profile (greyed "from your profile"), format pre-selected from card choice; tone slider (formal ↔ approachable), language multi-select, deadline picker with earliest-date hint |
| 5 | Instant completeness check | Lawyer | On submit: green "Brief complete — routed to production" or red list of the 2–3 missing fields (bounce happens in seconds, not days) |
| 6 | Order tracker (Lawyer) | Lawyer | Horizontal stepper: Submitted ✓ → Brief confirmed ✓ → Script in progress → **Script approval (waiting on you, 31 h left)** → Production → Final approval → Delivered; reminder bell |
| 7 | Approval link (mobile-style) | Lawyer | Card with the draft script rendered scene-by-scene; two buttons: **Approve** / **Request change**; change modal = pick scene + reason-code dropdown (unclear wording · wrong emphasis · too formal · missing credential · other) + optional note |
| 8 | Producer queue | Producer | All active orders as cards sorted by SLA risk (amber < 24 h left, red breached); each card: lawyer, format, countdown, stage |
| 9 | Order detail (Producer) | Producer | Brief JSON view (the structured data), timeline of every state transition with timestamps, audit trail of change requests |
| 10 | Dashboard (Producer/Manager) | Producer | KPI tiles: videos in flight, median lead time, SLA compliance %, rework loops this week; mini bar chart "wait vs work" |
| 11 | Before/after toggle | both | A switch that replays the same request through the OLD flow (email → 3–7 day queue → clarification emails → …) for contrast — the money shot of the demo |

## Demo click-path (≈ 2 minutes)

1. Lawyer dashboard → "Request a video"
2. Format catalogue → play the "Practice-Area Explainer" preview → choose it
3. Brief form → only 3 fields to fill (objective, key messages, deadline) — rest auto-filled → submit → **instant green confirmation with routing**
4. Cut to Producer → the order appears at the top of the queue with the full Brief JSON — no clarification tab needed
5. Producer marks "Script ready" → cut to Lawyer: phone-style approval link with **31 h SLA countdown** → click "Request change" on scene 2 → pick reason "wrong emphasis" → note → submit → Producer instantly sees a structured change card (not an email) → resolves → Lawyer approves
6. Order tracker animates to "Delivered" — total elapsed shown: **8 days** (vs. baseline overlay: 21)
7. Before/after toggle: replay in the old flow, watch the days burn in the intake queue animation

## Data the demo must be seeded with (use exactly these — consistent with `05 .../kpi-data.md`)

- Lawyer: "Mei Chen — Corporate Law, cross-border M&A, EN/中文" (profile: 14 years, PwC alumni, 3 jurisdictions)
- Baseline ghost stats for the before/after toggle: intake queue 3–7 days · brief loop ≥4 iterations · lead time 14–28 days · rework ~90%
- Iteration-1 stats: lead time target 7–12 days · SLA 48 h/gate · reminders 24 h/40 h · QAR target ~45%
- One order already "Delivered" in 8 days, one "In production", one "Waiting on lawyer — 31 h left"

## API surface the UI exercises (show in a dev drawer in the demo)

`GET /v1/templates` · `GET /v1/profiles/{lawyerId}` · `POST /v1/requests` · `GET /v1/requests/{id}` (state machine) · `POST /v1/requests/{id}/approval` (approve / structured change request) · `POST /v1/reminders` · webhooks `request.submitted`, `sla.breach`

---

## PASTE THIS INTO YOUR DEMO AI

> Build a single-file clickable web prototype (HTML+Tailwind or React, no backend, all data mocked in JS) called **"HiLegal Studio — Intake & Approvals (v1)"**. It demonstrates a standardized video-request workflow for a legal-tech platform. Professional SaaS look: white background, deep-navy primary (#0F2A43), gold accent (#C9A227), Inter font, rounded cards, subtle shadows. Two roles via a top tab switcher: **Lawyer** and **Producer**.
>
> **Lawyer side:** (1) Dashboard "Your videos" with 3 seeded orders showing status chips and SLA countdown badges, and a primary button "Request a video". (2) A format catalogue screen with 5 cards — Lawyer Intro, Practice-Area Explainer, Client Testimonial, FAQ, Case Study — each with a fake 30-second animated preview (CSS/emoji placeholder fine), typical length, and "best for" text. (3) Clicking a card opens a 12-field structured brief form where 9 fields are pre-filled and greyed with the label "from your profile" (practice areas, languages, credentials, photo, avatar consent, tone, contact, format, length) and only 3 are editable (objective textarea, key messages, deadline picker with an earliest-date hint). Submitting runs a visible 1-second "completeness check" animation, then shows a success screen: "Brief complete — routed to production, no queue" with the order appearing in the lawyer's tracker as a horizontal stepper: Submitted ✓ → Brief confirmed ✓ → Script in progress → Script approval → Production → Final approval → Delivered.
>
> **Approval interaction:** from the lawyer dashboard, an order sits at "Script approval — waiting on you, 31 h left" with a badge. Opening it shows a script rendered as scene cards (Scene 1 Hook, Scene 2 Credentials, Scene 3 Practice focus, Scene 4 Call-to-action) and two big buttons: **Approve** and **Request change**. Request change opens a modal: select scene, reason-code dropdown (unclear wording / wrong emphasis / too formal / missing credential / other), optional note. After submitting, switching to the Producer role shows this change as a structured card — not an email.
>
> **Producer side:** (1) A queue of active order cards sorted by SLA risk with amber (<24 h) and red (breached) states. (2) An order detail page showing the brief as clean structured JSON, a vertical timeline of every state transition with timestamps, and the change-request audit trail. (3) A KPI dashboard: tiles for videos in flight, median lead time, SLA compliance %, rework loops this week; and a stacked bar "wait vs work minutes".
>
> **The centerpiece:** a global toggle in the header labeled "Old process ↔ HiLegal Studio". In "Old process" mode, replaying a request shows a mock animation of the legacy flow: request email sits in an intake queue with a day-counter rapidly counting 3–7 days, then 4 rounds of clarification emails, then a 21-day total lead-time readout with ~90% rework likelihood. In "HiLegal Studio" mode the same request completes with 0 clarifications and an 8-day delivery. Show a comparison summary card at the end: lead time 21 d → 9 d, rework 90% → 55%, first-pass acceptance 10% → 45%.
>
> Seed data: lawyer "Mei Chen — Corporate Law, EN/中文, 14 yrs, 3 jurisdictions". All numbers must match exactly: SLA 48 h per gate, reminders at 24 h and 40 h, lead-time target 7–12 days. Include a small dev drawer (footer button) listing the API endpoints the UI exercises: GET /v1/templates, GET /v1/profiles/:id, POST /v1/requests, GET /v1/requests/:id, POST /v1/requests/:id/approval, POST /v1/reminders. Everything in English. Make every button work; no dead ends.
