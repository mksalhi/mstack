---
name: debug
description: "Use when something is broken, throwing, failing, flaky or slow, or for TDD and regression tests. Triggers: 'debug', 'diagnose', 'why is this failing'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Diagnosing bugs

Run the phases in order. Skip one only with a stated reason.

## Fix root causes

- Reproduce first, ask "why" until you reach the root cause, and fix it there.
- No silencing guards: a nil check that hides a crash fixes a symptom. A workaround that needs a paragraph of comment means the code is wrong.
- Grep for every instance of the pattern and fix them all.
- Stuck? Instrument; don't guess.
- Read `GLOSSARY.md` and ADRs in the area, if they exist.
- **Fails after restart:** suspect stale persistent state (config, caches, lock files) before code. If clearing it fixes things, make state validation the fix.

### Two fixes failed: attack the premise

When two fixes sharing one premise fail the same check, suspect the premise.

1. Write the premise down: the one sentence every failed fix assumed.
2. Test it directly with a rerunnable script. For an imbalance (load, contention, leaks), count it per actor: which actors hold it, not how much.
3. If the same few actors hold most of it every run, find what assigns them that role; that is the next "why". Remove the asymmetry (rotate, randomize, move the role) instead of compensating for it.

Start the next fix only after steps 1 and 2. If the premise checks out fine, look elsewhere and keep the script as evidence.

## Redact

Show every secret as `<REDACTED>` in commands, output and artifacts. Read credentials from env vars so they stay out of output. From captured artifacts, quote only the lines that matter.

## Phase 1: Build a feedback loop

This is the skill. Everything after it needs a fast, deterministic pass/fail signal that goes red on _this_ bug. Spend most of your effort here.

Ways to build one, roughly in order:

1. **Failing test** at whatever seam reaches the bug.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) asserting DOM, console or network.
5. **Replay a captured trace** (request, payload, event log) through the code path in isolation.
6. **Throwaway harness**: a minimal subset (one service, mocked deps) hitting the bug path with one call.
7. **Property / fuzz loop**: for "sometimes wrong output", run 1000 random inputs.
8. **Bisection harness**: the bug appeared between two known states, so automate boot-and-check and `git bisect run` it.
9. **Differential loop**: same input through old vs new version (or two configs), diff outputs.
10. **HITL bash script**, last resort: if a human must click, drive them with `scripts/hitl-loop.template.sh`.

Make it faster (cache setup, narrow scope), sharper (assert the exact symptom, not "didn't crash") and deterministic (pin time, seed RNG, isolate the filesystem and network). A 30-second flaky loop is barely better than none.

**Non-deterministic bugs:** raise the reproduction rate: loop the trigger 100 times, parallelize, add stress, narrow timing windows, inject sleeps. 50% is debuggable, 1% is not.

**No loop possible:** stop and list what you tried. Ask the user for an environment that reproduces it, a redacted artifact (HAR, logs, core dump, recording), or permission for temporary production instrumentation. Don't hypothesize without a loop.

**Done when** you name one command (script, test invocation, curl) you have already run, with its invocation and redacted output, that is:

- [ ] **Red-capable**: drives the actual bug path and asserts the user's exact symptom, so it goes red on this bug and green once fixed.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: unattended; a human only via `scripts/hitl-loop.template.sh`.

No red-capable command, no Phase 2. Building a theory from code before it exists is the failure this skill prevents.

## Phase 2: Reproduce and minimise

Run the loop. Confirm it shows the failure the **user** described, not a nearby one, at a debuggable rate.

Then shrink it: cut inputs, callers, config, data and steps one at a time, rerunning after each. Done when removing any remaining element turns it green.

## Phase 3: Hypothesise

Generate **3–5 ranked, falsifiable hypotheses** before testing any:

> "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

Discard or sharpen any hypothesis without a prediction. Show the ranked list to the user before testing, without waiting for a reply.

## Phase 4: Instrument

Each probe tests one Phase 3 prediction; change one variable at a time. Prefer a debugger or REPL, then targeted logs at the boundaries that tell hypotheses apart, never "log everything and grep". Tag debug logs with a unique prefix such as `[DEBUG-a4f2]` so cleanup is one grep.

**Perf regressions:** skip logs. Take a baseline (timing harness, profiler, query plan), then bisect.

## Phase 5: Fix and regression test

Write the regression test **before the fix**, at a seam that exercises the bug as it happens at the call site. A seam too shallow to replay the real chain gives false confidence; if there is no correct seam, say so.

With a correct seam:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original (un-minimised) scenario.

No test beats a bad one: one that tests mocks, encodes the implementation, depends on timing or global state, or needs expensive infrastructure for a small fix. Without a good seam, the Phase 1 loop is the regression check.

- Never change a test to match a wrong implementation, or weaken an assertion unless the expected behavior changed.
- For a flaky bug, make the test deterministic.

For plain TDD on a simple bug, Phases 1-2 shrink to "write the failing test and watch it fail for the intended reason".

## Phase 6: Cleanup

Before declaring done:

- [ ] The Phase 1 loop no longer reproduces the bug.
- [ ] The regression test passes, or the missing seam is documented.
- [ ] `[DEBUG-...]` instrumentation is gone (grep the prefix).
- [ ] Throwaway prototypes are deleted.
- [ ] The report shows the check failing before and passing after, or why failing-before couldn't be shown.
- [ ] The commit or PR message states the confirmed hypothesis.
