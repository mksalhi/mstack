# Typography

Review the rendered page at real content lengths. Keep the project’s typeface and scale; never introduce a new or paid face. Words belong to [copy](../copy.md), heading semantics to [accessibility](../accessibility/index.md), RTL layout to [layout](../layout/index.md), and contrast to [colors](../colors/index.md).

## Defaults when the project has none

- Anything that wraps to three or more lines needs a line-height of at least 1.4.
- Below 18px, use weight 400 or more. Weights under 300 only at 28px and above.
- Measure: 60 to 75 characters (`max-w-[65ch]`, or `max-w-xl` to `max-w-2xl` at 16px).
- Heading sizes must descend with level within a section. A child heading bigger than its parent is a finding.

## Rules agents get wrong

- iOS input zoom: never disable zoom. Choose:
  - `text-base sm:text-sm` (changes mobile look), or
  - Keep 16px and `scale()` the input; divide width and line-height by the scale, set `origin-left` (`origin-right` in RTL), and draw the field surface on a wrapper (scaled element shrinks its own border/background).
- Use properties, not raw tags: `font-weight: 650`, `font-optical-sizing: auto`, `font-variant-numeric: tabular-nums`. `font-variation-settings: "wght"` does nothing on a non-variable fallback. Use raw tags only for custom axes (`"GRAD"`) and stylistic sets (`"ss01"`).
- Load every face you use; otherwise the browser synthesizes bold/italic.
- Ship `.woff2` only on the web. Never `.ttf` or `.otf`.
- Use tabular figures on changing numbers: timers, counters, prices, table columns.
- Wrapping:
  - `text-wrap: balance` on headings; `pretty` on short descriptions; neither in long-form text.
  - `overflow-wrap: break-word` where IDs/URLs could overflow.
  - `nowrap` on badges.
- Truncation: use `truncate` or `line-clamp`. If the missing text matters, keep the full value reachable.
- Underlines: prefer `text-underline-position: from-font` and `text-decoration-thickness: from-font`. Only `text-decoration` color animates reliably.
- Font smoothing: set `antialiased` once at the root, never per component.
- Bidi:
  - Set `lang` and `dir` where direction changes.
  - Isolate mixed number-and-text with `<bdi>`; never reorder digits.

Resize the viewport to catch wrapping and truncation. Use the format in [review](../review/index.md#output).
