# UI polish

Keep the project's component library, tokens and density. Use the exact radius, stroke and opacity values written here.

Other areas own: motion of any kind (whether to animate, easing, duration, press scale, springs, stagger, enter/exit, icon swaps, theme-switch transitions, motion performance), the [animate area](../animate/index.md); text wrapping, font rendering, tabular numbers and text spacing, the [typography area](../typography/index.md); hit areas, focus, keyboard, ARIA and reduced motion, the [accessibility area](../accessibility/index.md); grouping, section spacing, breakpoints and spatial RTL, the [layout area](../layout/index.md).

## Rules

- **Concentric border radius.** Outer radius = inner radius + padding. Radius, shadow and outline recipes: [surfaces.md](surfaces.md).
- **Optical over geometric alignment.** When geometric centering looks off, nudge manually: buttons with icons, play triangles, asymmetric icons.
- **Shadows for elevation, borders for structure.** A border that exists only for depth becomes a layered transparent `box-shadow`. Keep borders that show structure or state: dividers, separators, selected and focus states.
- **Image outlines.** A `1px` outline at `oklch(0 0 0 / 0.1)` in light mode, `oklch(1 0 0 / 0.1)` in dark. Never a near-black (slate, zinc) or tinted neutral.
- **Icon stroke matches text weight.** `1.5px` beside regular (400) text, `2px` beside semibold (600). One stroke weight per icon set, one icon library per surface. Sizing and RTL: [icons.md](icons.md).
- **One SVG, recolored per state.** Icons use `currentColor`; hover, selected and disabled come from CSS color and opacity, never separate assets. Outline is default; fill marks active. Animating the swap is an icon swap in the animate area.

## Reporting

**Severity.** `HIGH` breaks an interaction or hides a control's state (an active tab with no visible signal). `MEDIUM` is a visible surface or icon inconsistency (mismatched nested radii across a card set). `LOW` is isolated polish (a missing image outline).

**Verification.** Without a browser: check every defined state (hover, focus, active, loading, empty), plus radii, shadows and icon strokes, from the code. With one: walk each state in both themes.

**Format.** Use the standalone format in the review area's [review format](../review/review-format.md#standalone-domain-reports), with "No actionable UI-polish findings" as the empty result.
