
# Motion critique

Needs `sheets.sh` from the kit; if missing, run `engine.md` first.

## 1. Make the sheets

```bash
./sheets.sh out/final.mp4          # contact.png, phone.png, loop_check.mp4
./sheets.sh out/final.mp4 4.1      # plus strip.png: 12 consecutive frames from 4.1s
```

Draft first: `node render.mjs --fps 2 --out out/draft.mp4` then `./sheets.sh out/draft.mp4`.

- `contact.png`: whole film at 2 fps.
- `phone.png`: the film at 360 px wide.
- `strip.png`: one fast action frame by frame. Make one for every fast morph, swap and cut.
- `loop_check.mp4`: plays twice to expose the seam.

## 2. Look, as a harsh director

Open every image. Judge what is on screen, not what the code intended.

For an unanchored read, spawn the `motion-critic` agent with only the sheet paths and the brief (Codex has no plugin agents: run a fresh session given only the sheets and the text of `agents/motion-critic.md`).

Score 1 to 10:

| Criterion | An 8 means |
|---|---|
| Hook | The first 2 seconds show the single most striking image. |
| Readability | Every word is legible in `phone.png`. |
| Motion | Objects move on springs with mass; camera and full-frame moves use quintic smootherstep. No linear slides, no dead frames. |
| Variety | Something new every 2 to 4 seconds. |
| Composition | Clear focus in each shot, with depth and room for text. |
| Brand accuracy | Real UI, logo, colours and type. Nothing invented. |
| Sound sync | Every hit lands on its visible event. |

Hunt specifically for:

- Text overlapping text during a swap.
- Anything sliding at constant speed.
- Corner labels or a frame border.
- A centered title on a gradient, or everything fading in.
- Blurry scaled text.
- A beat where nothing happens.
- A stutter or jump at the loop seam.
- One scene's elements visible in the next.

## 3. Log, fix, re-render

Write scores and the three biggest problems, with timestamps, to `docs/review_log.md`. Fix those three. Re-render only changed seconds (`node render.mjs --from 4 --to 6 --out out/fix.mp4`), remake sheets, rescore.

## 4. Stop rule

After the last round, do the full render and show the user the final contact sheet and scores.
