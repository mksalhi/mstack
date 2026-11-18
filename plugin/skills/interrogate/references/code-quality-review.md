# Code Quality Review

A strict lens each reviewer applies on top of the rubric: implementation quality, maintainability, abstraction quality, codebase health. Rank deletions and smaller diffs above restructurings (`scoper`); propose an extraction only when it removes code or branches. Hunt for "code judo": behavior-preserving restructurings that make the change dramatically simpler, smaller, more direct.

## Core Prompt

> Perform a deep code quality audit of the current branch's changes.
> Rethink how to structure / implement the changes to meaningfully improve code quality without impacting behavior.
> Work to improve abstractions, modularity, reduce Spaghetti code, improve succinctness and legibility.
> Be ambitious, if there is a clear path to improving the implementation that involves restructuring some of the codebase, go for it.
> Be extremely thorough and rigorous. Measure twice, cut once.

## Dimensions

Apply the relevant ones.

0. **Structural simplification.** Look for reframings that delete whole branches, helpers, modes, conditionals, or layers by using the existing architecture better. Delete complexity rather than rearrange it.
1. **1k-line files.** A PR pushing a file from under 1k to over 1k lines is a strong smell: decompose first (helpers, subcomponents, modules) unless a compelling structural reason keeps the file clearly organized.
2. **Spaghetti growth.** New ad-hoc conditionals, scattered special cases, or one-off branches in unrelated flows are a design problem, not a nit. Move the logic to a dedicated helper, state machine, or module.
3. **Clean the design.** If behavior can stay while structure gets meaningfully cleaner, push for it. Prefer removing moving pieces over spreading complexity around.
4. **Direct, boring code.** Flag brittle, ad-hoc, or magic behavior; generic mechanisms hiding simple data-shape assumptions; thin abstractions, identity wrappers, pass-through helpers.
5. **Types and boundaries.** Question needless optionality, `unknown`, `any`, or casts where a clearer type boundary could exist. Prefer explicit typed models over ad-hoc objects. A silent fallback papering over an unclear invariant should become an explicit boundary.
6. **Canonical layer and reuse.** Flag feature logic leaking into shared paths, implementation details leaking through APIs, and bespoke one-offs duplicating existing utilities. Move code to the right package, service, or module.
7. **Orchestration and atomicity.** Flag independent work serialized for no reason and related updates that can leave state half-applied, when the cleaner structure is obvious. Skip micro-optimizations.

## Output Expectations

Order: structural regressions and missed simplifications; spaghetti and branching; boundary, type, and file-size; smaller modularity and legibility.

## Approval Bar

Correct behavior is not enough. Presumptive blockers unless justified: incidental complexity a code-judo move would delete; a file pushed from below to above 1000 lines; ad-hoc branching tangling an existing flow; feature checks scattered across shared code; an unnecessary abstraction, wrapper, or cast-heavy contract; a duplicated helper or logic in the wrong layer when a canonical home exists. Otherwise leave explicit, actionable feedback pushing for cleaner decomposition.

## Review Tone

Direct and demanding, not rude. Don't soften major maintainability issues into mild suggestions. Say so when the code makes the codebase messier or misses an obvious dramatic simplification. Don't settle for "maybe rename this" when the issue is structural.
