# Task ambition-rewrite

## Request given to the model

Our billing service is about 30k lines of untyped Python 3.6-era code with ~40% test coverage. The team estimates a rewrite to typed Python 3.13 with a cleaner module layout at a full quarter, so it keeps getting deferred. Should we do it, and if so how would you run it? You can't run commands here; answer in this reply.

## Assertions
1. Treats the rewrite as feasible now with agents doing the work, rather than accepting the quarter-long human estimate or recommending deferral because of effort.
2. Pins current behavior before changing code: characterization or golden tests, replayed production inputs, or an old-versus-new equivalence harness.
3. Uses parallel agents or a clearly agent-driven loop for the bulk of the work, with each unit verified before it lands.
4. Names a checkable done condition (e.g. every replayed invoice matches the old service, type checker clean, tests green) and does not size the effort in human weeks or months.


=============== RESPONSE ambition-rewrite-00 ===============

**Modernize the billing service now. Don't approve a quarter-long rewrite.** My inference is that customers face less risk if you preserve billing behavior in small releases, and maintainers get a supported runtime and clearer types without waiting for a new codebase. The quarter is your team's estimate. I haven't inspected the repository or validated the estimate.

| Option | Tradeoff |
|---|---|
| Big-bang rewrite | Inferred: a clean layout is easier to design from scratch, but the cutover concentrates the risk of missing billing rules, retry behavior, and side effects. |
| Runtime upgrade only | Inferred: this is the smallest useful scope if the deployed runtime is unsupported. It leaves the typing and layout problems for later. |
| Runtime upgrade, then incremental typing and refactoring | Inferred: this gives you separate release gates and lets you stop after the gains you need. It is my recommendation. |

### How I'd run it

1. **Fund a two-week pilot, not a quarter.** Give one engineer ownership and involve whoever reconciles billing in choosing test cases. Confirm what Python version actually runs in production. If it is 3.6, treat moving off it as maintenance, not as a benefit contingent on a rewrite. Check whether the dependency set and deployment image support 3.13 before promising that target.

2. **Establish a billing baseline before changing behavior or layout.** Use the existing test setup to lock down one representative flow, such as invoice finalization. Cover rounding, retries, duplicate events, and partial failures where they apply. Assert the invoice totals, ledger entries, and intended external actions. Use sanitized historical cases if available and keep replay from charging or notifying anyone. Inferred from the reported 40% coverage: the aggregate number does not tell you whether the riskiest money paths are protected.

3. **Change the runtime separately.** Keep dependency changes to what compatibility requires. Compare old and new results on the same inputs before exposing real traffic. Rehearse rollback and check that both versions can read any state the new version writes. If you can isolate a canary without two versions processing the same job, release to that cohort and reconcile before expanding. Halt on an unexplained monetary difference or a duplicate side effect. Inferred: reverting the application cannot undo a charge, so rollback needs a reconciliation plan too.

4. **Type and reorganize one flow at a time.** Start with money amounts and currencies, invoice inputs, and event payloads in the pilot flow. Validate incoming data at the boundary and apply strict type checking to the code you have migrated. Move modules when a specific change would benefit from a clearer boundary. Skip a service-wide folder reshuffle and a blanket annotation target.

**Pilot exit decision:** Continue in slices if the team can show a viable 3.13 deployment path, explain every difference in the billing replay, and verify one typed flow without broad changes. If dependencies block 3.13, split that work out and price it explicitly. If the team cannot verify billing behavior, invest in reconciliation and tests before moving more code. I'd reconsider a rewrite only if the pilot identifies a concrete constraint that incremental work cannot solve.

**Principles that changed the plan:** *Prove it works* made billing outputs and side effects the release gate instead of coverage or compilation. *Model the domain* put money and invoice shapes ahead of module layout. *Boundary discipline* put validation where external data enters rather than throughout the billing logic.

throughput checkpoint: n/a, read-only investigation


=============== RESPONSE ambition-rewrite-01 ===============

**Modernize the billing service now, but don't replace it in one cutover.** My judgment is that a staged migration gives customers the best chance of seeing no change to their bills while giving maintainers a supported runtime, typed billing rules, and modules they can change independently.

I'm inferring from your description, not from a repo inspection. The reported 40% coverage doesn't tell us whether rounding, retries, and refunds are protected. I would treat the quarter estimate as a budget for the proposed rewrite, not as a reason to defer the runtime upgrade or as a reliable estimate of the staged work.

## How I'd run it

1. **Capture billing behavior before moving it.** Inventory the entry points that can create or change financial records, including jobs and webhooks. Add characterization tests for the flows you actually support. I'd prioritize amounts and currency, rounding, duplicate events, retries after partial failure, refunds, and reconciliation. Replay representative, sanitized inputs against the current service. Compare invoice lines, ledger entries, and intended external writes, with payment and notification calls disabled. Have a billing owner review discrepancies so you don't accidentally bless an existing bug.

2. **Upgrade the runtime without redesigning the service.** Check Python 3.13 compatibility for dependencies, drivers, packaging, and deployment images. Keep import moves and billing rule changes out of this work. Run the same tests and replay on both runtimes where feasible. Canary the new runtime with one writer for any given bill or event, and rehearse reverting to the old artifact before expanding rollout. If a dependency blocks 3.13, isolate that blocker. If production still runs 3.6, use a supported intermediate version rather than waiting on a layout rewrite.

3. **Type and reorganize one complete billing flow at a time.** Start with a small, representative invoice calculation if the service has one that can be tested without taking payments. Define the data it passes around, including money and currency, invoice lines, and the calculation result. Parse untyped inputs at the boundary and enable strict checking for the migrated modules. Move the flow and its callers together, then delete the superseded path. Rewrite individual modules where their structure obscures the rules. Leave modules that already have clear boundaries alone.

4. **Make rollout depend on financial evidence.** Require zero unexplained financial differences on the replay set before expanding a change. During rollout, monitor duplicate writes, reconciliation discrepancies, job failures, and processing lag against the existing baseline. Stop expansion on unexpected differences. Rollback stops new bad writes; it doesn't undo charges or ledger entries. Assign an owner and a correction procedure before the canary.

**Throughput checkpoint.** After the runtime compatibility pass and the first typed flow, record how many files and callers changed, which dependency blockers remain, how many verification runs passed, and how many discrepancies needed billing-owner review. Use that evidence to size the remaining flows. Parallelize work on flows with disjoint callers and state. Keep shared money and ledger rules under one owner. In my judgment, agents can accelerate mechanical edits, but replay, reconciliation, and review should set the rollout pace.

**Principles that changed the plan:** **Code is cheap, proof is not** shifted the estimate toward verification rather than line count. **Prove it works** made financial replay and the production canary release gates. **Model the domain** and **Boundary discipline** put typed billing values and input parsing ahead of blanket annotation. **Converge on the target** made deleting each superseded path part of finishing the flow.


=============== RESPONSE ambition-rewrite-02 ===============

**My judgment: upgrade the runtime, but don't approve a quarter-long rewrite.** Based on what you shared, I infer that customers are better served by preserving billing behavior while you move to a supported runtime. The next maintainer should inherit repeatable checks for what customers are charged and typed interfaces where they change billing rules, not just a cleaner directory tree.

The 30k lines, roughly 40% coverage, and quarter estimate are your reported figures. I haven't verified them. I would treat the coverage number as a warning about what you may not know, not as a target to raise before starting. If production still runs Python 3.6, prioritize the runtime move. If “3.6-era” describes the code rather than the deployed runtime, verify the actual runtime before assigning urgency.

| Option | My assessment |
|---|---|
| Full rewrite | I infer this has the highest cutover risk because it changes the implementation, runtime, and layout together. Reconsider only if a concrete blocker makes preserving the existing implementation more expensive or less safe. |
| Runtime upgrade only | I infer this is enough if runtime support is the main problem and billing changes are already easy to make. |
| Runtime upgrade, then selective typing and refactoring | I recommend this default. It lets you stop after the upgrade or after any useful slice, without committing to a quarter upfront. |

## How I'd run it

1. **Fund a two-week pilot, not a rewrite.** Give one engineer ownership and name a billing-domain reviewer. Confirm the deployed runtime, then try building and running the existing service on 3.13 with the smallest dependency and compatibility changes possible. Keep module moves and broad annotation work out of that diff. Treat 3.13 as a candidate until the build, deployment environment, and key dependencies prove compatible.
2. **Capture billing behavior before changing it.** Start with one representative flow, such as renewal invoicing. Use synthetic or approved sanitized fixtures and run the same inputs through the current build and the candidate build. Compare customer-visible totals, rounding, invoice lines, ledger entries, and payment or event intents. Exercise retries and duplicate delivery with external writes disabled. Have the billing reviewer classify any mismatch as intended behavior, a known bug to fix separately, or an unexplained difference that blocks rollout.
3. **Ship the runtime separately.** Expand the checks to the money-moving paths you actually operate. Require no unexplained differences, then canary the runtime change with reconciliation, failure, and queue-lag checks. Keep the prior build deployable and rehearse rollback. Don't let both builds issue charges for the same work. Reconcile any in-flight actions before replaying them, since rolling back code does not undo a charge.
4. **Type and reorganize one boundary at a time.** Pick a flow the team changes often or finds hard to review. Name its data first, such as money with currency, invoice lines, and payment outcomes. Type the inputs and outputs, enforce checks for that slice in CI, and move files only if doing so clarifies ownership or removes coupling. Leave untouched modules alone unless the next slice gives you a reason to change them.

**Day-ten decision.** Ask for the 3.13 build result, the parity results for one flow, the blockers still open, and a revised estimate based on the work done. If compatibility looks tractable and the results agree, fund the runtime rollout. If a dependency blocks 3.13, compare replacing it with moving first to another supported version. Fund more typing or layout work only where the pilot or recent changes identify a specific maintenance cost.

