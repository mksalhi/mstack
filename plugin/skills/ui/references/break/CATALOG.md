# Worst-case catalog

Realistic breaking values by field kind; use the rows matching your Phase 1 table. Use `example.com`, `example.org` or `.test` domains for emails and URLs.

## People and names

| Value | Breaks |
| --- | --- |
| `Aleksandra Wiśniewska-Kowalczyk` | Long, hyphenated, diacritics; wraps, hyphen is a break point |
| `Christopher Alexander Montgomery III` | Suffix; naive initials give `CI` |
| `Konstantin Oberhauser-Wettstein` | Long compound; overflows single-line rows |
| `Jo` | Empty-looking column; naive initials `J` |
| `J` | Single-character initials; tiny click target if the name is the link |
| `Ólafur Darri Ólafsson` | Accented capital; uppercase/sort logic, initials `ÓÓ` |
| `Đặng Thị Ngọc Hân` | Stacked diacritics; clipped by tight `line-height` + `overflow: hidden` |
| `王秀英` | CJK, no spaces; first+last-word initials find one word, breaks anywhere |
| `نور الهدى عبد الرحمن` | RTL; punctuation and icons on the wrong side without `dir="auto"` |
| `Seán O'Brien-Ó Súilleabháin` | Apostrophe and accents; escaping, initials, search |
| `María José de la Cruz y Fernández` | Lowercase particles; initials `Md`/`MF`, last-name sorting |
| `dana` | All lowercase; initials must still be uppercase |
| `🦊 Fox` | Emoji first; `.charAt(0)` returns half a surrogate pair (`�`) |
| `👩🏽‍💻 Priya` | ZWJ sequence; `.length` 7+, slicing splits it |
| `  Sam   Lee ` | Extra spaces; initials from empty words, odd gaps |
| *(missing)* | Only an email; UI needs a fallback |

## Emails, URLs, identifiers

No spaces, so nowhere to wrap.

| Value | Breaks |
| --- | --- |
| `bartholomew.fitzgerald@northwind-industries-holdings.example.com` | Pushes siblings off the row without `overflow-wrap: anywhere` |
| `a@b.co` | Layout that assumed a long email looks empty |
| `first.last+billing-notifications@example.com` | Validation rejecting `+`; truncation hides the meaningful part |
| `ops@sub.department.region.example.co.uk` | Subdomains, two-part TLD; domain extraction |
| `https://example.com/workspaces/acme/projects/q3-launch/docs/9f8e7d6c5b4a?tab=comments&filter=unresolved` | Overflow; end-truncation hides the differing part |
| `9f8e7d6c-5b4a-4c3d-8e2f-1a0b9c8d7e6f` | UUID; monospace width, middle-truncate |
| `Q3 Board Deck — FINAL (revised) v12 [approved by legal].pdf` | End-truncation hides version and extension; brackets and dashes |
| `IMG_20250914_183022_HDR_portrait_edited_edited.HEIC` | Unbreakable, uppercase extension |
| `@a` / `@thisisaverylongusernamethatisallowed` | Handle extremes |

## Labels, titles, and copy from data

| Value | Breaks |
| --- | --- |
| `Senior Product Design Engineer, Platform Infrastructure` | Three lines in a secondary slot |
| `Invitation expired 12 days ago` | Badge wraps or squeezes the name column |
| `Benachrichtigungseinstellungen` | 30-char German compound, unbreakable |
| `Paramètres de confidentialité et de sécurité` | Translation runs ~30% longer |
| Twelve tags: `design`, `frontend`, `q3`, `urgent`, `needs-review`, … | Wall of tags; needs a `+8` overflow |
| Tag `customer-feedback-from-enterprise-onboarding` | One tag wider than its container |
| `Untitled` / empty string / `   ` | Collapsed heading, zero-height row |
| `<script>alert(1)</script>` / `&amp;` / `**bold**` | Must render as literal text |
| `Line one` + newline + `Line two` | Doubles row height or silently dropped |
| 2,000-character pasted description | Clamps, "show more", textarea growth |

## Numbers and money

| Value | Breaks |
| --- | --- |
| `0` | "0 members", empty progress bar, divide-by-zero percentages |
| `1` | "1 members", "1 days ago" |
| `1284` | Needs `1,284` |
| `1000000` | Badge width; compact `1M` where precision doesn't matter |
| `12345678.9` as currency | `$12,345,678.90` overflows totals columns |
| `-42.5` | Negative sign, red logic, accounting parentheses |
| `0.1 + 0.2` | `0.30000000000000004` rendered raw |
| `142%` / `-3%` | Progress bars past their bounds |
| `null` / `undefined` / `NaN` | Rendered literally |
| `1.284` in `de-DE` vs `1,284` in `en-US` | Hardcoded separators |
| Live change `99` → `100` | Width jump without `tabular-nums` |

## Collections

| Value | Breaks |
| --- | --- |
| 0 items | Empty state, if any |
| 1 item | Lonely grid card; "1 of 1" |
| Exactly page size, and +1 | "Showing 40 of 40", empty page 2 |
| 1,000+ unpaginated | Scroll perf, render time, memory; "Showing 40 of 1,284" |
| One item 10× the others | Grid rows stretch to the tallest |
| Identical names | Name is the only distinguishing field |

## Time

| Value | Breaks |
| --- | --- |
| Now | "0 seconds ago" instead of "just now" |
| 12 days, 11 months, 3 years ago | Relative-time thresholds; go absolute after about a week |
| Future date | "in 3 days" vs "-3 days ago" |
| `1970-01-01` | Zero timestamp shown as real |
| `2025-12-31T23:30:00-08:00` | Different day in UTC vs user timezone |
| `1,284 hours` | Never rolls up to days |

Use `Intl.RelativeTimeFormat` and `Intl.DateTimeFormat`.

## Images and media

| Value | Breaks |
| --- | --- |
| Avatar URL 404s | Broken-image icon instead of initials |
| No avatar | Fallback initials, color, size parity |
| 4000×200 panorama | Distortion without `object-fit: cover` |
| 200×4000 tall image | Same; blows out card height |
| Transparent or dark logo in dark mode | Invisible |
| Slow-loading image | Layout shift without dimensions or `aspect-ratio` |

## States

| Value | Breaks |
| --- | --- |
| Loading | Skeleton mismatches final layout; spinner shifts content |
| API error | No error state, or raw `TypeError: Cannot read properties of undefined` |
| Partial data | Mixed optional fields misalign rows |
| Every status at once (`active`, `invited`, `expired`, `suspended`) | Varying badge widths |
| No permission | Disabled actions change row layout |
| Current user in the list | "You" labels, self-inapplicable actions |

## Environment

Flip to the worst case, then change these:

| Condition | Breaks |
| --- | --- |
| 320px container | Every overflow at once |
| Narrow sidebar (280px) | Full-width components reused |
| 2560px wide | Unreadable line length, stranded content |
| 200% zoom / large text | Fixed heights clip text |
| Dark mode | Hardcoded colors, invisible borders and logos |
| `dir="rtl"` | Icons, chevrons, padding, trailing-action order |
| Touch device | Hover-only actions (••• on hover) unreachable |
