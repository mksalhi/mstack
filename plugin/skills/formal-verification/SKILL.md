---
name: formal-verification
description: "Use to formally verify a race, retry, state machine, parser or unsafe code tests can't reach, leaving a skill that rechecks it, or to resync that model. Triggers: 'model-check this', 'prove this invariant', 'is the model still true to the code'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
  requires: "Java 11+ and TLA2TOOLS"
---

# Formal verification

Two modes, picked by whether a verify skill already covers the area:

- **Create**: find where exhaustive checking matters most, verify one property there, and leave a project-local skill that rechecks it.
- **Maintain**: bring an existing verification back in line with code that changed without it. A stale check can keep passing on code that no longer exists, and that pass looks like a proof.

Driving the running app like a user is `verifier`'s job. The user must be able to trust and act on the result without learning the verification language.

## Rules for both modes

- **True to the code.** Every model or proof part points to code a reviewer can open; what the verification treats as one atomic step is atomic in the code; names come from this repo.
- **Able to fail.** Show each property failing on a broken variant of the code it guards (a removed check, a reordered step).
- **Findings stay findings.** When current code breaks the property, report it with the counterexample in the code's terms. Never weaken the property or model until it passes. Edit only the verification (models, harnesses, property files, the verify skill), never product code unless the user asks.
- **Honest about scope.** State what is verified, under which bounds and assumptions, and what is left out.
- **Readable without the tool.** The property and the harm in one plain sentence each; a counterexample as a short step sequence in the code's words.
- **Cheap to rerun.** One command, a reproducible tool version, a run short enough to use on every relevant change.
- **Kept in step with the code.** Record the files and functions each check covers and the commit at which you last confirmed the verification describes them (the sync commit).

## Create

### Choose the target from the code

Start from any area or bug the user named, and ask only what the code can't tell you. Pick the strongest promise the code makes where a break harms users and tests rarely reach the breaking case, not the easiest one to verify.

### Let the question choose the tool

Pick the cheapest tool that answers the question:

- Bad event orderings → model checker over a small design model; TLA+ is the default in any language.
- Code behaving for every input (memory safety, overflow, data-structure invariants) → a verifier that runs on the code. None for this language: say so, and test the real code with generated inputs, not a hand model.
- Must hold at every size, beyond a bound → may need a proof assistant.

Prefer tools the repo's developers can install and run, and say why you chose it.

### Generate the verify skill

Write `.claude/skills/<name>/SKILL.md` with frontmatter naming the area and when to use it (without frontmatter it never registers). From the skill alone, the next agent must be able to tell whether a change touches verified code, run the check, tell a real bug from a modeling error, and update the verification for intended changes. Include the coverage record and sync commit, and say to advance the sync commit only after confirming the verification describes the code at the new commit. Use the repo's real commands, paths and names.

### Prove it before you hand off

Follow the generated skill once, as the next agent would, on a scratch change that breaks the property in real code. It must catch the break. Drop the scratch change and confirm the check is back to passing, or failing only on findings you will report. If it misses the break or a step doesn't run, fix the skill or verification, not the scratch change. An unrun skill is a draft.

### Hand off

Tell the user: what you verified, the tool and why, the bounds, what it found in plain words, how to run it, and what it doesn't cover. Suggest a second target only if you found a close one. Point at `/mstack:formal-verification` for resyncing after changes that skipped the recheck.

## Maintain

Applies to a skill generated in Create mode, or any project-local skill running a model checker, prover, or code-level verifier against named code.

### Outcomes

Give each check one outcome and say which (updated and bug can combine):

- **in sync**: nothing since the last sync alters what the check describes, and it passes.
- **updated**: the verification now describes the changed code, and it passes.
- **bug**: the verification describes current code and the code breaks the property. A code finding, not drift.
- **blocked**: couldn't be brought in line or couldn't run. Say exactly why.

### Pass

1. **Find the checks.** Search by behavior (usually under `.claude/skills/`) for a project skill running a verifier against named code, or use the one the user named. For each check collect the property, covered code, bounds and assumptions, run command, and sync commit. No verify skill → stop and switch to Create. No recorded sync commit → use the last commit that changed the verification files, and say so.

2. **Run it as it is.** Run each check once before changing anything; record the result. A pass only means the old description holds; don't classify a failure as drift or bug until step 5.

3. **Read every change to covered code.** Diff covered files from the sync commit to now and read each commit message. Include moved code (a renamed, split, or relocated covered function) and new code touching guarded state (e.g. a new function writing the same fields). Classify each change:
   - **No effect**: alters nothing the verification describes (formatting, comments, uncovered paths). Check against the model or harness, not the commit message.
   - **Verification no longer describes the code**: an atomic step became two, a branch added or removed, a check moved, a new path reaches guarded state, a value's range changed. The model or harness must change.
   - **Promise changed on purpose**: evidence in the change (doc comment, tests, changelog, commit message) says it's intended. The property must change; cite the evidence.
   - **Promise may be broken**: no such evidence. Treat a following failure as a bug candidate.

4. **Update from the code, not from the result.** Write the update from the code before rerunning: each changed part points to code a reviewer can open, one atomic code step stays one verification step. Change a property only for an intended promise change, recording old wording, new wording, and evidence. Keep bounds unless the change makes them wrong; report any reduction.

5. **Rerun and judge each result.**
   - **Pass:** break the new code the way the property guards against (remove a new check, reorder a new step), confirm the check catches it, drop the break.
   - **Fail:** replay the counterexample against the real code step by step. A step that can't happen in code → the verification is wrong; fix it and say what was wrong. Every step possible → bug: name the introducing commit, give the counterexample as steps in the code's words, and state the harm in one sentence. A cheap test or repro against real code may go in the report as evidence; never commit it to product code.

6. **Update the verify skill**: covered code, commands, bounds, assumptions, and sync commit (set to the commit you checked; don't move it for a blocked check, and say so). Then follow the skill once as the next agent would to confirm its steps run.

### Report

For each check:

- the outcome and the commits you read;
- what changed in the verification, each with a short reason: code changed shape, or promise changed on purpose (with evidence);
- the rerun result and the break that showed the updated check can still fail;
- each bug in plain words: counterexample steps in the code's words, the harm, the introducing commit;
- what remains uncovered, including new code it should cover.

Say outright which failures were verification drift and which were code bugs. For a check that passed before updating and fails after, say the old pass was on a stale description.

Put verification updates in their own change, separate from any product fix.