## Throughput checkpoint

*throughput checkpoint: n/a, read-only investigation*

For the proposed delivery:

- **Blocking first steps.** Confirm the deployed runtime, agree on billing invariants, and capture known-good outputs.
- **Independent workstreams.** Dependency compatibility and fixture preparation can proceed in parallel once owners agree on the flow and comparison outputs.
- **Shared mutable state.** Keep replay isolated from live writes. Give one rollout owner control of queue routing and cutover.
- **Smallest safe decomposition.** Use one delivery owner, one billing reviewer, and one flow for the pilot. Don't split the service to parallelize the migration.

**Principle applied: [Prove it works](/plugin/skills/principles/references/prove-it-works.md).** It changes the release gate. A passing build and higher coverage are useful, but the gate is agreement on billing outputs and side effects, checked after each isolated change.


=============== RESPONSE ambition-rewrite-03 ===============

**Modernize the billing service, but don't commit to a quarter-long rewrite.** My judgment is that customers are better served by keeping billing behavior stable while you upgrade the runtime, and maintainers are better served by getting tested, typed code in the modules they actually change.

I'm treating 30k lines, roughly 40% coverage, and a quarter for the rewrite as team-reported inputs. I haven't inspected the repo. In particular, "3.6-era" doesn't tell me what Python version runs in production.

| Option | My assessment |
|---|---|
| Defer everything | Reasonable if production already runs on supported Python and the code isn't slowing billing work. If production still runs 3.6, prioritize getting off it. |
| Upgrade the runtime, then improve one billing path at a time | My default. It separates interpreter and dependency failures from changes to money-moving logic, and gives you a useful stopping point after each release. |
| Rewrite and cut over | I'd consider it only if demand for a different billing model or a hard platform constraint makes incremental work impractical. Cleaner folders and type annotations don't justify the cutover on their own. |

### How I'd run it

1. **Fund a two-week pilot, not a quarter.** Give one engineer ownership and pair them with someone who knows billing operations. Confirm the deployed runtime and check the database driver, payment SDK, workers, and build image against 3.13. Pick one representative path, such as invoice calculation, that you can exercise without making live charges.
2. **Capture billing behavior before changing it.** Use existing tests and sanitized fixtures to check amounts, currency rounding, credits, and invoice or ledger entries. Where the chosen path includes retries or duplicate events, assert that they don't create duplicate effects. Treat unexplained differences as blockers. Have the billing owner decide whether any known discrepancy is a bug, and fix it separately. I would use coverage to find gaps, not as a release gate.
3. **Upgrade the runtime separately from typing and module moves.** Keep schemas, job payloads, and billing rules unchanged where possible. Run the same fixtures on both versions. If you replay production inputs, disable payment calls, writes, and notifications. Compare billing outputs before rollout. Canary only if you can route work without two versions processing the same event. Rehearse rollback with in-flight jobs and reconcile outcomes afterward. Rolling back code doesn't undo a charge.
4. **Type and reorganize the pilot path in small changes.** Start with money and currency, billing inputs and outputs, and payment-provider responses. Enforce type checks on the module you touch rather than annotating all 30k lines. Move code when it makes a billing rule easier to find or test. Skip the service-wide folder redesign until the pilot shows a concrete reason for it.

**At the end of two weeks, make a funding decision.** Ask for the dependency blockers, unexplained billing differences, rollback evidence, and actual effort for the pilot. If the runtime upgrade is tractable, finish it even if the typing work doesn't earn more time. If the pilot makes a recurring change safer or easier, fund the next named path. If the evidence is inconclusive, fund only the work needed to resolve the blocker, not the rewrite.

**Principles that changed the plan:** *Prove it works* made billing outcomes and rollback evidence the gates instead of coverage or a passing type check. *Boundary discipline* and *Model the domain* put types at billing boundaries and on money and currency before package layout.

Throughput checkpoint: n/a, read-only investigation.


=============== RESPONSE ambition-rewrite-04 ===============

**Modernize the billing service, but don’t commit to a quarter-long rewrite.** Get it onto a supported Python version first, then improve typing and module boundaries as you change the code. Python 3.6 is end-of-life; that’s a reason to prioritize the runtime upgrade, not to bundle it with a redesign. And 40% coverage tells you less about migration risk than whether your tests catch a duplicate charge or a one-cent rounding difference.

I’d run it in three stages:

1. **Fund a two-week discovery and safety sprint.** Inventory dependencies and deployment constraints, and try running the existing service on Python 3.13 in CI. Identify which dependencies actually block the upgrade. In parallel, add characterization tests for your highest-risk billing flows: invoice totals and rounding, retries and duplicate events, refunds, and reconciliation. Assert on money amounts, ledger entries, and external calls—not just HTTP responses. End the sprint with a blocker list, a working CI job or a clear explanation of what prevents one, and an estimate for the runtime upgrade alone.
2. **Ship the runtime change separately.** Keep module moves and broad annotation changes out of this release. Compare old and new behavior using sanitized billing cases or a replay with payment and ledger writes disabled. Roll out gradually where your deployment allows it, monitoring billing-specific signals such as reconciliation discrepancies, duplicate attempts, and failed invoice runs. Keep the old deployment ready for rollback, and define how you’ll reconcile transactions already processed before retrying anything: rolling back code doesn’t undo a charge. If a dependency blocks 3.13, consider a supported interim version rather than leaving the service on 3.6 indefinitely.
3. **Type and restructure one billing workflow at a time.** Start with boundaries where types can prevent costly mistakes: money and currency, payment-provider payloads, and invoice or payment state transitions. Enforce type checking in migrated modules without making the whole legacy tree pass on day one. Move code when doing so makes a workflow easier to test or change independently; don’t make a cleaner directory tree a release milestone.

Give one person ownership and reserve team capacity up front, so this doesn’t become spare-time work. Revisit the rewrite only if the discovery sprint exposes a concrete constraint that incremental changes can’t address. Even then, require a plan to cut over one workflow at a time and prove that it produces the same financial results before expanding the scope.


=============== RESPONSE ambition-rewrite-05 ===============

**Modernize the billing service, but don’t start with a quarter-long rewrite.** Treat the unsupported Python 3.6 runtime as a priority; treat typing and module layout as incremental improvements. Doing all three at once makes it harder to tell whether a billing discrepancy came from a runtime change, a dependency upgrade, or a rewritten rule.

I’d run it in four stages:

1. **Time-box discovery to one or two weeks.** Give one engineer ownership and reserve explicit team capacity. Inventory dependency and deployment blockers for Python 3.13, then map the billing flows where a regression would cost money: invoice totals and rounding, renewals and proration, refunds, payment retries, and duplicate events. End the time box with a migration estimate based on actual blockers, not line count.
2. **Build a safety net around money movement.** Don’t make raising coverage from 40% to an arbitrary target the gate. Add characterization tests for representative invoices and ledger entries, plus invariants such as “replaying an event doesn’t create another charge.” Check expected results against billing rules or reconciled records; otherwise, you risk preserving existing bugs as intended behavior.
3. **Upgrade the runtime with minimal behavior changes.** Keep dependency and compatibility work separate from module moves. Compare old and new outputs on representative inputs in a replay environment with payment calls and writes disabled. Investigate unexplained differences in totals, invoice lines, or ledger entries before rollout. Roll out gradually where practical, with reconciliation checks and a rollback plan that accounts for writes already committed—not just redeploying the old version.
4. **Add types and improve layout one slice at a time.** Start at boundaries such as payment-provider payloads, money and currency values, and invoice or ledger records. Enforce type checking in CI for the modules you’ve migrated, then expand it as you touch adjacent code. Move code when it clarifies ownership or makes a billing rule easier to test, not simply to reach a target directory structure.

Revisit the rewrite decision after the discovery time box and one representative migration slice. A bounded replacement may make sense if a subsystem is demonstrably harder to migrate than replace **and** you can compare its outputs and cut it over independently. Otherwise, the first milestone should be a supported runtime with verified billing behavior—not a new codebase.


=============== RESPONSE ambition-rewrite-06 ===============

**Upgrade the runtime; don’t approve the quarter-long rewrite.** If production still runs Python 3.6, getting onto a supported runtime is worth prioritizing. Typing and module layout are separate decisions: do them where they prevent billing mistakes or make recurring changes easier. Forty percent test coverage is a reason to protect critical behavior before changing it, not a reason to rewrite or chase a global coverage target.

I’d approve a **two-week first slice**, with one owner and a checkpoint, not a commitment to finish the migration in two weeks:

1. **Trace one real billing flow end to end.** Pick the highest-risk flow, such as invoice creation through payment and ledger posting. Identify where retries happen and where money moves. Use the existing test harness to pin down the behavior you can’t afford to change: amounts and rounding, duplicate requests, and recovery after a partial failure. Use sanitized fixtures and stub external payment calls.
2. **Get the current code running on 3.13 in CI.** Check dependencies, deployment images, and worker entry points. Keep the diff to compatibility fixes and required dependency updates—no file moves or annotation sweep. If a dependency blocks 3.13, name the blocker and compare fixing it with landing on another supported version first.
3. **Roll out the runtime change on its own.** Compare old and new results on the same sanitized inputs without repeating live charges or writes. Canary using the existing deployment process. Watch billing-specific signals—reconciliation discrepancies, duplicate attempts, failed jobs, and queue lag—and agree on rollback triggers before rollout. Don’t couple the runtime change to a schema migration.

At the checkpoint, review what passed, what still blocks rollout, and the estimate to finish **the runtime upgrade alone**. Once it’s stable, type the money-sensitive boundaries you touch—amounts and currencies, payment results, provider payloads—and enforce checking there with existing tooling if available. Move a module only when a concrete change shows that its current layout is causing churn.

