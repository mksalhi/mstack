

######## TASK ambition-estimate

## Request given to the model

Before you start: how long will it take you to add offline sync with conflict resolution to our React Native notes app? About 40 screens, an Express backend, Postgres, Jest tests, and a Detox e2e suite. Give me your estimate and plan. You can't run commands here, so answer in this reply.

## Assertions
1. Sizes the work in agent terms (sessions, hours of agent time, files, subagents or verification runs), not as days or weeks of a human engineer's time.
2. Proposes building the whole feature now rather than a reduced MVP, a spike, or a phased multi-week rollout that waits on approvals.
3. Names concrete verification that would prove it works: tests for the conflict logic plus driving the real app (e.g. Detox or a simulator) through offline edits, reconnect and a conflict.
4. Does not end by asking permission or a list of clarifying questions it could have defaulted; any open question comes with the default it would take.

=============== RESPONSE ambition-estimate-00 ===============

**Estimate: 10–20 hours of agent execution, unmeasured.** That is my planning guess for implementation and verification, not a delivery commitment. The goal is for users to edit notes offline without losing work, and for maintainers to have one sync path rather than separate logic in 40 screens. I have not inspected the repo or run the suites.

The estimate assumes text notes, a shared client data layer, and working Jest and Detox setups. I’d budget for roughly **20–35 changed files, one owner with two parallel implementation workstreams, and 4–6 verification runs or batches**. My inference is that the number of distinct note write paths matters more than the screen count. Direct API writes scattered across screens, offline attachments, or collaborative rich-text editing would push the estimate up.

### Plan

1. **Trace the note flows and settle the sync contract.** Inventory every read and mutation path, including delete and restore if supported. Define the records first: a local note, a pending mutation with a unique operation ID and base revision, a server revision, a deletion marker, and a pull cursor.
2. **Build the Express and Postgres sync path.** Apply mutations and record their operation IDs in the same transaction so retries cannot apply a change twice. Return changes in a stable order so clients can resume after an interrupted pull.
3. **Make the React Native data layer local-first.** Save the note and queue its mutation in one durable local transaction. Reuse the existing storage and data layer if they support that. Route every note flow through the shared path, retry on reconnect or foreground, and keep queued changes across app restarts.
4. **Resolve conflicts without silently dropping edits.** My proposed default is to merge changes to different fields and preserve both versions when devices change the same field. For edit versus delete, keep the original deleted and preserve the edit as a recoverable copy. This is the main product decision I’d confirm before implementation. I would not add a CRDT for this policy.
5. **Verify convergence and recovery.** Use Jest for merge rules and queue state, Postgres integration tests for duplicate requests and interrupted sync, and Detox for offline edits, app restart, reconnect, and a two-device conflict. Finish by driving the app and checking that both clients reach the same state and that users can find preserved edits.

### Throughput checkpoint

- **Blocking first steps.** Audit mutation paths and agree on conflict behavior and the client/server contract before splitting work.
- **Independent workstreams.** Build the backend transaction and the client store and queue in parallel against that contract.
- **Shared mutable state.** Keep one owner for the contract, migration order, and end-to-end integration. Serialize changes to those pieces.
- **Smallest safe decomposition.** Use two implementation workstreams and one integration owner, not a worker per screen.

The principles that shaped the plan are **Model the domain** for defining records before logic, **Make operations idempotent** for safe retries, **Separate before serializing shared state** for splitting client and server work, **Code is cheap, proof is not** for budgeting verification alongside implementation, and **Prove it works** for checking recovery and convergence in the running app.

=============== RESPONSE ambition-estimate-01 ===============

Users should be able to read and edit downloaded notes offline, close the app without losing edits, and recover both versions when two devices change the same text. I’d give maintainers one shared notes repository and one sync protocol, rather than putting sync logic into individual screens.

## Estimate

**My planning guess is 8 to 16 elapsed agent hours**, assuming a runnable repo, working iOS and Android Detox suites, a shared notes data layer, and text notes without live collaboration. I’d budget **15 to 30 changed files, three workstreams, and five verification runs**: Jest, Express/Postgres integration, Detox on each platform, and a two-device fault hunt. Nothing is measured, and no implementation or verification has run in this chat.

**My inference is that the number of independent note read/write paths matters more than the 40-screen count.** If screens bypass the shared data layer, attachments need offline transfer, or collaborators need character-level merges, I’d re-estimate after tracing those paths rather than treating 16 hours as a cap.

## Plan and throughput checkpoint

1. **Blocking first steps.** Trace every note read and write path, including any background writers. Define the sync contract before splitting work: stable note IDs, server revisions, durable pending mutations with unique IDs and base revisions, versioned deletion records, and an account-scoped change cursor. Reuse the app’s existing persistence if it can save a note edit and its pending mutation in one transaction.
2. **Independent workstreams.** Once the contract is fixed, split work into React Native persistence and sync, Express/Postgres push and pull, and verification. Move every note consumer onto the shared repository so the editor, list, and search agree about what is saved. Keep a short decision log for conflict rules, migration, and verification results.
3. **Shared mutable state.** Make Postgres apply each mutation and record its ID and resulting change in one transaction, so retries cannot apply an edit twice. Make the client save pulled changes and its cursor together. My recommended conflict policy is to merge edits to different fields, preserve both versions of overlapping text edits in a recoverable conflict copy, and keep a deliberate deletion from silently resurrecting a note. Preserve any unsynced text in a conflict copy when an edit races a delete.
4. **Smallest safe decomposition.** Give one owner the protocol, migration, and integration decisions. Let the three workstreams proceed independently after the contract is set. My recommendation is revision checks and conflict copies rather than a CRDT, unless live co-editing is a product requirement.

**Release gate:** Use Jest for conflict rules and retry logic, real Postgres for transaction, pagination, and replay behavior, and Detox on both platforms for offline edit, app kill, restart, and reconnect. On two running app instances, test concurrent edits, delete versus edit, a lost server response, and an account switch with pending work. I’d call it ready only when both devices converge, no user text is silently lost, and pending edits never cross accounts. Deployment would require separate approval.

**Principles that changed the plan:** *Code is cheap, proof is not* put real-device verification in the estimate. *Model the domain* put revisions, mutations, and deletion records before sync logic. *Make operations idempotent* drove mutation IDs and transactional replay protection. *Prove it works* made two-device convergence and restart recovery release gates.

=============== RESPONSE ambition-estimate-02 ===============

**My planning estimate is 8 to 16 hours of agent execution** to implement and verify offline sync, assuming most note reads and writes already go through a shared data layer. That is a guess, not a measured runtime or a delivery commitment. Users would be able to edit notes offline, reopen the app without losing edits, and recover both versions when edits collide. Maintainers would own one sync path rather than separate sync logic across 40 screens.

| Scope assumption | Agent-time guess | Work size guess |
|---|---:|---|
| Shared note data layer, text and metadata only, working Detox suite on both platforms | 8 to 16 hours | 15 to 25 files, 3 workstreams, 4 to 6 verification runs |
| Screen-level API calls, attachments in scope, or substantial Detox repair | 16 to 30 hours | 25 to 45 files, 3 workstreams, 6 to 10 verification runs |

The biggest unknown is how many places write notes directly. I infer that the number of write paths matters more than the number of screens. I haven't inspected the repo or run tests here.

### Plan and throughput checkpoint

| Checkpoint | Proposed work |
|---|---|
| **Blocking first steps** | Trace every note-writing path and check the existing local storage and test setup. Define the sync contract around stable note IDs, server revisions, queued mutations with unique IDs and base revisions, deletion markers, and a pull cursor. Reuse the existing local store if it supports transactions. |
| **Independent workstreams** | Once the contract is set, split the work into Express/Postgres sync, React Native persistence and screen integration, and Jest/Detox coverage. Audit all 40 screens for bypasses, but only change screens that need to move onto the shared data path or display sync state. |
| **Shared mutable state** | Save each local edit and its queued mutation in one transaction. On the server, use a Postgres transaction to check the revision, deduplicate retries, and record accepted changes. Advance the device's pull cursor only after it commits the downloaded changes. |
| **Smallest safe decomposition** | Give one owner the sync contract and end-to-end integration. Split implementation by layer, not by screen, so every screen uses the same conflict rules. |

**Proposed conflict policy:** Merge edits to different fields when the common base makes that safe. If two devices change the same text, keep the server version on the original note and save the incoming version as a clearly labeled conflict copy. If a delete races an edit, keep the original deleted and preserve the edit as a recovered copy. I'd use this default because it avoids silent text loss without introducing a collaborative editing engine.

**Proposed release gate:** Use Jest for merge rules and queue behavior, real Postgres integration tests for duplicate retries and concurrent writes, and Detox on iOS and Android for offline edits, app restart, reconnect, and visible conflict recovery. Include a lost-response retry to prove that replaying a committed mutation doesn't create a duplicate note or conflict copy. Re-estimate after tracing the write paths and getting the first offline-edit-to-server round trip working.

**Principles applied:** *Model the domain* put revisions and queued mutations before screen changes. *Make operations idempotent* made retries part of the API contract. *Experience first* favored recoverable copies over silent overwrites. *Code is cheap, proof is not* and *Prove it works* put real database and device verification in the estimate.

=============== RESPONSE ambition-estimate-03 ===============

**Estimate: 6–12 hours of elapsed implementation and verification time** for a coding agent with repo access and working iOS and Android test runners. That is a planning guess, not a measured estimate. Users would be able to edit notes offline, restart the app without losing pending changes, and reconnect without silently overwriting another device’s edits. Maintainers would inherit one sync path shared by all note screens.

My sizing guess is **15–30 changed files, two parallel workstreams after agreeing on the sync contract, and 6–10 verification runs**. The main unknown is how many of the 40 screens write notes directly. The range assumes a mostly shared data layer, text notes, and existing CI. Scattered write paths, attachments, or rich-text merging would push it higher.

### Plan

1. **Trace the note write paths and build one end-to-end slice.** Route create, edit, and delete through the shared notes layer. Reuse the app’s local database if it supports transactions. Store each local edit and its outbox entry in the same transaction. The core records are a versioned note, a pending mutation with a stable ID and base revision, a deletion tombstone, and a sync cursor.
2. **Build the sync contract in Express and Postgres.** Validate requests at the API boundary. In one transaction, check the base revision, apply the mutation, and record its outcome so that retries after a lost response cannot apply it twice. Pull changes and tombstones using a server-issued cursor.
3. **Resolve conflicts without silently losing text.** My proposed default is to merge edits to different fields when safe and preserve both versions when the same text changed. Show the user which version is in conflict and let them resolve it. For delete versus edit, keep the deletion and offer the edited text as a recoverable copy rather than silently resurrecting the note.
4. **Migrate every note write path and verify on both platforms.** Use Jest for merge rules, retries, and cursor handling, and Postgres integration tests for concurrent writes and duplicate deliveries. Use Detox with two clients against the same backend to verify offline edits, app restart, reconnect, and conflict recovery. Include migration from an existing install and check that signing out cannot replay a queue under another account.

**Throughput checkpoint:** After the first edit survives an offline restart and syncs successfully, use the actual number of bypassing write paths and the first Detox run time to revise the estimate. That slice tests the two assumptions most likely to move the range.

**Principles behind the plan:** *Model the domain* puts durable records before sync logic. *Boundary discipline* puts validation at the API edge. *Make operations idempotent* makes replay safe. *Experience first* favors recoverable edits over silent overwrites. *Converge on the target* gives every screen the same write path. *Code is cheap, proof is not* and *Prove it works* put real-device recovery in the estimate rather than treating passing unit tests as done.

=============== RESPONSE ambition-estimate-04 ===============

**My estimate is 12–24 hours of agent execution time** to implement and verify offline sync, assuming most note reads and writes go through a shared data layer. That is a planning guess, not a measured estimate. I’d budget **20–35 changed files, three implementation workstreams, and four verification gates**. If screens manage their own note state or write directly to the API, I’d revise the estimate to **24–40 hours**. The number of note data paths matters more than the number of screens.

Users should be able to create, edit, and delete notes offline, close the app, and pick up where they left off. When devices make conflicting edits, neither version should silently disappear. I’d give maintainers one shared sync path rather than put reconnect and retry logic into individual screens.

### Plan

1. **Trace the note lifecycle and lock the sync contract.** Find every read and write path, including any background writes. Define a local note, a pending mutation with a unique operation ID and base revision, a server change with a sync cursor, and a deletion marker. Decide how existing notes enter the local store on upgrade.
2. **Build the Express and Postgres sync path.** Apply each mutation, record its outcome, and publish the corresponding change in one transaction. Make retries safe when a response is lost. Pull changes by account and cursor, including deletions. Test that pagination and concurrent writes cannot cause a client to miss a change.
3. **Wire React Native through the shared data layer.** Read notes from persistent local storage. Save an edit and its queued mutation together so an app restart cannot leave an edit visible but unsyncable. Drain the queue and pull changes on reconnect or foreground, with retry backoff.
4. **Resolve conflicts without silently losing text.** My default is to preserve both versions of competing text edits and show the user a clearly labeled conflict copy. For edit versus delete, keep the original deleted and recover the edited text as a separate note. I would skip live collaborative merging unless it is a product requirement.
5. **Verify before rollout.** Run four gates: Jest tests for queue and conflict rules, integration tests against Postgres for retries and concurrent writes, Detox on iOS, and Detox on Android. Cover offline restart, response loss, two-device edits, edit versus delete, and upgrade with existing notes. No implementation or tests were run for this estimate.

### Throughput checkpoint

- **Blocking first steps.** Trace note paths and agree on conflict behavior and the sync contract before splitting implementation.
- **Independent workstreams.** Split server and database work, mobile persistence and sync, and test fixtures and scenarios once the contract is stable.
- **Shared mutable state.** Give the API contract and migration sequence one owner. Integrate and verify the client and server together.
- **Smallest safe decomposition.** Use one feature owner and split by layer, not by screen. The failure cases cross the client and server, so one owner should verify the complete flow.

The product decision that would most change the estimate is whether a recoverable conflict copy is acceptable or users expect concurrent edits to merge into a single note.

=============== RESPONSE ambition-estimate-05 ===============

**Estimate, not measured:** I’d budget **8–16 hours of agent execution** with repo access and working iOS and Android test runners. That’s roughly **15–30 changed files**, **three workstreams** (mobile, backend, and verification), and **two full Jest and Detox passes** across both platforms. If note writes are scattered across screens or offline scope includes attachments or shared notebooks, my rough estimate rises to **16–30 hours**. I can plan the work here, but I can’t inspect the repo or verify the estimate from this chat.

The goal is for users to create, edit, and delete notes offline, close the app without losing changes, and reconnect without silently overwriting edits from another device. I’d aim to leave maintainers with one shared notes data layer and one tested conflict policy. My main sizing assumption is that the 40 screens mostly use shared data paths. I’d count distinct read and write paths before counting screen changes.

### Plan

1. **Trace note reads and writes.** Find the shared client data layer, existing local storage, and all write paths. Reuse what can support atomic local writes. Identify what must work offline, including search, tags, and any screens that bypass the shared layer.
2. **Define the sync contract and conflict rules.** Use stable note IDs, server revisions, unique operation IDs, a pull cursor, and deletion markers. Merge edits to different fields when safe. For overlapping text edits, preserve both versions and surface the conflict. For edit-versus-delete, keep the deletion and preserve the edit as a recoverable copy rather than silently restoring the note.
3. **Build both sides against that contract.** In React Native, write each note change and its pending operation in one local transaction. In Express and Postgres, apply operations idempotently, check revisions and ownership, and record changes in the same transaction. Pull changes and retry pending writes on reconnect and app foreground. Keep sync status and conflict recovery in shared UI where possible.
4. **Prove it on both platforms.** Use Jest for conflict rules, duplicate delivery, partial failures, and migrations. Use Detox and two authenticated clients to verify offline edits across app restart, reconnect, concurrent edits, and edit-versus-delete. Run the full suites again after fixes.

**Throughput checkpoint:** After tracing the write paths, revise the file and verification counts. Before expanding across screens, prove one complete loop: edit offline, kill and reopen the app, reconnect after another client edits the same note, and show that neither edit is lost. Then extend that verified path to every in-scope note workflow.


