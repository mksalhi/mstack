# Colors

Never report a contrast value you did not measure, and never estimate a color you could compute.

Contrast requirements belong to the [accessibility area](../accessibility/index.md); surfaces, shadows and icon color to the [polish area](../polish/index.md).

## Match the project's color system

Reuse the project's tokens and notation; never add a second notation to fix one value. For a new system, default to `oklch()`; elsewhere, generate in the project's notation with a color library ([color-formats.md](color-formats.md)).

## A system is ramps, not colors

One neutral ramp, one accent ramp, and only the status ramps the product renders. A second accent hue only when two things must be distinguishable at a glance.

## Every step has a job

Each step exists because a role consumes it (page background, component hover, border, solid fill, body text); generate no unused steps. Tailwind `50`–`950` and Radix `1`–`12` mappings: [palette-structure.md](palette-structure.md).

## Name primitives by hue, semantics by role

Primitives name a value (`--blue-500`) and are never applied in a component. Semantic tokens name a job (`--color-text-secondary`), point at a primitive, and are the only tier components reference ([token-naming.md](token-naming.md)).

## Use a token only in its role

Never borrow a token because its value is right today (a separator used as text color). If a role has no token, add one.

## Hold the hue across the ramp

- Steps step evenly in *perceived* lightness.
- Hue stays constant end to end.
- Vividness peaks mid-ramp and falls off at both ends.
- Steps sit denser at the light end than the dark end.
- Both ends stop short of pure black and white.

Use a color library, not your eye ([palette-generation.md](palette-generation.md)).

## One color, one meaning

One purpose per color across the interface; hues within `15°` count as the same color. If the accent means interactive, never put it on static text, and never render an interactive element neutral. Color as sole carrier of meaning belongs to the accessibility area.

## Fill exactly one action per view

When fill encodes primary emphasis, one primary action gets it; peers stay neutral. Color the background, not the label. Several colored backgrounds are fine when they encode distinct states or categories rather than competing peers.

## Measure the rendered pair, then report

Measure the foreground against the background it actually renders on. On failure, report the pair, its measured value and the threshold it misses, and leave the colors alone unless asked; remeasure after any change ([contrast.md](contrast.md)).

## Pick a gradient's interpolation space

- **`in oklab`**: default; even brightness, no hue surprises.
- **`in oklch`**: sweeps around the hue wheel, staying vivid; use when a two-hue gradient goes gray in the middle.
- **sRGB default**: darkens and mutes the midpoint.

See [color-usage.md](color-usage.md).

## Before you finish

| Mistake | Fix |
| --- | --- |
| Token named for its appearance (`--color-blue-button`) or first use (`--color-sidebar-gray`) | Name it for its role: `--color-accent-solid`, `--color-bg-surface` |
| `--color-primary` meaning the brand and `--color-text-primary` meaning body text | Reserve `accent` for the brand; let `primary` mean "most prominent of its group" |
| Ramp spaced evenly across the full range | Tighten the light end until `50` and `100` read as two surfaces |
| Same saturation number reused across hues | Match the proportion of each hue's own maximum, not the raw value |
| Status hue that collides with the accent hue | Move it until destructive and primary read apart side by side |
| Dark mode made by mechanically reversing the light palette | Reverse as a starting point, then reduce vividness, widen the dark end and recheck every pair |
| `prefers-color-scheme` setting some tokens and a `.dark` class setting others | Pick one switching mechanism and use it throughout |
| Contrast fixed by changing hue | Change lightness, the channel contrast responds to |
| P3 color with no sRGB fallback | Declare the sRGB value first, then override inside `@media (color-gamut: p3)` |

## Reporting

**Severity.** `HIGH` makes content unreadable or assigns a misleading semantic color. `MEDIUM` is a noticeable theme, token or gamut failure. `LOW` is isolated polish.

**Verification.** Without a browser: token values, the gamut of every declared color, both theme blocks present, contrast computed from the declared token pair. With one: the background actually rendered behind the text (including opacity and any image beneath), measured in light and dark. A failing pair is reported, not repainted.

**Format.** Use the standalone format in the review area's [review format](../review/review-format.md#standalone-domain-reports), with "No actionable color findings" as the empty result.
