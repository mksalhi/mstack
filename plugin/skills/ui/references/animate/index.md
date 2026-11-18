# Building animations

This file is the only source of motion values for the whole `ui` skill. Auditing a codebase's motion goes to [audit.md](audit.md), React Native goes to [animate-expo](../animate-expo/index.md), and reviewing a diff goes to [review](../review/index.md). For a button, dropdown, tooltip, modal, drawer, toast, accordion, stagger, hold-to-confirm, tab indicator, scroll reveal, drag, icon swap, image placeholder or theme-switch request, start from [RECIPES.md](RECIPES.md).

**Animating something that shouldn't move is the worst failure, and writing zero lines is a valid answer.** Make the call yourself rather than offering a menu. Take every value from the tables here, extend the project's existing tokens, and ship reduced-motion support and hover gating in the same change. Motion must never block input: an element takes the next click mid-animation (iOS 11 Calculator's fading keys swallowed taps, so 1+2+3 gave 24), and nothing hijacks scroll.

## 1. Should it animate?

| How often it's seen | Decision |
|---|---|
| 100+ times a day, or triggered by keyboard (shortcuts, command palette) | Never animate |
| Tens of times a day (hover, list navigation) | Near-imperceptible, or nothing |
| Occasionally (modals, drawers, toasts) | Standard |
| Rarely or first-time (onboarding, success) | This is where delight goes |

Then name the purpose: connecting states, feedback, keeping the user oriented, pointing at what changed, or explanation (marketing only). If you can't name one, don't build it. Data the user reads never moves for style.

## 2. Tool

Stop at the first one that fits:

1. CSS transition: hover, press, toggling a class.
2. `@starting-style`: entry on mount.
3. CSS animation: predetermined motion that has to stay smooth while the page loads.
4. WAAPI `element.animate()`: programmatic control, or per-element random delays.
5. Motion (`motion.dev`): springs, layout, exits, gestures.

For a toast, drawer, dropdown or command menu, use the project's component library rather than a hand-rolled `<div>`.

## 3. Properties

- Animate only `transform` and `opacity`. `clip-path` is also allowed, and `height` only for accordions.
- To move a border or underline, use an `::after` with `scaleX`, or SVG. Borders step in whole pixels.
- Never start from `scale(0)`. Start from 0.9 to 0.97 with `opacity: 0`.
- Anything anchored to a trigger (popover, menu, tooltip) uses `transform-origin: var(--transform-origin)`. Modals stay centered.
- Prefer percentage `translate` over pixel values.
- In Motion, write `animate={{ transform: "translateX(100px)" }}`. The `x`, `y` and `scale` shorthands drop frames under load.
- Never drive a child's transform from a CSS variable on its parent.
- Name the transitioned properties (`transition-[scale,opacity]`); never `transition: all`.
- Use `will-change` only on `transform`, `opacity` or `filter`, and only after you've seen a first-frame stutter.
- Keep any transition-time `blur()` under 20px.
- A steady 30fps beats a 60fps that drops frames.

## 4. Easing and duration

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* enter, exit, default */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* moving on screen */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS-like sheet */
```

- **Curves.** Use plain `ease` for hover and color, and `linear` for constant motion and progress. **Never `ease-in` on UI**, and never the weaker built-in `ease-out` on a deliberate animation. Take any other curve from easing.dev, never hand-roll one.
- **Durations.** Press: 100 to 160ms. Tooltip: 125 to 200ms. Dropdown: 150 to 250ms. Modal or drawer: 200 to 300ms. Lean short.
- **UI stays at or under 300ms.** The only named exemptions are marketing motion and Sonner's 400ms `ease`.
- **Press:** `scale(0.97)` on `:active`, always 0.97.
- **Stagger:** 30 to 80ms per item, 100ms between semantic groups. Stagger never blocks input.
- **Springs** are for gestures, momentum and anything interruptible: `{ type: "spring", duration: 0.5, bounce: 0.2 }`. Keep bounce between 0.1 and 0.3; visible bounce only for drag-to-dismiss and playful moments. Icon swaps use `duration: 0.3, bounce: 0`.

## 5. Interruption

- Anything fired rapidly (toasts, toggles) uses transitions, which retarget; keyframes restart from zero.
- Gestures use springs, which carry velocity.
- Exit the way the element came in.
- Make the deliberate phase slow and the response fast: hold-to-confirm takes 2s `linear`, and release takes 200ms `ease-out`.

## 6. Reduced motion and hover

- **Movement is opt-in.** The base style transitions only opacity and color; transforms go inside `@media (prefers-reduced-motion: no-preference)`. In JS, check `useReducedMotion()`.
- **Reduced means gentler, not none.** Remove movement but keep opacity feedback.
- **Gate hover motion** with the hover query in [mobile-web](../mobile-web.md#hover-sticks-after-a-tap).

## Never ship

Each of these is an automatic block in review:

- `transition: all`
- `scale(0)`
- `ease-in`
- Built-in `ease-out` on a deliberate animation
- Animation on a keyboard action
- UI motion over 300ms with no named exemption
- A centered origin on a popover
- Keyframes on toasts or toggles
- Animating layout properties
- Motion's `x`, `y` or `scale` under load
- Ungated `:hover` motion
- Movement outside the reduced-motion guard
- Everything entering at once
- State shown only by motion
- Animation that swallows input
- Scroll hijacking

## Output and feel

Write the code, then at most three lines: the frequency tier and purpose, the ingredients (tool, properties, curve, duration), and any feel check the code can't settle. To check feel:

- Play the animation at 2 to 5 times its duration, or step through it frame by frame in DevTools' Animations panel.
- Test gestures on a real phone over the LAN; the Simulator misses touch feel.
- Look at opacity-and-height pairings again the next day. They have no formula.
