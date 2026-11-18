---
name: motion-video
description: "Use for any video rendered from code (launch film, product reel, explainer, motion ad) or one stage of one: brief, render engine, sound, frame critique."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
  requires: "Node 20+, ffmpeg, headless Chrome"
---

# Motion video

Each step names the file in this directory with the detail; read it at that step. For one stage alone (janky render, scoring a draft, adding sound), go straight to that file.

## Inputs

Ask once, in one message; default anything unanswered:

- Subject: product and URL, or the announcement in one line.
- Duration (default 15–20 s) and formats (default 9:16; 1:1 and 16:9 on request).
- Brand colours and fonts, or permission to read them from the site.
- A reference: frame, video, or image folder.
- Music: a file, or "synthesize".
- On-screen words: headline and call to action. If you write them, say they are placeholders.

## Pipeline

1. **Engine.** No `render.mjs`? Scaffold with `engine.md`; run the starter render once.
2. **Assets and reference.** With `reference.md`, gather real assets from the URL into `./assets` and list them. With a reference, write `docs/style_guide.md`.
3. **Beat grid.** With `sound.md`, measure the track into `beats.json`, or pick a tempo and use `beatGrid()`.
4. **Brief and shot list.** With `brief.md`, fill the matching template into `docs/brief.md` and write `docs/shotlist.md` on the beat grid. **Show the shot list and wait for a yes.**
5. **Build.** Scenes in `index.html` against `window.seek(t)`, springs from `motion.js`, house rules in `AGENTS.md`.
6. **Draft and critique.** Render a draft, make sheets, run `critique.md`: at least three rounds, until every score is 8+.
7. **Sound.** `cues.json` from the final shot list, run `audio.mjs`, verify timing by measurement.
8. **Final render.** `node render.mjs --fps 60 --sub 4` per format, mix into `out/final.mp4` at −14 LUFS (social reel; −16 for web or help-center), per `sound.md`.
9. **Deliver.** `out/final.mp4` per format, `out/contact.png`, a poster frame, and a note: what was verified, what was not (the mix has not been heard), what to improve next.

## Hard rules

- Real product UI only. Never invent a screen.
- No `Math.random`, no timers and no CSS transitions in render mode.
- No centered title on a gradient, no everything-fades-in, no corner labels.
- Never show the user a film whose frames you have not looked at.
- End on the held final frame. A loop-restart fade-out belongs to the looping preview, not the MP4.

## Notes

- A page already animated with CSS keyframes renders as is: "Pages built with CSS keyframes" in `engine.md`.
- One project folder per brand; later films reuse assets, style guide, engine and voices ("another one for [FEATURE], 15 seconds, vertical, same look").
