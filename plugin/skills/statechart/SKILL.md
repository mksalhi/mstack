---
name: statechart
description: "Use to show a PM what a user sees as a Mermaid statechart checked by a TLA+ model, or to turn an agreed chart into a TLA+ skeleton. Triggers: 'statechart', 'show the PM the bug'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
  requires: "Java 11+ and TLA2TOOLS"
---

# Statechart

- Label states and steps with what’s on screen and what the user does or sees happen; no variable or action names in labels. The scripts call this user the reader (readerActions, reader steps).

Run:
`node <mstack>/skills/statechart/scripts/statechart.mjs --help`
- TLC needs Java 11+ and TLA2TOOLS set to the path of tla2tools.jar.
- --png fetches @mermaid-js/mermaid-cli through npx.
- Work in a scratch folder outside the repo; output lands next to the input.

## Pick the direction
- Use from-spec when a TLA+ model exists or code is concrete enough; from-chart otherwise.
- If code has a TLA+ spec, start from a copy: add user-visible variables and keep its invariants.
- To audit code against that spec, make the copy model what the code does and pass the spec unchanged as --against, checked with the config its authors say it passes (pass it as --against-config unless it has the spec’s file name).
- One mapping labels both models; label only from variables both have.
- In a code model or new spec: tie every variable and action to openable code and name it from that code; each action is one atomic code step; comment each action condition with the file and line that checks it, as in \* pay.ts:120.

## Spec to chart
- Choose states the PM cares about; split only to separate two bugs.
- Each PM-agreed rule is one invariant with the PM’s sentence as its comment. Each rule must name what the user sees or gets and the code that can change it; refuse a rule missing either.
- For “after it settles” rules, define Settled == ~ENABLED System, System being the disjunction of non-user actions.
- Report each broken rule as a bug; never weaken a rule to make the chart pass.
- Run from-spec and fill its mapping: labels in state and step; user actions in readerActions by action name. If two bugs end on the same screen via different code paths, add cause naming the code path. To color by PM concern, return group; rule-breaking states keep a red border.
- If there is an open fix, model it from the code and pass it as --fixed.
- Render with --png and read every PNG; fix any label that reads like code and rerun.
- Replay each bug’s story against real code, one step per model action. Drive only user- or client-reachable entry points and assert only what they see; grepping source or asserting your own flags proves nothing. Say which part a run proves vs code reading. If a test copies code it can’t import, give the copy’s commit and line range and what it leaves out. A non-repro means the model is wrong until shown otherwise: fix the model, not the rule.

## Chart to spec
- Draw the PM-agreed chart: one region per independently changing thing, one %% never line per rule (with the PM’s sentence), and “the app closes” as an edge to the next visible state.
- Run from-chart. A broken rule is a design bug; take it to the PM.
- Add real code’s guards and variables to the spec from from-chart and rerun. For each difference, ask whether code is wrong or the chart needs correcting.

## Hand off
- Give the PM each chart’s PNG and Mermaid source, plus one line per bug: the rule it breaks, the numbered steps, whether it reproduced, and whether the open fix fixes it.
- With --against, also say whether the spec already lists it (in configs stories.md names, in the spec’s notes, or not at all).
- Never report a rule holds while the command lists conditions with no file and line. Take every quoted count from summary.json. Attach stories.md and the regenerate command. Say what the model leaves out.
