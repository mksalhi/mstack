### Trace forensics

- Read existing artifact; do not re-run capture.
- Dump trace/heap into sqlite before reading: one row per sample, frame, or node.
- Find cause: query top-time frames; walk hot path. Leak: follow retainers to GC root. Spindump: find on-CPU/blocked thread and wait reason.
- Map hot frame to file, symbol, and line via artifact symbols. Unmapped isn’t a diagnosis: resolve symbols or state they’re absent.
- If paired capture exists, diff to confirm; else give strongest supported hypothesis.
- Deliver cited diagnosis; no fix unless asked; route to Bug fix or Perf issue. Throughput checkpoint: `throughput checkpoint: n/a, read-only forensics`.
- Reply: artifact and format; reduced finding; source location; artifact paths; whether a paired capture confirmed.