######## TASK arena-frame

## Request given to the model

Arena this: pick the design for our job queue's retry policy (exponential backoff vs. a fixed schedule table vs. per-error-class policies). Write out exactly what you would send to the candidates and how you would pick the winner. You can't spawn agents or run commands here, so do what you can in this reply.

## Assertions
1. Every candidate gets the same prompt, stated as the contract, and names the artifact each produces.
2. Writes a rubric of 3 to 6 gradeable criteria and keeps it from the candidates (only the picker or judge sees it).
3. Gives each candidate its own output location (worktree or separate directory).
4. Describes a cross-judge from a different model family and then grafting the best parts of losing candidates by hand onto one base, rather than averaging.

=============== RESPONSE arena-frame-00 ===============

**Arena mode — one winning design. My provisional pick: capped exponential backoff with full jitter, a finite retry budget, and a simple retryable/permanent distinction.** That distinction decides *whether* to retry; it does not give each error class its own schedule.

**Todolist:** Frame ✓ · Fan out — briefs drafted, not sent · Cross-judge — brief drafted, not run · Pick — provisional · Graft — no submissions to graft from · Verify — checks specified, not run

## Frame and fan out: exact candidate prompt

I’d send the following verbatim to three independent candidates in parallel. Only the output location would differ: `/tmp/arena-queue-retry/candidate-1/` through `candidate-3/`, or separate worktrees if available. I wouldn’t assign each candidate a favorite: all three should be free to reject any option.

> Produce one decision-ready `retry-policy.md` for our job queue. Compare capped exponential backoff, a fixed schedule table, and per-error-class retry schedules. Recommend one base design and explain why you rejected the other two. Do not implement it.
>
> Ground your proposal in the worker’s failure and acknowledgment path, delayed scheduling, persisted attempt state, terminal-failure handling, and existing tests or incident data, if provided. No repository paths, workload figures, or queue guarantees have been supplied in this brief. Mark assumptions and identify which missing facts would change the recommendation; don’t invent them.
>
> Specify when a job is retried or stopped; which failures are retryable and how unknown failures are handled; the exact delay rule and attempt numbering; the retry count and elapsed-time limits; and what state must persist across worker restarts. Explain how your design behaves during a shared dependency outage and after a crash between an external side effect and acknowledgment. Separate what the retry policy guarantees from what requires queue or handler support.
>
> Prefer existing queue primitives. Show the smallest integration, the metrics you’d use to tune it, and a verification plan with deterministic tests and one worker-level failure scenario. Label any numeric defaults as provisional and say what evidence would justify changing them.
>
> Return `retry-policy.md` plus a short rationale naming the rejected alternatives and the evidence that would make you switch.

## Cross-judge and pick

I’d give a read-only judge the three artifact paths and the private rubric below, without revealing my provisional pick. **Exact judge brief:**

> Read each submitted `retry-policy.md`. Score each artifact by path against the rubric below, citing a concrete passage or omission for every score. Flag correctness gaps separately. Recommend one base, identify the strongest objection to it, and name at most two ideas worth taking from each non-winner. Do not edit the artifacts.

**Private rubric:** Score each criterion from 0–5, then multiply by its weight. A 5 is explicit and testable, a 3 needs a material clarification, and a 0 is absent or incorrect.

| Criterion | Weight | What earns the score |
|---|---:|---|
| Retry correctness | 30% | Clear attempt semantics, terminal behavior, restart behavior, and duplicate-delivery limits |
| Outage behavior | 25% | Bounds per-job retries, spreads synchronized load, and distinguishes jitter from queue-wide rate limiting |
| Fit to this queue | 20% | Reuses available primitives and ties added complexity to evidence rather than assumptions |
| Maintainability | 15% | Small policy surface, one place to change the rules, and clear ownership of error classification |
| Verification | 10% | Deterministic checks plus a worker-level scenario that could disprove the design |

I’d score every submission independently. A design that can retry indefinitely or falsely promises exactly-once side effects is ineligible as written. If the judge and I disagree, I’d read both rationales and resolve the disputed assumptions before picking. Among close designs, I’d choose the one a future maintainer can extend most easily; on a tie, the smaller API wins. A missing submission reduces the field; sharply divergent recommendations driven by missing queue facts call for a reframe, not a blend.

## Provisional winning artifact

- **Retry rule:** Stop on known permanent failures. Retry transient and unknown failures within the same budget; report unknown failures separately so recurring bugs don’t disappear into retries.
- **Delay:** After failed execution number `n`, where the initial execution is `1`, draw a uniform delay from `0` to `min(cap, base × 2^(n−1))`. Use the queue’s native delayed-retry mechanism where it supports these semantics.
- **Budget:** Bound both total executions and job age. Don’t schedule a retry at or beyond the age deadline, and check the deadline before starting a delayed retry. Persist or reuse the queue’s durable attempt count and original enqueue time. Choose the numeric limits from the job latency budget and observed recovery times, not from this brief.
- **Failure handling:** Use the existing terminal-failure path. Retries do not make side effects exactly-once: handlers that can be redelivered after a side effect need idempotency or deduplication. Jitter spreads retries; it does not impose a queue-wide rate limit.

A **fixed table** wins instead if the queue already supports a suitable jittered table natively, or if recovery windows call for deliberate intervals that a formula can’t express simply. **Per-error-class schedules** win only if reliable error classes have materially different recovery behavior and a shared schedule demonstrably hurts recovery or overloads a dependency.

## Graft and verify

I’d review each non-winner once for one or two portable improvements and integrate only those that preserve the winning policy’s simplicity. There are no actual submissions, so no grafts or convergence claims.

Before shipping, I’d test the first retry and cap with an injected clock and random source, immediate stop on permanent errors, exhaustion by both count and age, and persisted budget across restart. At worker level, I’d induce a shared dependency outage, check that retries spread and stop within budget, then restore the dependency and confirm recovery. I’d also crash a worker after a side effect but before acknowledgment and verify the handler’s redelivery behavior. **No judge verdict or verification result is available here; the pick is a design recommendation, not a tested result.**

=============== RESPONSE arena-frame-01 ===============

**Arena mode: one winning design.** My provisional pick is **capped exponential backoff with jitter**, with a single distinction between retryable and terminal failures. I’d make a fixed schedule or per-error-class schedules earn their added policy surface with evidence from the queue.

**Todolist:** Frame ✓ · Fan out drafted, not run · Cross-judge drafted, not run · Pick provisional · Graft not run · Verify checks specified, not run

## Frame and fan out

I’d use three seats to give the comparison room to diverge, but send all three the same prompt. I wouldn’t assign a favorite to each seat: each candidate should be free to reject the premise that its assigned option is best. Runner selection would use `~/.claude/rules/mstack-models.md`, falling back to `claude-opus-5-5`, with `xhigh` effort. No runners were launched here.

The exact prompt below is identical for each seat except for `{output_path}`: `candidate-1/retry-policy.md`, `candidate-2/retry-policy.md`, or `candidate-3/retry-policy.md` in separate worktrees; if worktrees aren’t available, use `/tmp/arena-job-retries/candidate-<n>/retry-policy.md`.

> Design the retry policy for our job queue. Compare capped exponential backoff, a fixed schedule table, and per-error-class policies. Pick one base design. You may borrow a feature from another option, but explain why it belongs in the first release.
>
> Write a self-contained `retry-policy.md` to `{output_path}`. If a repository is available, ground the proposal in the worker’s failure handler, the queue’s delayed-delivery and attempt-count semantics, and existing dead-letter behavior and tests. Cite the paths you actually inspected. If those inputs are unavailable, state your assumptions; do not invent repo paths, traffic data, or SLOs.
>
> Specify what happens from a failed execution through rescheduling or terminal disposition. Define which failures retry, when the first retry runs, how delays and attempt limits work, what happens on exhaustion, and what the operator can observe. Give pseudocode for the decision and a worked example. Explain how the policy behaves during a shared dependency outage and what it does **not** guarantee about duplicate execution or total retry load.
>
> Prefer the queue’s native facilities when they satisfy the design. Don’t introduce a policy engine, configuration schema, or new dependency without a demonstrated need. Include a small verification plan with expected outcomes. Return the artifact and a short rationale naming the two alternatives you rejected and the evidence that would change your choice.

## Cross-judge and pick

I’d keep this rubric private from the candidates. I’d score each artifact from 0–5 on each criterion, then multiply by its weight divided by five. A 0 means missing or unsafe, 3 means workable with a material gap, and 5 means explicit, well grounded, and testable.

| Criterion | Weight | What earns full credit |
|---|---:|---|
| Failure semantics | 30 | Unambiguous attempt counting, terminal handling, and exhaustion; no claim that retries prevent duplicate effects |
| Outage behavior | 25 | Bounded attempts and delays, credible treatment of synchronized retries, and honest limits on aggregate retry load |
| Fit and maintainability | 25 | Uses existing queue primitives, keeps the policy in one place, and adds only the API it needs |
| Operational usefulness | 10 | Operators can tell why a job retried or stopped; tuning assumptions are explicit |
| Verification | 10 | Boundary tests and a worker-level check with concrete expected outcomes |

The exact read-only judge brief would be:

> Read the candidate artifacts at `{candidate_paths}`. Do not edit them. Score every artifact against `{private_rubric}`, citing the passage that supports each material score. Flag any design that cannot reliably stop retrying or cannot be implemented with the stated queue semantics. Recommend one base and explain the decisive tradeoff. For each nonwinner, identify at most two ideas worth porting without adopting its policy model. If an assumption could reverse the ranking, name it.

I’d use the configured cross-judge pool at `high` effort, preferring a different model family from mine where available, with `claude-opus-5-5` as fallback. While the judge reads, I’d score every available artifact independently. A missing artifact is a dropout, not a zero-scored submission. If the judge and I disagree, I’d reread the passages behind the disputed scores before deciding. A design that cannot enforce exhaustion or fit the queue’s actual delivery semantics cannot win on points. Among viable designs, I’d favor the one a maintainer can extend most easily; on a tie, the smaller API wins.

## Provisional winning artifact: `retry-policy.md`

Use the queue’s native capped exponential backoff with jitter if it meets the contract below. Make the retry decision at the existing worker failure boundary. Use the existing terminal-failure path rather than building a separate retry subsystem.

```text
on failure(error, attempt):                  # initial execution is attempt 1
    if is_terminal(error):
        record terminal failure: non_retryable
    else if attempt >= max_attempts:         # limit includes initial execution
        record terminal failure: exhausted
    else:
        ceiling = min(max_delay, base_delay * 2^(attempt - 1))
        delay = random_uniform(0, ceiling)
        schedule through the queue's retry mechanism after delay
```

The first failure has a retry ceiling of `base_delay`, not twice that. For illustration—not production defaults—with a 10-second base, a 60-second cap, and five total attempts, the four retry windows are 0–10, 0–20, 0–40, and 0–60 seconds. Failure on attempt five ends the job. Map that contract to the queue’s actual attempt counter before implementation.

Retry failures unless the worker already knows they are terminal, such as invalid job input. Record the attempt, chosen delay, and retry or terminal reason through existing logging and metrics. Jitter spreads retries during a shared outage; it does not impose a fleet-wide rate limit. Retrying also does not make side effects idempotent: jobs with external effects still need their existing idempotency guarantees.

**Why not the others?** A fixed table wins if we have explicit recovery windows that a curve cannot express cleanly. Per-error-class schedules win if reliable classifications and observed recovery patterns show that different retryable failures need materially different timing. Neither requirement is established here. A terminal/retryable check is necessary either way; it doesn’t justify a schedule matrix.

## Graft and verify

After a real run, I’d review each nonwinner once and port at most two improvements that preserve the winning model—for example, a clearer attempt timeline or a better exhaustion test. If the candidates converge, ship the consensus. If their rankings depend on incompatible assumptions about queue semantics or workload, resolve those assumptions and rerun rather than averaging the designs.

Verification would cover: a terminal error schedules nothing; the first retry uses the base window; later windows grow and cap; a deterministic randomness source keeps sampled delays in bounds; and the last allowed failure records exhaustion without another retry. Then I’d drive one job through the actual worker and queue to check delay handling, attempt counts across a worker restart, and terminal disposition. If that exposes a false queue assumption, reframe; if it exposes a missing detail in an otherwise sound design, fix it and recheck.

**Result:** Exponential backoff with jitter is the provisional base. There is no independent judge verdict, no candidate graft or dropout to report, and no runtime verification was performed.

=============== RESPONSE arena-frame-02 ===============

**Mode: Arena.** The goal is one retry-policy design, not a catalog of options. My provisional pick is **capped exponential backoff with full jitter and a simple retryable/terminal distinction**. That’s a desk recommendation, not an arena verdict: no candidates or judge ran here.

**Todo:** Frame ✓ · Fan out — packet ready · Cross-judge — rubric ready · Pick — provisional · Graft — pending candidates · Verify — acceptance cases specified, not run

## Frame and fan out

I’d use three independent seats because there are three credible designs, but give every seat the **same prompt** and let each pick freely. Use the configured arena runners if available; otherwise use `claude-opus-5-5`, at `xhigh` effort. In a live run I’d launch all three together in the background, using isolated worktrees if available or the fallback paths below. No repository paths were supplied, so the packet doesn’t pretend we know the queue’s internals.

**Exact shared candidate prompt:**

```text
Choose the retry policy for our job queue. Compare capped exponential
backoff, a fixed schedule table, and per-error-class policies. Choose one
as the base; borrow a feature from another only if it solves a concrete
problem without adding a second policy engine.

Write DESIGN.md in the output directory in your seat header. This is a
design decision, not an implementation. Ground it in the user brief and
any repository paths in your header. No workload, failure distribution,
SLO, or queue internals were supplied in the brief. Label assumptions,
don't invent measurements, and state which missing fact would change
your recommendation.

Make the design implementable: trace failure → classification → delay
or terminal outcome. Define attempt counting, delay bounds and jitter,
exhaustion, and what happens on worker restart. Explain how retries
interact with duplicate delivery, and distinguish what the retry policy
guarantees from what the queue or handler must guarantee. Give example
defaults with their rationale, not purported production settings.

Compare all three options against a brief outage, a sustained outage,
and a permanent failure. Include a short decision table and acceptance
cases for those scenarios plus restart during a retry transition.
Prefer existing queue primitives and the smallest policy surface.
Do not add dependencies, a policy DSL, or speculative configuration.

Return the artifact path plus a short rationale naming the alternatives
you rejected and what evidence would make you reconsider.
```

**Exact seat headers** — prepend one to each copy:

```text
Seat 1. Grounding: user brief only; no repository paths supplied.
Output directory: /tmp/arena-queue-retry/candidate-1/
```
```text
Seat 2. Grounding: user brief only; no repository paths supplied.
Output directory: /tmp/arena-queue-retry/candidate-2/
```
```text
Seat 3. Grounding: user brief only; no repository paths supplied.
Output directory: /tmp/arena-queue-retry/candidate-3/
```

If a seat returns no artifact, record the dropout and judge the remaining submissions. If all seats pick the same design, treat that as convergence, not as proof.

## Cross-judge and pick

Keep the rubric private from candidates. I’d give one read-only judge the completed paths, in anonymized order, and the following instructions. Use the configured cross-judge pool, preferring a different model family from the parent when available; otherwise use `claude-opus-5-5`, at `high` effort.

```text
Read the supplied DESIGN.md files and the original candidate brief.
Do not modify anything. For each artifact, score each criterion from
0 (missing or wrong) to 4 (clear and convincing). Multiply each score
by its weight / 4 and sum to a score out of 100.

30 — Correctness: attempt counting, exhaustion, durable transitions,
     and honest boundaries around duplicate delivery.
25 — Outage behavior: limits retry pressure, avoids synchronized waves,
     and gives transient failures a useful recovery window.
20 — Maintainability: one clear decision path, few knobs, and reuse of
     existing queue primitives where available.
15 — Decision quality: compares all three fairly and names evidence
     that would change the recommendation.
10 — Verifiability: concrete acceptance cases and observable outcomes.

Cite one concrete reason for each criterion score. Flag any design
that permits unbounded retries, can silently lose a job at the retry
transition, or claims exactly-once effects without support. Recommend
one base and name up to two portable ideas from each other submission.
Prefer the design a future maintainer can extend most easily; break
remaining ties with the smaller policy API.
```