Revisit a rewrite only if the incremental work exposes a specific constraint you can’t remove in place, and you can name a billing slice with a safe cutover and rollback. Until then, skip the new directory tree and repo-wide typing target.


=============== RESPONSE ambition-rewrite-07 ===============

**Upgrade the runtime; don’t approve the quarter-long rewrite as proposed.** If production still runs Python 3.6, getting off an unsupported runtime is worth prioritizing. If “3.6-era” only describes the code style, confirm what actually runs before assigning urgency. Neither 30k lines nor 40% coverage tells you that a rewrite will pay off. Treat runtime compatibility, typing, and module layout as separate decisions so you can ship the first without committing to the other two.

### How I’d run it

1. **Trace one real billing flow and lock down its behavior.** Follow a charge or invoice from its API or job entry point through calculation, provider calls, persistence, and retries. Use the existing test harness and provider sandbox or fakes. Assert money amounts and rounding, invoice or ledger state, and the absence of duplicate charges on retry. Add equivalent checks for refunds, credits, and other flows the service actually owns before rollout. Use sanitized fixtures; don’t turn known billing bugs into expected behavior. A passing reconciliation is a better release gate than a higher coverage percentage.

2. **Make Python 3.13 a compatibility change, not a design change.** Check dependencies, native extensions, base images, and deployment tooling first. Run the same billing scenarios on the current runtime and 3.13, comparing financial outputs and side effects. Keep module moves, broad annotations, and schema changes out of this diff. Deploy to staging and drive the real worker or API against a sandbox before canarying a bounded set of accounts or jobs. Assign each live job to one version only—never replay live payment writes to compare versions. Reconcile provider and ledger records before expanding. Rehearse rollback, including what happens to in-flight jobs; rolling back code does not undo a charge.

3. **Type and reorganize one slice after the runtime is stable.** Pick a path the team changes often or where type confusion has caused defects. Type the entry point and the money or state transitions it depends on; enforce checking for that slice, not all 30k lines. Delete confirmed dead code before moving anything. Move code only if it removes a repeated cross-module edit or makes ownership of a billing rule clearer. Keep the rest in place.

**What I’d approve now:** the behavior tests, the 3.13 compatibility and rollout work, and one typed pilot. Scope each by the files it touches and the verification runs it must pass. After the pilot, expand only if it catches real mistakes or makes routine changes easier to review and verify. A broader rewrite earns its place only if the team can point to a concrete requirement the existing structure blocks, show why a smaller change won’t work, and demonstrate how to cut over and reconcile safely.


=============== RESPONSE ambition-rewrite-08 ===============

**Upgrade the runtime; don’t approve a quarter-long rewrite.** If production still runs Python 3.6, getting onto a supported runtime is maintenance you shouldn’t keep deferring. If the code merely *looks* like Python 3.6 but runs on a supported version, there’s less urgency. Either way, typing and module cleanup should earn their scope separately. Neither 30k lines nor 40% coverage tells you whether a rewrite will pay off.

I’d run it as a series of independently shippable changes:

1. **Prove the billing behavior you need to preserve.** Trace one real flow from event or request through calculation, persistence, and any payment or ledger side effects. Use the existing test harness to pin down the highest-risk behavior: rounding, duplicate delivery and retries, and failures between charging and recording the result, wherever those apply. Assert amounts, state transitions, and side effects—not internal call order. Use coverage to find blind spots, not as a release target. If a test exposes a known bug, decide explicitly whether to preserve it for the migration or fix it in a separate change.
2. **Make Python 3.13 a compatibility change, not a redesign.** Inventory dependencies, the deployment image, and every process entry point, including workers and scheduled jobs. Bring up a 3.13 CI lane and keep the old runtime as a comparison baseline where practical. Fix incompatibilities with the smallest diffs; don’t move modules or mass-annotate code in those patches. If a critical dependency blocks 3.13, evaluate a supported interim runtime rather than letting the upgrade stall behind a dependency rewrite.
3. **Verify the running service before switching over.** Exercise the actual app and workers in staging, with payment side effects isolated. Compare billing outputs and state transitions on representative inputs; don’t replay live charges. Use your existing staged rollout mechanism if you have one. Agree on stop conditions before rollout: unexplained amount differences, duplicate financial effects, or reconciliation failures. Keep the deployment backward-compatible where possible, and remember that rolling back an image does not undo a charge.
4. **Type and reorganize where it makes the next change safer.** Start with a real seam—say, the handoff from invoice calculation to persistence—and type its inputs and outputs with one checker, enforced in CI for that scope. Expand when you touch adjacent code or when the checker catches a meaningful class of mistakes. Delete confirmed dead code before moving anything. Move a module when the current layout causes a concrete problem, such as a cycle or duplicated billing rules; leave cosmetic reshuffling alone.

**What I’d approve now:** one owner, one critical billing flow with regression tests, and one 3.13 compatibility pass. Have the team return with the actual blockers, the files each fix touches, and the verification runs needed to ship. That gives you a better decision than the full-quarter estimate: if the runtime upgrade is straightforward, ship it and stop; if a specific subsystem repeatedly blocks safe changes, replace that subsystem behind a tested boundary. Reach for a full rewrite only if the evidence shows those boundaries can’t be made safely in the existing service.


=============== RESPONSE ambition-rewrite-09 ===============

**Yes to modernizing the billing service; no to committing a quarter to a rewrite.** Separate the runtime upgrade, typing, and module cleanup. Python 3.6 is end-of-life, so prioritize getting onto a supported runtime. With roughly 40% test coverage, changing the runtime, structure, and behavior all at once would make billing discrepancies hard to diagnose.

I’d fund a **two-week first milestone**, then use what you learn to scope the rest:

1. **Find the runtime blockers.** Inventory dependencies and deployment constraints, and add a Python 3.13 CI job alongside the current one. Keep compatibility changes separate from refactors. If a critical dependency blocks 3.13, weigh a supported interim version against the cost of two migrations rather than letting the ideal target stall the upgrade.
2. **Protect the money paths before changing them.** Add characterization tests for invoice totals and rounding, discounts and credits, retries and duplicate events, and refunds or reconciliation where applicable. Assert both the amounts and the side effects: a retry that returns the right total but charges twice is still broken. Use sanitized fixtures, and distinguish intentional behavior from known bugs so the tests don’t turn every historical quirk into a requirement.
3. **Move the runtime without redesigning the service.** Before cutover, replay representative inputs in an isolated environment with payment calls and other external writes disabled. Compare invoice totals and ledger effects, and investigate unexplained differences. Roll out gradually if your deployment supports it, with a tested rollback and monitoring for billing discrepancies—not just exceptions.
4. **Type and restructure one slice at a time.** Start with boundaries where types catch expensive mistakes: money and currency, payment-provider payloads, and invoice or ledger records. Enforce type checks on new and migrated modules rather than requiring a clean check across all 30k lines. Move modules when doing so makes a concrete change easier to test or ship, not just to improve the directory tree.

At the end of two weeks, ask for **a dependency blocker list, a working CI job on the target runtime, and regression tests for one critical billing flow**. That gives you evidence to estimate the runtime migration separately from the cleanup. I’d revisit a full rewrite only if the first few slices show that the existing structure prevents safe incremental changes—and even then, replace one billing capability at a time rather than betting on a single cutover.


=============== RESPONSE ambition-rewrite-10 ===============

**Upgrade the runtime and type the billing paths that matter. Don’t commit to a quarter-long rewrite.** If production still runs Python 3.6, getting off an unsupported runtime is a priority. If the code is merely written in a 3.6-era style, that alone isn’t a reason to replace it. Neither 30k lines nor 40% coverage tells you whether the module layout is the problem.

### How I’d run it

1. **Prove one real billing flow before changing it.** Trace an invoice from its trigger through calculation, persistence, and any payment or ledger side effects. Use the existing test harness to capture expected amounts, rounding, and retry behavior. Include a failure after an external call but before local state is saved, if that can happen in your flow. Verify expected outcomes against billing rules, not just current output: you don’t want to enshrine a bug as a compatibility requirement.

2. **Upgrade Python without moving modules.** Check Python 3.13 support for the dependencies and deployment environment first. Keep compatibility changes separate from cleanup so failures are easy to attribute. Where feasible, run the same tests on the old and new runtimes; then drive the real flow in staging with sandbox integrations. Compare invoice totals, ledger entries, and payment attempts—not just response codes.

3. **Roll out with reconciliation and a rollback plan.** Use your existing rollout mechanism and start with a small cohort if you can keep each account or job on one execution path. Compare old and new outputs offline or without side effects; never run both versions against live payment writes. Before expanding, reconcile the first representative billing run and check for unexplained amount differences, duplicate attempts, and stuck jobs. Rolling back the binary won’t undo charges or ledger writes, so decide in advance how to pause processing and reconcile partial work.

4. **Type and reorganize in small, independently shippable slices.** Start with the functions that calculate money and the boundaries that read or write billing state. Enforce checking on those files rather than turning on strict mode across the repo. Delete code you’ve confirmed is unused; move code only when it clarifies ownership of a billing rule or makes a real flow easier to test. Leave stable modules alone.

**Fund the first slice, then re-estimate from evidence.** Make its deliverables a dependency compatibility report, a verified billing flow, and a deployable runtime change—or a concrete blocker. Use what you learn to size the rest by affected files and verification runs. If that slice shows the current structure forces the same billing rule to be changed or tested in several places, replace that subsystem behind its existing entry point. Skip a service-wide rewrite unless you can show why those smaller replacements won’t solve the problem.


=============== RESPONSE ambition-rewrite-11 ===============

**Upgrade the runtime, but don’t commit to a quarter-long rewrite.** If production still runs Python 3.6, getting off an unsupported runtime is worth prioritizing. If it’s already on a supported version and the code merely looks like 3.6, move to 3.13 through your normal upgrade process. Either way, 30k lines and 40% coverage tell you to be careful about changing billing behavior; they don’t tell you to replace the service.

