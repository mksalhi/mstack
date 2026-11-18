### Trace forensics

**You own the diagnosis from the artifact.** The capture already exists (unlike **Runtime forensics**): read it, don't re-run it. Generic tooling: a DevTools or trace parser for cpuprofile and `.json.gz`, a text editor for a spindump, heap tooling for a heapsnapshot.

1. Identify the format and load it. Parse large artifacts in a subagent and keep only the reduced finding (Guard the context window).
2. Dump the trace or heap snapshot into sqlite, one row per sample, frame, or node, before reading.
3. Narrow to the cause. Query the frames holding the most time and walk the call tree to the hot path. Leak: follow the retainer chain to a GC root. Spindump: find the thread stuck on-CPU or blocked and its wait reason.
4. Map the hot frame to file, symbol, and line via the artifact's symbols. An unmapped frame is not a diagnosis: resolve the symbols or say the artifact lacks them.
5. With a paired capture, diff before and after to confirm. Otherwise label the finding the strongest hypothesis the artifact supports.
6. Hand back a cited diagnosis, no fix unless asked; route to Bug fix or Perf issue. Throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only forensics`.

**Reply:** artifact and format, reduced finding, source location, artifact paths, whether a paired capture confirmed it.
