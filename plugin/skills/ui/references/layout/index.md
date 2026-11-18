# Layout

Build structure, then stress-test it: resize, translate, mirror for RTL. Write every fix in the project's styling system. The numbers below are starting points for interfaces with no established density system; where one exists, use it as written. Keep deliberate platform chrome, compact professional tools and project tokens where they pass the stress tests.

Hit areas and focus belong to the [accessibility area](../accessibility/index.md); radius and shadows to the [polish area](../polish/index.md); animation to the [animate area](../animate/index.md); line length and text spacing to the [typography area](../typography/index.md).

## Group with space, not lines

Space first, background shapes second, separator lines last. The gap between groups is at least 2× the gap within one (`8px` intra-group to `16px`+ inter-group). Edges and ordering: [grouping-and-alignment.md](grouping-and-alignment.md).

## Keep controls distinct from content

Every interactive element gets a background shape, a border, or a consistent placement zone.

## Align to shared edges

Pick alignment edges and stick to them. One project spacing step per level of subordination (`16px` default). Use logical properties (`padding-inline-start`, `margin-inline-end`) for direction-dependent layout; physical left/right only for genuinely physical geometry.

## Order by importance

Most important content near the top and the leading edge; reading order flows top-to-bottom, leading-to-trailing.

## Hint at hidden content

Progressive disclosure needs a visible affordance: the project's established cue, the next item peeking `16–32px` past the scroll edge, or a disclosure control.

## Breathing room between targets

Without a density system, start with `12px` between adjacent bordered or filled controls and `24px` around borderless text- and icon-only ones. Compact layouts may use less if accessibility-area hit areas don't overlap and controls stay distinct. Margins and breakpoints: [spacing-and-adaptivity.md](spacing-and-adaptivity.md).

## Inset buttons from the edges

In content layouts, keep full-width buttons inside the layout margins with a visible radius, near `16px` inline on mobile. Edge-to-edge actions are fine when they follow platform chrome, account for safe areas and stay distinct from system UI.

## Content bleeds, controls float

Backgrounds and media extend to the viewport edges. Controls and text stay inside layout margins and safe areas (`env(safe-area-inset-*)`). Sticky chrome floats above content rather than blocking it.

## Hold structure until it breaks

Breakpoints come from the content, not device presets. Keep the expanded layout while it fits; collapse late. Prefer container queries for components; test the smallest and largest sizes first.

## Plan for growth and clipping

Translated strings grow, short ones proportionally most. No fixed width or height on text containers; let rows wrap. Test with pseudo-localization and one representative locale. Never park a critical action where resizing or scrolling clips it; keep it in flow or in stable chrome.

## Reporting

**Severity.** `HIGH` blocks content or an action at a supported viewport. `MEDIUM` harms hierarchy, reading order or adaptability. `LOW` is isolated alignment or spacing polish.

**Verification.** Without a browser: logical properties in place of physical ones, container and media queries against the supported viewport list, DOM order against intended reading order. With one: every supported width, 200% zoom and the RTL mirror.

**Format.** Use the standalone format in the review area's [review format](../review/review-format.md#standalone-domain-reports), with "No actionable layout findings" as the empty result.
