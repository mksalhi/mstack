# Animation audit playbook

The eight audit categories and what to hunt for. Target values live in [index.md](index.md); cite them from there and copy them exactly into findings and plans.

## 1. Purpose & frequency

Every animation needs a purpose (spatial consistency, state indication, feedback, explanation, preventing a jarring change); "looks cool" on a frequent element isn't one. Apply the frequency table in index.md step 1: tens of times/day means remove or drastically reduce.

Hunt for: animations on keyboard-initiated actions, command palettes with open/close transitions, decorative motion on constantly hit list items or hovers. The strongest fix is often deleting the animation.

## 2. Easing & duration

`ease-in` on UI is always a finding. Plans introduce the index.md custom curves as tokens matching repo conventions and hold durations to its table (UI ≤300ms unless an exemption is named).

Hunt for: `ease-in`, bare `ease`/`linear` on entrances, UI durations >300ms, delay plus animation on every tooltip in a toolbar (after the first they should be instant).

## 3. Physicality & origin

Hunt for: `scale(0)`, pure-fade entrances with no initial transform, `transform-origin: center` (or none) on trigger-anchored elements (target `var(--transform-origin)`), pressable elements with no press feedback. Modals are exempt from origin; don't report `center` there.

## 4. Interruptibility

Rapid or reversible motion (stacking toasts, toggles, drags, expand/collapse) must use transitions or springs, not keyframes. Entry without JS: `@starting-style` (fallback: `data-mounted` set in `useEffect`). Gestures use springs (index.md configs, including the icon-swap exception). Symmetric timing on press-and-release is a finding; deliberate phases are slower, responses snap.

Hunt for: `@keyframes` on toasts/toggles, gesture handlers tweening fixed-duration keyframes, drags without velocity dismissal (`Math.abs(distance)/elapsedMs > ~0.11`), hard stops at drag boundaries instead of rising friction.

## 5. Performance

`transition: all` is always a finding. Target for Motion shorthands: `animate={{ transform: "translateX(100px)" }}`. Use CSS/WAAPI for predetermined motion, JS/springs for dynamic and gesture motion.

Hunt for: `transition: all`, animated `width`/`height`/`margin`/`padding`/`top`/`left`, Motion `x`/`y`/`scale` on busy pages, `setProperty('--x', …)` driving child transforms, rAF loops doing what CSS could, transition blur ≥20px.

## 6. Accessibility

Target: index.md step 7 (opt-in movement, `useReducedMotion()`; fewer and gentler, not zero) and the hover query in the [mobile-web area](../mobile-web.md#1-hover-state-stuck-after-tap). Movement with no reduced-motion handling is **HIGH**.

Hunt for: movement with no `prefers-reduced-motion` handling, ungated `:hover` motion, reduced-motion implementations that remove all feedback, state changes shown only by motion.

## 7. Cohesion & tokens

Hunt for: motion personality mismatched across components (one bouncy component in a crisp dashboard), near-identical hand-typed easings/durations that should be one token, all-at-once group entrances where index.md stagger belongs (stagger never blocks interaction), double-exposing crossfades (mask with `filter: blur(2px)` during the transition).

## 8. Missed opportunities

Places that should animate: teleporting state changes and layout jumps, trigger-spawned panels with no spatial motion, rare high-emotion moments (first-run, success) with no delight. Tools: `translateY(100%)` percentages and `clip-path: inset()` reveals, no hardcoded px. Report at most a handful, grounded in seams you observed.
