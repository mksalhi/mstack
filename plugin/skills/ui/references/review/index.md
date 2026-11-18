# Interface review

Route the interface through each domain area, collect their evidence and consolidate one ranked verdict. This file owns orchestration only; never duplicate or override a domain's rules here.

Report on evidence, not taste. A trigger below is a failure whatever the style guide says; a density, radius or voice you merely disagree with is not a finding. `Approve` requires that you inspected what you claim.

## 1. Resolve the scope first

Infer the screen, flow, feature or repository scope from the request and workspace; state it in the output. Cover it across every domain in step 4, including empty, loading, error and narrow-width states where they exist. Report at most 15 findings. Show which domains and states you actually inspected.

Scope too large to inspect credibly: narrow to one complete flow (the one the request centers on, else the entry path every user passes). State the boundary and what it excluded. Never imply uninspected surfaces were reviewed.

## 2. Resolve a change with change-review.md

A request naming a branch, pull request, commit range or uncommitted changes is a change review. First resolve its scope, read the diff, expand to affected surfaces and classify every finding per [change-review.md](change-review.md). Severity, ranking, the cap and the verdict stay here, and cover `Introduced` and `Regression` only.

## 3. Recon before judgment

Identify the framework, styling system, component library, design tokens, supported viewports and any preview or test command. Write every fix in the project's idiom; never ask it to adopt a different stack.

Read the project's interface docs: `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `AGENTS.md`, `CLAUDE.md`, a design-system doc, Storybook docs, interface ADRs. Name which you found, or that there are none. A documented convention never retires a finding; it changes where you report. When a guideline or shared token is the cause, report it once against that source, with the components as its locations.

## 4. Use domain areas as the sources of truth

Read each area's file directly, plus its references. Complete each domain review before consolidation, in this order:

1. accessibility: [../accessibility/index.md](../accessibility/index.md)
2. layout: [../layout/index.md](../layout/index.md)
3. copy: [../copy.md](../copy.md)
4. typography: [../typography/index.md](../typography/index.md)
5. colors: [../colors/index.md](../colors/index.md)
6. polish: [../polish/index.md](../polish/index.md)
7. animate: [../animate/index.md](../animate/index.md). Its **Never ship** table is the criteria list, with values from its **Easing and duration** section.
8. mobile-web: [../mobile-web.md](../mobile-web.md), only when the scope includes a phone-sized or touch surface. Its **Never ship** table.

Take each domain's principles, references and verification checks; replace its severity ladder and format with the ones here.

If an area file cannot be read, mark that domain `Not reviewed`, name it and continue. Mark mobile-web `Not reviewed: no mobile surface in scope` when that is the reason. Never recreate its rules from memory, substitute a neighbour or claim holistic coverage.

When two areas cover one issue, assign it to the owner of the underlying rule, note secondary effects in the **Why** cell, and report it once.

## 5. Require evidence

Every finding cites `path/to/file:line` and shows the current implementation. When runtime behavior determines the result, never report a code-level finding from visuals alone or a visual finding from source alone.

## 6. Rank by user impact

- `HIGH`: blocks a task, misleads the user, hides content or controls, risks data loss, or is a repeated systemic failure.
- `MEDIUM`: meaningfully harms comprehension, efficiency, adaptability or consistency.
- `LOW`: isolated polish with limited task impact.

Within a severity, rank by reach and how much one fix buys; a token or shared-component fix outranks the same symptom in one leaf.

**Escalation triggers.** Once the owning area confirms one, it is `HIGH` on sight, however minor the surface:

- An interactive control with no accessible name.
- A keyboard-reachable control with no visible focus indicator.
- A control or path reachable by pointer but not by keyboard.
- Motion or auto-playing content that ignores `prefers-reduced-motion`.
- Content or a control clipped, overlapped or unreachable at 320px width or 200% zoom.
- Body or control text whose rendered contrast pair fails its required ratio.
- State or meaning carried by color alone.
- A destructive action with no confirmation, undo or distinct treatment.
- Truncated content with no way to reach the full value.
- Content or a control reachable only past a scroll edge or behind a disclosure with no visible cue.
- An error that names no way to recover.
- A semantic color used against its meaning, such as the danger hue on a non-destructive action.
- A state change carried by motion alone, with no color, icon or label left when the animation does not run.

Triggers rank above every other finding. When more fire than the cap allows, list them first and say how many the cap excluded; the cap never hides a blocker. Triggers set severity, not rules: the owning area decides whether the symptom is present. In a change review, a confirmed `Regression` against a trigger is `HIGH` even where the pre-existing symptom would be `MEDIUM`.

## 7. Prefer the cheaper fix

Propose the earliest fix that works:

1. **Delete.** A separator space would carry, an animation on a high-frequency interaction, ARIA a native element makes redundant, a ramp nothing imports.
2. **Use the platform.** Native element, native control, the browser's focus ring.
3. **Reuse what the project has.** An existing token, spacing step or motion curve.
4. **Correct the value.** Wrong easing, radius, gap or contrast pair, using the owning area's exact value.
5. **Add.** A new token, wrapper, media query, or ARIA the platform cannot supply.

A fix written at step 5 where step 1 was available is its own finding; report the deletion instead.

## 8. Consolidate systemic findings

One root cause is one finding, with every confirmed location in the same row. Never pad to the cap; a short review or no findings is valid.

## 9. Verify what can be verified

Run the safe, relevant checks the project offers. Inspect the rendered interface when runtime behavior or visual judgment matters, and report the exact command or interaction and its result. A check you cannot run is **Not verified**, never a finding.

## 10. Review without mutating by default

A review is read-only unless the user also asks you to implement the findings. Then keep the consolidated report as the change scope and re-run the relevant verification afterward.

## Output

Report in [review-format.md](review-format.md): scope and coverage, the findings table, verification and the verdict. A review is not finished until reported there.
