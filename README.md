# OM-Project_Presentation_HiLegal – web version

Group 9 | Peking University HSBC Business School | Operations Management

HTML version of our presentation "Scaling HiLegal's lawyer video production". One file per slide, a viewer with a slide preview and a present mode, live animations on the current-process and final-iteration slides.

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

## Slide preview

- Left: all slides. Click one to open it.
- Centre: the slide at full size, with live animations.
- Below: slide number, **file path** (e.g. `slides/iter2.html`, "Copy path" button) and the speaker notes.
- **Live reload** is on by default: when you or an agent saves a slide file, the view updates within ~3 seconds.
- **Version** dropdown (top bar): earlier versions of the current slide from the GitHub history of the `presentation` branch. Pick one to inspect it (view only). Only pushed commits appear; needs internet.
- Keys: ← → or ↑ ↓ change slide, **P** starts Present mode, **R** reloads.

## Changing slides

Ask your coding agent to update the relevant slide file and push the change to the `presentation` branch. For example: "In `slides/iter2.html`, shorten the evidence text. Follow STYLE.md."

The browser viewer displays slides, notes and earlier versions. Changes are made through Git. Always fetch or pull the latest branch before editing because team members may also update the files.

## Present mode

- Click **▶ Present** or press **P**. Opens full screen from the current slide.
- → / Space / Page Down: next | ← / Page Up: back | Home / End: first / last
- Click the right half of the screen for next, the left half for back.

## Presenter notes (several devices, synced)

`presenter.html` shows the notes of the current slide, ◀ ▶ buttons and a shared timer (Start / Pause / Reset, 15:00 budget, ahead/behind from each slide's TIME). Every device in the same room sees the same slide and the same time.

1. Click **Presenter notes** in the top bar. The page creates a room (code in the header).
2. **Copy link for others** and send it to the team; any number of phones or laptops can join.
3. **Open on projector** opens Present mode in the same room: the projector follows the ◀ ▶ buttons, and its own keys or clicks move everyone else.

Sync runs through the public relay ntfy.sh (only slide id and timer state; anyone with the room code can join). Needs internet.
- **N** shows or hides speaker notes | **Esc** exits.
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

### Preview controls

- Scroll over the slide preview to move between slides. The sidebar and notes scroll independently.
- Use the panel icons beside **Notes** to show speaker notes below or on the right. The chevron collapses or reopens them; **N** does the same.
- The browser remembers the notes position and whether the panel is collapsed.
