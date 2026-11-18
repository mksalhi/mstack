# Build the lever

**Rule:** Build a script, codemod or generator instead of working by hand.

When the work isn't trivial, build the tool that does it instead of doing it by hand. A deterministic script reruns for free and gives the reviewer one artifact to read and rerun: "trust me" becomes "run this".

Default to the lever. Skip it only for trivial tasks: a couple of obvious edits visible at a glance.

- Do the first unit by hand to learn the recipe, then build the tool. Prove it by rerunning on that unit and diffing against the hand version. Make it safe to rerun.
- Codemod or script for edits, generator for repetitive files, dump-to-sqlite query for analysis, rerunnable check for verification.
- A deterministic lever beats fan-out: if the tool covers every unit in one pass, run it yourself; don't fan out delegates to hand-apply it.
- When fanning out to subagents, write the lever as a skill they all read (recipe, verification contract, do-not-touch fences), outside their write scope so they can't edit the contract.
- Applying this produces a file. Cited this principle with no codemod, script, generator, or delegate skill in the diff? You didn't apply it.
- Commit the lever when the work outlives the session.

The bar is triviality, not repetition: a one-off earns a lever when the lever makes it checkable. Per [`scoper`](../../scoper/SKILL.md), build the smallest script that does or proves the job, never a framework.

Distinct from [Encode lessons in structure](encode-lessons-in-structure.md) (recurring instruction to guardrail); this is throughput and reviewability now. [Prove it works](prove-it-works.md) decides what a verification lever must observe.
