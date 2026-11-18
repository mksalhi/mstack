# Building animations

Turn a motion request into code that passes the [review area](../review/index.md) on the first try. To survey a codebase's motion and plan fixes, follow [audit-workflow.md](audit-workflow.md). Diff critique is the review area; React Native is the [animate-expo area](../animate-expo/index.md). Clip-path, gestures and drag, transforms, performance traps and debugging: [design-eng.md](design-eng.md).

This file is the single source of truth for motion values across the `ui` skill's areas (easing tokens, durations, press scale, springs, stagger, reduced motion).

## Hard rules

- Animating something that shouldn't animate is the worst failure; writing zero lines is a valid outcome. Next worst is wrong ingredients (`ease-in` entrance, `scale(0)`, keyframes on a toast, a sluggish dropdown).
- Never offer motion options as a menu. Make the call, give the reason in one line, write the code.
- Run the sequence in order. Steps 1 and 2 gate everything.
- Take every curve, duration and spring config from the tables below. Never invent one (e.g. `cubic-bezier(0.4, 0, 0.2, 1)`).
- Extend existing tokens (`--ease-out`, a duration scale). A parallel system is a defect.
- Reduced motion and hover gating ship with the animation, not as a follow-up.
- Motion never gets in the way. The element takes the next click or keypress mid-animation (iOS 11 Calculator's fading keys swallowed taps, so a fast 1+2+3 gave 24), and nothing hijacks scroll. Scroll-linked effects driven by the user's own scroll are fine.
- Cheapest tool that works. No motion library for a fade.

## The build sequence

### 1. Should this animate at all?

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette toggle) | No animation. Ever. Stop. |
| Tens of times/day (hover, list navigation) | Near-imperceptible or nothing |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, success, celebration) | Delight budget lives here |

Keyboard-initiated actions are disqualified outright (Raycast has no open/close animation). If the request fails this gate, say so, write no animation, and offer the non-motion alternative (instant state change, static affordance).

### 2. What is the purpose?

The strongest purpose is connecting states: the user's action visibly becomes its result, so the flow from A to B is explicit instead of a jump. Name one: **connecting states**, **feedback**, **spatial consistency** (keeping the user oriented), **guiding attention** to what changed, **state indication**, **preventing a jarring change**, **explanation** (marketing/onboarding only; motion can say what a static image can't, like a rotating globe that shows every region instead of picking some), **delight** (rare/first-time tier only). Can't name it? Don't build it. Data the user reads or acts on doesn't move for style (no mouse-tracking on a banking graph).

### 3. Pick the tool (stop at the first that fits)

| Need | Tool |
| --- | --- |
| Hover, press, color, class/attribute toggle | CSS transition |
| Entry on mount, no JS state | CSS `@starting-style` |
| Predetermined motion that must stay smooth while the page loads | CSS animation (off main thread) |
| Programmatic control, no library | WAAPI (`element.animate()`) |
| Springs, layout, exit, gesture-driven values | Motion (`motion.dev`) |

CSS for predetermined motion, JS for dynamic and interruptible motion. WAAPI also makes per-element randomized delays, durations or positions easy (a flickering flame, twinkling stars), which reads more natural than one shared value. It runs off the main thread only for composited properties (`transform`, `opacity`), and that depends on the browser, so profile before claiming it. If the task needs a component (toast, drawer, command menu, dropdown), use the project's library (Radix, Base UI, shadcn), not a hand-rolled `<div>`.

### 4. Pick the properties

