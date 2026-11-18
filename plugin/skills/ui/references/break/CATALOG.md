# Worst-case values

Use `example.com` and `.test` domains.

| Field | Values and what they break |
|---|---|
| Names | `Aleksandra Wiśniewska-Kowalczyk` (long, hyphenated) · `Christopher Alexander Montgomery III` (initials "CI") · `Jo`, `J` (tiny link target) · `Đặng Thị Ngọc Hân` (stacked diacritics clipped by tight line-height) · `王秀英` (no spaces) · `نور الهدى عبد الرحمن` (RTL without `dir="auto"`) · `María José de la Cruz y Fernández` (particles, sorting) · `dana` (lowercase) · `🦊 Fox` (`.charAt(0)` gives half a surrogate) · `👩🏽‍💻 Priya` (ZWJ, `.length` 7+) · `  Sam   Lee ` · missing (only an email) |
| Emails, URLs, IDs | `bartholomew.fitzgerald@northwind-industries-holdings.example.com` · `a@b.co` · `first.last+billing@example.com` (validators that reject `+`) · `ops@sub.region.example.co.uk` · a long URL whose distinguishing part is at the end · a UUID · `Q3 Board Deck — FINAL (revised) v12.pdf` (end-truncation hides the version) · `IMG_20250914_183022_HDR_edited.HEIC` |
| Text from data | `Senior Product Design Engineer, Platform Infrastructure` · `Benachrichtigungseinstellungen` · a French string about 30% longer than the English · 12 tags (needs "+8") · one 45-character tag · `Untitled`, `""`, `"   "` · `<script>`, `&amp;`, `**bold**` (must render literally) · an embedded newline · a 2,000-character paste |
| Numbers | `0` (divide by zero) · `1` ("1 members") · `1284` (needs a separator) · `1000000` · `$12,345,678.90` · `-42.5` · `0.1+0.2` · `142%` and `-3%` past a progress bar's bounds · `null`, `NaN` · de-DE vs en-US separators · `99` to `100` live (width jump) |
| Collections | 0 · 1 (a lonely card) · exactly the page size, and one more · 1,000+ unpaginated · one item 10 times the others · identical names |
| Time | now ("0 seconds ago") · 12 days, 11 months, 3 years (switch to absolute after about a week) · future dates · `1970-01-01` · a date that lands on a different day in UTC · `1,284 hours`. Use `Intl.RelativeTimeFormat`. |
| Media | an avatar URL that 404s · no avatar · a 4000×200 panorama · a 200×4000 image · a dark logo in dark mode · slow loads with no `aspect-ratio` |
| States | loading (the skeleton doesn't match the layout) · a raw `TypeError` shown as the error · partial optional fields · every status at once · no permission · the current user in the list |
| Environment | a 320px container · a 280px sidebar · 2560px wide · 200% zoom · dark mode · `dir="rtl"` · touch (actions that only appear on hover) |
