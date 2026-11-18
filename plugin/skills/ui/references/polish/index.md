# Polish

Motion: [animate](../animate/index.md); text: [typography](../typography/index.md); focus/hit: [accessibility](../accessibility/index.md); spacing: [layout](../layout/index.md).

## Surfaces

- Concentric radius: outer = inner + padding; past 24px or uneven insets, choose each radius.
- Shadows give depth; borders give structure. Depth-only borders become a ring shadow:
```css
  --shadow-border: 0 0 0 1px oklch(0 0 0 / .06), 0 1px 2px -1px oklch(0 0 0 / .06), 0 2px 4px oklch(0 0 0 / .04);
  /* dark */ --shadow-border: 0 0 0 1px oklch(1 0 0 / .08);
```
  Keep borders for dividers, tables, input outlines, focus/selected.
- Image outline: `outline: 1px solid oklch(0 0 0 / .1); outline-offset: -1px`, dark: `oklch(1 0 0 / .1)`. Never tinted neutrals; never `border`.
- Optical alignment: in icon+label buttons, icon-side padding is 2px less (`ps-4 pe-3.5`).

## Icons

- Stroke: 1.5/2/2.5px next to 400/500–600/700 (24px grid). One library per surface; if no variants, keep native.
- One SVG with `currentColor`; states via CSS color/opacity. Strip hardcoded fills.
- Outline by default; fill only when active. Animate swap in [animate](../animate/RECIPES.md).
- Size: verify at smallest (16/20/24).
- RTL: Flip (`rtl:-scale-x-100`): arrows, text-align, volume waves, send. Don’t flip: logos, checkmarks, clocks, media playback.

Check all defined states in both themes. Use the format in [review](../review/index.md#output).
