# Details and accessibility

## Underlines

```css
a {
  text-underline-position: from-font;
  text-decoration-thickness: from-font;
}
abbr { text-decoration: underline dotted; }
```

Or tune manually:

```css
a {
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
  text-decoration-skip-ink: auto;
  text-decoration-color: var(--color-gray-1000);
  transition: text-decoration-color 200ms ease-out;
}
a:hover { text-decoration-color: var(--color-gray-1200); }
```

## Selection

- `::target-text` styles the phrase a shared link scrolls to.
- The Custom Highlight API styles ranges such as search matches without extra markup.

## Forms and editable text

- `::placeholder` styles the empty-field hint.
- `caret-color` colors the insertion bar; skip fully custom carets.

### iOS input zoom

Both fixes are correct; they differ in design impact.

**Size up on mobile.** `16px` on small screens, design size from `sm` up; the mobile input no longer matches desktop.

```tsx
<input className="text-base sm:text-sm" type="email" />
```

**Scale the text down.** Keep `font-size: 16px` and transform to the intended size. Widen by the inverse of the scale, divide `line-height` by the same factor, pin with `origin-left` (`origin-right` under RTL), and drop the transform above the breakpoint.

```tsx
// 13px rendered from a 16px font-size: 13 / 16 = 0.8125
<div className="flex h-10 items-center rounded-[10px] bg-gray-300 px-2.5">
  <input
    className="h-full w-[calc(100%/0.8125)] origin-left scale-[0.8125] bg-transparent text-base leading-[calc(1.125/0.8125)] outline-none sm:w-full sm:scale-100 sm:text-[13px]"
    type="email"
  />
</div>
```

The transform shrinks the whole box: a wrapper draws the field's surface and the input stays transparent, with no background, border or ring on the scaled element.

## Decorative text

| Property | Effect |
| --- | --- |
| `::first-letter` | Drop cap, widely supported |
| `::first-line` | Styles only the first line |
| `initial-letter` | Sizes the drop cap; limited support, no Firefox yet |
| `background-clip: text` | Clips a background or gradient to the letter shapes |
| `-webkit-text-stroke` | Outlines the letters; works across modern browsers despite the prefix |
| `text-shadow` | Like `box-shadow` but follows the character shapes |

Lines inside stroked letters come from unmerged overlapping contours in variable fonts; static fonts avoid it.

## Sizes

Typography must survive zoom, a larger browser font size, and overridden line height or letter spacing.

| Text | Size |
| --- | --- |
| Long-form body starting point | Around `16px`, verified in the actual typeface and measure |
| Inputs and menus starting point | Around `14px` |
| Captions | `13px` |
| Floor | Rarely below `12px` |