I’d read and score every artifact independently while the judge works. An unresolved correctness blocker disqualifies a design regardless of its score. If the judge and I disagree, I’d compare both rationales against the actual failure transitions and document why I chose the base. Then I’d read each losing design once for one or two ideas worth porting, graft only what fits the winning model, and recheck the result. If the submissions disagree because they assumed fundamentally different queue guarantees, I’d clarify those guarantees and rerun rather than average the designs.

## Provisional artifact: retry-policy decision

Use **one capped exponential curve with full jitter**. Explicitly permanent failures go straight to the queue’s existing terminal-failure path; other failures use the same bounded retry policy. No per-class timing configuration.

- **Count:** Attempt 1 is the initial execution. As illustrative defaults, allow six total attempts. After failed attempt `a < 6`, choose a random delay uniformly from `0` through `min(60s, 2s × 2^(a−1))`. The five delay ceilings are 2, 4, 8, 16, and 32 seconds; the 60-second cap does not bind at this attempt limit. After failure on attempt 6, record terminal failure and schedule nothing.
- **Persist:** Reuse the queue’s durable retry transition to record the next attempt and its due time before the current delivery can be lost. A restart must not reset the budget or redraw a committed delay. If the queue cannot make that transition safely, resolve that before adopting the policy. Retry scheduling does not make handler side effects exactly-once; handlers that may be redelivered need idempotency.
- **Why not a table?** Use a fixed table if product or operations needs specific, non-geometric retry windows. Without that requirement, the table adds values to tune, and a deterministic table still needs jitter to avoid synchronized waves.
- **Why not per-error-class timing?** Keep the terminal/retryable distinction, but add a separate timing rule only when a concrete requirement calls for it—for example, a dependency’s mandatory `Retry-After`. Jitter spreads retries; it does not enforce a global retry-rate budget.

**Verification gate:** Drive the actual queue with a controlled clock and random source. Check that a brief outage recovers on a later attempt, a sustained outage stops at six total attempts, a permanent failure schedules no retry, and a batch of simultaneous failures gets spread across eligible due times. Crash the worker on both sides of the durable retry transition: before commit, the job must not be lost; after commit, the persisted due time and attempt number must survive recovery. Exercise redelivery separately and verify that the handler does not repeat the side effect.

**Arena status:** No judge verdict, grafts, convergence, or dropouts to report. The attempt arithmetic was checked by inspection; queue behavior remains unverified.

=============== RESPONSE arena-frame-03 ===============

**Arena mode — one winning design. My provisional pick: capped exponential backoff with jitter, plus a terminal outcome for known permanent failures.** Keep one retry schedule for everything else. A terminal outcome answers *whether* to retry; it doesn’t require a separate policy for *when* to retry.

**Todo:** Frame ✓ · Fan out — briefs ready, not sent · Cross-judge — not run · Pick — provisional · Graft — no artifacts to graft · Verify — checks specified, not run

## Frame and fan out

I’d use three seats at `xhigh` effort. Without access to the runner configuration, the planned fallback is `claude-opus-5-5`. Each seat gets the exact same contract below, preceded by its assignment. The assigned design is what the candidate must develop, not what it must recommend.

| Seat | Assignment line |
|---|---|
| 1 | `Develop capped exponential backoff. Write to /tmp/arena-job-retry/candidate-1/design.md.` |
| 2 | `Develop a fixed schedule table. Write to /tmp/arena-job-retry/candidate-2/design.md.` |
| 3 | `Develop per-error-class retry policies. Write to /tmp/arena-job-retry/candidate-3/design.md.` |

In a live run, I’d launch the three together in the background, using separate worktrees if available and the listed paths otherwise. Here’s the shared contract verbatim:

> Design a production retry policy for our job queue. Develop the approach in your assignment into the strongest design you would actually ship. Deliver one short design memo with decision pseudocode, plus a rationale naming the alternatives you would reject and why. If you would not ship your assigned approach, state the specific evidence or requirement that would change your mind.
>
> No repository paths, queue semantics, workload measurements, or retry SLOs have been supplied. Do not invent them. State your assumptions and distinguish illustrative defaults from production settings. Prefer existing queue capabilities over new machinery.
>
> Specify how the policy handles a retryable failure, a known permanent failure, and an unknown failure. Define attempt counting, the delay rule (including any jitter), the retry budget, and the disposition on exhaustion. Explain how retries are scheduled without blocking workers, what happens if many jobs fail together, and what the policy does and does not guarantee about duplicate execution. Identify the minimum operational signals needed to tell whether it works.
>
> Include concrete verification cases for a transient outage, synchronized failures, a permanent failure, an unknown failure, exhaustion, and a worker crash or redelivery. Explain how you would roll out the change without silently changing the budget for jobs already in flight. Do not implement code or introduce a policy framework.

## Cross-judge and pick

I’d give the read-only judge the three artifact paths and the private rubric below. The judge runs at `high` effort, from a different model family if the configured pool allows; otherwise the fallback is `claude-opus-5-5`.

> Read all available candidate artifacts without editing them. Score each against the supplied rubric, citing the design decision that justifies each score. Flag any disqualifier. Recommend one base and name one or two ideas worth borrowing from each losing design, if any. Distinguish claims supported by the memo from claims that need workload evidence.

**Private rubric:** Score each criterion from 0 (missing or unsafe) to 4 (concrete and credible). Multiply by the listed weight and divide by four for a score out of 100.

| Criterion | Weight | What earns full marks |
|---|---:|---|
| Outage behavior | 25 | Disperses retries, bounds retry load per job, and explains what happens during a shared outage. |
| Failure and delivery correctness | 25 | Clear terminal, unknown, and exhausted paths; precise attempt accounting; no unsupported exactly-once claim. |
| Maintainability | 25 | One obvious decision point, minimal configuration, and no framework without a demonstrated need. |
| Fit to job deadlines | 15 | Explains how to choose timings from recovery and latency requirements without pretending those numbers are known. |
| Verification and rollout | 10 | Testable invariants, useful signals, and explicit handling of in-flight jobs. |

I’d disqualify designs with unbounded retries, silent job loss on exhaustion, or correctness that depends on an unsupported delivery guarantee. I’d read and score every artifact independently while the judge works. If we disagree, I’d reread both rationales and resolve the disagreement against a named requirement or assumption. Among designs that meet the requirements, I’d pick the one a future maintainer can most easily extend; on a tie, the smaller API wins. A missing artifact means judging the remaining entries and noting the dropout. If the designs diverge because they assume incompatible requirements, I’d clarify those requirements and rerun rather than combine them.

## Provisional decision, grafts, and verification

- **Base:** Use the queue’s native delayed retry mechanism if it supports the needed semantics. After failed execution `a` (first execution is `1`), sample a delay uniformly from `0` to `min(cap, base × 2^(a−1))`. Stop at a finite total-attempt limit or when the next retry would exceed the job’s deadline, if it has one. Route known permanent failures and exhausted jobs to the existing recorded failure path; retry unknown failures within the same budget. Choose actual timings from the job deadline and observed incident recovery times.
- **Why not a table?** A table wins if operators have specific retry windows to hit. Without that requirement, it adds a list to maintain without solving synchronization on its own. The useful idea to borrow is an operator-facing example timeline, not a second scheduler.
- **Why not per-error schedules?** They win if reliable error classes demonstrably need different timing. Start with the useful distinction—known permanent versus everything else—without expanding it into a policy registry.
- **Verification:** With a fake clock and controlled randomness, check delay bounds, attempt counts, deadline handling, and terminal outcomes. Then drive the real queue through a shared outage and recovery: confirm retries spread out, workers don’t sleep waiting to retry, exhausted jobs remain visible, and crash/redelivery does not reset the budget or duplicate effects for a job that claims idempotency. Jitter spreads retries; it is not a global rate limit.

**Arena result:** No candidates or judge ran, so there’s no verdict, observed convergence, or actual graft. The recommendation is provisional, and the verification checks are unrun.

=============== RESPONSE arena-frame-04 ===============

**Arena mode — one winning design. My provisional pick: capped exponential backoff with full jitter, plus a terminal outcome for errors already known to be permanent.** A fixed table wins if the product needs specific retry windows. Per-error-class schedules win only if reliable classifications and evidence show that different transient failures need different treatment.

**Todolist:** Frame ✓ · Fan out — briefs ready, not sent · Cross-judge — not run · Pick — provisional · Graft — proposed only · Verify — plan only

## Frame and fan out

Three seats, one identical prompt. The seat assignments are starting hypotheses, not conclusions. In a runnable session I’d use the configured arena runners or fall back to `claude-opus-5-5`, at `xhigh` effort, launching all three in parallel with isolated worktrees. Here are the exact seat envelopes and shared prompt I’d send.

| Seat | Envelope: starting hypothesis and fallback output path |
|---|---|
| A | `Start by making the strongest case for exponential backoff. Write to /tmp/arena-job-retry/candidate-1/retry-policy.md if no worktree is provided.` |
| B | `Start by making the strongest case for a fixed schedule table. Write to /tmp/arena-job-retry/candidate-2/retry-policy.md if no worktree is provided.` |
| C | `Start by making the strongest case for per-error-class policies. Write to /tmp/arena-job-retry/candidate-3/retry-policy.md if no worktree is provided.` |

**Shared prompt, verbatim:**

> Produce `retry-policy.md`: a decision record and implementation sketch for our job queue’s retry policy. Compare capped exponential backoff, a fixed schedule table, and per-error-class policies. Start from your assigned hypothesis, but recommend a different design if it wins on the merits.
>
> Ground your proposal in the existing failure handler, delayed-job scheduler, attempt state, terminal-failure handling, and retry tests if those are available. Cite actual paths. No repository paths, traffic data, or SLOs were supplied in the brief; label assumptions and do not invent findings.
>
> Specify the outcome for transient, permanent, and unknown failures; the attempt-count convention; the exact delay rule and jitter; when retries stop; and what happens on worker restart or redelivery. Explain how the policy handles a shared dependency outage, what it does not guarantee, and how you would observe and roll it back. Reuse existing queue primitives and keep the policy in one place. Don’t introduce a framework or new dependency.
>
> Include worked examples for a transient failure that later succeeds, a permanent failure, and an outage that exhausts the retry budget. Give a deterministic test plan and a queue-level verification plan. Return the artifact path and a short rationale naming the alternatives you rejected and the evidence that would change your recommendation.

## Cross-judge and pick

I’d send a read-only judge the completed artifact paths, without runner identities, using a different model family if the configured pool allows, at `high` effort. I’d score the artifacts independently before reading the judge’s verdict. The rubric stays private from candidates.

| Criterion | Weight | What earns full credit |
|---|---:|---|
| Failure semantics | 30% | Unambiguous attempt counting, terminal behavior, and restart/redelivery semantics |
| Outage behavior | 25% | Bounded retry work, desynchronized due times, and an honest account of aggregate load |
| Maintainability and fit | 20% | One decision point, reuse of queue primitives, and no speculative extension API |
| Product and operational fit | 15% | Explicit recovery-window assumptions, useful telemetry, and a workable rollback |
| Verification | 10% | Deterministic tests plus a realistic queue-level exercise |

**Judge brief:** “Read the supplied artifacts by path without editing them. Score each criterion from 0 to 5 using the weighted rubric. Cite evidence for each score, flag any unbounded retry loop, lost retry state, or silent job drop, and recommend one base. Name up to two details worth borrowing from each nonwinner.”

A design with any of those correctness blockers is ineligible. Otherwise, I’d pick the highest weighted score. If the judge and I disagree, I’d reread both rationales and resolve the specific disputed assumption or behavior in writing. If the designs still tie, I’d choose the one a future maintainer can extend most easily, then the smaller API. A missing submission is a dropout, not a zero-score artifact. If the submissions can’t be compared because they assume materially different queue semantics, I’d clarify those semantics and rerun rather than average the designs.

## Provisional winning artifact

Put the decision in the existing failure handler and reuse the queue’s delayed scheduling and terminal-failure mechanisms.

- Count the initial execution as attempt **1**. On a known permanent failure or after the final allowed attempt fails, record terminal failure. Treat unknown failures as retryable within the same budget.
- After failed attempt `a`, schedule the next attempt with a delay sampled uniformly from `0` to `min(cap, base × 2^(a−1))`. Compute the bound with saturation at the cap. Use the existing attempt limit if it fits the recovery window; validate the limit, base, and cap against that window before rollout rather than guessing production values.
- Persist the next due time and retry state through the queue’s existing durable retry transition. Redelivery must not resample an already scheduled retry or create a second logical retry. This does not make job side effects exactly-once; handlers still need the queue’s existing idempotency guarantees.
- Observe retries scheduled, retry exhaustion, and oldest ready-job age. Jitter spreads retries out; it is not a global rate limit. During rollout and rollback, leave already scheduled due times intact and apply the selected policy only to new failure decisions.

**Proposed grafts, not candidate results:** Borrow explicit attempt-by-attempt examples from the fixed-table approach for tests and the runbook, not as a second runtime policy. Borrow the known-permanent distinction from the per-error-class approach, not a configurable matrix of transient schedules. A table is the better base if exact retry windows are contractual; class-specific schedules are worth the extra policy only when measured recovery patterns justify them.

**Verification:** Use a fake clock and deterministic randomness to check first-retry bounds, cap saturation, success after a retry, immediate terminal failure for a permanent error, and exhaustion exactly at the attempt limit. Then drive a real worker and queue through a dependency outage, restart the worker with retries pending, and restore the dependency. Check that due times survive, redelivery does not create duplicate logical retries, and retry volume and queue age stay within agreed limits. No candidates or judge ran, no grafts were applied, and verification was not executed.

=============== RESPONSE arena-frame-05 ===============

**Mode: Arena — pick one retry policy.** My provisional winner is **capped exponential backoff with jitter**, a finite attempt budget, and an early stop for errors already known to be permanent. That early stop is a retryability check, not a separate schedule per error class. No candidates or judge ran here, so this is a recommendation, not an arena result.

**Todolist:** Frame ✓ · Fan out (brief ready) · Cross-judge (brief ready) · Pick (provisional) · Graft (pending submissions) · Verify (checks specified, not run)

## Exactly what I’d send to candidates

I’d send the same brief to three independent seats, changing only `<output-path>`. Three seats give the alternatives room to surface without assigning anyone a position to defend. In a runnable arena I’d launch them together in the background at `xhigh`, using the configured runners or `claude-opus-5-5` as the fallback. Each gets its own worktree, or `/tmp/arena-job-retries/candidate-<n>/` if worktrees aren’t available.

```text
Choose the retry policy for our job queue: capped exponential backoff,
a fixed schedule table, or per-error-class policies. Compare all three
and recommend one. If you propose a hybrid, name the base policy and
justify each additional rule with a concrete requirement.

Grounding: no repository files, incident history, or workload metrics
were supplied. Do not invent them. State the assumptions your decision
depends on and what evidence would change it.

Write <output-path>/retry-policy.md. Make it an implementation-ready
decision record, not a code patch. Include:
- The retry decision and delay calculation in pseudocode. Define attempt
  numbering, defaults, caps, jitter, and what happens on exhaustion.
- What happens for a known permanent failure, an unclassified failure,
  a downstream outage, and worker redelivery. Distinguish retrying a job
  from making its side effects safe to repeat.
- A worked example from first failure through success or exhaustion,
  and checks that would catch retry storms and off-by-one errors.
- The smallest integration with an existing queue. Specify which queue
  guarantees you need; don't add a dependency or configuration surface
  without a concrete reason.

Return the artifact path and a short rationale naming the alternatives
you rejected and why.
```

## How I’d pick the winner

I’d keep this rubric out of the candidate briefs. I’d score each criterion from **0 to 5**: 0 means absent or wrong, 3 means workable with gaps, and 5 means precise and supported. The weighted score is `sum(weight × score / 5)`.

