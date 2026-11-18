# Worst-case values

Use `example.com` and `.test` domains.

- Names: `نور الهدى عبد الرحمن` (needs `dir="auto"`), `🦊 Fox`, `  Sam   Lee `, missing (email-only).
- Emails/URLs/IDs: `first.last+billing@example.com`, `bartholomew.fitzgerald@northwind-industries-holdings.example.com`, a long URL whose distinguishing part is at the end, `Q3 Board Deck — FINAL (revised) v12.pdf`.
- Text from data: `Benachrichtigungseinstellungen`; 12 tags (show "+8"); one 45-character tag; `Untitled`, `""`, `"   "`; render `<script>`, `&amp;`, `**bold**` literally; an embedded newline; a 2,000-character paste.
- Numbers: `0` (divide by zero), `1` ("1 members"), `1284`, `1000000` (locale separators), `$12,345,678.90`, `0.1+0.2`, `142%`, `-3%` (bounds), `null`, `NaN`, live change `99`→`100` (width jump).
- Collections: exactly page size and one more; 1,000+ unpaginated; one item 10× others; identical names.
- Time: now ("0 seconds ago"); 12 days, 11 months, 3 years (switch to absolute after about a week); future dates; `1970-01-01`; date differing by UTC; `1,284 hours`. Use `Intl.RelativeTimeFormat`.
- Media: avatar URL 404; no avatar; 4000×200 panorama; 200×4000 image; dark logo in dark mode; slow loads without `aspect-ratio`.
- States: loading (skeleton mismatch); raw `TypeError` as error; partial optional fields; every status at once; no permission; current user present.
- Environment: 320px container; 280px sidebar; 2560px wide; 200% zoom; dark mode; `dir="rtl"`; touch (hover-only actions).
