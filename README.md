# OM-Project_Presentation_HiLegal – web version

Group 9 · Peking University HSBC Business School · Operations Management

HTML version of our presentation "Scaling HiLegal's lawyer video production". One file per slide, a viewer with an edit view and a present mode, live animations on slides 4 and 9.

## Run it

The viewer loads the slide files, so it needs a local web server. Opening `index.html` by double-click does not work; the page then only shows a hint.

**Windows: double-click `start.bat`.** It starts a small local server and opens http://localhost:8000. Close the server window to stop it.

Other options:

```bash
npx serve .
```

```bash
python -m http.server 8000
```

On Windows without Node or Python:

```bash
powershell -ExecutionPolicy Bypass -File tools/serve.ps1
```

Then open http://localhost:8000 (or the address `npx serve` prints).

## Edit view

- Left: all slides. Click one to open it.
- Centre: the slide at full size, with live animations.
- Below: slide number, **file path** (e.g. `slides/iter2.html`, "Copy path" button) and the speaker notes.
- **Live reload** is on by default: when you or an agent saves a slide file, the view updates within ~3 seconds.
- Keys: ← → or ↑ ↓ change slide, **P** starts Present mode, **R** reloads.

To change a slide, tell your agent the file path, e.g. *"In `slides/iter2.html`, shorten the evidence text. Follow STYLE.md."*

## Present mode

- Click **▶ Present** or press **P**. Opens full screen from the current slide.
- → / Space / Page Down: next · ← / Page Up: back · Home / End: first / last
- **N** shows or hides speaker notes · **Esc** exits.
- Slides marked `hidden` (the internal team-questions and review slides) are skipped.
- Direct link to present: `http://localhost:8000/?present#cover`

## Working with agents and Git

- `AGENTS.md`: rules for any coding agent (Codex, Claude, DeepSeek, …). `CLAUDE.md` points Claude Code to it.
- `STYLE.md`: colours, fonts, layout, process-map geometry, content rules.
- Pull before you edit, commit small changes per slide, push often.

## Folder structure

```
index.html        viewer
deck.json         title and slide order
slides/           one HTML file per slide
assets/           logos, hero image, group photo
animations/       full-screen animation pages (play buttons)
runtime/          viewer code (deck.js, deck.css)
tools/serve.ps1   local server for Windows
```
