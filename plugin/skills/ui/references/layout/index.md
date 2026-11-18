# Layout

Defaults when no density system; otherwise use it. Hit areas/focus: [accessibility](../accessibility/index.md). Radius/shadows: [polish](../polish/index.md). Measure/text spacing: [typography](../typography/index.md).

- Prefer space to lines for grouping; separators only in dense data. Between-group gaps ≥2× inside gaps (e.g., 8px inside, 16px+ between).
- Controls need a visible affordance (fill, border, underline, or fixed zone). Static badges must not mimic adjacent buttons.
- Use logical properties (margin-inline-start, inset-inline-end; Tailwind ms-4 pe-6 text-start). Physical sides only for physical geometry. Progressions mirror in RTL; hand-placed elements don’t auto-mirror.
- Importance: put the key number/content first (top/leading). One primary action; overflow extras after 2–3.
- Hidden content needs a cue. Let the next item peek 16–32px past a scroll edge via container padding; keep snap points on the content edge. Label disclosure with what it hides.
- Spacing between controls: ≥12px between bordered/filled; ≥24px around borderless text or icon buttons.
- Content bleeds; controls float. Media/backgrounds can run to edges; text/controls stay within margins and env(safe-area-inset-*). Full-width buttons sit inside margins (~16px on mobile) with a radius; edge-to-edge only for platform chrome.
- Breakpoints come from content; collapse late. Prefer container queries; test smallest and largest sizes first.
- Growth: never fix text box sizes; size buttons from the label. Pseudo-localize. Primary actions must never be clippable. In a scrolling modal, the action row does not scroll.

Verify at all supported widths, at 200% zoom, and in RTL. Use [review](../review/index.md#output).
