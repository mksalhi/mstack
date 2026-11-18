---
name: debug
description: "Use when something is broken, throwing, failing, flaky or slow, or for TDD and regression tests. Triggers: 'debug', 'diagnose', 'why is this failing'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Diagnosing bugs

Run the phases in order. Skip one only with explicit justification.

## Fix root causes

- Reproduce first; ask "why" until you hit the root cause, and fix it there.
- No silencing guards (a nil check that hides a crash is a symptom fix). A workaround that needs a paragraph-long comment means the code is wrong.
- Fix the pattern: grep for every instance.
- Stuck? Instrument (logging, the actual error); don't guess.
- Read `GLOSSARY.md` (if it exists) and ADRs in the area you touch.
- **Fails after restart:** suspect stale persistent state before code (config, caches, lock files, serialized state). If clearing a state file restores behavior, make state validation the fix.

### Two fixes failed: attack the premise

When two or more fixes sharing one premise fail the same gate, suspect the premise.

- **Write the premise down**: the one sentence every failed fix assumed.
- **Take a census** of the imbalance per actor (which actors hold it, not how large) as a rerunnable script, per Build the lever (`principles`).
- **Read the skew.** If the same few actors hold most of it every run, find what assigns them that role; that is the next "why".
- **Remove the asymmetry instead of compensating.** Rotate, randomize, or move the role. Return paths, shared pools, batched hand-offs, or periodic rebalances leave the assignment in place.

Start the next fix only once the premise is written and the census exists. An even census means the premise is not the cause; look elsewhere and keep the census as evidence.

## Redact

Redact every secret as `<REDACTED>` in commands, outputs and artifacts you show. Build loops on env vars so credentials stay out of output. From captured artifacts (auth headers), quote only the signal lines. If redacted output is not enough, say so and ask the user.

## Phase 1: Build a feedback loop

This is the skill. Bisection, hypotheses and instrumentation all consume a **tight** pass/fail signal that goes red on _this_ bug. Spend disproportionate effort here.

Ways to build one, roughly in this order:

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

Tighten it: faster (cache setup, skip unrelated init, narrow scope), sharper (assert the specific symptom, not "didn't crash"), deterministic (pin time, seed RNG, isolate filesystem, freeze network). A 30-second flaky loop is barely better than none.

**Non-deterministic bugs:** aim for a higher reproduction rate, not a clean repro. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. 50% is debuggable, 1% is not; keep raising it.

**No loop possible:** stop and say so; list what you tried. Ask the user for (a) access to an environment that reproduces it, (b) a redacted artifact (HAR, log dump, core dump, timestamped recording), or (c) permission for temporary production instrumentation. Do not hypothesise without a loop.

**Done when** you name one command (script, test invocation, curl) you have already run, with its invocation and redacted output, that is:

- [ ] **Red-capable**: drives the actual bug path and asserts the user's exact symptom, so it goes red on this bug and green once fixed.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: unattended; a human only via `scripts/hitl-loop.template.sh`.

Reading code to build a theory before this command exists is the failure this skill prevents. No red-capable command, no Phase 2.

## Phase 2: Reproduce and minimise

Run the loop. Confirm it produces the failure the **user** described (not a nearby one), reproduces across runs (or at a debuggable rate), and captures the exact symptom (error, wrong output, timing) to verify the fix against.

Then shrink to the smallest scenario that still goes red: cut inputs, callers, config, data and steps one at a time, re-running after each. Done when every remaining element is load-bearing (removing any one turns it green). Do not proceed until reproduced **and** minimised.

## Phase 3: Hypothesise

Generate **3–5 ranked, falsifiable hypotheses** before testing any:

> "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

No statable prediction: discard or sharpen it. Show the ranked list to the user before testing; don't block on it if they're AFK.

## Phase 4: Instrument

Each probe maps to one Phase 3 prediction. Change one variable at a time.

1. **Debugger / REPL** if available.
2. **Targeted logs** at boundaries that distinguish hypotheses. Never "log everything and grep".

Tag every debug log with a unique prefix, e.g. `[DEBUG-a4f2]`, so cleanup is one grep.

**Perf regressions:** skip logs. Establish a baseline (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5: Fix and regression test

Write the regression test **before the fix**, and only at a **correct seam**: one that exercises the real bug pattern as it occurs at the call site. A too-shallow seam (single caller when the bug needs several, a unit test that can't replicate the chain) gives false confidence. No correct seam is itself a finding: note and flag it.

With a correct seam:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original (un-minimised) scenario.

Prefer no test over a bad one (tests mocks, encodes the implementation, depends on timing or global state, needs expensive infra for a small fix, or would be deleted after proving the fix). Without a good seam, the Phase 1 loop is the regression check.

- Never change a test to match a wrong implementation; never weaken an assertion unless expected behavior really changed.
- Keep the test on this bug; consider sibling coverage after, if the bug exposes a class.
- Flaky bug: make the test deterministic and name the signal it locks down.

Plain TDD on a simple bug: Phases 1–2 shrink to "write the failing test and watch it fail for the intended reason".

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The report names the failing-before check and its failure, and the passing-after run (or why failing-before could not be shown)
- [ ] The correct hypothesis is stated in the commit / PR message
