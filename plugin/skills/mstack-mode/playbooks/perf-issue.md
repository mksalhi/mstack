### Perf issue

- Own measurement; tie every fix to a measurement.
- Capture a baseline trace via matching control skill.
- Use strategies only when the trace shows their signal: elimination (needs the how pass), caching (name invalidation first), scheduling off the interactive path (measure that path, not total work).
- Plan from the trace; architect across boundaries. After each attempt, capture a post-fix trace; verify.
- Parse/compare artifacts (JSON to sqlite, diff). Flag "inconclusive" or wrong-surface.
- Cite the measurement in the PR.
- Reply: baseline number, post-fix number, delta, artifact path.
