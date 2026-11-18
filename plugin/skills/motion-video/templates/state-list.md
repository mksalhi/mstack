# State-list brief: one shape, never cut

## Inputs to collect first

- The product and its URL.
- 8 to 12 UI states that tell its story, in order.
- The real data shown in each state.
- Brand colours, fonts, and one accent.
- Music: a royalty-free track near 120 BPM, or "synthesize".
- Formats.

## Direction

One container stays on screen and never cuts: each state is the same element changing size, corner radius and fill while content swaps behind a short blur. A cursor causes every change with a visible action.

Neutral warm background, one accent. Springs with a tiny overshoot at most.

Banned: bouncy easing, glows, gradients on UI chrome, particle bursts, any beat where nothing happens.

## Structure

[120] BPM, [8] bars, and something changes on every beat.

[logo] → [call-to-action button] → [email field, typed] → [loader] → [success check] → [dashboard card] → [chart draws itself] → [tooltip on hover] → [command palette] → [toast] → [logo]

## Build rules

1. One HTML file, one canvas, `window.seek(t)`. No CSS transitions, no timers, no state between frames.
2. Closed-form springs from `motion.js`. Any value with several targets uses `track()`.
3. Text inside the container uses `swapAlpha()`: in after the morph starts, out before the next one.
4. A moving indicator stretches: its leading edge is on a stiffer spring than its trailing edge.
5. The beat grid comes from the track (`beats.py`) or from `beatGrid()`. Start on a downbeat. UI sounds land on beats.
6. Final render at 60 fps with 4 blended subframes.

## Gotchas

- Draw text at its final size. Scaling a small text bitmap up makes it blurry.
- The last frame must equal the first, including the cursor's position and velocity.
- The cursor moves on its own `track()`, arrives before each click, and never teleports.

## Gate

Collect the inputs, then show the state list laid out on the beat grid. Write code only after the user agrees to it.