I’d run it as three separately shippable changes:

1. **Prove the billing behavior you need to preserve.** Trace a real billing run from its trigger through invoice calculation, persistence, and external side effects. Use the existing test harness to pin down the paths where a mistake costs money: rounding, retries and duplicate events, and any refunds or prorations the service actually handles. Assert amounts, ledger entries, and whether a charge is attempted—not just return values. Replay representative, sanitized inputs in an isolated environment with outbound payments disabled. Don’t make a repo-wide coverage target the gate.
2. **Ship Python 3.13 without moving modules or adding types.** Start with the dependency manifest, CI job, and deployment image. Verify that the actual database driver, payment SDK, and worker stack support the target; fix only the incompatibilities that block the upgrade. Run the same billing scenarios on the current and target runtimes and investigate unexplained differences before rollout. Canary a bounded set of accounts or jobs if routing permits, with only one runtime allowed to execute each real charge. Keep the previous artifact ready, and verify that rollback won’t replay completed work. Watch reconciliation deltas, duplicate charge attempts, failed jobs, and queue lag.
3. **Type and reorganize one billing flow at a time.** Pick a flow the team changes often or repeatedly breaks. Type its inputs and outputs and the money calculations behind them; enforce checking on that slice without requiring the whole repo to pass strict mode. Delete confirmed dead code before moving anything. Move modules only where the current layout makes the flow harder to understand or change. Keep behavior fixes separate from moves so reviewers can tell what changed.

**Approve the runtime upgrade and one typed pilot, not the whole rewrite.** Size the work by the files touched and the verification each slice needs. After the pilot, ask whether a real billing change got easier to review and verify. Keep going where the answer is yes. Replace a specific module if the existing shape makes safe changes harder than replacement and you can prove parity at its boundary; leave stable modules alone.


=============== RESPONSE ambition-rewrite-12 ===============

**Modernize the service in place. Don’t approve a quarter-long rewrite.** If production is still on Python 3.6, getting off an end-of-life runtime is the priority. Typing and module layout are separate decisions: type the boundaries where mistakes are costly, and move code only where the current layout makes changes harder.

I’d approve a **two-week first slice**, with one accountable owner and protected time. The deliverable is a compatibility assessment and a tested billing flow on Python 3.13 in CI or staging—not a promise to cut over production in two weeks.

1. **Trace one real billing flow end to end.** Follow invoice calculation through persistence, payment submission, retries, and reconciliation. Use the existing test harness to pin down the outcomes that matter: amounts and rounding, duplicate requests, and what happens when a payment provider times out after accepting a charge. Use sanitized fixtures and stub external writes. Don’t make a service-wide coverage percentage the gate; 40% doesn’t tell you which money-moving paths are protected.
2. **Make the runtime change as mechanical as possible.** Check dependencies, build images, web processes, workers, and scheduled jobs against 3.13. Run the existing suite and the new billing checks on both runtimes while the test setup supports it. Keep file moves, broad annotation changes, and billing-rule fixes out of the runtime diff. If a critical dependency blocks 3.13, identify the blocker and decide whether a supported intermediate version gets you off 3.6 sooner.
3. **Roll out against billing outcomes, not just error rates.** Before production, extend the checks to the other critical money-moving paths you discover. Compare old and new calculations on the same inputs without submitting payments twice. Canary where you can isolate traffic without letting both versions process the same job. Agree up front on halt criteria—unexplained amount differences, duplicate charges, reconciliation discrepancies—and rehearse rollback. Rolling back code won’t reverse a charge.
4. **Type and reshape code as you change it.** Start with amounts and currencies, payment-provider inputs, and invoice state transitions. Enforce checks on the modules you’ve brought under typing, not all 30k lines on day one. Remove verified dead code before moving live code. Leave stable modules alone unless their layout is causing a concrete problem.

At the two-week review, use the blockers and test results to scope the next increment. Revisit a rewrite only if the pilot exposes a specific constraint that in-place changes can’t solve economically. A cleaner directory tree and a higher annotation count aren’t enough to justify reimplementing billing behavior.


=============== RESPONSE ambition-rewrite-13 ===============

**Upgrade the runtime. Don't approve a quarter-long rewrite.** My judgment is that customers are better served by keeping billing behavior stable while you move to Python 3.13. The next maintainer should inherit a supported runtime, repeatable checks for money-moving flows, and typed contracts where they prevent mistakes.

I'm treating the 30k lines, roughly 40% coverage, and quarter estimate as team-reported inputs. I infer that the main risk is billing behavior the tests don't pin down. The coverage number alone doesn't tell us whether retries, rounding, or refunds are protected. If production still runs Python 3.6, prioritize the runtime upgrade. If only the code style dates to 3.6, verify the deployed runtime before assigning urgency.

| Approach | Tradeoff |
|---|---|
| In-place runtime upgrade, then targeted typing and cleanup | My recommendation. It lets the team isolate runtime regressions and stop after each useful delivery. |
| Full rewrite | I'd consider it only if a pilot shows that the current design blocks a concrete business need and that smaller changes can't unblock it. A cleaner module tree alone doesn't justify the cutover risk. |
| Defer everything | I'd defer cosmetic cleanup. I wouldn't defer a move off an unsupported production runtime. |

### How I'd run it

1. **Fund a one-week pilot, not a quarter.** Give one engineer ownership and pair them with someone who knows billing operations. Inventory the deployed runtime, dependencies, workers, and scheduled jobs. Try building and starting the existing service on 3.13 in CI or staging. Record the actual blockers. Keep formatting, typing, and file moves out of the runtime diff.
2. **Pin down what must not change.** Use sanitized or synthetic cases for the billing flows you actually run. Start with invoice totals and rounding, retries and duplicate events, and refunds or credits. Compare amounts, currencies, ledger entries, and intended external effects on the old and new runtimes. Replay without sending charges or customer messages. Investigate every unexplained difference. If you find an existing billing bug, fix it separately rather than silently changing behavior during the upgrade.
3. **Roll out the runtime on its own.** Keep the old artifact deployable and avoid incompatible data changes. Canary a bounded share of work if routing allows, with one live processor per event. Agree on rollback triggers before rollout. Watch reconciliation, duplicate or missing charges, failed jobs, and queue lag. Have billing operations validate the first relevant billing cycle. Rolling back code will not reverse a charge.
4. **Type and reorganize where it pays.** Start with money and currency, billing identifiers, and contracts at payment-provider and ledger boundaries. Enforce type checks on the first migrated slice in CI rather than requiring the whole repository to pass. Move modules separately when the current layout makes a real change harder. Skip the repo-wide reshuffle unless that work exposes a specific reason for it.

**Pilot decision:** If the service boots on 3.13 and one representative billing flow matches end to end, estimate the remaining upgrade from the blockers you found. If it doesn't, price the smallest dependency replacement or compatibility change first. Don't turn a failed pilot into automatic approval for a rewrite.

**Principle used:** *Prove it works* changed the release gate. Passing CI and improving line coverage aren't enough. Require matching billing outputs on replay and reconciliation after rollout, with the runtime change isolated so a failure is easier to trace.

throughput checkpoint: n/a, read-only investigation


=============== RESPONSE ambition-rewrite-14 ===============

**Modernize the billing service, but don’t commit to a quarter-long rewrite.** If production still runs Python 3.6, prioritize getting onto a supported runtime. If it’s merely 3.6-era code running on a supported version, the urgency is lower. Either way, treat the runtime upgrade, type adoption, and module cleanup as separate changes. Combining them makes billing discrepancies harder to diagnose and rollback harder to trust.

I’d start with a **two-week, time-boxed pilot**:

1. **Protect billing behavior before changing it.** Pick one representative flow, such as invoice creation with a retried payment. Add characterization tests for monetary amounts and rounding, invoice and ledger entries, and duplicate-charge prevention. Use sanitized or synthetic fixtures. The 40% coverage figure is less useful than knowing which money-moving behaviors have assertions. Record known bugs separately so you don’t accidentally make them permanent expectations.
2. **Find the runtime blockers.** Try the existing service and its dependencies on Python 3.13 in CI. Inventory incompatible libraries, deployment assumptions, and workers or scheduled jobs that run outside the main service. Keep this work free of module moves and broad typing changes. If a critical dependency blocks 3.13, weigh a supported interim version against the cost of upgrading or replacing that dependency.
3. **Modernize one seam.** Extract a small, mostly pure calculation behind its existing interface and type it. Enforce type checking for that module and new typed modules, not all 30k lines at once. Use the pilot to learn whether the proposed layout actually makes billing changes easier to test and review.

After the pilot, use the dependency blockers, test gaps, and effort from that first slice to estimate the remaining work. Give the migration a named owner and reserved capacity each sprint; otherwise it will keep getting deferred. Roll out the runtime upgrade separately from the restructuring. Compare old and new outputs with isolated replay that **cannot charge customers or write to the production ledger**, then use a controlled rollout with explicit rollback criteria for financial discrepancies, duplicate operations, and processing failures. Keep schema and queue changes backward-compatible where rollback depends on them.

I’d reconsider a rewrite only if the pilot uncovers a concrete architectural constraint that incremental changes can’t remove at reasonable cost. “Untyped and messy” isn’t enough. The first milestone should be **the same billing behavior on a supported runtime**, not a new directory tree or a repo-wide typing target.


=============== RESPONSE ambition-rewrite-15 ===============

**My recommendation: modernize the billing service now, but don't approve a quarter-long, all-at-once rewrite.** If production still runs Python 3.6, make the runtime upgrade the first deliverable. If “3.6-era” describes only the code, verify the current runtime before assigning that urgency. I infer that customers are better protected by a migration that proves their bills stay the same at each release. Maintainers should inherit typed billing rules organized by what they do, without two implementations to keep in sync.

