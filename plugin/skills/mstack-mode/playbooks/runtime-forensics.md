### Runtime forensics

**You own the diagnosis. Instrument the live process, don't theorize from source.** The deliverable is a cited diagnosis, not a fix.

1. Capture a real artifact on the matching surface via the control skill: CPU profile for a spinning process, heap snapshot for a leak, CDP trace for a visual glitch.
2. Reduce it to the cause: the hot-path function, the retainer chain from the leaked object to a GC root, the loop firing without input. Parse large artifacts in a subagent (Guard the context window) and keep the reduced finding in the main thread.
3. Prove the mechanism cheaply: inject instrumentation via CDP eval on the running process, or hotfix the live code without reloading.
4. Map the finding to source: file, symbol, the line that allocates or schedules.
5. Throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only forensics`.

**Reply:** the signal captured, the reduced finding, how you proved the mechanism, the source location, artifact paths. No fix unless asked. Hand back to Bug fix or Perf once the cause is known.
