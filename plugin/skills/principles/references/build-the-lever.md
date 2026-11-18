# Build the lever

Rule: Build a script, codemod, or generator instead of working by hand. Default to the lever; skip only trivial, obvious edits.

- Do the first unit by hand, then build the tool; rerun on that unit and diff; make safe to rerun.
- Use: codemod/script for edits; generator for repetitive files; dump-to-sqlite query for analysis; rerunnable check for verification.
- Prefer one deterministic pass you run yourself over fan-out.
- If fanning out, write the lever as a skill they all read (recipe, verification contract, do-not-touch fences), outside their write scope so they can't edit the contract.
- If cited with no codemod, script, generator, or delegate skill in the diff, you didn’t apply it.
- The bar is triviality, not repetition; a one-off earns a lever when it makes results checkable. Per [scoper](../../scoper/SKILL.md), build the smallest script, never a framework.
