# Prove it works

Verify against the real artifact, not a proxy.
- Check process liveness directly.
- Read actual values, not cached/derived.
- On failure, suspect the observation before the system.

Make rerunnable checks as a lever per [Build the lever](build-the-lever.md).

Per unit: bracket each change—known-good, one change, run the check. Advance only on green; failures localize to that unit.

Start from trunk. Rebase only unpushed; merge trunk into pushed/long-lived. Run per-unit checks even when automated.

Delivery order: red then green; scaffold first; subtraction before reshape; baseline before treatment; small, single-purpose commits.
