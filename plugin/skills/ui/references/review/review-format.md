# Review output format

Format for a full review and for a domain area reporting alone ([Standalone domain reports](#standalone-domain-reports)).

## Scope and coverage

State the exact scope, stack and styling conventions, the convention documents found in recon and any review boundary. Then coverage:

| Domain | Evidence inspected | Result |
| --- | --- | --- |
| Accessibility | Files, components, states, or checks | Findings count or `Clear` |

Include every domain listed in [index.md](index.md) step 4. `Clear` means inspected with no actionable finding; `Not reviewed` must say why.

## Findings

One table, ordered by severity, then reach:

| Severity | Domain | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- |
| HIGH | Accessibility | `src/Dialog.tsx:42` | `<button><XIcon /></button>` | Add `aria-label="Close"` and hide the icon from the accessibility tree | The icon-only control has no accessible name |

- **Severity** comes from [index.md](index.md) step 6, **Rank by user impact**.
- **Location** cites `path/to/file:line`, or the exact screen and component when there are no source files.
- **Before / After** show the current implementation and an actionable replacement, in their cells, never as separate "Before:"/"After:" lines.
- **Why** names the violated principle and its user impact.
- **Domain** is the owning area's name.

One row per root cause, listing every affected location. Respect the finding cap. With no findings, omit the table and state "No actionable interface findings."

## Verification

List each check, its exact command or steps and the observed result. Separate passed checks from **Not verified** ones.

## Verdict

- `Block`: one or more `HIGH` findings remain. Do not ship until fixed.
- `Approve`: no `HIGH` remains; `MEDIUM` and `LOW` stay in the table as work to do. Never `Approve` a domain you did not inspect.

## Change-scoped reviews

When [change-review.md](change-review.md) resolved the scope, use its **Review output format** (scope block, statuses). Severity, ranking, the cap and the verdict are the ones above and cover `Introduced` and `Regression` only.

## Standalone domain reports

A domain area run alone (accessibility, colors, copy, layout, polish, typography) uses its own **Reporting** severity examples and verification checks, and this format for the rest.

Group findings under the principle each violates, by severity, one row per root cause listing every location:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

`Location` is `path/to/file:line`. `Why` names the principle and the user impact.

Report every check you could not run as `Not verified`. End with the verdict above. With nothing to report, state "No actionable <domain> findings" and report verification.
