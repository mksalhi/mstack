
# Motion brief

Pick the smallest brief that fits. Copy its template from `templates/` to `docs/brief.md` in the project, fill the brackets with the user, and keep it next to the film.

| The user wants | Template | Length of film |
|---|---|---|
| To test the setup, or a reel that shows off technique | `templates/showreel.md` | 10 to 60 s |
| A launch or product video | `templates/product.md` | 15 to 40 s |
| A UI film where one element morphs through the product | `templates/state-list.md` | 15 to 30 s |
| A long piece: a story, a music video, an overnight run | `templates/director.md` | 1 to 5 min |

## What a brief needs

- **A genre with known rules** ("a launch film" beats adjectives).
- **A length.** 15 s fits six to eight shots in one pass.
- **A reference.** See `reference.md`.
- **States, not vibes:** what is on screen at each beat ("the button becomes the loader at beat 3", not "feel premium").
- **Bans.** Defaults are in the house rules.
- **A gate:** shot list before code.

A showreel has no idea in it: use it once to prove the setup, then write a real brief.

## The director's brief

For a long film, the brief casts the model as the crew and gives the film in one line, what it may use and spend, and its gates:

- **Logline**, plus what the viewer should feel at the end. Check every decision against it.
- **References and inputs:** what to keep, what to push.
- **Tools, keys and budget:** skills to load, APIs in `.env`, spending limit.
- **Character bible**, if any: proportions, palette, expressions, what stays fixed through every style change.
- **Beat sheet** with timestamps: hook in the first 2 s, something new every 2 to 4 s.
- **Text on screen:** when words go huge vs sit as captions, with room left in the composition.
- **Gates:** plan, rig, stills, animatic, full pass, polish, sound, render. None skipped.
- **Critique loop:** `critique.md`.
- **Deliverables**.

Long-film patterns:

- **Subagents per chapter.** Write `docs/ANIMATION_GUIDE.md` first so every subagent shares the style, `docs/STORYBOARD.md` after the first pass, then split chapters.
- **Generate, then trace.** A video model renders base shots (physics, character motion), then the film is redrawn in code on top so only the code layer is seen. Needs a user-provided video API key and budget.

For an unattended run, say so in the brief: show the shot list, then continue if there is no answer after a stated time.

## Keys

Keys go in `.env`; the brief names the variable ("the voice key is `ELEVENLABS_API_KEY` in `.env`"). Never write a real key into a brief.
