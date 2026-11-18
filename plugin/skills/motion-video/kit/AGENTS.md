# Motion house rules

For every film in this project.

## Render contract

- A film is a pure function of time. `window.seek(t)` paints the exact frame for second `t`, and `window.FILM` gives `{ width, height, duration }`.
- In render mode there are no CSS transitions, no `setTimeout`, no `requestAnimationFrame`, and no state carried from one frame to the next.
- Randomness comes from `rng(seed)` in `motion.js`. `Math.random` and `Date.now` are banned.
- Objects move on springs (`spring()`, `track()` in `motion.js`); camera and full-frame moves use quintic smootherstep (`smoother()`). UI gets a tiny overshoot at most, type none.
- Render with `node render.mjs`. Output is H.264, yuv420p, CRF 16.
- Lay out in format units (`U`, `CX`, `CY`), never fixed pixels, so 9:16, 1:1 and 16:9 share one timeline.

## Look

- Banned defaults: a centered title on a gradient, everything fading in, labels in the corners, borders around the frame, glow on UI chrome, generic particle bursts.
- One display typeface and one UI typeface. One accent colour unless the brief says otherwise.
- Something new every 2 to 4 seconds; the first 2 seconds carry the hook.
- Real product UI is captured, cropped and animated. Never draw a screen from imagination.

## Sound

- Music and effects are synthesized in code (`audio.mjs`) unless a track is supplied.
- Measure a supplied track first (`beats.py`): cuts and state changes on beats, big moments on downbeats, effects on hits.
- Normalize the final mix to −14 LUFS for a social reel and −16 LUFS for a web, help-center or product film (the rule in mstack's motion-video skill, `sound.md`).

## Look before you show

1. Render a draft (`node render.mjs --fps 2 --out out/draft.mp4`), run `./sheets.sh out/draft.mp4`, and open the images.
2. Score 1 to 10: hook in the first 2 seconds, readability at phone size, motion quality, variety, composition, brand accuracy, sound sync.
3. Fix the three worst problems. Repeat until every score is 8 or higher, for at least three rounds.
4. Only then render in full.

## Secrets

- API keys live in `.env` and are referred to by variable name. Never paste a key into a prompt, a file that gets committed, or a frame.
