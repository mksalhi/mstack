# Interface review

Route scope through each domain area, then merge into one ranked verdict. Report evidence, not taste.

For a branch, PR, commit range or uncommitted changes, diff against the merge base, never change the checkout, never pick `HEAD~1` yourself, never Approve an empty scope. Give each finding a Status (Introduced, Regression, Pre-existing); only the first two count toward the cap and verdict. Open [change-review.md](change-review.md) when resolving that target, its exclusions and consumers.

## Steps

1) Scope: Name the screen/flow/repo; include empty, loading, error, and 320px/narrow states. If too big for one pass, split flows across subagents and cover them all.

2) Recon: Note framework, styling system, tokens, and any preview command; read UI conventions (AGENTS.md, CLAUDE.md, design-system docs). Write fixes in the project’s idiom. A convention doesn’t excuse a finding. If a shared token/guideline is the cause, report it once against that source.

3) Domains, in order:
   1. [accessibility](../accessibility/index.md)
   2. [layout](../layout/index.md)
   3. [copy](../copy.md)
   4. [typography](../typography/index.md)
   5. [colors](../colors/index.md)
   6. [polish](../polish/index.md)
   7. [animate](../animate/index.md), use its Never-ship table
   8. [mobile-web](../mobile-web.md), only for phone or touch surfaces

   If a domain file can’t be read, mark Not reviewed; never rebuild its rules. An issue spanning two areas goes to the owner, reported once.

4) Evidence: Every finding cites file:line and the current code. Don’t report a runtime finding from source alone, or a code finding from a screenshot alone.

5) Severity: HIGH blocks/misleads/hides/risks loss/systemic. MEDIUM hurts comprehension/efficiency/consistency. LOW is isolated polish. Rank within a severity by reach; a token fix beats the same symptom in one leaf.

6) Fix ladder: delete → use the platform → reuse a project token → correct a value → add. Adding where deleting would work is a finding.

7) Consolidate: One root cause is one row listing every location. Max 15 findings; never pad.

8) Verify: Use the project’s checks. Anything you couldn’t run is Not verified, not a finding. A review is read-only unless the user also asked for fixes.

## Always HIGH

- Interactive control with no accessible name.
- Keyboard-reachable control with no visible focus indicator.
- Pointer-reachable control not reachable by keyboard.
- Motion ignoring prefers-reduced-motion.
- Content clipped or unreachable at 320px width or 200% zoom.
- Text contrast pair fails its ratio.
- Meaning by color alone.
- Destructive action with no confirm, no undo, and no distinct treatment.
- Truncation with no way to reach the full value.
- Content past a scroll edge or disclosure with no visible cue.
- Error that names no way to recover.
- A semantic color used against its meaning.
- State carried only by motion.

## Output

1) Scope, stack, and conventions found.
2) Coverage: Domain | Evidence inspected | Findings count, Clear, or Not reviewed (why).
3) Findings: Severity | Domain | Location | Before | After | Why. If none: “No actionable interface findings.”
4) Verification: each check with its command and result; list Not verified separately.
5) Verdict: Block if any HIGH remains, otherwise Approve. Never approve a domain you didn’t inspect.

A single-domain run uses the same table without the Domain column. Its empty result is “No actionable <domain> findings.”
