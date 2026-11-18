# Wrapping and punctuation

## Measure (line length)

Long-form text: 60–75 characters per line, in any unit. `65ch` measures directly; at a `16px` body the range is roughly `560px` to `680px`, so Tailwind `max-w-xl` (`576px`) and `max-w-2xl` (`672px`) fit. Recheck if the body size changes.

## Smart punctuation

| Instead of | Use |
| --- | --- |
| Straight quotes `"..."` | Curly quotes that curve around the text (keep straight quotes in code) |
| Hyphen in ranges | En dash: `2010–2020` |
| Two hyphens for an aside | Em dash character |
| Three periods `...` | The single ellipsis character `…` |
| Regular space in `16 px` | `&nbsp;` so the value never breaks apart |
| Uncontrolled word breaks | `&shy;` to mark where a word may break |

## Internationalization

- **Long paragraphs align by their own language.** Snippets of one or two lines follow the UI's direction; a paragraph of three or more lines aligns to its own script. Use `text-align: start` with correct `lang`/`dir` on the paragraph.
- **Never reverse digits.** Never reorder numbers manually; wrap mixed number-and-text values in `<bdi>` where adjacent RTL text disturbs them.
