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

The chart shows what an app's user sees, for a PM to judge. Label states with what is on screen ("Paying") and steps with what the user does or sees happen ("tap Pay", "the charge goes through"); no variable or action names in labels. The scripts call this user the reader (`readerActions`, reader steps).

Run `node <mstack>/skills/statechart/scripts/statechart.mjs --help` for commands and how to read a chart. TLC needs Java 11+ and `TLA2TOOLS` set to the path of `tla2tools.jar`; `--png` fetches `@mermaid-js/mermaid-cli` through `npx`. Work in a scratch folder outside the repo; output lands next to the input.

## Pick the direction

`from-spec` when a TLA+ model exists or the code is concrete enough to model. `from-chart` when there is no model and the PM should agree on behavior before code is written or changed.

If the code has a TLA+ spec, start from a copy: add the user-visible variables and keep its invariants. To audit code against that spec, make the copy model what the code does and pass the spec unchanged as `--against`, checked with the config its authors say it passes (pass it as `--against-config` unless it has the spec's file name). One mapping labels both models, so label only from variables both have. In a code model or new spec, tie every variable and action to openable code and name it from that code; each action is one atomic code step; comment each action condition with the file and line that checks it, as in `\* pay.ts:120`.

## Spec to chart

1. Choose states. Name what the PM cares about but the screen hides ("Paying, charged twice"). Start with few states; split only to separate two bugs.
2. Write each PM-agreed rule as one invariant, with the PM's sentence as its comment. Each rule names what the user sees on a screen or gets from a request, and the code that can change it; refuse a rule missing either. For rules that apply once things settle, define `Settled == ~ENABLED System`, `System` being the disjunction of non-user actions. Report each broken rule as a bug; never weaken a rule to make the chart pass.
3. Run `from-spec` and fill in its mapping file: labels in `state` and `step`, user actions in `readerActions` by action name. When two bugs end on the same screen via different code paths, add `cause` naming the code path. To color states by PM concern ("Toast shown"), return that group from `group`; the legend names groups, and rule-breaking states keep a red border.
4. If there is an open fix, model it from the code and pass it as `--fixed`.
5. Render each chart with `--png` and look at every PNG: each numbered path reads in order; a label reading like code means fix `state` or `step` and rerun.
6. Replay each bug's story against real code (test or live repro), one step per model action. Drive only user- or client-reachable entry points and assert only what they see; a test asserting a flag it set, or searching source text, proves nothing. Say which part a run proves and which part code reading proves. A test copying code it can't import gives the copy's commit and line range and what it leaves out. A bug that doesn't reproduce means the model is wrong until shown otherwise: fix the model, not the rule.

## Chart to spec

1. Draw the PM-agreed chart: one region per independently changing thing (connection, sync badge), one `%% never` line per rule with the PM's sentence, and "the app closes" as an edge to the state the user sees next.
2. Run `from-chart`. A broken rule is a design bug in the agreed chart; take it to the PM.
3. Add the real code's guards and variables to the spec `from-chart` wrote and rerun. For each printed difference, ask the PM whether the code is wrong or the chart needs correcting.

## Hand off

Give the PM each chart's PNG and Mermaid source, plus one line per bug: the rule it breaks, its steps as the chart numbers them, whether it reproduced, and whether the open fix fixes it. With `--against`, also say whether the spec already lists it (in configs `stories.md` names, in the spec's notes on what the model leaves out, or not at all). Never report a rule holds while the command lists conditions with no file and line. Take every quoted count from `summary.json`. Attach `stories.md` and the regenerate command. Say what the model leaves out.
