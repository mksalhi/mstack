# Typography

A label, a table cell, a headline and an article paragraph do not share one set of rules. When reviewing, read the rendered page at real content lengths, not just the code. Write every fix in the project's styling system with the exact values below; the [cheat sheet](css-cheat-sheet.md) maps declarations to Tailwind.

The words belong to the [copy area](../copy.md); semantic heading structure to the [accessibility area](../accessibility/index.md); spatial RTL layout and logical properties to the [layout area](../layout/index.md); contrast measurement to the [colors area](../colors/index.md). This area owns how text renders, wraps and behaves in mixed-direction content.

## Serve the right format

`.woff2` on the web; `.woff` only as a very-old-browser fallback; never `.ttf`/`.otf`.

## Properties over raw tags

Use the CSS property when one exists: `font-weight: 650`, not `font-variation-settings: "wght" 650`; `font-optical-sizing: auto`, not `"opsz"`; `font-variant-numeric: tabular-nums`, not `font-feature-settings: "tnum" 1`. Raw tags only for custom axes (`"GRAD" 80`) and niche features (`"ss01" 1`). See [variable-fonts-and-opentype.md](variable-fonts-and-opentype.md).

## Load intended weights and styles

Load every face the design uses; browsers otherwise synthesize distorted ones. Set `font-synthesis: none` only after checking every required bold, italic, small-cap, superscript and subscript form stays distinct across the fallback stack.

## Fewer fonts, sizes and weights

Rarely more than three fonts. Pair for contrast (serif headline over sans body), never two near-identical sans-serifs. Below `18px`, weight `400`+; weights under `300` only at `28px`+. See [choosing-fonts.md](choosing-fonts.md).

## Use a type scale with semantic names

A small set of sizes, deviated from as little as possible. On a team, name sizes by use (`text-body-sm`); default names like `text-sm` are fine solo. See [spacing-and-sizing.md](spacing-and-sizing.md).

## Heading sizes descend with level

Map heading levels to descending scale steps so a subordinate heading never overpowers its parent. Adjacent small levels may share a size if weight or spacing keeps them distinct. Choose the heading element by semantics first, never for its default size.

## Line-height by role

Headings around `1.1`; body `1.5` to `1.6`; unitless values. Anything wrapping to three or more lines needs at least `1.4`, even in a height-constrained row.

## Letter-spacing by size

Slightly negative on large headings; slightly positive on small uppercase labels; none on body copy.

## Cap the measure

Cap long-form text around 60–75 characters per line, in any unit. See [unit choices and the pixel equivalents](wrapping-and-punctuation.md#measure-line-length).

## Wrap deliberately

- `text-wrap: balance` on headings.
- `text-wrap: pretty` on descriptions.
- `overflow-wrap: break-word` where a long word, link or ID could escape the container.
- `white-space: nowrap` on labels and badges.

Skip `balance` and `pretty` in long-form text. Use `text-align: start` in interfaces; reserve justify for specific editorial layouts.

## Tabular numbers on changing values

`font-variant-numeric: tabular-nums` on timers, counters, prices and any value that changes.

## Truncate without losing content

One line: `text-overflow: ellipsis` + `overflow: hidden` + `white-space: nowrap`. Several: `line-clamp`. When the missing text matters, keep the full value reachable in a tooltip or expanded view.

## Write copy naturally, style with CSS

Store text in natural case; present with `text-transform`. Smart punctuation in rendered text:

- Curly quotes in prose, straight quotes in code.
- En dash for ranges: `2010–2020`.
- The single ellipsis character, not three periods.
- `&nbsp;` to hold `16 px` together.
- `&shy;` to mark where a long word may break.

Full table: [wrapping-and-punctuation.md](wrapping-and-punctuation.md#smart-punctuation).

## Underlines from the font

Use `text-underline-position: from-font` and `text-decoration-thickness: from-font`; tune with `text-decoration-thickness`, `text-underline-offset` and `text-decoration-skip-ink`. A dotted underline (`text-decoration-style: dotted`) hints at extra information such as an abbreviation. Only color animates reliably on `text-decoration`; for any other underline animation, build a separate element.

## Inputs at 16px on mobile

iOS Safari zooms the page when an input's text is under `16px` and doesn't zoom back. This is the one home for that fix (the mobile-web area points here). Never disable zoom. Ask which fix the design wants:

- Size the input up on mobile (`text-base sm:text-sm`); changes its small-screen look.
- Keep `font-size: 16px` and render the intended size with `transform: scale()`, compensating width and `line-height`; identical everywhere, more code.

Recipes: [details-and-accessibility.md](details-and-accessibility.md).

## Size and contrast floors

Long-form body starts at `16px`; move off it only for a nameable reason (typeface runs small, narrow measure, dense professional tool). UI text: `14px` for inputs and menus, `13px` captions, rarely below `12px`; inputs still `16px` on mobile. For low-looking contrast, measure with the colors area, classify with the accessibility area, and leave colors alone unless asked.

## Font smoothing on the root

`-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` once on the root layout, never per component (Tailwind `antialiased`).

## Language and bidi behavior

Set `lang`. Set `dir` at the document or the content boundary where direction changes. Preserve digit order; isolate mixed-direction values with `<bdi>`. Paragraph alignment by script: [wrapping-and-punctuation.md](wrapping-and-punctuation.md#internationalization).

## Keep useful text selectable

Text stays selectable; a `::selection` color must stay legible. `user-select: none` only on controls whose label is not content (buttons, tabs, chips, drag handles), never on body text, `body` or plain links.

## Reporting

**Severity.** `HIGH` makes text unreadable or truncates content with no way to recover it. `MEDIUM` breaks the type system or heading hierarchy. `LOW` is isolated polish.

**Verification.** Without a browser: computed size and weight per heading level, checked descending; declared line-height and measure; truncation against realistic string lengths. With one: resize the viewport to catch wrapping, widows and truncation.

**Format.** Use the standalone format in the review area's [review format](../review/review-format.md#standalone-domain-reports), with "No actionable typography findings" as the empty result.
