# Building animations

Source of motion values for ui. Open [RECIPES.md](RECIPES.md) when building a dropdown, tooltip, toast, accordion, stagger, drag-to-dismiss, icon swap, theme switch or tab indicator. Open [audit.md](audit.md) when asked to audit a codebase's motion; an audit never edits source and writes only plans. For React Native, open [animate-expo](../animate-expo/index.md) instead.

Animating something that shouldn’t move is the worst failure; zero lines is valid. Take values here, extend tokens, and ship reduced-motion + hover gating in the same change. Motion must never block input; never hijack scroll.

## 1. Should it animate?
- 100+ times/day or keyboard-triggered: never animate
- Tens/day (hover, list nav): near-imperceptible or none
- Occasional (modals, drawers, toasts): standard
- Rare/first-time: delight
- Name the purpose (connect states, feedback, orient, point at change, explain). If none, don’t build. Content users read never moves.

## 2. Tool (stop at first that fits)
1) CSS transition. 2) @starting-style. 3) CSS animation (must stay smooth pre-hydration). 4) WAAPI element.animate(). 5) Motion (springs, layout, exits, gestures). Use the component library for toast/drawer/dropdown/command menu.

## 3. Properties
- Animate transform and opacity; height only for accordions.
- Borders/underlines via ::after scaleX or SVG.
- Never start from scale(0); start 0.9–0.97 with opacity: 0.
- Anchored surfaces use transform-origin: var(--transform-origin); modals stay centered.
- Prefer percentage translate.
- In Motion, write animate={{ transform: "translateX(100px)" }}; avoid x/y/scale shorthands under load.
- Don’t drive a child’s transform from a parent CSS var.
- Name transitioned properties (never all).
- will-change only on transform/opacity/filter, and only after a first-frame stutter.

## 4. Easing and duration
```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* enter, exit, default */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* moving on screen */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS-like sheet */
```
- Curves: ease for hover/color; linear for constant/progress. Never ease-in on UI; avoid the built-in ease-out for deliberate motion.
- Durations: press 100–160ms; tooltip 125–200ms; dropdown 150–250ms; modal/drawer 200–300ms. UI ≤300ms (exemptions: marketing; Sonner 400ms ease).
- Press: scale(0.97) on :active.
- Stagger: 30–80ms per item; 100ms between groups; never blocks input.
- Springs for gestures/momentum/interruptible: { type: "spring", duration: 0.5, bounce: 0.2 } (bounce 0.1–0.3). Icon swaps: duration: 0.3, bounce: 0.

## 5. Interruption
- Rapid fires (toasts, toggles): transitions retarget; keyframes restart.
- Gestures carry velocity via springs.
- Exit mirrors enter.
- Make deliberate slow, response fast (e.g., hold 2s linear; release 200ms ease-out).

## 6. Reduced motion and hover
- Movement is opt-in: base transitions only opacity/color; transforms inside @media (prefers-reduced-motion: no-preference). In JS, check useReducedMotion().
- Reduced means gentler, not none; keep opacity feedback.
- Gate hover motion behind `@media (hover: hover) and (pointer: fine)`.

## Never ship
- transition: all
- scale(0)
- ease-in
- Built-in ease-out on deliberate UI
- Animation on a keyboard action
- UI motion >300ms without named exemption
- Centered origin on a popover
- Keyframes on toasts/toggles
- Animating layout properties
- Motion’s x, y or scale under load
- Ungated :hover motion
- Movement outside reduced-motion guard
- Everything entering at once
- State shown only by motion
- Animation that swallows input
- Scroll hijacking

## Output and feel
After code, add ≤3 lines: frequency tier + purpose; ingredients (tool, properties, curve, duration); any feel check. To check feel: play at 2–5× speed or scrub frames; test gestures on a real phone.