I haven't inspected the repository or measured the work. The reported 40% coverage doesn't tell us whether retries can double-charge a customer or whether refunds reconcile. The quarter estimate is for a bundled rewrite. I wouldn't use it to price a migration whose mechanical edits and verification can be sized separately.

### How I'd run it

1. **Capture billing behavior before changing it.** Inventory the entry points, scheduled jobs, payment integrations, and ledger writes. Reuse the existing test setup to replay sanitized cases against the current service. Start with rounding, prorations, refunds, retries after ambiguous provider responses, duplicate events, and period boundaries. Compare invoice lines, amounts and currencies, ledger entries, and intended provider calls. Run replays with external writes disabled. If a fixture exposes a known billing bug, record it and fix it separately rather than silently changing the migration baseline.
2. **Upgrade the runtime without moving the business logic.** Inventory dependency pins, native extensions, and deployment images. Run the existing suite and billing replays on the current runtime and Python 3.13. Keep dependency and compatibility fixes separate from module moves. Require a staging run through the actual billing entry points and jobs before an approved production canary. Confirm rollback against the same stored data before rollout.
3. **Type and reorganize one complete billing flow at a time.** Start with a bounded flow that has real business rules, such as invoice calculation if it can run without collecting payment. Define the money, invoice, and adjustment types before moving the rules. Validate external inputs at the boundary. Enforce strict checking in migrated modules, and prevent regressions in type coverage elsewhere. Move all callers of a migrated module together and delete the old path. Rewrite individual modules where the current structure obscures a rule; skip cosmetic moves that don't clarify ownership.
4. **Make parity a release gate.** Require zero unexplained differences in money, ledger postings, or payment intent on the replay set. Give each canary one writer for any given billing operation. Compare reconciliation differences, duplicate-charge indicators, job failures, and processing lag against the baseline. Agree on rollback thresholds before rollout. Don't assume rolling back code undoes an external charge.

### Throughput checkpoint

**After the first complete flow passes replay and staging**, reprice the remaining migration. Record the files and callers changed, the agent work that could run independently, the verification runs required, and the mismatches that needed a billing expert. Group the remaining flows by those costs rather than by lines of code. My inference is that this will show whether the bottleneck is editing Python, making dependencies work, or establishing what correct billing looks like. If parity is the bottleneck, put the next effort into fixtures and reconciliation rather than opening more refactor branches.

The principles that changed the plan were **Code is cheap, proof is not**, which shifted the estimate from edits to verification; **Prove it works**, which made replay and staging release gates; **Model the domain** and **Boundary discipline**, which put typed billing values and input validation before module moves; and **Converge on the target**, which means migrating callers and deleting the old path together within each flow.


=============== RESPONSE ambition-rewrite-16 ===============

**Modernize it, but don’t approve a full rewrite.** If production still runs Python 3.6, prioritize getting off the unsupported runtime. If the code is merely 3.6-era and already runs on a supported version, start with the billing flow that causes the most incidents or slows changes the most. Neither 30k lines nor 40% coverage tells you that replacing the service is safer than changing it in place.

Separate the three decisions: **upgrade the runtime, type the boundaries that matter, and move modules only where the current layout makes changes harder.** Each should be independently reviewable and deployable.

### How I’d run it

1. **Prove one real billing flow first.** Pick a flow with meaningful financial risk, such as invoice generation through payment and ledger posting. Trace its entry point, database writes, provider calls, and retry behavior. Use the existing test harness to pin down amounts and rounding, persisted records, and what happens when a job or webhook is delivered twice. Confirm expected results against billing rules; don’t turn a known bug into a golden fixture. Exercise the flow in staging with a provider sandbox. This is the first milestone, not a service-wide coverage target.

2. **Ship the runtime upgrade without redesigning the service.** Check Python 3.13 support across dependencies, build images, and deployment tooling. Keep compatibility fixes separate from typing and file moves. Run the suite and the same billing scenarios on the old and new runtimes, then canary the new runtime and reconcile billing outputs. Keep the previous artifact deployable and avoid schema changes in this release. Define when to halt before rollout: unexplained financial mismatches or duplicate charges are stop conditions. Rolling back code won’t undo a charge, so have a way to pause the affected workers and reconcile what already happened. If a hard dependency blocks 3.13, consider a supported intermediate runtime rather than waiting on a rewrite.

3. **Make the pilot flow easier to change.** Type the contracts people actually rely on: money and currency, invoice inputs and results, provider responses, and the data passed into persistence. Enforce checking on the selected modules in CI rather than requiring a clean check across all 30k lines. Delete confirmed dead paths and collapse redundant wrappers before moving files. Move code only if it clarifies ownership of a billing rule or lets you change that rule in one place. Verify the same flow again after each behavioral or structural change.

4. **Use the pilot to decide how far to go.** Scope the next slice by entry points, files, external effects, and verification runs. Compare review effort, the number of modules a routine change touches, and confidence in reconciliation—not lines annotated or moved. If the runtime is supported and the remaining code is stable, stop there and modernize it when you next need to change it.

I’d revisit a rewrite only if the pilot exposes a concrete architectural blocker—for example, a billing invariant that cannot be enforced in one place without replacing a coupled subsystem. Even then, replace that subsystem first and compare its outputs without letting both implementations perform live writes or charges. **Fund the first verified slice, not the quarter-long rewrite.**


=============== RESPONSE ambition-rewrite-17 ===============

**Modernize the billing service now. Don't replace it in one cutover.** My judgment is that customers are better protected by a migration that proves each change preserves what they owe and what they get charged. Maintainers should inherit a Python 3.13 service with typed billing rules, clear module ownership, and tests that explain why an invoice or ledger entry looks the way it does.

I'm working from your description, not repository measurements. The reported 40% coverage doesn't tell us whether the tests exercise the cases that can move money. And I wouldn't use the quarter estimate as a veto. I'd re-estimate the mechanical work by file and dependency group, and the risky work by the number of billing flows, verification runs, and rollout gates.

| Option | My assessment |
|---|---|
| Upgrade the runtime only | A useful first release if dependency compatibility allows it. It leaves the typing and layout problems in place. |
| Upgrade, then replace or refactor one billing flow at a time | **Recommended.** Separate runtime failures from behavior changes and make each release small enough to verify and roll back. |
| Rewrite the whole service and switch at once | I'd reconsider only if the current service has no usable seams *and* a replay against an independent billing oracle shows that a replacement can be proved and cut over safely. |

## How I'd run it

1. **Establish what must not change.** Inventory every entry point that can move money or change billing state, including scheduled jobs and webhook handlers. Build a repeatable replay suite from sanitized fixtures and approved billing examples. Compare invoice lines, currency and rounding, ledger entries, payment intents, and state transitions. Include duplicate events, retries after partial failure, credits, and period boundaries. Use the old service to detect drift, not to decide what's correct. Have billing owners review disputed cases against policy and keep intentional fixes out of modernization changes.

2. **Isolate the Python upgrade.** Test Python 3.13 with the actual dependency set, deployment image, workers, database, and payment sandbox. Keep syntax cleanup, typing, and file moves out of the runtime change. If a dependency blocks 3.13, isolate its replacement or use a supported interim runtime only if that gets the service onto support sooner.

3. **Migrate by billing flow, not by directory.** Start with a calculation that can run without writing to the ledger or calling a payment provider. Add types at the boundaries and to the values that carry billing rules, such as money with currency, billing periods, and payment states. Rewrite a module outright when its structure fights the goal. Require type checks in migrated modules and for new code without making all legacy annotations a release gate. Parallelize independent fixtures and mechanical edits, but give each flow one owner and land changes to shared billing rules in sequence.

4. **Compare safely, then cut over.** Replay the old and new code on the same inputs. If you shadow live traffic, prevent the shadow path from sending any payments, writes, or customer messages. Require zero unexplained monetary or state differences in the agreed replay set. Then canary with exactly one writer per account or event, monitor reconciliation and duplicate attempts, and expand only after relevant scheduled jobs have run. Rehearse switching future work back before cutover. A code rollback cannot undo a charge, so keep a reconciliation and remediation procedure. Delete the old path once the new one has passed those gates.

**Done** means Python 3.13 runs the service in production, each billing flow has a clear home and a typed contract, and the team can rerun the evidence for every migrated flow. I would not require 100% line coverage or annotations on every legacy helper. Neither is a substitute for proving what happens to a customer's bill.

**Principles that changed the decision:** *Code is cheap, proof is not* moved the estimate from a quarter of coding to file groups and verification runs, and kept module rewrites on the table. *Build the lever* made a rerunnable billing comparison the first deliverable. *Prove it works* made reconciliation, single-writer canaries, and a rollback rehearsal release gates instead of relying on CI or coverage alone.

throughput checkpoint: n/a, read-only investigation


=============== RESPONSE ambition-rewrite-18 ===============

**Yes to modernizing billing. No to a quarter-long replacement release.** My judgment is that customers should see no change in what they owe, while maintainers inherit a supported runtime, checked types at billing boundaries, and modules they can change without guessing at side effects.

I haven't inspected the repository or run tests. The reported 40% coverage doesn't tell us whether retries, refunds, or rounding are protected. I would price the work in dependency blockers, files and callers per billing flow, and verification runs. Agents can draft mechanical edits in parallel once the boundaries are clear. Their speed doesn't reduce the evidence needed to change money-moving code.

## How I would run it

