# Colors

Never report a contrast value you didn't measure. Reuse the project's tokens and notation, and never add a second notation to fix one value. Whether a pair must pass is decided by [accessibility](../accessibility/index.md); surfaces and icon color belong to [polish](../polish/index.md). If you're building or auditing a palette or token system, read [palette.md](palette.md).

## Rules

- **One color, one meaning.** Hues within 15° count as the same color. If the accent means "interactive", never put it on static text, and never render an interactive element in a neutral color.
- **Use tokens only in their role.** Never borrow `--color-border` for caption text because its value happens to fit today. If a role has no token, add one. Components reference semantic tokens, never primitives like `--blue-500` or Tailwind's `bg-brand-500`.
- **One filled action per view** when fill signals the primary action; its peers stay neutral. Several colored fills are fine when they encode different states.
- **Gradients.** Use `linear-gradient(in oklab, …)` by default. The default sRGB interpolation darkens the midpoint, and opposite hues in oklab go gray, so use `in oklch shorter hue` or add a middle stop for those. Keep text off gradients, or measure contrast at the worst point.
- **P3 needs a fallback.** Declare the sRGB value first, then override inside `@media (color-gamut: p3)`. A P3 color without a fallback is HIGH.
- **Every custom color needs light, dark and `prefers-contrast: more` values.** Use one switching mechanism throughout: the media query alone, a `.dark` class once users can override the system theme, or `light-dark()` with `color-scheme` set. Mixing mechanisms is a finding.
- **Locale meaning.** In Chinese financial UIs, red means a gain and green a loss. Make gain and loss colors per-locale tokens if the product ships there.

## Contrast

Measure the foreground against the background it actually renders on, which is usually the nearest ancestor that paints one. That includes opacity, `color-mix()`, translucent `backdrop-filter` surfaces (test the lightest and darkest content behind them) and text over images (test the worst region). **Report a failing pair; don't repaint it unless asked.**

| Content | APCA min, preferred | WCAG 2 AA |
|---|---|---|
| Body text | Lc 75, 90 | 4.5:1 |
| Labels, headlines | Lc 60, 75 | 4.5:1 (3:1 at ≥24px or ≥18.5px bold) |
| Large text ≥36px | Lc 45, 60 | 3:1 |
| UI components, focus rings | Lc 30 | 3:1 |

- **APCA is the default for design decisions.** WCAG 2 is the gate when the project claims conformance.
- **Lc is signed:** compare the absolute value. Disabled and placeholder text has a floor of Lc 30.
- **Fix lightness first,** keeping hue and chroma, then measure again. A background near 75% perceived lightness caps even black text at about Lc 60, so change the background instead. Pushing lightness can leave the gamut; lower the chroma to stay in it.

**Severity:**

- **HIGH:** text is unreadable, or a semantic color is misleading.
- **MEDIUM:** a theme, token or gamut failure.
- **LOW:** polish.

Use the format in [review](../review/index.md#output).
