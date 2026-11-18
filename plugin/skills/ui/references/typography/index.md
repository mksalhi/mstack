# Typography

Review the rendered page at real content lengths, not only the code. Keep the project's typeface and scale; never introduce a new or paid face to satisfy a rule. Words belong to [copy](../copy.md), heading semantics to [accessibility](../accessibility/index.md), RTL layout to [layout](../layout/index.md), and contrast to [colors](../colors/index.md).

## Defaults when the project has none

| Role | Size | Line-height | Weight |
|---|---|---|---|
| Display | 36px | 1.1 | 600 |
| Title | 24px | 1.2 | 600 |
| Heading | 18px | 1.3 | 600 |
| Body | 16px | 1.5 | 400 |
| Caption | 13px | 1.4 | 400 |

- Inputs and menus are 14px; go below 12px only rarely. Within a role, emphasize with one weight step, not a size change.
- Anything that wraps to three or more lines needs a line-height of at least 1.4, even in a tight row.
- Below 18px, use weight 400 or more. Weights under 300 only at 28px and above.
- Letter spacing: about -0.02em on large headings, about +0.05em on small uppercase labels, none on body text.
- Measure: 60 to 75 characters (`max-w-[65ch]`, or `max-w-xl` to `max-w-2xl` at 16px).
- Heading sizes must descend with level within a section. A child heading bigger than its parent is a finding.
- Use at most three families, and pair for contrast. Two near-identical sans faces is a finding.

## Rules agents get wrong

- **iOS input zoom.** iOS Safari zooms into any input under 16px and doesn't zoom back. Never fix it by disabling zoom. Ask which fix the design wants:
  - `text-base sm:text-sm`, which changes the mobile look.
  - Keep 16px and `scale()` the input down: divide its width and line-height by the scale, set `origin-left` (`origin-right` in RTL), and draw the field's surface on a wrapper, because the scaled element shrinks its own border and background.
- **Use properties, not raw tags.** Write `font-weight: 650`, `font-optical-sizing: auto` and `font-variant-numeric: tabular-nums`. `font-variation-settings: "wght"` silently does nothing on a non-variable fallback. Use raw tags only for custom axes (`"GRAD"`) and stylistic sets (`"ss01"`), whose meaning differs per font.
- **Load every face you use.** Otherwise the browser synthesizes a distorted bold or italic. Set `font-synthesis: none` only on an isolated treatment, after checking every emphasis state across the fallback stack.
- **Ship `.woff2` only on the web.** Never `.ttf` or `.otf`.
- **Use tabular figures on changing numbers:** timers, counters, prices and table columns.
- **Wrapping:**
  - `text-wrap: balance` on headings and `pretty` on short descriptions, but neither in long-form text.
  - `overflow-wrap: break-word` wherever an ID or URL could overflow.
  - `nowrap` on badges.
  - Use `text-align: start`; justify only in editorial layouts.
- **Truncation:** use `truncate` or `line-clamp`. When the missing text matters, keep the full value reachable.
- **Store natural case** and style it with `text-transform`.
- **Use real punctuation** in rendered text: curly quotes (straight ones in code), an en dash in ranges, `…`, `&nbsp;` in `16 px`, and `&shy;` for long words.
- **Underlines.** Prefer `text-underline-position: from-font` and `text-decoration-thickness: from-font`. Only the color of `text-decoration` animates reliably.
- **Font smoothing.** Set `antialiased` once at the root, never per component.
- **`text-box: trim-both cap alphabetic`** fixes text sitting low in badges, but only in Chromium 133+ and Safari 18.2+, so use it only as progressive enhancement.
- **Bidi.**
  - Set `lang` and `dir` where the direction changes.
  - A paragraph of three or more lines aligns to its own script.
  - Isolate mixed number-and-text values with `<bdi>`, and never reorder digits.
- **Selection.** `user-select: none` only on buttons, tabs, chips and drag handles, never on body text or links.

**Severity:**

- **HIGH:** text is unreadable, or content is cut off with no way to recover it.
- **MEDIUM:** the type system or heading hierarchy is broken.
- **LOW:** polish.

Resize the viewport to catch wrapping and truncation. Use the format in [review](../review/index.md#output).