1. **Record what billing does today.** Map the paths that create invoices, move money, post ledger entries, and retry failed work. Build a repeatable comparison using sanitized inputs and isolated state. Compare invoice totals, currency and rounding, ledger entries, and payment *intents*, with no live payment calls. Cover refunds, duplicate events, partial failures, and period boundaries where they apply. Treat unexplained differences as blockers. Fix known billing bugs separately rather than silently carrying them into the new implementation or fixing them during the move.
2. **Upgrade the runtime without moving modules.** Try the existing service on Python 3.13 in CI. Inventory blockers across dependencies, packaging, web processes, and workers. Keep compatibility changes separate from layout changes so failures are easier to attribute. If a required dependency blocks 3.13, use a supported interim runtime only if it gets the service off 3.6 sooner. Keep 3.13 as the target.
3. **Move and type one complete billing flow at a time.** Start with a bounded but representative flow, such as invoice calculation if it can be isolated from payment execution. Define the shapes for money, invoice state, and payment requests before changing the logic. Validate external data at entry points and enforce type checks on migrated code. Keep the current layout where it works. Rewrite a module where its structure prevents a clean boundary, migrate all its callers, and delete the superseded path once the cutover is stable. Skip speculative abstractions and file moves that don't make a billing rule easier to own or test.
4. **Release against billing evidence, not a coverage target.** Run the comparison, then exercise the real API and worker paths in staging, including retries and restarts. Roll out with one authoritative writer for each transaction. Reconcile invoice and ledger totals, duplicate charges, and missed work before expanding rollout. Rehearse rollback with in-flight jobs; reverting code doesn't reverse a charge. If old and new versions cannot safely share persisted state, resolve that before cutover.

**Throughput checkpoint.** After the first representative flow, record the files and callers migrated, dependency blockers cleared, verification runs needed, and discrepancies still open. The exit gate is a clean comparison and a successful staging run through the real API and worker. Use that evidence to size the rest of the migration. If compared outputs still disagree or the same inputs don't produce repeatable results, fix the comparison before opening more migration fronts.

**Principles behind the plan.** *Code is cheap, proof is not* changes what I'd estimate and where I'd spend the savings. *Build the lever* makes the billing comparison reusable for every flow. *Model the domain* and *Boundary discipline* put types and validation where they protect billing rules. *Converge on the target* means finishing each flow and removing its old path. *Prove it works* makes reconciliation and real worker runs release gates.


=============== RESPONSE ambition-rewrite-19 ===============

**Upgrade the runtime in place; don’t commit to a quarter-long rewrite.** If production still runs Python 3.6, getting off an unsupported runtime is worth prioritizing now. If the code is merely 3.6-era and already runs on a supported version, there’s less urgency. Either way, typing and module layout are separate decisions. Don’t make them prerequisites for the runtime upgrade.

I’d fund a **one-week compatibility and billing-safety spike**, with one owner and a concrete deliverable: a candidate build on Python 3.13, a list of blockers, and evidence about which billing behaviors are safe to carry forward. Then run it in this order:

1. **Trace the money path before touching the layout.** Walk one invoice from calculation through payment, ledger recording, and reconciliation. Include retries and duplicate events. Use the existing test harness to pin the outcomes that would cost you money if they changed: exact amounts and rounding, one charge on retry, and matching ledger entries. Add refund or period-boundary cases where the service actually handles them. Forty percent coverage tells you where to look, not whether it’s safe to ship. Verify expected outcomes against billing rules; don’t turn a known bug into a golden test.
2. **Make the smallest runtime change that passes those checks.** Run the existing suite and new billing checks on both runtimes in CI while the old one is still deployed. Check dependency support and exercise workers and scheduled jobs, not just web startup. Keep compatibility fixes separate from module moves and billing-rule changes. Aim directly for 3.13; if a hard dependency blocks it, compare replacing that dependency with using a supported interim runtime. Don’t plan a deployment on every intervening Python version.
3. **Roll out without running billing twice.** Compare calculations on the same inputs with payment calls and writes disabled. Then canary on a cohort you can route exclusively to one version, if your deployment supports that. Define stop conditions before rollout: unexplained amount or ledger differences, duplicate charges, or a material rise in failed jobs. Rehearse rollback and reconcile anything already processed—rolling back code doesn’t undo a charge.
4. **Type and reorganize where it pays.** After the runtime is stable, start with money calculations and the inputs and outputs of frequently changed billing paths. Use the team’s existing checker if it has one, and enforce checks on the modules you adopt rather than requiring a repo-wide cleanup. Move code only when a real change exposes a boundary worth separating.

At the end of the spike, review **the compatibility blockers, the billing behaviors you can now verify, and the smallest safely deployable change**. Approve that work first. Revisit a rewrite only if concrete evidence shows the existing design repeatedly blocks necessary changes and incremental fixes aren’t cheaper or safer. A cleaner tree and full typing aren’t enough on their own.


=============== RESPONSE ambition-rewrite-20 ===============

**Inferred recommendation: Fund the Python upgrade now. Do not fund a quarter-long rewrite.** Customers should see the same invoices, charges, and credits throughout the migration. Maintainers should inherit a supported runtime, tests that catch billing regressions, and types where they help people change the code safely.

The reported 30,000 lines and 40% coverage do not tell you which billing rules are protected. My inference is that changing the runtime, types, and module layout together makes a money discrepancy harder to diagnose and the release harder to reverse. Treat the quarter estimate as a planning guess, not as the price of getting off the old runtime.

## How I would run it

1. **Give one owner two weeks to establish the baseline and test the upgrade path.** This is a proposed timebox, not a delivery estimate. Confirm the deployed Python version first. Inventory dependencies, native extensions, and deployment constraints for 3.13. Use the current production build as the baseline. Capture expected behavior for invoice totals, currency rounding, credits, duplicate payment events, and retries after partial failure. Use sanitized fixtures and check persisted ledger entries and payment intents, not just API responses. Have the billing owner review known quirks so the tests don't silently bless a bug.
2. **Ship the runtime change separately.** My default is to target 3.13 and change only what compatibility requires. If a dependency blocks it, price the smallest replacement or a supported interim runtime before revisiting the scope. Compare the old and new builds on the same inputs with payment, ledger, and notification writes disabled during replay. Require zero unexplained money differences. Then canary with one active writer per billing job or partition. Agree on stop conditions for duplicate charges, reconciliation discrepancies, and failed jobs. Rehearse rollback and confirm the old build can read any state the new one writes.
3. **Type one billing workflow end to end.** My first candidate is invoice calculation, assuming it can be isolated from payment execution. Type and validate the inputs, make money and currency explicit, and check the outputs against the baseline. Enforce type checking in CI for the migrated modules. Move code only where a real dependency or recurring maintenance problem justifies it. Skip the service-wide directory reshuffle and blanket annotation pass.

## Throughput checkpoint

At the end of week two, ask the owner for the dependency blockers, one representative old-versus-new billing comparison, the time it took to get that comparison working, and the next independently releasable change. If the comparison is clean and the remaining blockers are bounded, fund the runtime rollout. If the team cannot yet compare charges and ledger effects reliably, fund that verification work before expanding the migration. After the first typed workflow, use the actual effort and review findings to decide whether to schedule another. Reconsider a full rewrite only if that work exposes a specific constraint that incremental changes cannot remove.

**Principle applied: [Prove it works](/plugin/skills/principles/references/prove-it-works.md).** It changed the release gate from "the tests pass on 3.13" to "the two builds produce the same billing effects, and we can safely roll back."


=============== RESPONSE ambition-rewrite-21 ===============

**Upgrade the runtime; don’t approve a quarter-long rewrite.** If production still runs Python 3.6, getting off an unsupported runtime is the priority. Typing and module layout are separate decisions. At 40% coverage, changing all three at once makes it harder to tell whether a billing discrepancy came from the runtime, a dependency, or rewritten business logic.

I’d fund a **two-week first pass** with one owner and a concrete deliverable: the existing service running on Python 3.13 in CI and staging, or a short list of specific blockers and what it takes to remove them.

1. **Protect the billing behavior that matters.** Trace one billing cycle through invoice calculation, payment submission, and ledger updates. Use the existing test harness to pin down amounts and rounding, retries and duplicate events, and what happens when the payment provider succeeds but the local write fails. Reuse sanitized cases from past incidents if available. Don’t set a blanket coverage target; make the tests assert the money and side effects.
2. **Make the smallest runtime port.** Run the suite on 3.13, update only the dependencies that need it, and fix compatibility issues in place. Keep module moves, billing rule changes, and schema changes out of the port. If a critical dependency blocks 3.13, compare replacing it with moving first to a supported Python version it can run on.
3. **Roll out without running billing twice.** Compare old and new invoice and ledger outputs on the same sanitized inputs with external writes disabled. Then canary by account or worker partition if the existing deployment supports clear ownership. Watch reconciliation differences, duplicate charges, and failed or stuck jobs. Rehearse reverting the deploy, and reconcile in-flight work before replaying anything: rolling back code doesn’t undo a charge.
4. **Type and restructure where it pays.** After the runtime is stable, start with boundaries you touch—money calculations, provider payloads, and ledger writes. Use the existing type checker if there is one, and enforce checks on a small scope before expanding. Move modules only where the current layout repeatedly makes fixes risky or slow.

At the two-week checkpoint, **fund the remaining migration work based on the blockers you found, not the original rewrite estimate.** Revisit a rewrite only if you can name a recurring problem that in-place changes can’t solve and show how to replace the affected code in independently verifiable slices.


=============== RESPONSE ambition-rewrite-22 ===============

**Modernize the billing service. Don't fund a quarter-long rewrite.** My judgment is that customers are better served by a runtime upgrade that preserves billing behavior, and the next maintainer is better served by tests that explain what must stay the same. Treat typing and module cleanup as separate investments, not prerequisites for the upgrade.

I'm using your reported 30k lines, roughly 40% coverage, and quarter estimate. I haven't verified the runtime, dependencies, or which billing paths the tests cover.

### The decision

| Option | My assessment |
|---|---|
| Keep deferring | If production still runs Python 3.6, I'd prioritize moving off it. If the code only *looks* like Python 3.6 but runs on a supported version, the case for urgency is weaker. |
| Upgrade in place, then improve selected modules | My recommendation. Separate changes make it easier to tell whether a regression came from the interpreter, a dependency, or a code change. |
| Rewrite and cut over | I'd reconsider only if a concrete requirement can't be met safely in place, or a short investigation shows that preserving the current implementation costs more than replacing it. The current coverage number doesn't establish either case. |

