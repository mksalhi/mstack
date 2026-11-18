### Visual parity

**You own pixel-exact equivalence. The baseline is the spec. Never touch it.** Verify by image diff, not by eye.

1. Before any migration, build a visual regression harness that screenshots the current component across its states, plus the target when matching two implementations. No baseline, no parity claim. This blocks everything after it.
2. No harness modifications, no baseline tampering, no restructuring a component to make a diff pass. If the baseline looks wrong, stop and ask.
3. Migrate one component at a time. Shared primitives migrate first as a blocking phase. Parallelize across worktrees, one owner per component (Separate before serializing shared state).
4. Image-diff each component against its baseline on the matching surface via the control skill. A nonzero diff fails. Investigate the pixel delta. `/loop` per component until the diff is zero.
5. Run **Opening a PR** per component or per safe batch.

**Reply:** components migrated, each diff result, the baseline harness location, what's left.
