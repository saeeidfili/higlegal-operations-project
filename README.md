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
- **Version** dropdown (top bar): earlier versions of the current slide from the GitHub history of the `presentation` branch. Pick one to view it (view only); "Copy restore request" copies a request for your agent to bring it back. Only pushed commits appear; needs internet.
- Keys: ← → or ↑ ↓ change slide, **P** starts Present mode, **R** reloads.

## Edit online (manual text changes)

Manual edits happen only in the online version: https://saeeidfili.github.io/higlegal-operations-project/

1. Open the slide, click **✎ Edit**. Every text on the slide gets a dashed frame; the speaker notes are editable too.
2. Change the text, then **Save to GitHub**. Each save is a commit on `presentation`, so it shows up in the Version dropdown, and everyone sees it after about 1 minute.
3. First save only: paste a GitHub token (classic, scope `public_repo`, your account needs write access to the repo). It stays in your browser.
4. In the Version dropdown, **Restore this version** brings an older version back as a new commit.

Layout, positions and colours are not editable here; ask an agent for that. If someone else saved the same slide in the meantime, the save is refused: copy your text, Cancel, wait a minute, Reload.

AI edits: work on GitHub directly (e.g. the GitHub connector in Claude) or **pull first** in your local copy, so the agent starts from the latest online edits.

To change a slide, tell your agent the file path, e.g. *"In `slides/iter2.html`, shorten the evidence text. Follow STYLE.md."*

## Present mode

- Click **▶ Present** or press **P**. Opens full screen from the current slide.
- → / Space / Page Down: next · ← / Page Up: back · Home / End: first / last
- Click the right half of the screen for next, the left half for back.
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