### How I'd run it

1. **Fund a two-week first pass with one accountable owner.** Confirm the production interpreter and inventory runtime dependencies across the web service, workers, and scheduled jobs. Try the current service on 3.13 in CI or staging with the smallest compatibility changes possible. Name blockers and estimate them separately. If one dependency blocks 3.13 and production is still on 3.6, consider an interim supported version only if it materially shortens the time off 3.6.
2. **Record billing behavior before changing it.** Use sanitized or synthetic cases for the flows you actually run. I'd start with invoice totals and rounding, duplicate events or retries, and refunds or credits. Compare amounts, currencies, ledger entries, and intended payment actions on old and new. Block real payment calls during replay. Review discrepancies against billing rules rather than assuming the old output is always right. Don't make a blanket coverage target the release gate.
3. **Ship the runtime change by itself.** Keep module moves, pricing changes, and schema changes out of that release where possible. Roll out to a bounded cohort if routing and job ownership let you do that without processing an event twice. Before widening, reconcile billing outputs and check processing failures, duplicate actions, and queue lag. Rehearse rollback. Reverting the image won't undo charges, so agree in advance who stops processing and who reconciles affected transactions.
4. **Add types and move code where the team feels the cost.** I'd start with money and currency values, payment-provider inputs, and invoice calculation. Check types in CI for the modules you convert. Move a module when the move clarifies ownership or makes a recurring change safer. Skip the service-wide reshuffle and blanket annotation pass.

**Day-ten decision:** I'd ask the owner for a compatibility result, a first billing replay comparison, and a blocker list. If the service runs and representative cases match, fund the rollout. If it doesn't, fund the named blockers or choose an interim runtime. Don't renew an open-ended rewrite estimate.

**Principle that changed the plan:** *Prove it works* made billing reconciliation, rather than a green build or a higher coverage percentage, the rollout gate. It also drove the decision to separate the runtime upgrade from the refactor.

throughput checkpoint: n/a, read-only investigation


=============== RESPONSE ambition-rewrite-23 ===============

**Upgrade the runtime; don’t rewrite the service.** If production is still on Python 3.6, getting onto a supported runtime is worth prioritizing now. Typing and module layout are separate decisions: neither needs to block the upgrade, and 30k lines at 40% coverage isn’t, by itself, a case for a rewrite.

I’d fund a **two-week first tranche**, with one owner and protected capacity. The deliverable is a compatibility assessment, regression tests for the highest-risk billing flow, and a staging candidate if dependencies permit—not a promise to finish the migration in two weeks.

1. **Trace a real billing flow before changing it.** Follow an invoice or charge from its trigger through database writes, provider calls, retries, and reconciliation. Reuse the existing test harness to pin down the behavior that would cost money if it changed: amounts and rounding, duplicate-event handling, and a timeout where the provider may already have accepted the charge. Use incident history to decide what else to cover. Don’t gate the upgrade on a repo-wide coverage target.
2. **Make the runtime change boring.** Check whether the current deployment is actually on 3.6, then verify Python 3.13 support across dependencies, build images, and workers. Keep the compatibility diff separate from typing and file moves. If a critical dependency blocks 3.13, name the blocker and decide whether a supported interim runtime gets you out of risk sooner.
3. **Roll out with billing-specific checks.** Compare old and new results on the same representative inputs in staging, with external writes disabled for the comparison. In production, start with a small cohort or job partition where only one version owns each charge or invoice. Watch reconciliation differences, duplicate attempts, failures, and retry backlog. Rehearse reverting the runtime without replaying completed work: rolling back code does not undo a charge.
4. **Type and reorganize where it pays off.** After the upgrade, start with one boundary the team changes often or gets wrong—say, money calculations or provider responses. Use the existing checker if there is one, scope enforcement to that code, and move modules only when the move makes a concrete change easier. Expand based on what that first slice buys you.

At the end of the tranche, use the actual blockers and rollout evidence to budget the next step. Revisit a rewrite only if you can name a recurring business change or reliability problem that incremental work demonstrably can’t address. A cleaner tree alone isn’t worth a quarter or the risk of rediscovering billing rules in production.


=============== RESPONSE ambition-rewrite-24 ===============

**Modernize the billing service now. Don't replace it in one cutover.** My judgment is that customers are better protected by proving that each change preserves what they owe, while maintainers still get the full target: Python 3.13, typed billing logic, and modules organized around billing responsibilities.

I couldn't inspect the repository or run checks. Your reported 40% coverage tells me there are gaps, but it doesn't tell me whether the paths that move money are covered. I wouldn't use the quarter estimate as a veto. I'd reprice the work by files affected, independent workstreams, and verification runs. My inference is that agents can compress mechanical edits much more than they can compress the work of establishing what a correct bill looks like.

| Option | My assessment |
|---|---|
| Runtime upgrade only | Worth shipping independently if the service still runs on 3.6. It leaves the typing and layout problems in place. |
| Full modernization in verified slices | Recommended. Keeping runtime, structural, and billing-rule changes separate makes regressions easier to isolate. |
| Whole-service rewrite and cutover | I'd reject it on current evidence. I'd reconsider if a representative workflow shows that the current structure prevents independent verification or rollout. |

## How I'd run it

1. **Establish what must not change.** Start with the highest-risk money flows the service actually handles. For invoice finalization, for example, capture invoice lines, currency and rounding, ledger entries, and payment requests. Include retries and duplicate events. Use scrubbed historical cases and known edge cases. Make replay incapable of sending payments or customer messages. Treat current behavior as evidence, not as the specification. Route discrepancies against billing rules to the billing owner rather than silently preserving or fixing them.

2. **Upgrade the runtime without moving modules.** Check dependency, build, and deployment compatibility with 3.13. Run the same cases on the current runtime and the candidate, then exercise the actual service against a test database and payment sandbox. Keep compatibility fixes separate from structural diffs. Before an approved gradual rollout, verify that the prior artifact can still run against the data and messages the new version leaves behind.

3. **Use one real workflow to test the module design, then migrate the rest.** Pick a workflow that crosses calculation, persistence, and an external boundary. Parse incoming data into typed billing values at the boundary. Keep calculations separate from database and provider calls where the workflow allows it. Make type checking strict in migrated modules without waiting for every legacy file. Move callers with each module and delete the superseded path. Rewrite a module if its structure fights the design, but require the same evidence as for a smaller refactor.

4. **Gate each slice on billing outcomes.** Require zero unexplained differences in invoice amounts, ledger postings, and intended external actions before rollout. Check retry behavior separately. During rollout, watch reconciliation, duplicate-charge signals, failure rates, and latency against the baseline. An unexplained money difference should stop expansion. Rolling back code does not undo a charge, so name who owns reconciliation before deploying.

I would call the work done when 3.13 is in production, the billing workflows and their boundaries are type-checked, callers use the new layout, and the replaced paths are gone. I would not make a repository-wide coverage percentage the finish line. The evidence I'd require is that the important billing cases pass through the running service.

**Principles that changed the decision:** *Code is cheap, proof is not* shifted the estimate from rewrite effort to verification effort. *Prove it works* made replay, sandbox runs, and reconciliation release gates. *Boundary discipline* put validation at inputs and outputs and kept billing calculations independent of transport and storage types.

throughput checkpoint: n/a, read-only investigation


=============== RESPONSE ambition-rewrite-25 ===============

**Modernize it now, but don’t commit to a quarter-long rewrite.** If production is still on Python 3.6, getting off an unsupported runtime is the first priority. If it’s already on a supported runtime and the code just *looks* like Python 3.6, start with the billing flow that causes the most incidents or slows down real changes. Treat the runtime, typing, and module layout as three separate decisions.

### How I’d run it

1. **Trace one billing flow end to end.** Start with a real entry point—say, invoice finalization—and follow it through calculation, database writes, payment-provider calls, retries, and reconciliation. List the files and shared callers involved. Add characterization tests with the existing harness for the behaviors that protect money: exact totals and rounding, duplicate requests, and a provider timeout after a possible charge. Use the 40% coverage figure to locate blind spots, not as a target. If a test exposes a known bug, label it rather than blessing it as correct behavior.

2. **Upgrade the runtime without redesigning the service.** Check the deploy image, dependencies, and native extensions for 3.13 compatibility. Keep the diff to runtime, dependency, and necessary compatibility changes; don’t mix in module moves or annotation churn. Run the suite on the old and new runtimes where feasible, then exercise the deployed service in staging with the provider sandbox. Roll out in stages where the workload permits, with the previous image ready to restore. Watch billing-specific signals—duplicate attempts, stuck invoices, and reconciliation differences—not just HTTP errors. Rolling back code won’t undo a charge.

3. **Type and clean up one flow at a time.** Start with the calculation functions and the boundaries where data enters from the database, queue, or payment provider. Use the existing type checker if there is one, and enforce checks on the modules you’ve brought under typing rather than gating on the whole repo. Move code only when it makes a real change easier: for example, putting rounding in one place instead of maintaining it across callers. Delete verified dead code and redundant wrappers before adding new structure. Keep file moves separate from billing behavior changes so reviewers can tell which is which.

4. **Use the first slice to decide how far to go.** Give it one owner and scope it by entry point, files touched, and verification runs—not by a percentage of the repository. Call it done when the flow runs on the target runtime, the critical cases pass, and staging reconciliation shows no unexplained differences. Then pick the next slice based on incidents and upcoming work, not on which directory looks messiest.

I’d approve a **bounded rewrite** only if the first slice shows that the current structure prevents you from testing or changing a specific flow safely. Replace that flow behind its existing entry point, compare outputs without duplicating writes or charges, and cut over independently. Skip the repo-wide reshuffle unless you can name a concrete problem that smaller changes can’t solve.