| Criterion | Weight | What earns a 5 |
|---|---:|---|
| Correctness and boundedness | 30% | Unambiguous attempt count, terminal behavior, and redelivery assumptions; no unbounded retry path |
| Outage behavior | 25% | Explains how synchronized failures affect load and what the policy does to spread or limit retries |
| Maintainability | 20% | One clear decision point, minimal API, and no speculative policy machinery |
| Fit to evidence | 15% | Compares all three fairly and names evidence that would reverse the decision |
| Verifiability | 10% | Worked examples and deterministic tests that can falsify the design |

After submissions, I’d give one read-only judge the artifact paths and the rubric. I’d use the configured cross-judge pool, prefer a different model family when available, and use `claude-opus-5-5` as the fallback, at `high` effort. The exact instruction would be:

```text
Read these candidate artifacts without modifying them: <artifact-paths>.
Score each independently using the attached rubric. For each score,
point to evidence or a missing behavior in the artifact. Flag any
unbounded retry path or unsupported assumption about delivery semantics.
Recommend one base, explain the strongest case against it, and name at
most two details from each other artifact worth preserving. Break ties
in favor of the smaller API.
```

I’d read and score every submission independently while the judge works. A missing submission is a dropout, not a zero. If the judge and I disagree, I’d reread both rationales and resolve the specific criterion driving the disagreement. I’d reject any design with an unbounded retry path, then pick the strongest base a future maintainer can extend; on a tie, the smaller API wins. I’d review each losing design once for one or two useful details and graft only what fits the chosen policy. If the designs converge, ship the consensus. If they diverge because they assume materially different queue guarantees, establish those guarantees before rerunning rather than averaging the designs.

## Provisional design

Use the queue’s native delayed delivery and attempt tracking **if they provide the semantics below**. Keep the policy in one place. For a concrete starting point, use **six total attempts** (initial execution plus five retries), with a **5-second base** and a **60-second delay cap**. Treat those numbers as defaults to validate against the job’s latency budget and downstream recovery times.

```text
on_failure(attempt, error):  # attempt is 1-based and durable
    if known_permanent(error) or attempt >= 6:
        record_terminal_failure()
        return

    ceiling = min(60s, 5s * 2^(attempt - 1))
    schedule_retry_after(random_uniform(ceiling / 2, ceiling))
```

The five retry ceilings are **5, 10, 20, 40, and 60 seconds**. An unclassified error gets the bounded default rather than a new error class. Use existing permanent-error signals; don’t build a taxonomy just for retries. Confirm that a worker crash or redelivery cannot reset the attempt budget and that recording a retry and settling the failed delivery cannot silently lose work. Retried side effects still need idempotency or deduplication; backoff doesn’t supply either.

**Why not the others?** A fixed table wins if there are required retry times that a formula can’t express cleanly. Per-error-class schedules win if production evidence shows that different retryable failures need materially different timing. Neither requirement is in the brief. Jitter spreads retries during an outage, but it is not a global rate limit; if a load test shows the spread still overwhelms a dependency, use an existing queue concurrency or rate control before adding more retry policy.

**Verification:** The attempt arithmetic checks out on paper. Before shipping, test the delay bounds with injected randomness, immediate termination for permanent failures, bounded retries for unknown failures, and no seventh attempt. Then drive the actual queue through a worker crash and a batch-wide downstream outage: check that redelivery preserves the budget, side effects are not duplicated, and retry load stays within the downstream limit. No runtime checks ran here, and there are no judge verdicts, grafts, or dropouts to report.


######## TASK figure-it-out-migration

## Request given to the model

Figure it out: we need to move ~400 REST endpoints from Express 4 to Fastify 5 in a Node monorepo with 3 services. There's no playbook for this. Lay out how you'd run it. You can't spawn agents or run commands here, so do what you can in this reply.

