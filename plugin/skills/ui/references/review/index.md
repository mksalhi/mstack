# Interface review

Route the scope through each domain area, then merge their findings into one ranked verdict. Domain rules live in the areas; this file only orchestrates. Report evidence, not taste: a density or radius you'd have chosen differently isn't a finding.

A branch, PR, commit range or uncommitted changes makes this a change review: resolve it with [change-review.md](change-review.md) first.

## Steps

1. **Scope.** State the screen, flow or repo you're covering, including its empty, loading, error and narrow-width states. If it's too big to inspect credibly, narrow to one complete flow and say what you left out.
2. **Recon.** Note the framework, styling system, tokens and any preview command, and read the project's UI conventions (AGENTS.md, CLAUDE.md, design-system docs). Write fixes in the project's idiom. A convention doesn't excuse a finding. If a shared token or guideline is the cause, report it once against that source.
3. **Domains, in order:**
   1. [accessibility](../accessibility/index.md)
   2. [layout](../layout/index.md)
   3. [copy](../copy.md)
   4. [typography](../typography/index.md)
   5. [colors](../colors/index.md)
   6. [polish](../polish/index.md)
   7. [animate](../animate/index.md), using its Never-ship table
   8. [mobile-web](../mobile-web.md), only for phone or touch surfaces

   If an area file can't be read, mark that domain `Not reviewed`; never rebuild its rules from memory. An issue that spans two areas goes to the area that owns the rule, reported once.
4. **Evidence.** Every finding cites `file:line` and the current code. Don't report a runtime finding from source alone, or a code finding from a screenshot alone.
5. **Severity.**
   - `HIGH`: blocks a task, misleads, hides content, risks data loss, or is systemic.
   - `MEDIUM`: hurts comprehension, efficiency or consistency.
   - `LOW`: isolated polish.

   Within a severity, rank by reach: a token fix beats the same symptom in one leaf.
6. **Fix at the cheapest rung.** Delete, then use the platform, then reuse a project token, then correct the value, and only then add. A fix that adds where deleting would work is a finding of its own.
7. **Consolidate.** One root cause is one row, listing every location. Report at most 15 findings, and never pad.
8. **Verify** with the checks the project offers. Anything you couldn't run is `Not verified`, not a finding. A review is read-only unless the user also asked for fixes.

## Always HIGH

Once the owning area confirms one of these, it's HIGH and it ranks above everything else, cap or not:

- An interactive control with no accessible name.
- A keyboard-reachable control with no visible focus indicator.
- A control reachable by pointer but not by keyboard.
- Motion that ignores `prefers-reduced-motion`.
- Content clipped or unreachable at 320px width or 200% zoom.
- A text contrast pair that fails its ratio.
- Meaning carried by color alone.
- A destructive action with no confirm, no undo and no distinct treatment.
- Truncation with no way to reach the full value.
- Content past a scroll edge or disclosure with no visible cue.
- An error that names no way to recover.
- A semantic color used against its meaning.
- State carried only by motion.

## Output

1. **Scope**, stack and the conventions you found.
2. **Coverage**: one row per domain, `Domain | Evidence inspected | Findings count, Clear, or Not reviewed (why)`.
3. **Findings**: `Severity | Domain | Location | Before | After | Why`. Why names the rule and its effect on the user. With no findings, write "No actionable interface findings."
4. **Verification**: each check with its command and result, with `Not verified` listed separately.
5. **Verdict**: `Block` if any HIGH remains, otherwise `Approve`. Never approve a domain you didn't inspect.

A domain area run on its own uses the same table without the Domain column. Its empty result is "No actionable <domain> findings."
