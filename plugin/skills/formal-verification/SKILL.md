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

Two modes:
- Create: choose where exhaustive checking matters most; verify one property; add a project-local skill that rechecks it.
- Maintain: bring an existing verification back in line with changed code.

## Rules for both modes

- True to the code: every model/harness/property references code a reviewer can open; each atomic verification step matches one atomic code step; use names from this repo.
- Able to fail: show each property failing on a minimal broken variant (e.g., removed check, reordered step).
- Findings stay findings: if current code breaks the property, report it with a counterexample in the code’s terms. Don’t weaken the property/model to pass. Edit only verification artifacts (models, harnesses, property files, the verify skill); never product code unless the user asks.
- Honest about scope: state what is verified, bounds and assumptions, and what’s left out.
- Readable without the tool: one plain sentence stating the property and the harm; counterexample as short steps in the code’s words.
- Cheap to rerun: one command, pinned/reproducible tool version, and fast enough for every relevant change.
- Kept in step with the code: record covered files/functions and the sync commit (the commit at which you last confirmed the verification describes them).

## Create

### Choose the target from the code
- Start from any area/bug the user named; ask only what the code can’t tell you.
- Pick the strongest user-facing promise where a break harms users and tests rarely hit it.

### Let the question choose the tool
- Bad event orderings → model checker over a small design model; TLA+ is the default in any language.
- Must behave for every input (memory safety, overflow, invariants) → code-level verifier. If none for this language: say so, and test the real code with generated inputs (not a hand model).
- Must hold at every size, beyond a bound → may need a proof assistant.
- Prefer tools repo developers can install/run, and say why you chose them.

### Generate the verify skill
- Write `.claude/skills/<name>/SKILL.md` with frontmatter naming the area and when to use it.
- From the skill alone, the next agent must know: covered code, how to run, how to tell a real bug from a modeling error, and how to update for intended changes.
- Include coverage and sync commit; advance the sync commit only after confirming the verification describes the code at the new commit.
- Use the repo’s real commands, paths, and names.

### Prove it before you hand off
- Make a temporary change that breaks the property in real code; the check must catch it.
- Drop the scratch change and confirm the check is back to passing (or failing only on true findings).
- If it misses the break or a step doesn’t run, fix the verification/skill, not the scratch.

### Hand off
- Tell the user: what you verified; the tool and why; bounds; findings in plain words; how to run; and what it doesn’t cover.
- Suggest a second target only if close.
- Point at `/mstack:formal-verification` for resyncing after changes that skipped the recheck.

## Maintain

End each check as in sync (nothing since the sync commit alters it, passes), updated (now describes the changed code, passes), bug (describes current code, which breaks the property) or blocked (couldn't align or run; say exactly why).

1. Find the checks (usually under `.claude/skills/`) with each one's property, covered code, bounds, run command and sync commit. No verify skill means switch to Create. No recorded sync commit means use the last commit that changed the verification files, and say so.
2. Run each once and record the result. Judge failures only at step 5.
3. Diff covered code from the sync commit to now, including moved, renamed or split code and new code touching guarded state. Classify each change as no effect, verification stale, promise changed on purpose (cite evidence), or promise may be broken.
4. Update from the code, not from the result. Change a property only for an intended promise change and record old wording, new wording and evidence. Keep bounds unless wrong; report any reduction.
5. Rerun and judge. On a pass, break the new code the way the property guards, confirm the check catches it, and drop the break. On a fail, replay the counterexample against real code. A step that can't happen means the verification is wrong, so fix it and say what was wrong. All steps possible means a bug, so name the introducing commit, give the steps in the code's words and the harm in one sentence.
6. Update the verify skill's covered code, commands, bounds and sync commit (the commit you checked; never move it for a blocked check). Then follow the skill once to confirm its steps run.

Report per check the outcome, commits read, what changed in the verification and why, the break that proved it can still fail, each bug in plain words, what stays uncovered, and which failures were drift versus code bugs. Put verification updates in their own change, apart from any product fix.