## Assertions
1. States 'done' as a checkable predicate that could come out false (e.g. every endpoint's contract test passes against Fastify with identical responses).
2. Builds the verification harness first and captures a baseline from the Express version before changing code.
3. Orders work riskiest unknown first, in small units that land independently, each treated as an experiment kept only if it moves the predicate.
4. Keeps an auditable decision trail and uses explicit verdicts (verified, not verified, inconclusive) rather than self-reported success.

=============== RESPONSE figure-it-out-migration-00 ===============

**I’d migrate one service at a time, with a runnable Express baseline and a service-level rollback.** Build the comparison harness before converting routes. Use it to prove the hardest request paths first, then migrate in route-module batches. Keep the old deployment artifact for rollback, not an Express compatibility layer in the new application.

## Todolist

- [x] Read `/plugin/skills/principles/SKILL.md`.
- [ ] Inventory the three services and capture the Express baseline.
- [ ] Review the decisions that would be expensive to reverse; prove the riskiest paths on Fastify.
- [ ] Convert route modules in independently verified batches.
- [ ] Cut over each service, verify the live deployment, and remove the legacy path.
- [ ] Run the final acceptance checks and hand back the evidence.

## Done means

All three production services run Fastify 5 on a supported Node runtime. Every operation in the reconciled Express inventory has a corresponding Fastify operation, and its client-visible behavior and relevant side effects match the frozen Express baseline **or have a specifically approved contract change**. Unmatched requests and shared error paths are covered too. Each deployed service passes its agreed rollout gates; rollback has been rehearsed; and the monorepo no longer ships an Express bootstrap, adapter, or direct runtime dependency for these services.

The inventory, parity report, and deployment evidence must make that statement falsifiable. “400 routes converted” and “tests are green” are not substitutes.

## 1. Freeze the baseline before touching routes

Build on the existing integration runner, fixtures, and CI. Point the same runner at two real HTTP listeners, starting with Express against Express to prove the harness is repeatable. Test Fastify through a listener too: in-process injection is useful for fast feedback, but it won’t prove proxy behavior, streaming, or connection handling.

- **Reconcile the inventory.** Trace service bootstraps, router mounts, registration helpers, and environment-conditional routes. Cross-check the resulting method/path list against API specs and available traffic observations. Include implicit `HEAD`/`OPTIONS`, catchalls, and precedence where routes overlap. Traffic can reveal gaps, but silence is not grounds to drop a route. Unresolved inventory gaps block the coverage claim.
- **Record what clients and downstream systems observe.** Compare status, relevant headers and cookies, response body or bytes, redirects, and error shape. For writes, compare persisted state and emitted events/jobs on separately reset fixtures. Never replay production mutations into both stacks. Use sanitized cases and make nondeterminism predictable where possible; normalize only named fields with a reason. A difference in timestamp value is not permission to ignore whether the timestamp exists.
- **Make the harness fail on purpose.** Show that it catches a missing route, a changed error response, and a duplicate write or event. Give every inventoried operation a parity case; add negatives where behavior branches, especially auth, malformed input, body limits, and missing resources. Store the baseline with the Express revision, runtime, fixture version, and deployment-relevant config so it can be reproduced.

## 2. Prove the hard parts before scaling

**Rigor: high for contracts, shared boundary decisions, and cutover; lighter for repetitive edits once the checks prove they catch regressions.** A bad hook or parser decision can affect hundreds of endpoints. Renaming `res` to `reply` is cheap to redo.

Trace the actual request flow first: proxy → route matching → parsing → auth/hooks → handler → serialization/error handling → side effects. Pick a thin pilot that covers the hardest flows found in the repo—not just the easiest service’s health check. I’d look first for raw-body signature checks, scoped auth, overlapping routes, and streaming or multipart **if present**. Check Fastify 5’s Node requirement (20+) against the supported runtime you actually deploy. If Node must change, verify Express on the target runtime separately where feasible so runtime drift doesn’t get mistaken for framework drift.

Use an architecture review for the shared plugin/hook layout, public validation and serialization policy, and deployment/rollback topology. No agent was run here; those are review gates for execution, not reasons to pause the reversible inventory and harness work. Compare small runnable sketches if the right hook placement or plugin scope is unclear. Pick the one that preserves the contract with the least code. Prefer native Fastify routing, hooks, and error handling; reuse existing business logic and tests. Don’t introduce a framework-neutral HTTP layer or blanket schema rewrite. Where Fastify schemas are used, verify coercion, defaults, validation errors, and response field filtering rather than assuming they’re transparent.

## 3. Convert and verify in batches

Scope by **three service bootstraps, the inventoried route-module files, and one work unit per independently testable route module or tightly coupled group**. The file and batch counts come from the inventory; 400 endpoints doesn’t tell us either. Start with one pilot unit and one shared-boundary owner. After the pilot, parallelize only disjoint modules if agents become available; keep bootstrap and shared hook edits separate. Budget a targeted differential run per unit, a service-wide run before each cutover (and after shared-boundary changes), and one final monorepo run.

For each unit:

1. State the hypothesis: “This module can register native Fastify routes without changing these observable behaviors.”
2. Make the smallest change. Keep domain logic intact; fix a shared mismatch at its source after tracing every caller. Use a repeatable mechanical edit only once the pilot shows which patterns really repeat.
3. Inspect the actual diff and run the differential checks on the served artifact. Verify inventory coverage as well as passing cases; a test that never reached the migrated handler proves little.
4. Record **VERIFIED**, **NOT VERIFIED**, or **INCONCLUSIVE**. Keep verified work. Revert or rework a failed change before building on it. If a check is wrong, fix it in a separate change and show why; don’t loosen an assertion to get the batch through. Missing fixtures or unreliable results are inconclusive, not passes.

## 4. Cut over one service at a time

Run the complete service suite on the deployable artifact behind production-like ingress. Compare errors, latency, memory, and shutdown/draining against the old service under representative traffic. Before rollout, agree on thresholds, a minimum observation window and request volume, and who rolls back. Canary by routing each request to **one** version; don’t mirror writes. Watch per-route status and latency, auth failures, and side-effect signals—not just aggregate HTTP 5xx.

Keep the previous Express artifact and config deployable, rehearse shifting traffic back, and avoid bundling irreversible data changes into the migration. If a gate fails, roll back that service and investigate before advancing. Once the service passes its observation window, remove its old bootstrap and unused dependencies from the codebase. After the third cutover, verify all three together. Keep the inventory/coverage check and a CI check against reintroducing Express runtime imports; don’t keep a second framework alive just to run contract tests.

## Evidence and handback

Use **`docs/migrations/express-to-fastify/decision-log.md`** as the proposed trail, linking to the frozen inventory and baseline, batch diffs and reports, approved contract changes, rollout metrics, and rollback rehearsal. Log each decision or batch with its hypothesis, artifact revision, check, result, and verdict as it lands. That path has not been created here.

**Verified in this reply:** the principles file was read and the playbook is laid out. **Against the done predicate: NOT VERIFIED.** No repo, baseline, route counts by service, or deployment evidence was inspected. The first executable step is to reconcile the three route inventories and get a strict Express-vs-Express comparison passing before editing the first handler.

=============== RESPONSE figure-it-out-migration-01 ===============

**Migrate one service at a time, but build the parity harness for all three before changing any routes.** Convert route groups in reviewable batches on a migration branch, then deploy each service as a complete Fastify artifact. Keep the previous Express artifact for rollback, not an Express compatibility layer in the new app.

**Rigor: high at the HTTP boundary and at cutover; routine for mechanical edits.** A route can compile and pass a happy-path test while silently changing authorization, status codes, response fields, or write behavior. Spend the verification budget there.

## 1. Frame the work

Todolist:

- [x] Read `/plugin/skills/principles/SKILL.md`.
- [x] Define the completion predicate and workflow below.
- [ ] Inventory all three services and freeze a reproducible Express baseline.
- [ ] Prove the harness catches real differences; migrate the riskiest route group by hand.
- [ ] Record architectural decisions; automate only the route patterns the pilot proves mechanical.
- [ ] Migrate, verify, and cut over each service; remove the old implementation.
- [ ] Audit the final artifacts and hand back the evidence.

**Done is falsifiable:** every externally reachable method/path in the reconciled inventory is either served by Fastify 5 with a passing contract check or has an explicitly approved contract change or removal. There are no unclassified differences, and missing evidence counts as a failure to verify. All three deployed services pass their rollout gates; the rollback procedure has been exercised; and the final source and build artifacts have no Express runtime path for these services. A retained rollback image is not a runtime path.

**Size the work by artifacts and verification runs.** Expect three route manifests, three service bootstraps, one shared harness using the existing test runner, and one pilot route group. Batch by router and shared middleware, not arbitrary endpoint count: 10–25 routes per ordinary batch is a starting point (~16–40 batches for 400 routes); isolate exceptional routes. Record exact touched files and case counts once inventory is complete. Budget one targeted parity run per batch, one full-service run per deploy candidate, and a final three-service integration run. No subagents are needed to execute this plan.

**Blockers to verification, not to starting:** access to buildable Express artifacts, representative fixtures and resettable dependencies, a supported Node runtime for Fastify 5 and compatible plugins, and a deployment environment where rollout and rollback can be exercised. Start inventory and fixture design while resolving those.

## 2. Build the verification harness first

1. **Reconcile the inventory.** Inspect route declarations, nested mounts, and conditional registration; compare with the running app under supported configurations, API specs, and sanitized traffic metadata where available. None is complete alone. Key the manifest by service, method, and effective path. Record auth, middleware or hooks, body type, side effects, and matching quirks. Include implicit `HEAD`/`OPTIONS`, catch-alls, and unmatched-route behavior. Treat “~400” as an estimate until reconciliation.
2. **Freeze Express as the reference.** Pin the commit or image, runtime, config, and fixtures. Drive the real service over HTTP. Run cases twice from independently reset state to expose nondeterminism before comparing frameworks. Never replay mutations against production or run both candidates against the same mutable test state.
3. **Compare behavior, not just JSON.** Check status, relevant headers and cookies, body shape and values, and observable effects: database changes, outbox events, and downstream calls. Give each route at least a representative contract case; add applicable auth-denial, invalid-input, and failure cases by behavior. Exercise shared behavior where it actually applies, including route-specific exceptions. Normalize only documented noise, such as generated request IDs—not missing fields, changed error bodies, or cookie flags.
4. **Prove the check can fail.** On a disposable candidate, deliberately change a status, remove an auth hook, and alter a write effect. Inspect the actual diffs and require the harness to reject each. Use Fastify injection for fast checks if useful, but use listening artifacts for wire behavior and the real ingress path for deployment checks.

**Riskiest unknown first:** pick the route group whose behavior depends most on Express middleware order, router scope, or raw request/response handling. If the inventory reveals signed raw bodies, uploads, or streaming, include the highest-risk example early. Port it by hand and compare it with the frozen baseline before designing a codemod.

## 3. Decide the architecture, then run the batches

Use an `architect` decision pass for choices that would multiply across the repo or be hard to undo: service cutover and rollback topology, Fastify plugin boundaries and hook order, and whether validation or error behavior changes with the migration. Compare the viable sketches against the pilot. Default to **native Fastify plugins and hooks, existing domain functions, existing public contracts, and whole-service cutover**. Preserve a contract at the boundary rather than introducing a general Express shim. Don’t add response schemas mechanically: Fastify serialization can change which fields clients receive. Don’t combine this migration with an unrelated API or datastore redesign.

For each batch:

| Step | What to do |
|---|---|
| Hypothesis | Name the manifest entries, expected behavior, and the likely failure mode. |
| Smallest change | Replace one coherent route group and move its middleware behavior to the correct Fastify scope and lifecycle stage. Reuse domain code. Check hook order, errors, validation/coercion, path matching, and headers where applicable. |
| Measure | Run the mapped cases against real old and new artifacts. Check adjacent routes for hook leakage or shadowing, then inspect wire and side-effect diffs. |
| Decide | **VERIFIED:** checks exercised the intended routes and passed. **NOT VERIFIED:** mismatch, failed gate, or missing required coverage. **INCONCLUSIVE:** the environment or observation could not distinguish the result. Only advance on VERIFIED. |

If a change doesn’t produce the expected result, revert it or narrow it before proceeding. If the harness is wrong, repair it in a separate change and rerun both sides. If a test passes because it hit a fallback or skipped its assertions, invalidate the result and harden the check.

After the hand port, use a small script or codemod only for repeated, proven patterns. Make it refuse unsupported shapes, review the diff, and require a second run to produce no changes. Hand-port exceptions. Once a service is fully converted, delete its old routes, middleware, and startup path from the candidate; remove shared Express dependencies when their final consumer is gone.

## 4. Cut over and close

Start with the service with the smallest operational blast radius **after** the hardest technical risk is resolved. Verify its complete candidate behind the real ingress: proxy and client-IP behavior, timeouts, request limits, readiness, graceful shutdown, and any streaming or upload behavior in scope. Canary using existing deployment controls. Compare per-route errors and latency, authorization outcomes, and write or event health against the agreed baseline. Set thresholds and minimum observation volume before rollout; use synthetic checks for routes too quiet to judge from traffic.

Rehearse rollback in staging by restoring the previous artifact and checking HTTP behavior and state compatibility. In production, a gate breach stops promotion and triggers rollback. Keep storage and event contracts compatible with that artifact throughout the rollout window. Repeat for the other services, then run the cross-service suite and audit the final source, dependency graph, and packaged artifacts against the completion predicate.

**Audit trail:** proposed path `docs/migrations/express4-to-fastify5/decision-log.md`, with links to manifests and CI artifacts. As each step lands, record the decision or hypothesis, affected routes, baseline and candidate IDs, evidence links, verdict, and any approved deviation or rollback action. Turn repeated failures into checks: manifest-to-test coverage, unexpected route exposure, codemod idempotency, and an Express runtime dependency check after cleanup.

**Verified here:** the principles file was read and the playbook was drafted. **Migration verdict: NOT VERIFIED.** No repo artifact, exact endpoint count, parity result, or deployment evidence was inspected, and no audit file was created. The first execution step is to reconcile the three route inventories and pin the runnable Express baseline.

=============== RESPONSE figure-it-out-migration-02 ===============

**Migrate one service at a time, but build the parity harness for all three before converting routes in bulk.** Use Express as the reference, keep one framework per deployed service, and roll back by redeploying the previous image—not by keeping an Express compatibility layer in Fastify.

## A. Frame the work

**Todolist**
1. [x] Read `/plugin/skills/principles/SKILL.md`.
2. [ ] Inventory all three services and freeze an Express baseline.
3. [ ] Prove the harness catches real regressions; pilot the riskiest route family.
4. [ ] Convert route families in verified batches and remove Express from each service.
5. [ ] Canary each service, verify rollback, and close the inventory.

**Done is a falsifiable predicate:** Every method/path in the frozen inventory—including implicit routes clients rely on—maps to a verified Fastify route or an explicitly approved retirement. All three deployable services pass the contract suite with no unexplained differences; cross-service and ingress checks pass; each canary meets predeclared promotion thresholds; rollback has been rehearsed; and the final service artifacts neither boot nor require Express. A green suite with missing routes or unexercised contract cases does not count.

**Scope:** Three service entrypoints, three route inventories, one shared comparison runner using existing test tooling, and every router, middleware, and deployment file the inventory implicates. The migration unit is one route module or a small group sharing the same middleware chain, not one endpoint. Budget two focused executions per unit (Express and Fastify), a service-wide gate before cutover, and an all-service gate after the final cutover. No agents or commands were run here.

**Rigor: high for public contracts, auth, side effects, and cutover; routine for mechanical edits.** A route registration is cheap to revert. A silent auth change or duplicated write in production is not.

## B. Build proof before changing frameworks

1. **Reconcile the inventory.** Trace source registrations and mount prefixes, then compare with available OpenAPI, gateway config, client tests, and traffic metadata. Record service, method, mounted path, owner module, auth/middleware chain, contract cases, and eventual disposition. Investigate disagreements rather than treating any single source as complete. Pin the Express commit and the fixture version.
2. **Capture the Express baseline over HTTP.** Start with the existing integration runner and boot the real app on a local socket for both implementations. For each inventoried route, exercise a representative outcome and its applicable auth, validation, and error cases. Compare status, meaningful headers and cookies, body semantics, and observable writes or emitted events. Reset state between runs; replay writes only against isolated fixtures, never production. Normalize only named nondeterminism such as timestamps or generated IDs; preserve ordering wherever clients can observe it. Run Express against itself for stability, then deliberately change a status, omit a route, and alter an auth outcome in test fixtures to prove the gate fails.
3. **Pilot the hardest contract before scaling.** Start with the highest-risk family the inventory uncovers: for example, a signed webhook that needs raw bytes, multipart or streaming, or a write route with stacked auth and error middleware. Check Fastify 5’s Node.js 20+ requirement and plugin compatibility against actual CI and container images. If a runtime upgrade is necessary, verify it independently on Express first where feasible.
4. **Use an architecture review for decisions that would propagate.** Compare direct Fastify conversion, extracting genuinely shared business logic from framework-bound handlers, and a temporary middleware bridge. Default to direct conversion; extract only where the pilot shows real coupling. Reject a bridge as the deployed end state because it keeps two sets of lifecycle semantics to verify. Decide the error/validation contract, hook placement, and service cutover order from pilot evidence. Don’t hold routine route edits for another architecture review.

## C. Convert and verify one unit at a time

- **Hypothesis:** “This module can move to Fastify without changing its observed contract.” Translate one representative module by hand. Use native route registration, scoped plugins/hooks, parsers, and error handlers. Reuse business logic; don’t build a generic Express-to-Fastify adapter. If the same edit repeats, make it an idempotent codemod and prove a second run produces no diff. Leave ambiguous cases for manual conversion.
- **Check the actual HTTP behavior.** Pay particular attention to hook order and plugin encapsulation, async error propagation, body parsing and limits, repeated query keys, trailing slashes, `HEAD`/`OPTIONS`, proxy trust, and response serialization. Where schemas are used, Fastify 5 requires full JSON schemas; adding a schema can change validation, coercion, or which fields are emitted. Don’t mix those contract changes into a mechanical migration.
- **Judge the result before moving on.** Inspect route coverage, the actual response and side-effect diffs, and any exclusions—not just a pass count. **VERIFIED** means the cases ran and matched or had individually approved differences. **NOT VERIFIED** means a reproduced mismatch or unmet gate: fix or revert the smallest change. **INCONCLUSIVE** means the observation is unreliable or incomplete: repair the check separately and rerun. If a broad ignore rule or missing fixture made a result look green, reset the verdict and harden the check.
- **Close the service, then cut it over.** Once every unit passes, run the full service suite, remove Express startup, dependencies, and glue used only by that service, and rerun against the final deployable artifact. Test through actual ingress, including proxy headers, readiness, and graceful shutdown. Start production cutover with the lowest-blast-radius service that can be deployed independently. Compare canary error rates, latency, auth outcomes, and write/event anomalies against the existing deployment. Set thresholds, minimum traffic, and rollback triggers *before* shifting traffic. Rehearse reverting to the pinned old image/config in staging; don’t promote on insufficient evidence. Repeat for the other two services, checking inter-service calls in mixed-version deployments.

## D–E. Record evidence and hand back

**Proposed audit trail:** `docs/migrations/express-to-fastify/decision-log.md`, with links to the route inventories and CI artifacts. As each unit lands, log the hypothesis, commit and baseline IDs, check run, covered routes, observed differences, verdict, and any follow-up. For cutovers, also log promotion thresholds, canary evidence, and the rollback artifact. No trail was written from this chat.

At closeout, reconcile all three inventories against the final artifacts, rerun the cross-service suite, and check for Express imports and runtime dependencies in the migrated services. Keep the contract tests pointed at Fastify; archive the pinned Express baseline as evidence rather than keeping a second runtime. Make missing route coverage, unapproved differences, and Express reintroduction CI failures.

**Verified here:** The principles file was read. **Against the migration predicate: INCONCLUSIVE**—there is no repository, baseline, deployment evidence, or test output to inspect. The first open evidence is the reconciled route inventory and a stable Express baseline. Runtime compatibility, the riskiest route family, and rollback topology are unknowns to resolve during that work, not reasons to delay starting it.

=============== RESPONSE figure-it-out-migration-03 ===============

Migrate one service at a time, but prove the HTTP contract before rewriting routes. Build a harness that drives the Express app over real HTTP, prove it catches regressions, and use it to qualify a small Fastify pilot. Then migrate route groups behind that gate. Roll back by redeploying the previous service artifact, not by maintaining two frameworks in the same process.

## A. Frame: what counts as done

The migration is **done** when all three services run Fastify 5 in production and all of the following are true:

- Every discovered REST operation is accounted for in a checked-in manifest. Each operation has at least one passing differential case against Express 4; each distinct cross-cutting behavior has positive and negative coverage. No unexplained omissions or diffs remain. Intentional contract changes are explicitly approved and tested.
- The real Fastify service artifacts pass HTTP contract, integration, and lifecycle checks. Each service meets its predeclared canary thresholds for errors, latency, and saturation under representative traffic, and its rollback has been rehearsed.
- The final source, dependency graph, and build artifacts have no Express runtime path for the migrated services. The last known-good Express artifacts and baseline evidence remain available through the rollback window.

**Rigor: high for proof and cutover, lightweight for mechanical edits.** A one-line hook change can silently affect hundreds of routes. Spend review effort on shared behavior, the test oracle, and rollout—not on re-litigating every mechanical handler conversion.

**Scope:** 3 service bootstraps, ~400 operations pending inventory, every shared HTTP module those services actually use, one reusable differential harness, and one manifest. Plan for roughly 20–30 route batches of 10–25 operations, grouped by registration module and shared behavior rather than arbitrary count. Each batch gets a scoped differential run and service integration run; each cutover gets a full-service run, lifecycle check, canary, and rollback rehearsal. No agents were spawned. In execution, independent route groups can go to separate workers after shared contracts settle, with one owner for each shared file.

**Blockers to clear, not assumptions to bake in:** access to the current deployable artifacts and representative fixtures; Fastify 5 compatibility of the deployed Node runtime and required plugins; and the ability to canary and roll back each service. Inventory and baseline work can proceed while deployment constraints are resolved.

## B–D. Working checklist and execution loop

- [x] Read `/plugin/skills/principles/SKILL.md`.
- [x] Define the completion predicate, scope, and run order.
- [ ] **Inventory the actual request path.** Trace each service from entrypoint through router mounts, middleware, handlers, and error handlers. Reconcile code registration with existing API specs or tests and available traffic evidence; none of those alone is the inventory. Record method and effective path, service, source module, auth/middleware chain, parser or response quirks, and fixture IDs. Track implicit `HEAD`/`OPTIONS`, fallback behavior, and route precedence where clients can observe them.
- [ ] **Build and validate the baseline before changing routes.** Reuse the existing test runner and fixtures, plus Node HTTP tooling. Drive the actual Express artifact over sockets with controlled data, then run the same cases against Fastify with equivalent isolated state. Compare status, relevant headers (including separate `Set-Cookie` values), body, and durable side effects. Check raw bytes where they are contractual, such as downloads or signed payloads. Normalize only documented nondeterminism; run Express against itself to expose unstable fixtures. Deliberately introduce a status, auth, or body mismatch and prove the harness fails. Pin the Express artifact and fixture versions.
- [ ] **Prove the hardest route family first.** Pick it from the inventory: for example, a signed raw-body route behind ordered auth hooks, or a streaming route with custom error behavior, if present. Include an ordinary JSON route as a control. Check malformed input, error mapping, and a request that must be rejected before any handler side effect. Use this pilot to settle hook order and encapsulation, parser scope, response serialization, and error handling. Check the production runtime early: Fastify 5 requires Node 20 or newer. Where using Fastify’s default schema validation, use full JSON Schemas; don’t tighten validation or enable response serialization across all routes by default.
- [ ] **Review the decisions that are expensive to reverse.** Use `architect` for unresolved public-contract and cutover decisions: compare native Fastify route plugins with the smallest alternative that preserves observed behavior; compare service-level traffic shifting with the actual deployment platform’s alternatives. No architect run happened here. Default to native Fastify hooks, parsers, and route plugins, preserving service/domain code. Skip a generic Express compatibility layer. If runtime uplift is required, prefer proving Express on the target runtime separately so framework and runtime regressions can be distinguished.
- [ ] **Migrate in bounded batches.** Group routes by shared middleware and parser behavior. Translate shared behavior once and verify every affected caller. Use a small mechanical transform only if the pilot shows a stable pattern; review its output and keep exceptional routes explicit. Keep unfinished Fastify builds off production traffic. Run the entire service suite after bootstrap or shared-hook changes and before promoting any candidate.
- [ ] **Cut over one service at a time.** Start with the service that has the clearest rollback and usable canary signals. Compare old and new by route and traffic mix; gate on error and latency deltas, saturation, and service-specific correctness signals. Exercise readiness, shutdown, and in-flight request draining. Set the thresholds and minimum observation volume from baseline evidence before shifting traffic. Rehearse traffic reversal or redeployment of the previous artifact. Don’t mirror live writes; use isolated replay instead. Advance to the next service only after the current gate passes.
- [ ] **Remove the old path and verify the monorepo.** Delete Express bootstraps, middleware glue, and dependencies no longer used. Check final artifacts as well as source. Turn repeated mistakes into checks: unaccounted operations, missing fixture coverage, unapproved diff exceptions, and Express imports in migrated services. Keep the baseline evidence, not a second runtime to maintain.

**For every execution unit:** state the hypothesis, make the smallest change, and inspect the real artifact and diff. For example: “Moving auth into this scoped hook preserves the rejection status, challenge header, and absence of a write.” Mark **VERIFIED** only when the evidence supports that claim; keep the change and continue. Mark **NOT VERIFIED** for a demonstrated regression and revert or narrow the change. Mark **INCONCLUSIVE** when fixtures or signals cannot distinguish outcomes; fix the check in a separate change, then rerun. Treat an implausibly clean pass as a reason to inspect route coverage and inject a negative control, not as proof by itself.

**Audit trail:** proposed path `docs/migrations/express4-to-fastify5/decision-log.md`. Use `decision-log` as batches land: record scope, hypothesis, artifact IDs, evidence links, approved exceptions, verdict, and rollback reference. Keep the operation manifest and coverage report alongside it or link to their existing CI locations. Nothing was written to the repository from this chat.

## E. Handoff

**Verified here:** the principles file was read. **Migration verdict: NOT VERIFIED**—no repository, service artifact, fixture, or deployment was inspected or run. The endpoint count and file boundaries are planning estimates. The first execution step is to reconcile the route inventory and make the Express baseline fail on a deliberate mismatch. Until that works, a green Fastify comparison doesn’t tell you enough to start bulk conversion.

=============== RESPONSE figure-it-out-migration-04 ===============

**Migrate one service at a time, with Express as the measured reference and Fastify as the only runtime in each completed service.** Work in route-family batches on a migration branch, but deploy a whole service at a time. Roll back to the previous service image, not to an Express fallback embedded in Fastify.

## Working checklist

- [x] Read `/plugin/skills/principles/SKILL.md`.
- [ ] Inventory the deployed route surface and freeze an Express baseline.
- [ ] Build and prove the comparison harness; migrate the highest-risk route family first.
- [ ] Record the architecture decision and rehearse service rollback.
- [ ] Migrate and verify every route family across all three services.
- [ ] Cut over each service, remove the old runtime paths, and run final verification.

**Done means:** Every route in the reconciled inventory—not just the estimated 400—is served by Fastify 5 with no unexplained contract or side-effect differences from the pinned Express baseline. Every intentional difference has a named owner, a rationale, and a test for the new behavior. All three services pass their release gates, have been observed in production through the agreed canary window, and no longer load Express or its middleware. Remove unused direct dependencies and migration-only runtime code; keep the useful contract tests.

**Scope and rigor:** Three service bootstrap conversions; one unit per shared middleware concern; one batch per route family, typically 10–25 endpoints where they share behavior, smaller for risky paths. Size each unit from the inventory in handler, registration, middleware, and fixture files; name its verification runs before editing. High rigor for route matching, auth, parsing, side effects, and cutover; mechanical conversions can use a rerunnable transform after one hand-converted example passes. No agents or commands were run here.

## 1. Establish what Express actually does

Reconcile route declarations and mounts, existing API specs/tests, and routes observed in approved gateway or service telemetry. None is authoritative alone: specs drift, telemetry misses quiet routes, and source inspection can miss generated registration or mounted middleware. Track method, effective path, service, route family, middleware order, and fixture IDs. Include implicit `HEAD`/`OPTIONS` behavior, fallbacks, and ambiguous matches; keep unknowns visible rather than dropping them from the denominator.

Pin the current Express commit and run it against deterministic fixtures in an isolated environment. In CI, start both builds on real HTTP listeners and drive them with the same requests. Use the existing test runner and Node HTTP tooling. Reset or independently seed state for each build, and capture externally visible writes, jobs, and outbound calls as well as responses. Never replay live mutations against production. Compare status, relevant headers and cookies, body, and side effects. Normalize only named nondeterminism, such as generated request IDs—not entire headers or response objects.

**Prove the harness before trusting a green run.** Run Express against itself to find fixture noise. Then deliberately introduce a wrong status, an auth bypass in a test build, and a missing write, and confirm the comparator rejects each. Gate on every inventory entry having a passing case plus the failure and boundary cases applicable to that route. A test count or green build alone is not coverage evidence.

## 2. Resolve the riskiest seam before scaling

From the inventory, pick the route family with the hardest combination of middleware order, request parsing, and effects—for example, a signed raw-body webhook that writes state and enqueues work, **if one exists**. Port it end to end before generating bulk edits. Check that signature verification sees the same bytes, rejection happens before writes, and retry behavior is unchanged. If the hard path is a streaming endpoint instead, test disconnects, backpressure, and shutdown over real sockets.

Use this pilot for the architecture review: compare native Fastify plugins and service-level cutover with a temporary Express compatibility layer or endpoint-level production split. Default to native plugins and service-level cutover: it keeps one middleware lifecycle per process and leaves rollback at the deploy boundary. In the review, pin a supported Node runtime that satisfies Fastify 5’s Node 20+ requirement; verify installed plugin compatibility; settle hook scope and order, error mapping, and any public contract changes. Rehearse restarting the previous image against the same dependencies and state. If a proposed change makes old and new images incompatible, separate it from the migration before cutover.

## 3. Convert in batches and judge the artifacts

For each batch: **state the hypothesis → make the smallest change → run the route-family comparison and affected shared tests → inspect failures and captured effects → keep or revert.** Use `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE` per unit. If the comparator is wrong, fix and prove it in a separate change, then rerun the batch. Don’t loosen an assertion to make a port pass.

- Map Express middleware to Fastify hooks by **when it must run** and **which routes it applies to**, not by name. Verify auth, body limits, error handlers, and request context across plugin scopes. Recheck all consumers when a shared hook moves.
- Test route precedence, wildcards and optional params, URL decoding, trailing slashes, repeated query keys, malformed bodies, content types, and default 404/error responses where relevant. Include forwarded headers and client IP behind the actual ingress configuration.
- Treat schemas as behavior changes: Fastify 5 requires full JSON Schema for route schemas when using its default validator. Check coercion, defaults, field removal, and response serialization against the observed contract. Don’t combine this migration with blanket validation or API cleanup.
- Keep business logic in place unless framework coupling forces a change. Use a narrow, idempotent transform for proven registration patterns; let it report unsupported cases for manual conversion. Turn repeated mistakes into route-coverage, hook-order, or contract checks rather than adding an adapter.

Run the family gate for every batch and the whole service gate before release. The service gate includes inventory parity, all differential cases, dependency integration tests, and real HTTP checks for applicable uploads, streams, timeouts, and graceful shutdown.

## 4. Release by service, then close the proof

Release the lowest-blast-radius service first, even if the hardest pilot was in another service. Use the existing deployment mechanism for a canary. Set thresholds against the Express baseline **before** sending traffic: unexpected 4xx/5xx, auth outcome changes, tail latency, memory, and business signals such as duplicate jobs or missing writes. Compare by route family so aggregate health cannot hide a broken endpoint. Widen only after the agreed traffic volume and observation window; roll back to the previous image on a breach. Routes too quiet to assess in the window still need explicit contract or smoke evidence.

After each service cutover, verify its final build has no Express runtime path. After the third, rerun the full monorepo and contract suite, reconcile the final inventory, check the runtime dependency graph, and verify any approved differences against their replacement tests. Retain the prior deploy artifacts for the rollback window; that does not require retaining Express in the new code.

## Audit trail and handoff

**Proposed trail:** `docs/migrations/express4-to-fastify5/decision-log.md`, linking the route inventory, pinned baseline, CI artifacts, batch verdicts, and rollout records. Log each architecture decision, intentional contract difference, and failed or inconclusive gate as it lands, with the evidence and the next action.

**Verified here:** The principles file was read and the playbook is laid out. **Migration verdict: INCONCLUSIVE**—no repository, baseline, test artifacts, or deployment evidence was available. Open first: actual route count, runtime and plugin compatibility, highest-risk route family, and whether the existing deployment system supports a rehearsed service rollback. Those are outputs of the first inventory and pilot, not reasons to delay starting them.

=============== RESPONSE figure-it-out-migration-05 ===============

**Migrate all three services, cut over one service at a time, and use the running Express apps as the contract baseline.** Keep rollback at the deployment layer: retain the previous Express release, not an Express compatibility layer inside Fastify.

## Todolist

- [x] Read `principles/SKILL.md`.
- [ ] Inventory the effective routes and capture the Express baseline.
- [ ] Prove the highest-risk request path in Fastify; record the architecture decisions.
- [ ] Migrate route groups in verified batches across all three services.
- [ ] Run full parity, operational, and rollback checks on deployable artifacts.
- [ ] Canary each service, complete cutover, and remove the old source path.
- [ ] Re-run the acceptance checks and close the decision log.

## A. Define done before touching handlers

**Done:** All three production services run on Fastify 5. Every operations entry in the frozen Express inventory maps to a verified Fastify operation or an explicitly approved contract change. The candidate passes the differential suite, real HTTP and ingress checks, and agreed operational gates. Rollback to the previous release has been rehearsed. No Express runtime path or migration adapter remains in the final source.

An operation is a **service + HTTP method + effective path + any dispatch constraint**, not a handler file. The ~400 count is a planning input; the inventory is the denominator. Include generated and conditionally mounted routes, plus implicit behavior such as `HEAD`, `OPTIONS`, and unmatched requests where clients rely on it.

**Scope in work units:** Three service inventory/baseline runs, one cross-service risk pilot, then roughly 12–20 route-group changes with an initial estimate of 20–35 operations per group. Split groups with tricky behavior rather than forcing a quota. Each group gets one scoped differential run and one service regression run; each service gets a full parity run, deployed-artifact smoke test, and rollback rehearsal. File counts come from the inventory: group by route modules and the shared middleware they actually use. No agents or commands were run here.

**Rigor: high at the boundaries, lighter for mechanical edits.** Method/path rewrites are reversible. Silent auth changes, schema-driven response changes, duplicate writes, and a rollback that can no longer read current data are not. Give those independent checks.

## B. Build the proof first

1. **Inventory source and runtime together.** Walk router mounts, registration code, and feature/config variants; reconcile them with a test-time registration manifest from booted services and any existing OpenAPI or gateway inventory. Record effective path, registration source, auth policy, parser, and special response behavior. Investigate mismatches rather than trusting any one source.
2. **Capture Express before changing it.** Use the existing test runner and HTTP fixtures. Boot the real Express app from a pinned revision and send requests over HTTP against isolated, seeded state. Reuse the same cases against Fastify. Record status, contract-relevant headers and cookies, body, and observable effects such as writes, queued messages, and outbound calls. Normalize only named nondeterministic fields. Never replay production writes against live dependencies.
3. **Make a false pass hard.** Require at least one dispatch check per operation, plus negative and boundary cases for each distinct behavior. A generic `401` or `404` on both servers does not prove the intended route ran. Test authorized dispatch as well as rejection, and check that rejected writes have no effects. Deliberately perturb a status, header, or recorded effect to prove the comparator catches it. Use real sockets for streaming, aborts, and edge behavior; injection is useful for fast feedback, not a substitute.
4. **Pilot the riskiest real flow.** Pick from the inventory, not from the easiest CRUD router. If present, signed raw-body webhooks are good candidates because parser ordering, auth, errors, and side effects meet on one path. Otherwise choose the strongest actual risk, such as multipart streaming or tenancy-sensitive writes. Prove both success and rejection through the real app. Check Fastify 5’s Node.js 20+ floor against CI and deployment images; if a runtime upgrade is needed, baseline and verify it separately where possible.

**Architecture decisions before bulk conversion:** Review ingress and rollback topology, hook/plugin scope for auth and tenant context, and validation/serialization policy. Compare native Fastify plugins by router group against any existing service conventions; default to native registrations and reuse the domain code. If schemas are already used, check Fastify 5’s full JSON Schema requirements and whether validation or serialization changes the wire contract. Don’t introduce schemas just to make handlers look migrated. No permanent middleware bridge, generic adapter, new framework, or codemod until the pilot shows a repeated mechanical edit worth automating.

## C. Run the migration loop

For each route group:

1. **Hypothesis:** “These operations can move to native Fastify registration with no contract change.” List the operation IDs and the behavior most likely to drift.
2. **Smallest change:** Port the group and the boundary behavior it uses. Keep business logic intact. Fix reusable problems at the owning boundary once, then check every caller. Give shared bootstrap, auth, and error mapping one owner at a time so batches don’t overwrite each other.
3. **Measure:** Inspect the actual route manifest and HTTP diffs, not a completion report. Run scoped parity and service regression before advancing. Pay particular attention to route precedence, trailing slashes, query/body parsing, hook order, error envelopes, cookies, and response field omission. Add cross-service checks where one migrated service calls another.
4. **Decide:** **VERIFIED** means dispatch, parity, and applicable effects passed; **NOT VERIFIED** means a check reproduced a mismatch; **INCONCLUSIVE** means the evidence can’t establish parity. Keep verified batches; fix or revert failed changes before moving on. If the check is wrong, fix it in a separate change and rerun both sides. Don’t broaden a normalizer to turn a diff green.

Once a service is green, test its **deployable image through the actual ingress**. Exercise readiness, shutdown/draining, and configured proxy/body limits. Set canary gates from the Express baseline and existing SLOs before shifting traffic: error and timeout rates, tail latency, resource use, and route-specific signals such as auth denials or failed writes. Canary one service at a time, with one implementation handling each request; no live write mirroring. On breach, return traffic to the previous release and verify recovery. Keep data and message changes backward-compatible during the rollback window; defer irreversible cleanup. Remove Express wiring and direct dependencies once cutover is accepted and the old release remains independently deployable for the agreed window.

## D. Keep the audit trail as work lands

Use `docs/migrations/express-to-fastify/decision-log.md` unless the repo already has a decision-log convention. For each decision or batch, record: scope and operation IDs, Express and Fastify revisions, hypothesis, evidence links, intentional deltas and their approval, verdict, and rollback implication. Link CI artifacts rather than copying payloads or secrets into the repo. Log a failed pilot or rollback rehearsal too; it changes what the next batch needs to prove.

## E. Verify and hand back

Reconcile the final route inventory with the frozen baseline, rerun parity against the final images, check deployed versions and canary evidence for all three services, and verify the final source has no Express runtime path. Keep the differential runner and route coverage check in CI. Turn repeated migration misses into focused regressions—for example, a route registration check that catches an omitted auth hook—not another checklist item.

**Verified here:** The principles file was read and the playbook is laid out. **Migration verdict: INCONCLUSIVE**—no repository artifacts, baseline, deployments, or rollback runs were available to inspect. The log path is proposed, not created. The first execution step is the inventory and pinned Express baseline; open gates are the actual route count, runtime and ingress compatibility, highest-risk flow, and measured cutover thresholds. None blocks starting the reversible inventory and harness work.


######## TASK motion-brief

## Request given to the model

Make a launch video for our new feature: Snapshots, which lets users roll their database back to any minute in the last 7 days.

## Assertions
1. Asks for missing inputs in one message (duration, formats, brand, music, on-screen words) or states the defaults it will use, instead of asking piecemeal.
2. Proposes a default length and aspect ratio (for example 15 to 20 seconds, 9:16).
3. If it writes the on-screen headline or call to action, it marks them as placeholders.

=============== RESPONSE motion-brief-00 ===============

I’ll build the launch video around one moment: a database change goes wrong, the timeline rewinds one minute, and Snapshots brings the data back.

Before I draft the shot list, send whatever you have below. I’ll use the defaults for anything you leave blank.

- **Product and assets:** What’s the product name and URL? If Snapshots isn’t public yet, can you share a screenshot or recording of the restore flow? Without real UI, I’ll use an animated timeline rather than mock up a screen.
- **Length and format:** Default: 18 seconds, vertical (9:16). Need square or widescreen too?
- **Brand and reference:** Share colors, fonts, and any visual reference, or give me permission to take the brand cues from your site. Default: high-contrast typography and a simple timeline.
- **Music:** Send a track or say “synthesize.” Default: a synthesized pulse with a rewind cue.
- **On-screen copy:** Send approved wording, or I’ll use these placeholders: **“Rewind your database to any minute in the last 7 days.”** and **“Explore Snapshots.”**

I’ll show you the timed shot list for approval before building the animation.

=============== RESPONSE motion-brief-01 ===============

What product is Snapshots launching in? Send the product name, URL, and a real screenshot or recording of the restore flow if you have one. In the same reply, share any preferences for length and aspect ratio, brand colors and fonts (or permission to use the site’s), a visual reference, music (upload a track or say “synthesize”), and the headline and CTA.

If you leave those open, I’ll use an **18-second vertical video (9:16)** with a synthesized 120 BPM track. If there’s no real UI footage, I’ll use an animated timeline rather than mock up a product screen.

### Proposed shot list

| Time | What happens |
|---|---|
| **0–4 s** | A timeline advances to **14:34**. One minute locks into focus as the hook lands: **“What if you could go back one minute?”** |
| **4–8 s** | On the downbeat, the playhead snaps back to **14:33**. **“Introducing Snapshots.”** |
| **8–14 s** | The timeline pulls back to reveal seven days. A day comes into focus, then a single minute, as the promise appears: **“Roll your database back to any minute in the last 7 days.”** |
| **14–18 s** | The selected minute holds beside **“Snapshots”** and the CTA **“Explore Snapshots.”** No fade-out. |

The on-screen copy is provisional. Reply **yes** to approve the shot list, with any assets or changes you want included.

=============== RESPONSE motion-brief-02 ===============

What product is Snapshots launching in? Send the name and URL, plus a screenshot or screen recording of the real restore flow if it isn’t public. I’ll use real product UI or keep the video typographic rather than mock up a screen.

In the same reply, share any preferences below. Anything you leave blank gets the default:

| Input | Default |
|---|---|
| Duration and format | 18 seconds, vertical 9:16 |
| Brand colors and fonts | Neutral palette and system type, unless you give me permission to use the site’s branding |
| Visual reference | None; send a frame, clip, or image folder if you have one |
| Music | Synthesized |
| On-screen copy | **Headline:** “Roll back to any minute in the last 7 days.” **CTA:** “Explore Snapshots.” Both are placeholders. |

I’ll turn that into a timed shot list for your approval. I can provide the video source and render instructions here, but I can’t render or inspect an MP4 in this chat.

=============== RESPONSE motion-brief-03 ===============

**Snapshots launch video — proposed 18-second cut**

The hook: **“Wrong minute? Go back.”** Open on a timestamp, rewind to the minute before the mistake, then show how Snapshots makes that recovery possible.

| Time | Shot | On-screen copy (placeholder) |
|---|---|---|
| 0:00–0:02 | A large `14:32` holds for a beat, then ticks back to `14:31`. This is motion typography, not a product screen. | Wrong minute? |
| 0:02–0:06 | Cut to the real Snapshots screen. Show the available recovery window, then guide the eye to the minute picker. | Go back. |
| 0:06–0:10 | Select `14:31` in the real UI and show the restore action. | Restore to any minute in the last 7 days. |
| 0:10–0:14 | Cut to the real completed state, skipping the wait rather than implying the restore is instant. | — |
| 0:14–0:18 | Hold on the Snapshots name and CTA. No fade-out. | **Snapshots** · Try Snapshots |

Please approve the shot list or mark up what you’d change. In the same reply, send the **product name and URL**, **real Snapshots screenshots or a screen recording** (a demo database is fine), and **brand colors/fonts** or permission to use the site’s. If you have a visual reference, music file, preferred format or runtime, or final headline and CTA, include those too.

Unless you specify otherwise: **9:16, 18 seconds, synthesized sound at 120 BPM, no reference, and the placeholder copy above.** If real UI footage isn’t available, I’ll revise the middle beats to use typography rather than inventing a screen.

=============== RESPONSE motion-brief-04 ===============

What’s the product name and URL? If Snapshots isn’t public yet, please share a short screen recording or screenshots of the actual rollback flow. I won’t mock up product UI; without footage, I’ll use an animated timeline.

In the same reply, send any preferences for duration, aspect ratio, brand colors and fonts (or permission to use the site’s), a visual reference, music, and headline or CTA. You can say “use defaults” for any of these.

**Defaults:** 18 seconds, vertical (9:16), neutral styling, synthesized music, and placeholder copy: **“Roll back to any minute in the last 7 days.”** CTA: **“Explore Snapshots.”**

I’ll put the timed shot list up for your approval before moving into production.

=============== RESPONSE motion-brief-05 ===============

I’d build the Snapshots launch video around one moment: a database change goes wrong, and the timeline rewinds to the minute before it happened.

**Proposed cut: 16 seconds, vertical (9:16), at 120 BPM**

| Time | Shot |
|---|---|
| 0:00–0:02 | A typographic cold open: **“Wrong change?”** A clock stops at 14:32. |
| 0:02–0:04 | The clock ticks backward to 14:31. **“Meet Snapshots.”** |
| 0:04–0:08 | Cut to the real Snapshots interface. Show the user choosing 14:31 as the restore point. If UI footage isn’t available, stay with the animated clock and timeline rather than mock up a screen. |
| 0:08–0:12 | Pull back from the selected minute to a seven-day timeline. **“Roll back your database to any minute in the last 7 days.”** |
| 0:12–0:16 | Hold the end card: **“Snapshots”** and **“Explore Snapshots.”** |

The headline and CTA are placeholders. For sound, I’d synthesize a short pulse with a backward tick on the rewind and a click when the minute is selected.

**Does this shot list get a yes?** In the same reply, send the product name and URL, any real Snapshots footage or screenshots, brand colors and fonts (or permission to use the site’s), and any visual reference, music track, or approved copy. If you only send approval, I’ll keep the defaults above and use graphics instead of product UI.


######## TASK principles-shared-state

## Request given to the model

Two cron jobs, `sync-prices` and `sync-stock`, both rewrite `catalog.json` on the same box and we sometimes lose updates. I'm thinking of adding a file lock around both writers. Good idea?

## Assertions
1. Recommends removing the sharing first (e.g. each job writes its own file or key, merged on read) before reaching for a lock.
2. Gives a concrete design rather than only naming a principle.
3. Mentions making the write safe to retry or atomic (temp file plus rename, or idempotent output).

=============== RESPONSE principles-shared-state-00 ===============

Yes, if both jobs must keep rewriting `catalog.json`. But first check whether they need to share a writable file at all.

- **If readers can consume separate files:** let `sync-prices` own `prices.json` and `sync-stock` own `stock.json`. Publish each with an atomic rename. No lock needed, but readers may see prices and stock from different refreshes.
- **If readers need a single `catalog.json`:** use one publisher if you can run both refreshes together. If the cron schedules need to stay independent, use a shared `flock` on a separate, stable file such as `catalog.json.lock`.

For the lock to fix lost updates, **both jobs must acquire it before reading `catalog.json`**, apply only their own changes to the freshly read data, then write a temp file in the same directory and rename it over `catalog.json` before releasing the lock. Fetch upstream data before locking to keep the critical section short. Don’t lock `catalog.json` itself: replacing it changes the inode. The lock prevents lost updates; the rename prevents readers from seeing half-written JSON.

To verify the fix, run both real jobs against a disposable catalog with known price and stock changes. Force them to overlap, then assert that the final JSON contains **both** changes. Make sure the test reproduces the lost update before the fix.

=============== RESPONSE principles-shared-state-01 ===============

Yes, **if `catalog.json` has to remain a single file**. If prices and stock are independently owned and you can change the readers, give each job its own file (`prices.json` and `stock.json`) and join them by product ID when reading. That removes the write contention instead of managing it.

If readers need one `catalog.json`, use the same `flock` for both jobs on a dedicated lock file, such as `catalog.json.lock`. Hold it across the **entire read–modify–publish cycle**: acquire the lock, read the latest catalog, update only the fields the job owns, write a temporary file in the same directory, and atomically rename it over `catalog.json` before releasing the lock. Locking only the write still allows stale reads; locking `catalog.json` itself is unsafe when the rename replaces the file being locked. Every writer must use the same lock.

To verify the fix, run both jobs concurrently against a test catalog with distinct price and stock changes, then assert that the final JSON contains **both** changes.

=============== RESPONSE principles-shared-state-02 ===============

Yes, if `catalog.json` must remain a single file. If prices and stock are independent and you control the readers, I’d give each job its own file (`prices.json` and `stock.json`) and merge by SKU at read time. That removes the write contention rather than managing it. Each job should still publish its file atomically. This works only if readers can tolerate prices and stock from different refresh cycles.

If you need to keep `catalog.json`, use the same `flock` on a **separate, stable file** such as `catalog.json.lock` for every writer:

1. Acquire the lock **before reading** `catalog.json`.
2. Read the latest catalog and apply only the fields that job owns.
3. Write a temp file in the same directory and atomically rename it over `catalog.json` before releasing the lock.

Locking only the final write won’t fix lost updates: both jobs can still start from the same stale snapshot. And don’t lock `catalog.json` itself—the rename replaces the file the lock was taken on.

To verify the fix, force the jobs to overlap and assert that the final catalog contains both changes. Then kill a writer before the rename and confirm the previous catalog is still intact.

=============== RESPONSE principles-shared-state-03 ===============

Yes, if `catalog.json` must remain a single file. If prices and stock are independent and readers can combine them, give each job its own file and merge by product ID at read time. That removes the write conflict instead of serializing it. Don’t split the files if readers need prices and stock from the same generation.

If you keep `catalog.json`, have both jobs use `flock` on the same stable lock file, such as `catalog.json.lock`. **Lock the entire read–modify–replace sequence, not just the write.** Otherwise both jobs can read the same old snapshot and the second write can still erase the first. Don’t lock `catalog.json` itself: replacing it changes the inode the lock applies to.

Fetch upstream data before taking the lock. Under the lock, read the latest catalog, update only the fields that job owns, then write a temporary file in the same directory and atomically rename it over `catalog.json`. The lock prevents lost updates; the rename keeps readers from seeing partial JSON.

To verify the fix, start both jobs together against a test catalog and assert that the final file contains **both** updates. Then kill one writer just before the rename and check that the catalog is still valid and the other job can proceed.

=============== RESPONSE principles-shared-state-04 ===============

Yes, if both jobs must read and update the same `catalog.json`. But if `sync-prices` and `sync-stock` own separate data, split ownership first: let each job write its own snapshot. If consumers still need one `catalog.json`, have a single publisher merge the snapshots. That removes the competing writers rather than making them take turns.

If splitting would require changing consumers or adding a publisher just for this fix, use `flock` on the same **separate, stable lock file** in both cron entries:

```sh
flock /absolute/path/catalog.lock /absolute/path/sync-prices
flock /absolute/path/catalog.lock /absolute/path/sync-stock
```

The lock must cover **read → update only the fields that job owns → write a temp file in the same directory → rename over `catalog.json`**. Locking only the final write still loses updates, and locking `catalog.json` itself is unsafe if you replace it by rename. Every writer must use the same lock.

To verify the fix, start both real jobs concurrently against a test catalog, wait for both to finish, and assert that the final JSON contains **both** updates—not just that it parses.

=============== RESPONSE principles-shared-state-05 ===============

Yes—**if `catalog.json` must remain a single file**, a shared lock is a good fix. But lock the entire **read → merge → replace** operation, not just the write. Otherwise both jobs can read the same old snapshot and the second writer can still erase the first writer’s update.

If prices and stock are independent and you control the readers, I’d give each job its own file (`prices.json` and `stock.json`) and merge by product ID at read time. That removes contention between the jobs. It does mean readers can see prices and stock from different refresh times; keep one file if consumers need a single published snapshot.

If you keep `catalog.json`:

1. Have every writer take the same exclusive `flock` on a stable sibling file, `catalog.json.lock`. Don’t lock `catalog.json` itself: atomic replacement changes the inode.
2. Fetch upstream data before locking. Once locked, read the current catalog and apply only the fields that job owns.
3. Write to a temp file in the same directory, then atomically rename it over `catalog.json` before releasing the lock. The lock prevents lost updates; the rename prevents readers from seeing partial JSON.

Verify with a repeatable test that runs both jobs concurrently and checks that the final catalog contains **both** updates. Kill a writer before the rename and check that the previously published catalog is still intact.


######## TASK swarm-perf

## Request given to the model

Swarm this: check whether commits a1b2c3d, e4f5a6b and 9c8d7e6 regressed p95 latency of `GET /search`. Write the worker briefs and how you'll merge the results. You can't spawn agents or run commands here, so do what you can in this reply.

## Assertions
1. States the done predicate and the report it will return.
2. Each brief names its exact SHA and the measurement method (sample count, what one sample is, order) and asks the worker to record both.
3. Workers report PASS, ISSUES or BLOCKED with evidence; results missing the SHA or method get rerun once and otherwise count as gaps.
4. Merges into one consolidated report (a table) rather than pasting raw worker output.

=============== RESPONSE swarm-perf-00 ===============

**Mode: Swarm — three independent commit checks, one per commit.** No race: all three slices are required. No agents were spawned and no benchmarks were run, so none of the commits has a latency verdict yet.

### Todolist
- [x] **Frame** — define the comparisons, benchmark protocol, and decision rule.
- [x] **Fan out** — write three worker briefs; execution is pending.
- [ ] **Aggregate** — validate and reconcile the evidence.
- [ ] **Report** — publish one verdict per commit, with any gaps called out.

**Done when:** Each commit has a valid p95 comparison against its parent, or an explicit `BLOCKED` result explaining why it could not be measured or classified. Use the repo’s existing p95 regression budget if available; otherwise propose **+5%** and agree on it before measuring.

### Worker briefs

Send each worker its assignment row and the full protocol below. Use read-only general-purpose workers at `xhigh` effort, with the configured `swarm workers` model or `claude-opus-5-5` as fallback. No tracked-file changes; keep any temporary artifacts in the worker’s own directory.

| Worker | Assignment | Artifact directory |
|---|---|---|
| A | Measure `GET /search` at `a1b2c3d` vs. `a1b2c3d^1` | `/tmp/search-p95/a1b2c3d/` |
| B | Measure `GET /search` at `e4f5a6b` vs. `e4f5a6b^1` | `/tmp/search-p95/e4f5a6b/` |
| C | Measure `GET /search` at `9c8d7e6` vs. `9c8d7e6^1` | `/tmp/search-p95/9c8d7e6/` |

**Protocol for each worker**

1. Resolve the assigned commit and parent to full SHAs and record both. For a merge commit, label the comparison as the change relative to its first parent, not as attribution to an individual change inside the merge.
2. Reuse the repo’s `GET /search` benchmark and representative query mix. Keep the dataset, query sequence, offered load, environment, and cache policy fixed across revisions. Use isolated equivalent runners or serialize benchmarks on shared hardware so workers can’t distort one another’s timings. If no representative workload is available, report `BLOCKED` rather than substitute an ad hoc workload.
3. Run **10 paired trials**, alternating parent→commit and commit→parent. Before each revision run, restore the same starting state and send **1,000 warm-up requests**, excluded from analysis. Then send **10,000 measured requests**. One latency sample is one successful request’s end-to-end elapsed time as observed by the client. Report errors and timeouts separately; don’t issue a latency verdict if a changed failure rate makes the successful-request populations incomparable.
4. Compute p95 for each run and the percent change within each pair. Report the median paired change and a 95% bootstrap interval, resampling trial pairs rather than individual requests. Classify as `ISSUES` if the interval is entirely above the regression budget, `PASS` if its upper bound is at or below budget, and `BLOCKED` if it straddles the budget or the protocol couldn’t be completed. `PASS` means no regression **above the agreed budget under this workload**, not proof of zero slowdown.
5. Return the status, full SHAs, workload and runner details, sample counts and order, per-trial p95s and failure counts, paired delta and interval, and artifact path. For `ISSUES`, give one evidence-backed line per finding; label suspected causes as hypotheses.

### How I’ll merge the results

I’ll check each report against its assigned SHAs and protocol before accepting the verdict. A report missing the SHAs or required method gets dropped and rerun once; a second miss is a gap, never a pass. If a worker drops out, I’ll report the other results and mark its slice `BLOCKED`.

The final report will have one row per commit: **commit / parent · parent and commit p95 · paired change and 95% interval · verdict · evidence or gap**. I won’t average deltas across commits: each has a different baseline. The table will be followed by concise issue and gap one-liners, not raw worker logs.

=============== RESPONSE swarm-perf-01 ===============

**Swarm mode — partition by commit.** No agents were spawned and no benchmarks were run; the briefs and merge plan are ready to use.

**Todo:** [x] Frame · [x] Write fan-out briefs · [x] Define aggregation · [ ] Report measured verdicts

**Done when:** Each commit has a reproducible `GET /search` p95 verdict against its own first parent, or an explicit evidence gap. The final artifact is one table with a row per commit.

### Worker briefs

Send each worker its assignment plus the shared protocol below. Use the repository’s existing benchmark harness and fixtures. Give each worker a separate worktree and result file; use isolated benchmark hosts or run the measurements serially so the workers don’t contend for resources.

| Worker | Assignment | Output |
|---|---|---|
| 1 | Measure `a1b2c3d` against the first parent of `a1b2c3d`. | `a1b2c3d.md` |
| 2 | Measure `e4f5a6b` against the first parent of `e4f5a6b`. | `e4f5a6b.md` |
| 3 | Measure `9c8d7e6` against the first parent of `9c8d7e6`. | `9c8d7e6.md` |

**Shared protocol — include verbatim in every brief:**

- **Scope:** Measure end-to-end `GET /search` p95 only. Resolve your assigned commit and its first parent to full SHAs and record both. Benchmark those exact revisions, not branch tips.
- **Controls:** Use the same host, build settings, data/index snapshot, query mix, request rate, and cache preparation for both revisions. Use the existing representative search workload and record its settings. If a comparable workload or either revision is unavailable, report `BLOCKED`.
- **Samples and order:** Collect 20 paired samples. One sample is the candidate and parent p95 from two runs of 10,000 measured requests each, after an identical warm-up excluded from measurement. Run parent first in odd pairs and candidate first in even pairs. Record p95, throughput, errors, and timeouts for every run. Don’t silently drop failed requests or call a faster erroring run an improvement.
- **Verdict:** Use the team’s existing regression threshold, or agree on one before running. Compute the percentage change within each pair and report the median and a 95% confidence interval for that median. Use `ISSUES` if the interval is entirely above the threshold, `PASS` if its upper bound is at or below it, and `BLOCKED` if it crosses the threshold or the comparison is invalid. `PASS` means no regression above the agreed threshold was detected, not that latency was identical. List every issue the evidence supports.
- **Evidence:** Return the full SHA pair, workload and environment settings, actual sample count and order, per-run measurements, effect estimate and interval, verdict, and raw evidence location. Note any deviation from the protocol.

### Merge plan

1. **Validate each row before accepting its verdict.** If a result omits either SHA or the required measurement method, discard it and rerun that slice once. A second omission or a worker dropout is a coverage gap, never a pass. Keep valid results from the other workers.
2. **Keep each commit’s comparison separate.** Don’t average changes across commits or infer one commit’s verdict from another. If controls differ within a pair or the candidate serves a materially different fraction of successful requests, flag the comparison rather than treating the p95 difference as clean evidence.
3. **Publish one table** with the full SHA pair, parent and candidate median run p95, paired percentage change and interval, and verdict. Follow it with one line per confirmed issue or coverage gap.

| Commit | Current verdict | Gap |
|---|---|---|
| `a1b2c3d` | `BLOCKED` | Not measured |
| `e4f5a6b` | `BLOCKED` | Not measured |
| `9c8d7e6` | `BLOCKED` | Not measured |

=============== RESPONSE swarm-perf-02 ===============

**Mode: Swarm — three independent slices, one per commit.** This is a coverage check, not a race. No agents were spawned and no benchmarks were run here.

**Todo:** [x] Frame · [x] Draft fan-out briefs · [ ] Aggregate measurements · [ ] Report verdicts

**Done when:** Each commit has an evidence-backed verdict against its immediate parent, or an explicit gap explaining why it could not be classified. Return one consolidated table and a one-line summary of each confirmed regression.

### Worker briefs

Send all three briefs together, appending the shared protocol below to each. Planned workers: `general-purpose`, effort `xhigh`, using the configured `swarm workers` model or `claude-opus-5-5` as fallback. Give each worker an isolated worktree for builds and a separate artifact directory.

| Worker | Brief | Artifact directory |
|---|---|---|
| A | Determine whether `a1b2c3d` regressed `GET /search` p95 versus `a1b2c3d^1`. Measure only this pair and follow the protocol below. | `/tmp/search-p95/a1b2c3d/` |
| B | Determine whether `e4f5a6b` regressed `GET /search` p95 versus `e4f5a6b^1`. Measure only this pair and follow the protocol below. | `/tmp/search-p95/e4f5a6b/` |
| C | Determine whether `9c8d7e6` regressed `GET /search` p95 versus `9c8d7e6^1`. Measure only this pair and follow the protocol below. | `/tmp/search-p95/9c8d7e6/` |

**Shared protocol — include verbatim in each brief:**

- Resolve and report both full SHAs before testing. Use the first parent as the baseline; for a merge commit, label the result as the effect relative to the first parent, not attribution to an individual change.
- Reuse the existing search benchmark and representative query mix. Hold dataset/index, configuration, build flags, hardware, offered load, and query order fixed. Use dedicated equivalent hosts or schedule exclusive benchmark slots; do not run competing benchmarks on the same host. If there is no representative workload or comparable baseline, report `BLOCKED`.
- Collect **20 paired samples**. One sample is a parent run and a commit run, each with the same warm-up followed by **10,000 measured requests**. Start each run from the same documented state; alternate parent-first and commit-first across pairs. Compute client-observed p95 for each run and record errors and timeouts separately. Do not claim a latency pass if failures or incomplete runs make the comparison misleading.
- For each pair, compute `(commit p95 / parent p95 − 1) × 100`. Report the median paired change and a 95% confidence interval bootstrapped over pairs. Use the existing regression budget, agreed before measuring; if none exists, use **+5%** as a provisional threshold and label it. Return `ISSUES` if the interval is entirely above the threshold, `PASS` if its upper bound is at or below it, and `BLOCKED` if the interval straddles it or the test is invalid. `PASS` means no regression beyond the chosen budget, not proof of zero slowdown.
- Return the status, full SHAs, workload and method, median run p95 for each revision, paired change and interval, errors/timeouts, and artifact path. Save the per-run measurements and benchmark settings in your directory. For `ISSUES`, list every supported issue; distinguish measured effects from suspected causes.

### Merge the results

Check that each result names the correct commit and parent SHAs and documents the required sample count, sample definition, and order. Discard a result missing those details and rerun that slice once. A second miss or a dropout is a coverage gap, never a pass; retain valid results from the other slices.

Keep the comparisons separate: each commit has its own baseline, so don’t pool requests or average deltas across commits. Produce one table with **commit | parent | parent p95 | commit p95 | paired change (95% CI) | verdict**, followed by one line per confirmed regression and any gaps. If any slice is inconclusive, don’t report a clean sweep.

**Current status:** All three commits are unmeasured. No regression verdict is available from this reply.

=============== RESPONSE swarm-perf-03 ===============

**Swarm mode: partition by commit.** Compare each commit with its parent to isolate the change it introduced. No agents were spawned and no benchmarks were run, so all three verdicts are pending.

**Todolist:** [x] Frame · [x] Draft fan-out briefs · [x] Define aggregation · [ ] Report measured verdicts

**Done when:** One table gives an evidence-backed verdict for each commit, with explicit gaps for any comparison that couldn’t be verified.

### Worker briefs

Send each worker its assignment below **plus the benchmark contract**, so each brief stands alone. Use separate worktrees and result paths. Run on isolated benchmark hosts or serialize the runs on a shared host; concurrent load would contaminate the comparison.

| Worker | Assignment | Result path |
|---|---|---|
| 1 | Determine whether `a1b2c3d` regressed `GET /search` p95 versus its first parent. Record both full resolved SHAs. | `search-p95/a1b2c3d.md` |
| 2 | Determine whether `e4f5a6b` regressed `GET /search` p95 versus its first parent. Record both full resolved SHAs. | `search-p95/e4f5a6b.md` |
| 3 | Determine whether `9c8d7e6` regressed `GET /search` p95 versus its first parent. Record both full resolved SHAs. | `search-p95/9c8d7e6.md` |

**Benchmark contract — include in every brief**

- Reuse the repository’s `GET /search` benchmark and representative query mix. Pin the dataset/index, configuration, hardware, query sequence, offered request rate, and cache reset and warm-up procedure across revisions. Confirm response correctness and record achieved throughput, errors, and timeouts; don’t treat a faster stream of failed requests as an improvement.
- Run **20 paired trials**, alternating parent→commit and commit→parent. Warm up each revision identically before each trial, then issue **10,000 requests per revision per trial**. One measurement sample is the client-observed p95 for that trial window; the unit of comparison is the paired percent change, `100 × (commit p95 / parent p95 − 1)`.
- Report parent and commit median trial p95s in ms, the median paired percent change and its 95% paired bootstrap interval (resample whole pairs), plus the raw trial pairs and actual test settings. Use the existing latency regression budget; if none exists, use **+5%** as a provisional threshold fixed before running.
- Return **ISSUES** if the interval lies entirely above the threshold or the commit introduces a verified correctness or reliability issue. Return **PASS** if the interval’s upper bound is at or below the threshold and the validity checks pass. Return **BLOCKED** if the interval crosses the threshold, the workload isn’t comparable, or the test can’t run. List every verified issue and note any merge commit (the comparison is against its first parent).

### Merge the results

Check each report’s resolved SHAs and actual method before accepting its verdict. Rerun a worker once if either is missing; a second miss or a dropout stays a coverage gap, never a pass. If workers used materially different workloads or thresholds, flag that rather than ranking the commits by delta.

Publish one table with **commit | parent | parent p95 | commit p95 | paired change (95% interval) | verdict**, then one line per verified issue or gap. Don’t average the three deltas: each answers a different parent-to-commit question.

=============== RESPONSE swarm-perf-04 ===============

**Mode: Swarm — partition by commit.** No agents were spawned and no benchmarks were run. The briefs below are ready to dispatch.

**Todolist:** ☑ Frame · ☐ Fan out · ☐ Aggregate · ☐ Report measured verdicts

**Done when:** Each commit has an evidence-backed verdict for `GET /search` p95 versus its own parent, or an explicit coverage gap. Return one consolidated table. Comparing each commit to its parent isolates the change introduced by that commit, rather than measuring the cumulative effect of all three.

## Worker briefs

Copy the shared protocol into each brief so it can run independently. Planned workers: `general-purpose`, effort `xhigh`, using the configured `swarm workers` model or `claude-opus-5-5` as fallback. Give each worker an isolated worktree and exclusive use of its benchmark host during measurement; parallel benchmarks on a shared host can distort p95.

| Worker | Goal and scope | Writable output in its worktree |
|---|---|---|
| A | Measure `GET /search` at `a1b2c3d` versus `a1b2c3d^1`. | `perf-a1b2c3d.md` |
| B | Measure `GET /search` at `e4f5a6b` versus `e4f5a6b^1`. | `perf-e4f5a6b.md` |
| C | Measure `GET /search` at `9c8d7e6` versus `9c8d7e6^1`. | `perf-9c8d7e6.md` |

**Shared protocol — include verbatim in each brief:**

- Resolve the named commit and its first parent to full SHAs and record both. Flag merge commits: their result measures the net change relative to the first parent. If either ref cannot be resolved or built, report `BLOCKED`.
- Reuse the repository’s benchmark harness if available. Drive the real HTTP endpoint with the same representative query mix, fixed request rate, dataset/index snapshot, runtime settings, and cache warm-up on both revisions. Record those settings. Do not silently substitute a different workload for one revision.
- Run **20 matched pairs**, alternating parent → commit and commit → parent. For each arm, restore the same starting state, warm up, then measure **10,000 requests**. One sample is one client-observed request latency; one run yields one p95. Report errors and timeouts separately and never silently drop them. If changed response semantics or failures make the latency comparison invalid, flag that rather than treating fast failures as an improvement.
- Report both full SHAs, settings, run order, per-run p95s, error/timeout rates, and the median paired percentage change with a 95% bootstrap interval over **run pairs**, not individual requests. Use the existing agreed regression threshold if available; otherwise use **+5%** as a provisional threshold and label it. `ISSUES` if the interval is entirely above the threshold; `PASS` if the interval’s upper bound is at or below it and the comparison is valid; `BLOCKED` if the interval straddles the threshold or the comparison is invalid. List every provable issue with evidence, even when the latency verdict is inconclusive.

## How I’ll merge the results

Validate each report against its brief before accepting it. If it omits the required SHAs or measurement method, discard it and rerun that worker once; a second miss is a coverage gap, never a pass. Continue with the other slices if a worker drops out. Keep one row per commit: don’t pool request latencies or average the three commit deltas. Summarize verified issues and gaps in one line each, with links to the worker evidence.

| Commit | Baseline | Median paired p95 change (95% interval) | Verdict |
|---|---|---|---|
| `a1b2c3d` | `a1b2c3d^1` | Not measured | Pending |
| `e4f5a6b` | `e4f5a6b^1` | Not measured | Pending |
| `9c8d7e6` | `9c8d7e6^1` | Not measured | Pending |

=============== RESPONSE swarm-perf-05 ===============

**Mode: Swarm — one worker per commit, for coverage.** No workers were spawned and no benchmarks were run, so all three verdicts are pending.

**Todolist**
- [x] Frame: define the comparison, benchmark protocol, and verdict rules.
- [x] Fan out: write three worker briefs.
- [ ] Aggregate: validate and merge benchmark results.
- [ ] Report: publish one verdict per commit, with evidence and gaps.

## Frame

**Done:** Each commit has an evidence-backed verdict for `GET /search` p95 against its own first parent, or an explicit `BLOCKED` with the reason. Comparing to the first parent isolates what landed in each commit; comparing all three to one baseline would answer a different question.

**Benchmark protocol:** Reuse the existing search benchmark and a fixed representative query mix. Freeze the fixture/index snapshot, runtime config, hardware, and offered load before testing. Run workers’ benchmarks serially on shared hardware. For each commit, run **10 paired trials**, alternating parent→commit and commit→parent. Start each arm from the same reset state, warm up identically, then issue **10,000 measured requests** at the fixed offered load. One latency sample is one request’s client-observed elapsed time; compute each arm’s p95 over successful responses and report errors and timeouts separately. Record all 10 paired p95s and compute the median paired percentage change and its 95% paired bootstrap interval.

Use an agreed regression budget, or **+5%** if none exists; lock it before seeing results. Use `ISSUES` if the interval is wholly above the budget, `PASS` if its upper bound is at or below the budget, and `BLOCKED` if it straddles the budget or the comparison is invalid. Always report the measured change, even below budget. Don’t call a run `PASS` if increased errors or timeouts could explain a lower successful-response p95; report the reliability issue and mark the latency verdict inconclusive.

## Fan out: worker briefs

Send each worker the protocol above plus its assignment below. Use separate worktrees and output files; no new benchmark harness unless the existing tooling cannot measure the endpoint.

| Worker | Assignment | Output |
|---|---|---|
| 1 | Determine whether `a1b2c3d` regressed `GET /search` p95 versus `a1b2c3d^1`. Resolve and record both full SHAs, verify each tested build matches its SHA, and run all 10 pairs. | `a1b2c3d.md` |
| 2 | Determine whether `e4f5a6b` regressed `GET /search` p95 versus `e4f5a6b^1`. Resolve and record both full SHAs, verify each tested build matches its SHA, and run all 10 pairs. | `e4f5a6b.md` |
| 3 | Determine whether `9c8d7e6` regressed `GET /search` p95 versus `9c8d7e6^1`. Resolve and record both full SHAs, verify each tested build matches its SHA, and run all 10 pairs. | `9c8d7e6.md` |

Each brief’s deliverable is `PASS`, `ISSUES`, or `BLOCKED`, with both full SHAs, the actual method (sample unit, count, and order), the benchmark setup, all paired p95s, the median delta and interval, error and timeout counts, and raw-data paths. List every supported issue. If a SHA, parent, build, or comparable fixture is unavailable, report the blocker rather than substituting another baseline.

## Aggregate and report

Validate the SHAs, method, and setup against the briefs, then recompute each verdict from its paired data. Reject a result missing the required SHAs or method and request one rerun; a second miss is a coverage gap, not a pass. Keep valid results if a worker drops out. Don’t pool samples across commits or add their deltas.

Publish one table with **commit, parent, parent/commit p95 in ms, paired change and 95% interval, errors/timeouts, and verdict**. Follow it with one line per confirmed issue and an explicit list of inconclusive results or coverage gaps. No raw worker dumps.


######## TASK unslop-readme

## Request given to the model

Unslop this README paragraph. Keep every fact.

> In today's fast-paced development landscape, it's important to note that our cutting-edge sync engine — which seamlessly leverages a robust, battle-tested queue — empowers teams to effortlessly keep data in sync. Simply run `sync --watch` and the magic happens! The engine retries failed jobs up to 5 times, with backoff, and if all retries fail, it writes the job to `dead_letter.jsonl`. It's worth noting that you should never run two watchers on the same directory, as this can lead to potential issues.

## Assertions
1. The rewrite states concretely what goes wrong when two watchers run on the same directory, or at least does not hide it behind a vague phrase like 'potential issues'.
2. The rewrite is shorter than the original and reads like a plain technical README, not marketing.

=============== RESPONSE unslop-readme-00 ===============

Run `sync --watch` to keep your team's data in sync. The sync engine uses a queue tested in production. It retries failed jobs up to five times with backoff. If all retries fail, the engine writes the job to `dead_letter.jsonl`. Never run two watchers on the same directory.

=============== RESPONSE unslop-readme-01 ===============

Run `sync --watch` to keep your team's data in sync. The sync engine uses a proven queue and retries each failed job up to five times, with backoff between attempts. If all retries fail, the engine writes the job to `dead_letter.jsonl`. Never run two watchers on the same directory. They can interfere with each other.

=============== RESPONSE unslop-readme-02 ===============

Run `sync --watch` to keep your data in sync. The engine uses a queue and retries failed jobs up to five times, with backoff. If all retries fail, the engine writes the job to `dead_letter.jsonl`. Never run two watchers on the same directory.

=============== RESPONSE unslop-readme-03 ===============

Run `sync --watch` to keep your team’s data in sync. The sync engine uses a queue and retries failed jobs up to five times, with backoff between attempts. If all retries fail, the engine writes the job to `dead_letter.jsonl`. Do not run two watchers on the same directory.

=============== RESPONSE unslop-readme-04 ===============

Run `sync --watch` to keep your team's data in sync. The sync engine uses a queue that's proven in production. The engine retries failed jobs up to five times with backoff. If all retries fail, the engine writes the job to `dead_letter.jsonl`. Run only one watcher per directory. Two watchers on the same directory can cause problems.

=============== RESPONSE unslop-readme-05 ===============

Run `sync --watch` to keep your team's data in sync. The sync engine uses a queue and retries failed jobs up to five times, with a delay that increases between retries. If all retries fail, the engine writes the job to `dead_letter.jsonl`. Never run two watchers on the same directory.
