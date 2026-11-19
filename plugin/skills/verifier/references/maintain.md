# Maintain

Upkeep for a project-local verification skill with a feature map. Cover every feature file from source and drive every feature live at least once; not every bullet needs its own drive.

The outcomes and edit scope in `SKILL.md` Maintain apply. Behavior the map describes that the app no longer does is doc drift (fix the map) or a product regression (report it).

## Pass

0. **Locate the target**: the project-local skill with launch/drive sections and a feature map (usually `.claude/skills/verify-*/`). Several → ask which; none → stop and point at Create mode.
1. **Index hygiene.** Read the feature map README, glob its siblings, fix missing, extra, duplicate, or dead entries. No generated inventory.
2. **Source wave.** One read-only subagent per feature file, concurrently. Each explains how the feature works from source, flags likely drift with citations, and returns one live-verification recipe. Children never drive the app or edit files. Return shape: feature summary / source entry points / likely drift or none / one recipe.
3. **Reconcile.** Every feature file has a summary. Merge recipes into as few app states as practical. Spot-check cited drift; don't re-prove clean claims. Sweep recent churn for user-facing surfaces missing from the map, citing a concrete source path for each.
4. **Live pass**, required even when source looks clean. The coordinator owns all driving, following the skill's own Launch model (one long-lived instance driven serially for servers/UIs, a fresh isolated session per drive for short-lived CLIs). Exercise every feature at least once. Hold three invariants throughout:
   1. Never drive an instance not health-checked since it last surprised you: doctor before first drive, on each fresh session where sessions are the unit, and after any failed drive; where doctor can't see the failure (wedged UI on a healthy process), reset to a known state or relaunch.
   2. Evidence captured so far survives every cleanup, checked at its named location.
   3. Nothing a drive started outlives its usefulness: clean failed-iteration residue whether the session is stuck, exited, or shared (shared: clean the residue, not the instance).

   A doctor failure caused by skill drift is drift: fix it under edit scope and retry once (restart only what the fix invalidated) before calling the pass `blocked`. A feature is `verified-unreachable` only with the concrete prerequisite (auth, entitlement, OS, external state) and the route attempted; a prerequisite the map omits is drift. Re-drive any triage harness fix live before it ships. Final teardown follows the last drive, including re-proofs; evidence stays.
5. **Triage.** Wrong or missing user-POV description → doc drift, fix it. Working behavior the harness can't drive → harness gap, fix it (helpers rule applies). Actually broken app behavior → product gap; record it for the user, keep it out of this PR.
6. **Ship or stop.** Changed: one PR of proven corrections, re-reading every changed file first. Clean or blocked: no PR; report outcome and coverage honestly.

Keep concise run notes (features covered, unreachable prerequisites, confirmed drift, outcome) in a scratch location; don't commit them.
