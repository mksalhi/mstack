# Colors

- Never report a contrast value you didn’t measure.
- Reuse the project’s tokens and notation; never add a second notation.
- Pass criteria: [accessibility](../accessibility/index.md). Surfaces and icon color: [polish](../polish/index.md). For palettes/tokens: [palette.md](palette.md).

## Rules
- One color, one meaning. Hues within 15° are the same. If the accent means “interactive,” don’t use it on static text; don’t render interactive elements neutral.
- Use tokens only in their role. Don’t borrow `--color-border` for text. If a role lacks a token, add one. Components reference semantic tokens, never primitives like `--blue-500` or `bg-brand-500`.
- One filled primary action per view when fill signals primacy; peers stay neutral. Multiple colored fills only to encode states.
- Gradients: use `linear-gradient(in oklab, …)` by default. sRGB darkens midpoints; opposite hues in oklab go gray—use `in oklch shorter hue` or add a middle stop. Keep text off gradients, or measure contrast at the worst point.
- P3 needs a fallback: declare the sRGB value first, then override inside `@media (color-gamut: p3)`. A P3 color without a fallback is HIGH.
- Every custom color needs light, dark and `prefers-contrast: more` values. Use one switching mechanism: the media query, a `.dark` class (once users can override), or `light-dark()` with `color-scheme`. Don’t mix.
- Locale: in Chinese financial UIs, red = gain, green = loss. Use per-locale tokens.

## Contrast
- Measure against the actual painted background (opacity, `color-mix()`, translucent `backdrop-filter` extremes, images’ worst region). Report the failing pair; don’t repaint unless asked.
- APCA drives design; WCAG 2 gates conformance.
  - Body: Lc 75 (90 preferred); WCAG 4.5:1
  - Labels/headlines: Lc 60 (75 preferred); WCAG 4.5:1 (3:1 at ≥24px or ≥18.5px bold)
  - Large ≥36px: Lc 45 (60 preferred); WCAG 3:1
  - UI/focus: Lc 30; WCAG 3:1
- Lc is signed: compare absolute value. Disabled/placeholder floor: Lc 30.
- Fix lightness first; very light backgrounds can cap contrast—change the background. If out of gamut, reduce chroma.

Use the format in [review](../review/index.md#output).
