---
name: debug
description: "Use when something is broken, throwing, failing, flaky or slow, or for TDD and regression tests. Triggers: 'debug', 'diagnose', 'why is this failing'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Diagnosing bugs

Run phases in order. Skip one only with a stated reason.

## Fix root causes

- Reproduce, ask “why” to the root cause, fix there.
- No silencing guards (e.g., nil checks that hide crashes).
- Grep for all instances of the pattern; fix them.
- Stuck? Instrument; don’t guess.
- Read `GLOSSARY.md` and ADRs.
- If failure survives restart, suspect stale persistent state (config, caches, lock files). If clearing fixes it, add state validation.

### Two fixes failed: attack the premise

- Write the one-sentence premise those fixes assumed.
- Test it directly with a rerunnable script.
- Start the next fix only after this test. If the premise holds, look elsewhere and keep the script as evidence.

## Redact

- Replace every secret with `<REDACTED>` in commands, output, and artifacts.
- Read credentials from env vars.
- From captured artifacts, quote only relevant lines.

## Phase 1: Build a feedback loop

- Produce a fast, deterministic pass/fail that goes red on this bug.
- Prefer: failing test; curl/HTTP script; CLI with fixture diffing stdout; headless browser assertions; bisection harness (`git bisect run`); differential loop; HITL last resort: `scripts/hitl-loop.template.sh`.
- Make it faster, sharper (assert exact symptom), deterministic (pin time/seed; isolate filesystem/network).
- For flaky bugs: raise repro rate (loop many times, parallelize, stress, narrow timing, inject sleeps). 50% is debuggable; 1% is not.
- If no loop: stop; list attempts; ask for a reproducing environment, a redacted artifact (HAR, logs, core dump, recording), or permission for temporary production instrumentation. Don’t hypothesize without a loop.
- Done when you can name one command you already ran, with invocation and redacted output, that is:
  - Red-capable: drives the actual bug path and asserts the user’s exact symptom.
  - Deterministic.
  - Fast (seconds).
  - Agent-runnable; a human only via `scripts/hitl-loop.template.sh`.
- No red-capable command, no Phase 2.

## Phase 2: Reproduce and minimise

- Run the loop; confirm the failure rate is debuggable.
- Minimise inputs, callers, config, data, and steps until removing any remaining element turns it green.

## Phase 3: Hypothesise

- Generate 3–5 ranked, falsifiable hypotheses with predictions. Discard any without a prediction.
- Show the ranked list to the user before testing.

## Phase 4: Instrument

- Each probe tests one Phase 3 prediction; change one variable at a time.
- Prefer debugger/REPL, then targeted boundary logs; tag with a unique prefix like “[DEBUG-a4f2]” for easy grep/cleanup.
- Perf regressions: skip logs; take a baseline (timing harness, profiler, query plan), then bisect.

## Phase 5: Fix and regression test

- Write the regression test before the fix at a seam that exercises the bug at the call site. If no correct seam, say so.
- Turn the minimised repro into a failing test; watch it fail. Apply the fix; watch it pass. Re-run the Phase 1 loop against the original scenario.
- Never change a test to match a wrong implementation, or weaken an assertion unless expected behavior changed. For flaky bugs, make the test deterministic. Without a good seam, the Phase 1 loop is the regression check.

## Phase 6: Cleanup

- The Phase 1 loop no longer reproduces the bug.
- The regression test passes, or the missing seam is documented.
- “[DEBUG-…]” instrumentation is removed (grep the prefix).
- Throwaway prototypes are deleted.
- The report shows failing-before and passing-after, or why failing-before couldn’t be shown.
- The commit or PR message states the confirmed hypothesis.
