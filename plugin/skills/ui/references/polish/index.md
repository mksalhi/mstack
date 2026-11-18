# Polish

Keep the project's components, tokens and density; use the values here only where the project has none. Motion belongs to [animate](../animate/index.md), text to [typography](../typography/index.md), focus and hit areas to [accessibility](../accessibility/index.md), and spacing to [layout](../layout/index.md).

## Surfaces

- **Concentric radius.** Outer radius equals inner radius plus padding: `rounded-2xl p-2` wraps `rounded-lg`. Past 24px of padding, or with uneven insets, choose each radius on its own.
- **Shadows for depth, borders for structure.** A border that exists only for depth on a card, button or popover becomes a ring shadow that adapts to any background:

  ```css
  --shadow-border: 0 0 0 1px oklch(0 0 0 / .06), 0 1px 2px -1px oklch(0 0 0 / .06), 0 2px 4px oklch(0 0 0 / .04);
  /* dark */ --shadow-border: 0 0 0 1px oklch(1 0 0 / .08);
  ```

  Keep real borders for dividers, table cells, input outlines and selected or focus states.
- **Image outline.** Use `outline: 1px solid oklch(0 0 0 / .1); outline-offset: -1px`, with `oklch(1 0 0 / .1)` in dark mode (Tailwind `outline-black/10 dark:outline-white/10`). Never a tinted neutral like slate or zinc, and never `border`, which shifts layout.
- **Optical alignment.**
  - In a button with an icon, the padding on the icon side is 2px less than on the text side (`ps-4 pe-3.5`).
  - Nudge a play triangle about 2px right.
  - Fix an asymmetric glyph in its viewBox before reaching for a translate.

## Icons

- **Stroke follows the adjacent text weight** on a 24px grid: 1.5px next to 400, 2px next to 500 to 600, 2.5px next to 700. Use one library per surface. If a set has no stroke variants, keep its native stroke.
- **One SVG with `currentColor`.** Hover, pressed and disabled states come from CSS color and opacity. Strip hardcoded fills on import.
- **Outline by default, fill for the active state** (the active tab, a toggled bookmark), never used interchangeably. Animating the swap belongs to [animate](../animate/RECIPES.md).
- **Check every icon at its smallest render size**, using the set's native grid (16, 20, 24). Always SVG.
- **RTL:**
  - **Flip** (`rtl:-scale-x-100`): navigation arrows and chevrons, text-alignment glyphs, volume waves, send.
  - **Don't flip:** logos, checkmarks, clocks and other physical objects, media playback.

**Severity:**

- **HIGH:** hides a control's state.
- **MEDIUM:** inconsistent radii or icons across a set.
- **LOW:** isolated polish.

Check every defined state in both themes. Use the format in [review](../review/index.md#output).
