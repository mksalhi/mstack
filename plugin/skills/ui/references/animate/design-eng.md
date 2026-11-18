# Design engineering reference

Techniques [index.md](index.md) and [RECIPES.md](RECIPES.md) don't cover. Values and the reduced-motion pattern stay in index.md; nothing here overrides them. Percentage translate, `transform-origin`, Motion shorthands and parent CSS variables are in index.md step 4.

## Transforms

`rotateX()`/`rotateY()` with `transform-style: preserve-3d` give CSS-only depth (orbits, coin flips, card turns):

```css
.wrapper { transform-style: preserve-3d; }
@keyframes orbit {
  from { transform: translate(-50%, -50%) rotateY(0deg) translateZ(72px) rotateY(360deg); }
  to   { transform: translate(-50%, -50%) rotateY(360deg) translateZ(72px) rotateY(0deg); }
}
```

## clip-path

`clip-path: inset(top right bottom left)`: each value eats in from that side. `inset(0 100% 0 0)` hides from the right; `inset(0 0 0 0)` shows all.

- Tabs with exact color transitions: [RECIPES.md](RECIPES.md#tab-indicator-with-a-color-transition).
- Hold to confirm: [RECIPES.md](RECIPES.md#hold-to-confirm).
- Comparison slider: overlay two images, clip the top with `inset(0 50% 0 0)`, drive the right inset from drag position.

## Spring-driven pointer tracking

For decoration only, interpolate pointer-driven values through `useSpring` with the default spring; on a graph the user reads, track directly or not at all.

```jsx
const rotation = useSpring(mouseX * 0.1, { duration: 0.5, bounce: 0.2 });
```

## Gestures and drag

- Dismiss on velocity or distance: `Math.abs(swipeAmount) / elapsed > 0.11 || Math.abs(swipeAmount) >= SWIPE_THRESHOLD`.
- Past a natural boundary, follow with rising resistance, not a hard stop.
- `setPointerCapture` once the drag starts.
- Ignore new touch points once dragging (`if (isDragging) return`).

## Performance traps

- Name transitioned properties: `transition-property: scale, opacity`, Tailwind `transition-[scale,opacity,filter]`. Tailwind `transition-transform` maps to `transform, translate, scale, rotate`; use it when only transforms move.
- A shared-layout tab indicator that stutters during navigation: move it to a CSS animation.
- `will-change` only for `transform`, `opacity`, `filter`, and only after you see a first-frame stutter (Safari benefits most). Never `will-change: all` or on every animated element. `clip-path` rarely earns it.
- Transition-time `filter: blur()` under 20px.

## Debugging

- Play at 2–5x duration or slow the Animations panel. Watch for two overlapping color states, abrupt easing start/stop, wrong scale origin, opacity/transform/color out of sync.
- Step frame by frame in the Chrome DevTools Animations panel.
- Look again the next day. Opacity paired with height in an entering list has no formula; tune by feel, recheck tomorrow.
- Test touch on a physical phone: dev server on the LAN, open by IP, debug with Safari Web Inspector or `chrome://inspect`. The Xcode Simulator misses touch feel.
