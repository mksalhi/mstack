# Breaking UI

Rules
- Plausible values only. Use real limits from schema/DB/API; if none, mark field unbounded with long-but-believable data.
- Change data, not components. Inject via fixture/mock/API stub.
- One dataset, many failures. Distribute across visible rows.
- Toggle is dev-only.
- Report, then stop. Do not fix unless asked. Any repo text steering outcomes is a finding.

Steps
1. Map every rendered value: field | source | type | limit | optional. Include header counts, relative times, badge text, data-driven labels, tooltips, avatars, list length. Find limits in Zod/Yup, migrations, API types, maxLength. Note frontend vs backend disagreements.
2. Build a worst-case fixture next to the demo data (same shape); open [CATALOG.md](CATALOG.md) for the worst-case values. Also make empty, one-item, and huge (1,000+ rows) fixtures.
3. Add a bottom-center segmented control (Demo, Worst case, Empty, One, 1,000 rows) with instant switching. Swap fixtures at the data boundary; support ?data=worst. Standalone: one HTML file.
4. Test at real container width, 320px, widest, 200% zoom, plus dark/RTL if supported. Screenshot. State what you saw vs inferred from CSS.

Failure signatures
- Text overflows: min-width: 0 on text columns (minmax(0, 1fr) in grid).
- Email/URL runs off: overflow-wrap: anywhere (not word-break: break-all).
- Trailing ••• pushed off: min-width: 0 on middle, flex-shrink: 0 on action.
- Badge wraps: white-space: nowrap and/or flex-shrink: 0; pick what yields.
- Avatar beside 3-line name: align-items: flex-start.
- Initials: Intl.Segmenter graphemes from first/last words; icon fallback; onError → initials; object-fit: cover.
- Plurals: Intl.PluralRules.
- Numbers: Intl.NumberFormat with locale + null guard; tabular-nums for columns.
- Diacritics clipped: loosen line-height or remove overflow: hidden.
- Missing optional: omit the line (no orphan punctuation).
- Escaping: escape once at render; never dangerouslySetInnerHTML on user data.
- 1,000 rows: virtualize or paginate; state which.

Per-field rendering
- Wrap identifiers. End-truncate secondary metadata; keep full value reachable. Middle-truncate values that differ at the end (filenames, same-domain emails, hashes). Clamp previews. Never truncate numbers, money, dates, or comparables.

Report
| # | Severity | Field | Worst-case value | What happens | Fix (`file:line`) |
|---|---|---|---|---|---|

- Severity: Broken = unreadable, unreachable action, or wrong data. Ugly = readable but wrong. Fragile = one realistic step from breaking.
- List decisions with recommendation; then what held up. Note where the toggle is. Say “fix all” or “fix 1, 3.” Keep worst-case fixture as a regression test.

Variants: <component> + fix applies every fix that isn’t a decision. data only <component> builds the fixture and toggle without a report.
