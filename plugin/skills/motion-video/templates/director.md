# Director's brief

You are the director, animator, sound designer and render engineer for a [DURATION] film made entirely in code. This is a multi-stage production; do not rush to a final render.

## The film in one line

[LOGLINE.] At the end the viewer should feel [FEELING].

## References and inputs

- `./refs/`: [video | frames | image library]. Take [palette, type, pacing]. Leave [subject, characters, logos].
- `./audio/track.wav`: [use unchanged and measure it first | none, synthesize the score].
- Skills to use: `engine.md`, `reference.md`, `sound.md`, `critique.md`[, others].
- APIs available in `.env`: [KEY_NAMES]. Budget: [AMOUNT]. Report what was spent.

## Look

[Three to five lines: palette, type, texture, camera language.]

Banned: [looks to avoid], plus the defaults in `AGENTS.md`.

## Characters

[If any: proportions, palette sampled from a reference sheet, expressions, and what must stay identical in every shot and every style.]

## Beat sheet

| Time | What happens |
|---|---|
| 0:00 to 0:02 | Hook: [the single most striking image] |
| 0:02 to 0:10 | [Act 1] |
| ... | Something new every 2 to 4 seconds |
| [END] | The last frame sets up the first, so it loops |

## Text on screen

[When words fill the frame, when they sit as captions, and where the composition leaves room for them.]

## Workflow, with gates

1. **Plan.** Write `docs/style_guide.md` and `docs/shotlist.md`: every shot with its time range, camera, text and sound. Show the shot list. [Wait for approval | If there is no answer after [10] minutes, continue.]
2. **Stills.** Build one still per shot. Make a contact sheet and critique it.
3. **Animatic.** Render at 960x540 with placeholder sound. Fix pacing here, before any polish.
4. **Full pass.** Animate every shot. Then a polish pass, a sound pass, and the final render.
5. **Subagents.** For chapters, write `docs/ANIMATION_GUIDE.md` first so every subagent shares the style, then one chapter per subagent. Write `docs/STORYBOARD.md` after the first pass.

Do not skip a gate.

## Critique loop

Per shot, at least three rounds: render three to five stills, score 1 to 10 on hook, readability at 360 px wide, motion, composition, depth, sound sync and polish. Log the scores and the three biggest problems in `docs/review_log.md`. Fix them. Repeat until every score is 8 or higher.

## Deliverables

- `out/final.mp4`
- `out/loop_check.mp4`
- `out/poster.png`
- `out/contact.png`
- `README.md` describing how to re-render, what was spent, and what you would improve next.
