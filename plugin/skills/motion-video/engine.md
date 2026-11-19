
# Motion engine

Every film is a page that paints the exact frame for any time `t`, plus a renderer that walks time, screenshots each frame and pipes them to ffmpeg. No clock, so renders are identical every run.

## Scaffold a project

Requires Node 20+ and ffmpeg on the PATH.

```bash
cp -Rn <this skill's directory>/kit/. .
chmod +x sheets.sh
npm init -y && npm i -D puppeteer
node motion.js          # self-check, prints "motion.js ok"
node render.mjs         # renders the starter film to out/silent.mp4
```

`cp -Rn` never overwrites: if the project already has an `AGENTS.md`, append the kit's house rules to it. The kit's `CLAUDE.md` is a one-line `@AGENTS.md` import. Set `CHROME_PATH` to use an installed Chrome.

| File | Job |
|---|---|
| `index.html` | The film. `SCENES` is a list of `{ from, to, draw(t) }`; `window.seek(t)` paints second `t`. |
| `motion.js` | `spring`, `track`, `smoother`, `swapAlpha`, `rng`, `beatGrid`, `loopT`, and the `SPRING` presets. |
| `render.mjs` | Seeks the page frame by frame and pipes screenshots to ffmpeg. |
| `audio.mjs`, `beats.py` | Sound (`sound.md`). |
| `sheets.sh` | Review images (`critique.md`). |
| `AGENTS.md` (+ `CLAUDE.md` shim) | House rules for every film in the project. |

## The contract

1. `window.seek(t)` paints the frame for second `t` and nothing else. No timers, CSS transitions, `requestAnimationFrame` during render, or state between frames.
2. `window.FILM = { width, height, duration }` tells the renderer what to capture.
3. Randomness from `rng(seed)`; never `Math.random` or `Date.now`.
4. One `index.html`, one canvas, no framework unless the user asks (Route B).

Verify by rendering twice and comparing hashes:

```bash
node render.mjs --fps 5 --out out/a.mp4 && node render.mjs --fps 5 --out out/b.mp4 && md5 -q out/a.mp4 out/b.mp4
```

## Writing scenes

- One `SCENES` object per shot; `draw(t)` gets time since scene start.
- Lay out with `U` (1/1080 of the short side), `CX`, `CY`, never pixel constants, so formats reframe instead of crop.
- One coordinate system per scene; wrap camera moves in `ctx.save()` / `ctx.restore()`.
- Draw text at final size; scaling a small bitmap blurs.

## Springs

Objects move on springs (closed-form, pure function of time); camera and full-frame moves use quintic smootherstep `smoother(p)` (springs kick at the start of a camera move).

```js
spring(t - 0.2, ...SPRING.snappy)            // 0 to 1, starting at 0.2s
track(t, [[0, 100], [1, 400], [1.6, 250]])   // a value that changes target twice
lerp(1, 1.4, smoother((t - 2) / 1.2))         // a camera zoom from 2s to 3.2s
```

- `SPRING.snappy`: buttons, toggles, leading edges. `standard`: cards, containers. `heavy`: big type, logo lockups. `playful`: mascots, stickers (visible overshoot).
- Multiple targets (cursor, container width) → `track`: one spring per change, continuous, any frame drawable alone.
- Stretching indicator: leading edge on a stiffer spring than trailing edge; draw between.
- Text in a morphing container: `swapAlpha(t, tIn, tOut)` so labels never overlap.
- Seamless loop: last frame equals first, including position and velocity. Use `loopT`; check with `sheets.sh`.

## Rendering

```bash
node render.mjs --fps 2 --out out/draft.mp4             # cheap draft, for a contact sheet
node render.mjs --from 4 --to 6 --out out/fix.mp4       # only the seconds that changed
node render.mjs --fps 60 --sub 4                        # final: 60 fps, 4 blended subframes (motion blur)
node render.mjs --format 16x9 --out out/silent-16x9.mp4
```

Render each format (`9x16`, `1x1`, `16x9`) from the same timeline, never crop; formats can render in parallel.

## Pages built with CSS keyframes

With no `seek`, `render.mjs` pauses every animation and sets its `currentTime`. Pass size and length:

```bash
node render.mjs --page teaser.html --size 1920x1080 --to 10
```

The page must keep everything on CSS or Web Animations timelines, hide preview-only chrome when `?render` is in the URL, and avoid `will-change` on anything the camera scales (blurs text).

## Route B: a framework

Only on request: **Remotion** (React) for series, templates, data-driven videos; **HyperFrames** (HTML and GSAP) for web-page thinkers. Installing their agent skills is the user's call; house rules and critique loop still apply.

## Effort

Medium for small fixes and re-renders, highest available for a new film, maximum only when the first three seconds carry a launch.