- `transform` and `opacity` only. Never `width`/`height`/`margin`/`padding`/`top`/`left`. `clip-path` is the sanctioned fourth (RECIPES.md); `height` is tolerated only for accordions.
- Never `scale(0)`. Start from `scale(0.9–0.97)` + `opacity: 0`.
- `transform-origin` at the trigger for popovers, dropdowns, menus, tooltips (`var(--transform-origin)` in Base UI). Modals are exempt and stay centered.
- Prefer percentage `translate()` (relative to the element's own size) over hardcoded px.
- In Motion, use the full transform string; `x`/`y`/`scale` shorthands drop frames under load:

```jsx
<motion.div animate={{ transform: "translateX(100px)" }} />  // not animate={{ x: 100 }}
```

- Never drive a child's transform from a CSS variable on the parent. Set `transform` on the element.
- A property outside the list has to move (a border, an underline, a stroke): fake it with a pseudo-element and `transform` (an underline is an `::after` with `scaleX`), or draw it in SVG. CSS borders step in whole pixels; SVG interpolates sub-pixels and looks smooth at the same cost.
- Smoothness beats frame rate: a steady 30fps reads better than a 60fps animation that drops frames. If it stutters on a mid-range device, simplify or cut it.

### 5. Easing and duration, or a spring

| Situation | Easing |
| --- | --- |
| Entering or exiting (and default) | `ease-out` |
| Moving / morphing on screen | `ease-in-out` |
| Hover / color change | `ease` |
| Constant motion (marquee, progress) | `linear` |

Never `ease-in` on UI; it delays the moment the user watches. Built-in curves are too weak; use:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like drawer (Ionic) */
```

Exception: a contextual icon swap without a library cross-fades on `cubic-bezier(0.2, 0, 0, 1)` over 300ms ([RECIPES.md](RECIPES.md#icon-swap)), icon swaps only. Need another curve? Take it from [easing.dev](https://easing.dev/) or [easings.co](https://easings.co/), never hand-rolled.

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–300ms |
| Marketing / explanatory, scroll reveals | Can be longer |

Perceived speed beats measured speed: a faster animation makes the same wait feel shorter, so pick the short end of each range unless the motion needs room to read.

- UI animations stay at or under 300ms. Only exemptions: the marketing row and a toast library's own timing (Sonner: 400ms `ease`). Name the exemption where used.
- Press feedback: `scale(0.97)` on `:active`, 100–160ms, `var(--ease-out)`. Always `0.97`.
- Stagger group entrances 30–80ms per item, up to 100ms between semantic groups (title, description, actions). Stagger never blocks interaction; high-frequency interactions get none.
- Use a spring for drag with momentum, elements that should feel alive, interruptible/reversible gestures, decorative mouse-tracking. Default `{ type: "spring", duration: 0.5, bounce: 0.2 }`. Bounce 0.1–0.3; visible bounce only for drag-to-dismiss and playful interactions. Icon swaps use `{ type: "spring", duration: 0.3, bounce: 0 }`.

### 6. Interruption and exit

- Transitions, not keyframes, for anything fired rapidly (toasts, toggles); transitions retarget, keyframes restart from zero.
- Springs for gestures (they carry velocity through interruption).
- Exit the way it entered (in from the bottom, out through the bottom).
- Asymmetric timing where the user decides: slow deliberate phase (hold-to-confirm: 2s linear), snappy response (release: 200ms ease-out).

### 7. Reduced motion and pointer gating

Movement is opt-in: the base style carries only opacity and color; transform motion lives under `no-preference`.

```css
.element { transition: opacity 200ms var(--ease-out); }
@media (prefers-reduced-motion: no-preference) {
  .element { transition: opacity 200ms var(--ease-out), transform 200ms var(--ease-out); }
}
```

```jsx
const reduce = useReducedMotion();
const closedX = reduce ? 0 : '-100%';
```

Reduced motion means fewer and gentler, not zero: keep transitions that aid comprehension, remove movement and position changes. Gate hover motion with the hover query in the [mobile-web area](../mobile-web.md#1-hover-state-stuck-after-tap), including its Tailwind caveat.

## Recipes

When the request matches button press, dropdown, tooltip, modal, drawer, toast, accordion, stagger and exit, hold-to-confirm, tab indicator, scroll reveal, drag-to-dismiss, icon swap, image placeholder, coded explainer, first-render skip, or theme-switch suppression, load [RECIPES.md](RECIPES.md) and start from the recipe.

## Never ship

Self-check before finishing; each is an automatic block in the review area:

| Never | Instead |
| --- | --- |
| `transition: all` | Name the exact properties |
| `transform: scale(0)` entrance | `scale(0.9–0.97)` + `opacity: 0` |
| `ease-in` on a UI element | `ease-out` or a strong custom curve |
| Built-in `ease-out` on a deliberate animation | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Animation on a keyboard shortcut or 100+/day action | No animation |
| UI duration over 300ms with no named exemption | The duration table |
| `transform-origin: center` on a trigger-anchored popover | `var(--transform-origin)` (modals exempt) |
| Keyframes on toasts, toggles, rapidly-triggered elements | CSS transitions |
| Animating `width`/`height`/`margin`/`padding`/`top`/`left` | `transform` / `opacity` |
| Motion `x`/`y`/`scale` props under load | Full `transform` string |
| Ungated `:hover` motion | The mobile-web area's hover query |
| Movement outside a `prefers-reduced-motion: no-preference` guard | Opt-in movement; opacity and color stay |
| Everything entering at once | The stagger values |
| A state change shown only by motion | A static cue too: color, icon, or label |
| Animation that ignores or swallows input while it runs | Accept input mid-animation; retarget instead |
| Scroll hijacking | Scroll-linked effects driven by the user's scroll |

## Output

Write the code, then at most a few lines:

- **Gate result**: frequency tier and named purpose; anything rejected and why.
- **Ingredients**: tool, properties, curve, duration or spring, one line each.
- **Feel-check**: if feel can't be judged from code (crossfade, spring bounce, opacity/height balance), say so and point at the check: play at 2–5× duration or in the DevTools animation inspector, step frame by frame, test gestures on a real device, look again the next day.

No report; the code is the deliverable. When feel can't be settled from code, say so instead of guessing a value.