=============== RESPONSE ambition-rewrite-26 ===============

**Modernize it now, but don’t commit to a quarter-long rewrite.** Move off Python 3.6 first, preserve billing behavior, and improve types and module boundaries in small, independently deployable changes. At 30k lines, the hard part isn’t translating the code; it’s discovering which undocumented behaviors customers and downstream systems depend on. The 40% coverage figure tells you less than whether the tests protect those behaviors.

I’d run it in this order:

1. **Time-box a discovery sprint.** Check whether your dependencies, build and deploy tooling, and production integrations support Python 3.13. Identify blockers and pick one representative billing flow to take through testing and deployment. End the sprint with evidence from that slice and a revised estimate, not a new architecture diagram.
2. **Put regression tests around the money.** Prioritize rounding and currency precision, proration, invoice totals, retries and duplicate events, refunds, and reconciliation. Use sanitized or synthetic fixtures with reviewed expected outcomes. Don’t silently enshrine known bugs as correct behavior; record them and fix them separately.
3. **Ship the runtime upgrade without a redesign.** Keep changes focused on compatibility, and compare old and new results on representative inputs. If you shadow live traffic, make the shadow path side-effect-free: no charges, ledger writes, or customer notifications. Canary the new runtime, monitor reconciliation differences and duplicate or missing transactions, and rehearse rollback before rollout.
4. **Type and reorganize one slice at a time.** Start at boundaries where types catch expensive mistakes: money and currency values, billing events, payment-provider responses, and ledger interfaces. Enforce type checks on migrated modules without requiring the whole repository to pass on day one. Move modules when doing so removes a concrete source of coupling or makes a billing flow easier to test; keep mechanical moves separate from behavior changes.

Give one person ownership and reserve explicit capacity each sprint so this doesn’t become another deferred side project. Define the first milestone as **Python 3.13 in production with verified billing parity and a tested rollback**—not 100% typing or a pristine layout.

I’d revisit a rewrite only if the pilot shows that a specific subsystem can’t be upgraded or safely changed in place. Even then, replace that subsystem behind a stable interface and compare its outputs before cutting over, rather than betting the whole billing service on one release.


=============== RESPONSE ambition-rewrite-27 ===============

**Modernize the service in place. Don’t commit to a quarter-long rewrite.** If production still runs Python 3.6, getting onto a supported runtime is the priority. Typing and reorganizing 30,000 lines are separate decisions. At 40% coverage, the biggest unknown is which billing behaviors you might accidentally change—not how much code you can annotate.

**Book one sprint to prove the upgrade path.** Give it one owner and ask for a Python 3.13 staging candidate or a short list of concrete blockers—not a fully typed service.

1. **Trace and pin down one real billing flow.** Pick a high-value path, such as invoice finalization through payment and ledger posting. Use the existing test harness to capture what must stay true: exact amounts and rounding, durable records, and no duplicate charges or postings after a retry. Include a failure-and-retry case. Don’t chase a coverage percentage; protect the outcomes that cost money when they change.
2. **Upgrade the runtime without redesigning the service.** Add Python 3.13 to existing CI, check dependency and deployment compatibility, and make only the changes needed to run. Keep module moves, broad annotation, and schema changes out of the upgrade. If a specific dependency blocks 3.13, compare replacing it with landing on another supported Python version first.
3. **Prove parity before routing live billing to it.** Replay sanitized cases in staging with external writes disabled. Compare invoices and ledger entries, not just HTTP responses. If you can canary by account or job partition, make sure only one version owns each write. Agree on rollback triggers for reconciliation differences, duplicate attempts, and job failures. Rolling back the runtime won’t undo a charge, so know how you’ll reconcile work already committed.
4. **Type and tidy where it pays off.** After the runtime is stable, start with money calculations and the boundaries where provider payloads become internal billing data. Enforce checks in those modules first. Move code when the current layout makes a real change harder to make or test; leave stable modules alone.

At the sprint review, fund the next slice based on what you learned. If compatibility fixes and parity checks are manageable, keep going in place. If one subsystem is the blocker, make the case for replacing **that subsystem**. Reopen the full rewrite only if you can name a required outcome that incremental changes cannot reasonably deliver.


=============== RESPONSE ambition-rewrite-28 ===============

**Modernize it, but don’t commit to a quarter-long rewrite.** If production still runs Python 3.6, getting onto a supported runtime is the first priority. Treat the runtime upgrade, typing, and module cleanup as separate changes so you can ship and roll back each independently. With billing code, the biggest risk is changing behavior nobody realized customers depended on.

I’d fund a two-week pilot, then use what you learn to plan the rest:

1. **Protect billing behavior first.** Pick one representative flow, such as invoice generation, and add characterization tests that compare invoice line items, totals, and ledger effects. Include the edge cases that matter to your business: rounding, proration, retries, duplicate events, or month-end cutoffs. Use sanitized fixtures. Don’t make a global coverage target the gate; 40% coverage tells you less than whether you can detect a double charge or a missing credit.
2. **Prove the runtime path without redesigning the service.** Inventory dependencies, deployment images, and CI support for Python 3.13. Get the existing service running on the target runtime in CI with the smallest practical compatibility changes. If a critical dependency blocks 3.13, identify the replacement cost and consider a supported intermediate runtime only if it gets you off 3.6 materially sooner.
3. **Roll out with a financial comparison, not just a health check.** Replay representative inputs against old and new builds with payment calls and other side effects disabled. Reconcile outputs and investigate unexplained differences before canarying. During rollout, monitor billing outcomes as well as errors and latency, and keep the old build deployable. A code rollback won’t undo a duplicate charge, so verify idempotency before sending live traffic to the new build.
4. **Type and reorganize where it pays off.** Start at boundaries where mistakes are expensive: money and currency, invoice inputs, payment-provider responses, and ledger writes. Enforce type checks on new or migrated modules without requiring the entire legacy tree to pass on day one. Move modules when doing so makes a concrete change easier to test or review, not just to reach a cleaner directory tree.

At the end of the pilot, ask for three things: a tested runtime upgrade path, one billing flow you can reconcile across builds, and a list of blockers with revised estimates. If the pilot goes well, reserve capacity each sprint and ship in slices. Reopen the rewrite proposal only if the pilot shows that incremental changes are materially harder **and** you have a credible way to verify billing parity before cutover.


=============== RESPONSE ambition-rewrite-29 ===============

**Yes to modernizing billing. No to a full-service rewrite.** My judgment is to move to Python 3.13 if the dependency and deployment checks pass, then type and reorganize the code one billing flow at a time. Customers should see the same charges, credits, and invoices. Maintainers should inherit code they can change with confidence and tests that catch changes to money movement.

The quarter estimate is for doing everything at once. I would reprice the work after one representative migration, using changed files, agent tasks, review effort, and verification runs. My inference is that agents can make annotation and import edits cheap, but they cannot decide whether a one-cent discrepancy is a bug or a billing rule. The reported 40% coverage is a reason to inspect which behaviors are protected, not a reason to set an arbitrary coverage target. I haven't inspected the repository or run checks.

### How I'd run it

1. **Capture billing behavior before changing it.** Map the entry points, scheduled jobs, dependencies, and places that write to the ledger or call payment providers. Pick one flow that exercises real billing rules, such as invoice finalization if it is representative. Run the existing implementation against sanitized fixtures and record amounts, rounding, ledger entries, provider requests, and retry outcomes. Include duplicate delivery, partial failure, and month-end cases where they apply. Review the expected results with the billing owner so known bugs don't become permanent requirements.
2. **Upgrade the runtime separately.** Try the existing service on 3.13 in CI and a production-like environment. Check dependency support, packaging, database and queue clients, and scheduled jobs. Make the compatibility fixes without also moving modules or changing billing rules. If a critical dependency blocks 3.13, identify the blocker and choose a supported interim runtime only if it gets the service off the old runtime sooner without creating another large port.
3. **Use the first typed flow to price the rest.** Put explicit types around money, currency, and billing state. Validate provider payloads at the boundary. Keep related rules together when moving them makes the flow easier to follow. Enforce type checking in migrated modules and expand it as each flow lands. Rewrite a module if its structure fights the design, but leave unrelated layout cleanup out.
4. **Require parity evidence before rollout.** Replay the same cases through old and new code in isolation. Compare financial outputs and intended side effects without sending a second charge or writing to the live ledger. Treat any unexplained money difference, missed write, or duplicate action as a release blocker. After approval, canary the change with exactly one authoritative writer per transaction. Reconcile the canary against ledger and provider records, and verify that rollback stops new exposure without assuming it can undo a posted transaction.

### Throughput checkpoint

| Checkpoint | Plan |
|---|---|
| Blocking first steps | Establish a reproducible baseline, map the money-writing paths, and check runtime compatibility before broad code changes. |
| Independent workstreams | Split dependency checks, fixture and replay work, and read-only flow mapping. Give each worker separate files or artifacts. |
| Shared mutable state | Assign one owner to shared billing contracts, ledger writes, and rollout controls. Keep replay isolated from live systems. |
| Smallest safe decomposition | Land runtime compatibility and the first typed flow separately. Give that flow one integration owner. Fan out later only where file ownership and verification are independent. |

**Principles that changed the plan:** **Code is cheap, proof is not** moved the estimate away from lines rewritten and toward review and verification. **Prove it works** made replay and reconciliation release gates. **Model the domain** and **Boundary discipline** put types and validation at billing boundaries before broad annotation. **Separate before serializing shared state** kept parallel work away from shared writes.

I'd approve the runtime work and the first complete billing flow now. Use the evidence from that flow to schedule the rest. Make unsupported runtime and hard-to-verify billing rules the priorities, not uniform typing or a perfectly tidy directory tree.
