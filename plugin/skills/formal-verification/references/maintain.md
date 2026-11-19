# Maintain

Applies to a project-local skill running a model checker, prover, or code-level verifier against named code.

## Outcomes
- in sync: nothing since last sync alters what the check describes, and it passes.
- updated: verification now describes the changed code, and it passes.
- bug: verification describes current code and the code breaks the property.
- blocked: couldn’t align or couldn’t run; say exactly why.

## Pass
1. Find the checks (usually under `.claude/skills/`). For each, collect the property, covered code, bounds/assumptions, run command, and sync commit. No verify skill → switch to Create. No recorded sync commit → use the last commit that changed the verification files, and say so.
2. Run it once; record the result. Don’t judge failures until step 5.
3. Diff covered code from the sync commit to now (include moved/renamed/split code and new code touching guarded state). Classify each change: no effect; verification no longer describes the code; promise changed on purpose (cite evidence); promise may be broken.
4. Update from the code, not from the result. Keep atomicity; change a property only for an intended promise change (record old wording, new wording, and evidence). Keep bounds unless wrong; report any reduction.
5. Rerun and judge. Pass: break the new code the way the property guards; confirm it catches; drop the break. Fail: replay the counterexample against real code. If a step can’t happen → verification wrong; fix and say what was wrong. If all steps possible → bug: name the introducing commit, give counterexample steps in the code’s words, and state the harm in one sentence. A cheap test/repro may go in the report; never commit it to product code.
6. Update the verify skill: covered code, commands, bounds, assumptions, and sync commit (set to the commit you checked; don’t move it for a blocked check). Then follow the skill once to confirm its steps run.

## Report
For each check: outcome and commits read; what changed in the verification with reason (code shape vs intended promise change with evidence); rerun result and the break used to show the updated check can still fail; each bug in plain words (counterexample steps, harm, introducing commit); what remains uncovered, including new code it should cover; which failures were verification drift vs code bugs. Put verification updates in their own change, separate from any product fix.
