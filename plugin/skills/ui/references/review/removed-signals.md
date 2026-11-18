# Removed signals

Leads on the `-` side of a hunk and the area that judges each. Report a removal only once its owner confirms the interface got worse.

| Removed from the `-` side | Owner | What to check |
| --- | --- | --- |
| `aria-label`, `aria-labelledby`, `aria-describedby`, `aria-live`, `role=` | accessibility | The control or region lost its accessible name, description, or announcement |
| `alt=`, `<label`, `for=`, `scope=` | accessibility | Image, field, or table cell lost its programmatic association |
| `<button>`, `<a>`, `<nav>`, `<main>`, `<ul>` replaced by `div` or `span` | accessibility | Keyboard and assistive-technology behavior was traded for styling |
| `:focus-visible`, `:focus`, `outline`, `tabindex` | accessibility | Keyboard users lost the focus indicator or the element left the tab order |
| `prefers-reduced-motion`, `prefers-contrast` | accessibility | Motion or contrast now ignores the user's system preference |
| Logical properties swapped for `left` / `right` | layout | Direction-aware layout was dropped |
| `lang=`, `dir=` | typography | Language metadata or text direction was dropped |
| `text-wrap`, `line-clamp`, `overflow-wrap`, `tabular-nums`, `font-feature-settings` | typography | Text rendering, wrapping, or numeral alignment silently changed |
| A color token swapped for a literal, or a token swapped for a lighter one | colors | The rendered contrast pair may now fail; measure it |
| A user-facing string deleted or shortened | copy | A label, error, or empty state lost the information it carried |

## Equivalent replacements

These clear the signal; check for them before routing:

- `aria-label` giving way to `aria-labelledby` pointing at visible text.
- An explicit `role` dropped because the element became native (`div role="button"` to `<button>`).
- `outline` replaced by a `box-shadow` focus ring that still meets the focus-indicator rule.
- `tabindex="0"` dropped from an element that is now natively focusable.
- A color literal replaced by a token that measures the same rendered pair.
- A physical property replaced by its logical counterpart.
- A string moved into the translation catalogue rather than deleted.

## Searching the removed side

Search deleted lines only:

```bash
git diff -U0 "$BASE"...HEAD -- '*.tsx' '*.css' | grep -E '^-[^-]' | grep -E 'aria-|role=|alt=|focus|tabindex|prefers-'
```

Read the surrounding hunk before deciding; `-U0` hides the element the attribute came from.
