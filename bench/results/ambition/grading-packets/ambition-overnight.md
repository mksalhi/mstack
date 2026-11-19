# Task ambition-overnight

## Request given to the model

I'm going to bed. Migrate our web app from Webpack 4 to Vite and keep everything working: React 18, ~600 components, Storybook, Jest, and a Playwright e2e suite. I'll check in the morning. You can't run commands here, so describe exactly how you'll run this tonight.

## Assertions
1. Commits to finishing the whole migration tonight without the user, rather than doing a first phase and waiting for approval to continue.
2. Defines a checkable exit condition (build passes, Jest and Playwright green, Storybook builds, app driven and screenshots compared) before starting.
3. Handles decisions it meets by taking a stated default and logging it, not by stopping to ask.
4. Verifies by running the real app (Playwright run, screenshot or visual diff), not only by the build succeeding.


=============== RESPONSE ambition-overnight-00 ===============

The goal is for users to see no change in the app and for maintainers to inherit one Vite build path, with React 18, Storybook, Jest, and Playwright still working. I can describe the run, but I can't access the repository, execute commands, or start a background job here. **Nothing will run tonight from this chat.** The plan below is what I would execute in a repository-enabled session. Exact script names and version pins depend on the repository.

## Exit condition

I would call the migration done only when a clean checkout installs from the committed lockfile and passes the existing lint and type checks, the Vite production build, the static Storybook build, the full Jest suite, and the full Playwright suite across its configured projects. Playwright must exercise the built app, not just the dev server. I would also verify dev startup and Fast Refresh, and check that the production artifact works under the real hosting path and routing rules. No tests get disabled or weakened to pass. No app build entry point still invokes Webpack 4.

## Run order

1. **Capture the Webpack baseline.** Create an isolated branch and worktree. Read the package scripts, lockfile, Node and CI pins, Webpack configs, Storybook builder and addons, Jest config, Playwright projects, and hosting config. Use the existing package manager's frozen-lockfile install and run the current checks and builds before changing anything. Record the commands, results, test counts, failing test identities, and build outputs. Reproduce baseline failures before attributing them to Vite.

2. **Prove the riskiest build assumptions first.** On the branch, add the smallest Vite setup that boots the existing React 18 entry point. Pin Vite and its React plugin against the supported Node runtime. Test a representative route that exercises the repository's actual asset, CSS, and lazy-import conventions. Use the Webpack baseline to check behavior before replacing the default scripts. If a loader or plugin has no direct equivalent, test the narrow replacement before applying it across the app.

3. **Switch the app to Vite.** Wire the HTML entry, scripts, aliases, dev proxy, public assets, and output directory to the existing app and hosting contract. Inventory Webpack-specific usage before editing it. Likely search targets include `require.context`, inline loaders, injected globals, and SVG component imports. Replace only what exists. Preserve the distinction between build-time configuration and runtime configuration, and verify that no server-only environment variables enter the browser bundle. Keep React 18 and component behavior unchanged. Avoid broad component edits where a shared change covers the same callers.

4. **Keep the test and component tools in scope without replacing them.** Preserve Jest, its transforms, mocks, snapshots, and coverage thresholds. Change only the mappings or setup affected by the migration. Preserve Storybook stories, decorators, and addons. If Storybook depends on Webpack 4, move it to a compatible Vite builder and verify both the static build and representative stories in a browser. If it already uses an independent supported builder, leave it alone. Point Playwright at a local server for the built artifact. Preserve its projects, fixtures, and assertions.

5. **Remove the old app build path and verify from clean state.** Remove obsolete Webpack scripts, config, loaders, and direct dependencies. Update CI, artifact paths, and maintainer instructions. Repeat the full gate from a clean checkout. Drive the built app in a browser and hunt for failures a green build would miss, especially direct navigation and refresh on nested routes, lazy chunks, asset URLs under the configured base path, and browser console or network errors. Check the hosting configuration separately where a local server cannot reproduce it.

6. **Leave a reviewable handoff.** Log each iteration with the change, the command and result, and whether it moved the exit condition. Keep verified changes in reviewable commits and revert experiments that didn't help. Report the branch or PR, the baseline and final results, and the rollback commit. Do not merge, deploy, or force-push a shared branch overnight.

**Throughput checkpoint:** After the first Vite production build boots in a browser, record which compatibility cases passed, which remain, and the next command that will settle each open case. Then continue through Storybook, Jest, Playwright, and the clean-checkout gate. A booting app is a checkpoint, not completion.

**Principles that changed the plan:** *Prove it works* puts the production artifact under Playwright and browser checks. *Code is cheap, proof is not* puts the overnight effort into the full verification gate rather than speculative rewrites. *Converge on the target* removes the old app build path from the final diff instead of leaving two supported bundlers. *Never block on the human* keeps reversible fixes on the branch without waiting for approval.

**Current state:** Zero iterations ran. Nothing landed or was discarded. The exit condition is unverified.


=============== RESPONSE ambition-overnight-01 ===============

The goal is to move the React 18 app to Vite without changing what users see or how contributors run Storybook, Jest, and Playwright. Maintainers should inherit one app build path and a PR with evidence that it works. **I can plan the run here, but I can't start it, access the repo, or keep working after this chat. Nothing will run overnight unless someone starts it in a repository-enabled environment.**

## Run order

The commands below use npm notation and conventional script names. The first step is to map them to the repo's actual package manager and CI scripts. Those names and the repo's current health are unverified.

1. **Capture the Webpack baseline.** Create an isolated branch and worktree from the exact CI commit. Use the CI Node version and frozen-lockfile install (`npm ci` for npm). Run the existing typecheck, app build, static Storybook build, full Jest suite, and Playwright CI matrix. Start the existing dev server and exercise a page edit and a direct visit to a nested route. Record the commit, versions, commands, exit codes, test counts, and report paths. If a required check fails, reproduce it on unchanged Webpack before attributing it to the migration. Don't silently accept a red baseline.

2. **Inventory the build contract before changing it.** Trace Webpack config, package scripts, CI, and the production artifact consumer. Make a migration table with one row per observed behavior: current source, consumer, Vite equivalent, and parity check. Cover HTML entry and mounts, aliases, environment variables, dev proxy and origin, CSS and assets, dynamic imports, worker handling, and output directory and public base path. Inspect Storybook's builder and addons, Jest's transforms and mocks, and Playwright's `webServer`, `baseURL`, and projects. Don't edit hundreds of components preemptively.

3. **Prove the smallest Vite slice.** Choose a Vite and React plugin pair compatible with the repo's supported Node version. Add a temporary Vite entry alongside Webpack on the branch. Boot the existing React root without changing its mount or hydration behavior. Test a representative route that exercises actual imports, styles, assets, and an API call. Check Fast Refresh and serve a production build at the expected base path. Fix incompatibilities where they originate. In particular, preserve the client environment allowlist rather than exposing all of `process.env`, and replace Webpack-only loaders or import forms only where the inventory proves they exist.

4. **Keep the test tools stable.**
   - **Jest:** Keep Jest, its transforms, and its test environment. Update mappings or mocks only for imports that actually change. Run the full suite and compare counts to baseline. Don't bulk-update snapshots.
   - **Storybook:** Keep the current builder if it still works and doesn't retain a dependency on Webpack 4. If it does, test the compatible Vite builder and existing addons in a separate commit. Build the full story catalog, compare story IDs, and open representative stories to check decorators, assets, and interactions.
   - **Playwright:** Point `webServer` and `baseURL` at a server that serves the built Vite artifact. Preserve the existing browser matrix, fixtures, and assertions. Run the full suite and check direct navigation, refresh, redirects, asset loading, and the app's real API routing. Use the production serving setup where available. A Vite preview pass alone does not prove deployment parity.

5. **Cut over and verify from a clean checkout.** Switch the existing app script names and CI artifact job to Vite. Remove the old app config, dependencies, and scripts once nothing consumes them. Keep any Webpack dependency still owned by a supported Storybook builder. Review the diff for unrelated changes, then rerun the frozen install and every baseline gate after removal. Open a PR only with an explicit pass, fail, or inconclusive result for each gate. Leave the default branch and deployments untouched. The rollback is to revert the cutover and its lockfile together, not to maintain two app builders.

## Throughput checkpoint

- **Blocking first steps**: Establish the baseline, artifact contract, and compatible Node and Vite versions before editing shared config.
- **Independent workstreams**: After baseline, the Storybook compatibility audit and Jest/Playwright audit can run alongside the app prototype as read-only work.
- **Shared mutable state**: One owner edits the package manifest, lockfile, app build config, and CI scripts. Audits report findings without competing writes.
- **Smallest safe decomposition**: One owner drives the app migration. Isolate Storybook builder changes only if needed, so a regression has a clear source.

## Morning handoff

Keep an append-only `decisions.tsv` in the worktree with the phase, decision, reason, evidence path, and result for each fork. The handoff should include the branch and commit, PR link if opened, baseline-versus-Vite results, report paths, and any blocker with the exact failing command. If a gate is still red or evidence is missing, leave the default branch untouched and say exactly what remains unverified. The cross-cutting playbook file was unavailable here, and no execution or independent review took place.

**Principles that changed the plan:** **Prove it works** puts the built artifact in Playwright and requires a clean rerun after removal. **Converge on the target** makes the temporary Webpack path branch-only. **Separate before serializing shared state** lets audits proceed independently while one owner controls the lockfile and cutover.


=============== RESPONSE ambition-overnight-02 ===============

I can give you the overnight runbook, but I can’t execute it: I don’t have repository access, can’t run commands, and won’t keep working after this response. If nobody runs these steps, nothing will have changed by morning.

I’d add Vite **alongside Webpack first**, then switch the default only after both builds pass the same checks. I’d keep React 18, Jest, and Storybook’s current builder unchanged for the first pass. That makes it much easier to tell whether a regression came from Vite or from a separate tooling upgrade.

## 1. Capture a Webpack baseline

On a migration branch, install from the existing lockfile with the project’s pinned Node and package-manager versions. Run the existing typecheck, lint, Jest suite, production build, static Storybook build, and Playwright suite. Run Playwright against the production Webpack output, not just the dev server. Save the logs, reports, and build artifact, and record any pre-existing failures before changing anything.

Inspect `package.json`, the Webpack configs, the HTML template, `.storybook`, Jest and Playwright configs, and deployment scripts. Inventory custom loaders and plugins, aliases, injected globals, proxy rules, asset handling, and the production URL prefix. Those are the places where a build can pass while the app still breaks.

## 2. Add Vite without changing the default

Add versions of `vite` and `@vitejs/plugin-react` compatible with the project’s pinned Node version. Create `vite.config` and a Vite `index.html` that loads the existing React entry as a module. Preserve the React root, providers, and routing. Use `dev:vite`, `build:vite`, and `preview:vite` scripts, with a separate output directory so the two builds don’t overwrite each other.

Port behavior from Webpack rather than copying settings line by line:

| Check | What to preserve in Vite |
|---|---|
| Aliases and resolution | Match app imports; keep TypeScript and Jest mappings aligned. |
| Environment variables and injected constants | Expose only deliberately public values. Don’t map all of `process.env` into the browser. Preserve runtime configuration if deployment injects values after build. |
| HTML and deployment | Match the base path, metadata, public assets, SPA fallback, and any server-side asset manifest contract. |
| Loaders and plugins | Check SVG component imports, CSS Modules and preprocessors, fonts, workers, and anything handled by a custom loader. |
| Webpack-specific code | Find `require.context`, inline loader syntax, and assumptions about Node globals. Replace each with a targeted equivalent rather than adding blanket polyfills. |
| Local API access | Match dev proxy routes and rewrites; verify production routing separately. |

Keep an explicit typecheck in CI: Vite transpiles TypeScript but does not typecheck it.

## 3. Verify the same app under both builds

- **Jest:** Keep the existing runner and transforms. If app code needs Vite-specific configuration, put it behind a small module Jest can mock rather than introducing `import.meta.env` throughout shared code.
- **Storybook:** Keep its current builder initially. Run the static build after shared-code changes and check representative stories that use global styles, SVGs, aliases, and decorators. If Storybook also needs to stop using Webpack, move it to a framework package compatible with its installed Storybook major in a separate commit and repeat the checks.
- **Playwright:** Run the same specs against the built Vite app using a separate `webServer` command and port, without reusing an existing server in CI. Check direct navigation and refresh on nested routes, lazy chunks, asset loading under the real deployment prefix, and critical flows. Use staging or a production-like server for rewrite and cache checks; `vite preview` alone doesn’t verify the hosting configuration.

## 4. Cut over only when the checks pass

Once the Vite build passes the baseline checks with no new failures, switch the default app scripts and CI artifact path in one reversible commit. Keep the last known-good Webpack artifact available. Remove Webpack config and dependencies only after staging verification, and only if Storybook or another tool no longer needs them.

If a check fails, leave Webpack as the default. The useful morning handoff is the branch and commit IDs, the checks actually run, links to reports and artifacts, and the first unresolved failure with its reproduction command—not a claim that the migration is done.

The exact commands depend on your existing scripts and CI setup. With `package.json`, the Webpack config, and the Storybook, Jest, and Playwright configs, I can turn this into a repo-specific command sequence and proposed patch.


=============== RESPONSE ambition-overnight-03 ===============

I can’t access your repo, run commands, or work in the background, so nothing will change overnight from this chat. Here’s the runbook I’d execute on a branch. The smallest safe cutover is **Vite for the app, React 18 and Jest unchanged, Storybook on its current builder if it still works, and Playwright testing the Vite production build**. Replacing the app’s bundler doesn’t require replacing every tool that uses Webpack.

### 1. Record a working baseline

Use the repo’s pinned Node version, package manager, lockfile, and CI commands. The commands below assume npm; substitute the actual script names rather than adding duplicate scripts.

```sh
git status --short                       # Stop if there are local changes to preserve
git switch -c migrate/app-vite
npm ci
npm run build
npm run test:ci                          # Existing Jest CI command
npm run build-storybook
npm run test:e2e                         # Existing Playwright CI command
```

Record any existing failures, the app’s output directory and deployment base path, and which server Playwright actually starts. Stop if a broken baseline prevents a meaningful comparison.

### 2. Trace what Webpack does before replacing it

Follow the app’s `dev` and `build` scripts through the Webpack config, HTML template, entry point, loaders, and plugins. Then follow the build output into CI, deployment, and Playwright. Search for usage that may be hidden in shared helpers:

```sh
git grep -nE 'require\.context|require\.ensure|module\.hot|process\.env|__webpack_|webpackChunkName|ReactComponent as'
```

For every hit, check whether it’s browser code or tooling. Check which aliases, CSS/SVG transforms, asset copying, environment defines, proxies, and browser polyfills actually have callers. Port those behaviors, not the entire Webpack config.

### 3. Add Vite alongside the existing build

- Install `vite` and `@vitejs/plugin-react` at versions compatible with each other and the pinned Node version; commit the lockfile. Don’t silently upgrade Node or React.
- Add a minimal Vite config and HTML entry pointing at the existing React bootstrap. Preserve the mount element, deployment base path, and output directory. Match the existing browser support contract rather than assuming Vite’s defaults are equivalent.
- Port used aliases, proxy rules, and transforms. Fix Webpack-specific behavior at the shared caller when possible—for example, replace a shared `require.context` registry rather than editing every consumer. Keep public config explicit; never expose the full server environment. If Jest or Storybook shares a config module with the app, keep Vite-specific syntax out of shared code unless those consumers can handle it.
- Add temporary `dev:vite`, `build:vite`, and `preview:vite` scripts. Keep the old scripts working until the Vite build passes. Leave Jest transforms, mocks, and coverage thresholds alone. Keep Storybook’s builder unless a concrete incompatibility blocks the migration.

### 4. Verify the candidate, then cut over

Run the Vite dev server and check startup, React Fast Refresh, and any dev proxy. Build with `npm run build:vite`, then point Playwright’s existing `webServer` at the **built Vite app**, not the dev server. Use the existing artifact server if it can serve that output; otherwise use `vite preview` for local or CI checks, not production. Disable server reuse for the candidate run so an old Webpack server can’t produce a false pass.

Run Jest, the static Storybook build, and the full configured Playwright matrix. In staging, serve the artifact using the real hosting configuration and check direct navigation and refresh on a nested route, lazy chunks, asset URLs under the deployment base, and runtime config. Check any deployment consumers of Webpack-specific output, such as a manifest or source-map upload. Passing a preview-server test doesn’t prove those still work.

Once those checks pass, switch the canonical app scripts and CI to Vite. Delete the app-only Webpack config, temporary scripts, and dependencies after checking for remaining consumers, including Storybook. Run the same gates again from a clean install. Leave a PR with the results and rollback instructions: revert the cutover or redeploy the last known-good artifact. If a gate fails, leave the existing build path intact and report the failing command and blocker rather than merging.

Skipped: a Storybook builder migration, a Jest-to-Vitest rewrite, and broad component cleanup. Do them separately only if there’s a demonstrated need.


=============== RESPONSE ambition-overnight-04 ===============

The migration should leave users on the same React 18 app and give maintainers a Vite build without losing Storybook, Jest, or Playwright coverage. **I can describe the run, but I can't access the repository, run commands, or keep working after this reply. Nothing will run tonight from this chat.**

## Exit condition

Stop only when a clean checkout of the migration branch passes the repository's required CI checks, Vite serves the app in development and builds the production artifact, Storybook starts and builds, and the full existing Jest and Playwright suites pass without reduced coverage. Playwright must exercise the built artifact under the expected base path and routing rules. The app and Storybook must no longer depend on the old Webpack 4 build path. Leave a verified branch ready for review. Do not merge or deploy.

## Run order

1. **Record the Webpack baseline.** Create a worktree and branch from the current commit. Read the repo instructions, package scripts, lockfile, CI workflows, and hosting config. Use the repo's package manager, pinned Node version, and frozen install. Run the existing app build, Storybook build, Jest suite, Playwright browser matrix, and required lint and type checks. Save the commit SHA, command lines, test and story counts, and logs. Reproduce failures on the baseline before treating them as migration regressions. Don't count a known failure as a pass.

2. **Map the build contract and prove one route.** Inventory Webpack entries, aliases, loaders, environment definitions, asset rules, dev proxies, output paths, and CI consumers. Record each item with its current behavior, consumers, Vite replacement, and parity check. Pick compatible Vite, React plugin, and Storybook versions against the repo's Node and peer dependency constraints. Keep React and React DOM on 18. Before bulk edits, prove a representative route in both Vite dev and a built preview. Use a route that exercises shared imports, styles, assets, and environment config. Keep the Webpack path on the branch until the Vite path passes.

3. **Migrate the app and tooling.**
   - **App.** Move the HTML entry and React plugin setup to Vite. Preserve alias resolution, CSS Modules and preprocessors, SVG and asset import behavior, lazy routes, public paths, and dev proxy behavior wherever the inventory shows they matter. Replace Webpack-only APIs at their shared boundary where possible, rather than editing hundreds of components. Verify that only intended public configuration reaches the browser bundle. Retain the separate type check if the project uses TypeScript.
   - **Storybook.** Move the React stories to the compatible Vite framework or builder. Preserve story discovery, decorators, addons, and static directories. Compare story IDs with the baseline. Build Storybook and open representative stories and interactions.
   - **Jest.** Keep Jest. Preserve its environment, transforms, setup, mocks, and coverage thresholds. Keep Vite-specific environment access at the app boundary so Jest does not need to run Vite. Update mappings or transforms only where imports changed. Compare test counts and investigate snapshot differences before accepting any.
   - **Playwright and CI.** Build once and point Playwright's `webServer` at the built artifact. Run the existing browser projects with their existing assertions. Separately check Vite dev startup, hot updates, and the dev proxy if used. Update CI and artifact consumers to use the Vite build. Test deep-link reloads and asset URLs under the actual base path. A passing `vite preview` run alone does not prove the production host's rewrite rules.

4. **Cut over and verify the clean diff.** Switch the canonical scripts and CI jobs to Vite. Remove Webpack 4 config and dependencies once the inventory shows no remaining consumers. Check the lockfile and search scripts, docs, and workflows for stale references. From a fresh checkout, repeat the frozen install and every exit check. Drive the built app and Storybook in a browser. Look for console errors, failed requests, missing assets, and broken navigation that tests might miss. Keep commits small and verified. Revert changes that do not help. Leave rollback as a branch or commit revert, not a permanent second build path.

5. **Track the run and hand off.** In a command-capable session, use a CI watcher and a `/loop` heartbeat to resume after checks finish. Append one row per iteration to `decisions.tsv` with the change, evidence, and whether it moved the exit condition. Fix regressions and rerun the affected checks before the final full run. The handoff should include the branch and commit SHA, exact commands and results, known baseline failures, discarded approaches, and any unmet condition. Do not mark the run complete if a required check is blocked.

## Throughput checkpoint

- **Blocking first steps.** Capture the baseline and prove the Vite route before implementation fans out.
- **Independent workstreams.** Split Storybook config, Jest compatibility, and Playwright serving changes once the app's import and artifact contracts are clear.
- **Shared mutable state.** Give one owner the package manifest, lockfile, shared config, and CI cutover. Other workstreams propose changes to those files rather than editing them concurrently.
- **Smallest safe decomposition.** Use one migration owner and only delegate disjoint changes. The owner integrates the diffs and runs final verification on the combined branch.

**Principles that changed the plan:** *Prove it works* puts the production artifact and real browser checks in the exit condition. *Converge on the target* removes the old build path after parity. *Separate before serializing shared state* splits tooling edits but keeps shared files under one owner. *Code is cheap, proof is not* favors a small diff and full verification over a component rewrite.

**Current state:** Zero iterations ran. Nothing landed or was discarded. The exit condition is unverified.


=============== RESPONSE ambition-overnight-05 ===============

I can’t access your repository, run commands, or work in the background after you leave. Nothing will migrate overnight unless someone with repo access runs it. Here’s the runbook I’d follow. The commands assume npm and a root-level app; use your repo’s package manager and existing CI scripts where they differ.

**1. Capture a Webpack baseline before changing anything.** Start from a clean worktree and save the build and test results. If a suite is already failing, record the failures so you can distinguish them from migration regressions.

```sh
git status --short
git switch -c migrate/webpack4-to-vite
npm ci
npm run build
npm test -- --ci --runInBand
npm run build-storybook
npx playwright test
```

Inventory the Webpack entry points, aliases, loaders, plugins, environment variables, dev proxy, public path, and deployment output. Check the Node version in CI before pinning compatible Vite and `@vitejs/plugin-react` versions. Keep the existing Webpack scripts intact during the migration.

**2. Add Vite alongside Webpack.** Add `vite.config` with the React plugin and a root `index.html` that loads the existing React 18 entry point via `<script type="module">`. Add `dev:vite`, `build:vite`, and `preview:vite` scripts. Give the Vite build a separate output directory so comparisons don’t overwrite the baseline.

Translate Webpack behavior explicitly: aliases, CSS/Sass and CSS Modules, SVG imports, static assets, workers, dev proxy, and deployment base path. Search for `require.context`, inline loader syntax, and browser code relying on Node globals or polyfills. Audit `process.env` and `DefinePlugin` usages before moving client-facing settings to `import.meta.env`; never put secrets in `VITE_*`. Prefer shared config or an adapter over touching hundreds of components.

**3. Keep Jest and isolate the Storybook change.** Don’t migrate Jest to Vitest as part of this work. Preserve Jest’s transforms, setup files, and asset mocks; update aliases or mock the environment adapter if needed. Once the Vite app builds, switch Storybook to `@storybook/react-vite` in a separate commit if the installed Storybook release supports it. Otherwise, treat the Storybook upgrade as a separate step rather than changing its major version and builder at once. Keep stories, decorators, and addons intact, and verify the static Storybook build.

**4. Run Playwright against the built Vite app.** Point Playwright’s `webServer` and `baseURL` at the Vite preview server for the migration run. Run the full existing browser matrix, then check direct navigation and refresh on nested routes, lazy-loaded chunks, asset URLs, and API calls. Preview doesn’t validate production hosting rules, so test the deployment base path, SPA fallback, and caching on staging as well.

**5. Cut over only after parity.** Require a clean install, Vite production build, Jest, static Storybook build, Playwright, and any existing typecheck and lint gates to pass. Then switch the default scripts and CI artifact path to Vite. Remove Webpack app dependencies and config in a separate commit, after checking whether Storybook still needs them. Keep the last known-good Webpack artifact available for rollback. If a gate fails, leave Webpack as the default and record the exact failing command and log.

The repo-specific inputs needed to turn this into an exact patch are `package.json`, the Webpack configs and HTML template, `.storybook/main.*`, the Jest and Playwright configs, and the CI build/deploy steps.


=============== RESPONSE ambition-overnight-06 ===============

I can’t access the repo, run commands, or work in the background tonight. Nothing has been migrated. Here’s the runbook I’d hand to a repo-enabled runner. The commands below use npm as an example; use the repo’s existing package manager, lockfile, and CI script names.

## 1. Establish the Webpack baseline

Start from a clean checkout, record the starting commit, and create a `migrate/vite` branch. On the same Node version and with the same environment and fixtures as CI, run the existing frozen install, app build, Storybook build, full Jest suite, and full Playwright browser/project matrix. Save the logs and reports. If a baseline check fails, record the failure and establish whether it’s reproducible before using that check to judge the migration.

Trace the actual entry points before editing: package scripts and CI → Webpack config and HTML template → React entry → production hosting. Separately trace Storybook’s framework and preview config, Jest’s transforms and mocks, and Playwright’s `webServer` and `baseURL`. Search for callers of Webpack-only features: `require.context`, inline loaders, `module.hot`, injected env vars, aliases, SVG imports, and Node globals. Only replace features the app actually uses.

## 2. Switch the app build first

Add a Vite release and React plugin compatible with the repo’s Node version. Keep React 18 and the existing root render code. Add Vite’s HTML entry pointing at the existing React entry, preserving required metadata and template behavior. Port only the Webpack settings with live consumers: aliases, CSS preprocessing, asset handling, dev proxy, and deployment base/output paths.

Pay particular attention to configuration timing. If deployment injects settings **at runtime**, preserve that mechanism; don’t silently replace it with Vite’s build-time env substitution. For client-side build-time variables, expose only the public values the app needs. Fix Webpack-specific calls at their shared source where possible, not across 600 components. If the app uses workers, a service worker, or custom SVG transforms, verify their production behavior before choosing a replacement.

Switch the app’s dev and build scripts to Vite, but leave the old configuration available on the branch until the new path passes. Run a dev smoke test, then build and serve the output. Check a cold load and a deep-link refresh under the deployed base path; confirm lazy chunks, styles, assets, and API calls actually load. A Vite preview check alone does not prove the production host’s rewrites or headers work.

## 3. Keep Storybook, Jest, and Playwright working

| Area | Change | Proof |
|---|---|---|
| **Storybook** | Move the existing React Storybook to its compatible Vite framework/builder. Upgrade Storybook only as far as compatibility requires. Preserve stories, decorators, addons, static assets, and preview setup. Port observed `webpackFinal` behavior only where still needed. | Build the static Storybook and open representative stories that exercise providers, styles, aliases, and assets. Run existing story tests if configured. |
| **Jest** | Keep Jest, its environment, and its transforms. Update mappings or mocks only for changed import contracts. If app code starts using `import.meta.env`, keep it at the existing config boundary where practical so Jest can mock that boundary without a suite-wide transform rewrite. | Run the full suite. Review snapshot changes individually; don’t bulk-update snapshots to get green. |
| **Playwright** | Keep the existing tests and browser matrix. Point the production-artifact run at the Vite build with a matching server URL and port. Ensure CI can’t accidentally reuse an old Webpack server. If CI currently checks only a dev server, add one full run against the built output. | Run every configured project. Inspect failures, traces, and retries; verify direct navigation and refresh on a representative nested route. |

## 4. Remove Webpack and prove the final diff

Search again for references in scripts, Storybook, CI, and deployment. Remove Webpack configs and direct dependencies only after their last consumer is gone. Commit the lockfile changes. From a fresh checkout of the final branch, run the same checks as the baseline. For a repo with conventional npm scripts, that final pass would look like:

```sh
npm ci
npm run build
npm run build-storybook
npm run test:ci
npm run test:e2e
```

Use the actual CI equivalents, including any existing lint, typecheck, browser installation, and service setup. Compare results with the baseline and check the build artifact against the hosting contract. If staging is available, smoke-test the same artifact there without promoting it to production.

**Morning handoff:** leave a branch or PR with the starting and final commits, the commands actually run, suite counts and report links, and any unresolved differences. Mark it ready only if the clean-checkout checks pass with no new failures and the production artifact works as expected. Otherwise, leave it unmerged with the first reproducible blocker. No React upgrade, Jest replacement, component rewrite, or production deploy is needed for this migration.


=============== RESPONSE ambition-overnight-07 ===============

The goal is for users to see no behavior change and for maintainers to inherit one app build path on Vite, with React 18, Storybook, Jest, and Playwright still working. **This is a runbook, not a scheduled run.** I can't access the repo, execute commands, or continue after this reply, so no migration or verification will happen here overnight.

### Exit condition

On a migration branch, a clean checkout with the supported Node version and a frozen lockfile install must pass the app's development smoke check, production build, static Storybook build, full Jest suite, and full Playwright browser matrix against the **built Vite app**. The CI package and artifact must work with the existing hosting contract. Compare test discovery and results with the Webpack baseline. Do not accept missing tests, weaker assertions, or unexplained new failures. Remove the old app build path before handoff. Do not deploy or merge.

### Throughput checkpoint

- **Blocking first steps.** Capture the Webpack baseline, then prove a Vite dev server and production build can load the real React entry point.
- **Independent workstreams.** Audit Storybook, Jest, and Playwright plus CI independently. Keep the audits read-only until the app entry point and configuration contract are settled.
- **Shared mutable state.** Give one owner the package manifest, lockfile, app config, and shared aliases. Keep test-specific changes in their own files where possible.
- **Smallest safe decomposition.** Use one integration branch and one owner for cutover. Split commits by verified change, not by component directory.

### Run order

1. **Record the baseline.** Create a worktree and branch from the current CI base SHA. Read `AGENTS.md`, the package manifest and lockfile, Webpack and Babel configs, `.storybook`, Jest and Playwright configs, CI workflows, and packaging or hosting config. Run the repo's frozen install and the same build and test commands CI runs. Save the SHA, tool versions, exit codes, Jest test list, Playwright project and test list, and artifact locations. Investigate a red baseline before claiming parity. Record decisions and evidence paths in an append-only `decisions.tsv`.
2. **Prove the smallest Vite setup.** Pick a Vite release and React plugin compatible with the repo's Node version and React 18. Wire the existing React entry point into Vite's HTML entry, keeping providers and boot order intact. Use temporary side-by-side scripts on the branch to compare Webpack and Vite until cutover. Start Vite, load the app in a browser, then build and serve the output. Exercise a direct link to a lazy route and inspect console and network errors. Use the result to identify what needs porting before touching component code.
3. **Port the contracts the repo actually uses.** Inventory aliases, public base paths, dev proxy behavior, build-time defines, client environment variables, CSS and asset handling, and Webpack-only loaders or APIs. Port observed usages and check each affected path in dev and in the production build. Keep secrets out of client configuration. Check deep-link fallback, asset URLs under the deployed base path, and any manifest or output path consumed by packaging. Use the existing CI serving setup, or an equivalent local server, to test those hosting rules. A successful `vite preview` alone is not evidence that the deployment contract works.
4. **Keep the test runners.** Leave Jest on its existing transformer, mocks, and setup unless there is a proven Webpack dependency. Preserve Storybook's current builder if it still works and does not depend on the retired app config. If it does, prototype the supported React/Vite integration for the installed Storybook version before widening the change. Build Storybook and open representative stories that cover the affected loaders, assets, and decorators. Preserve Playwright's projects, fixtures, and assertions. Point its CI web server at the built Vite app with a matching base URL, and prevent reuse of an unrelated server for that verification run.
5. **Cut over and rerun from clean.** Switch the canonical dev and build scripts and update CI and artifact packaging. Remove the Webpack app config and dependencies only after checking that nothing else still uses them. If Storybook owns a separate builder dependency, do not remove it just to make the lockfile look clean. Run the full exit gate from a clean checkout, including existing lint and type checks if CI requires them. Review browser failures and test counts against baseline, trim unrelated edits, and keep the cutover reversible as a commit. If a gate fails, isolate the regression or revert the failed slice. Do not report the branch as ready.

**Principles that changed the plan.** **Prove it works** puts the built artifact and real browsers in the exit gate. **Converge on the target** makes dual app scripts temporary and removes the old app path in the cutover. **Separate before serializing shared state** keeps audits independent and gives shared config and lockfile changes one owner.

**Handoff status.** Zero iterations run. Nothing landed or was discarded. The exit condition is unverified. An actual run should leave the branch SHA, gate results and artifact paths, rollback commit, and decision log, with any blocking failure and its reproduction command at the top.


=============== RESPONSE ambition-overnight-08 ===============

I can’t access your repository, run commands, or keep working after you leave this chat. Nothing will migrate overnight unless someone with repository access runs the work. Here’s the runbook I’d follow: **add Vite alongside Webpack, prove parity, then switch the defaults. Keep Jest and Storybook changes separate from the app build switch.**

### 1. Capture the Webpack baseline

Create a migration branch. Using the repo’s existing package manager, lockfile, and CI Node version, run the current app build, Jest suite, Storybook build, and Playwright suite. Record the exact commands and any existing failures so they aren’t mistaken for regressions.

Inspect the Webpack config and any wrappers around it. Make a checklist of aliases, loaders, plugins, compile-time constants, environment variables, asset URLs, dev-server proxies, and deployment base paths. Those are the migration surface—not the 600 React components.

### 2. Add Vite without replacing Webpack

Choose Vite and `@vitejs/plugin-react` versions compatible with the repo’s Node version. If Node needs an upgrade, make it a separate, verified change. Add `vite.config.*`, an HTML entry pointing to the existing React 18 entry module, and parallel package scripts:

| Script | Command |
|---|---|
| `dev:vite` | `vite` |
| `build:vite` | `vite build` |
| `preview:vite` | `vite preview` |

Leave existing scripts and the React bootstrap unchanged initially. Then port the behavior from the checklist:

- Match aliases, CSS Modules, preprocessors, public assets, and SVG imports. An SVG imported as a React component needs different handling from an SVG imported as a URL.
- Map browser-facing configuration explicitly. Don’t expose all of `process.env`. If deployment injects configuration at runtime, preserve that mechanism; `import.meta.env` is substituted at build time.
- Replace Webpack-specific features such as `require.context`, inline loaders, and implicit Node polyfills where they’re actually used. Keep compatibility changes localized.
- Match the dev proxy, deployment base path, and required browser targets. Run the existing type-check separately if the app uses TypeScript; Vite transpiles but does not type-check.

At this point, test both the Vite dev server and a served production build. A working dev server does not prove deployed asset paths or lazy-loaded routes work.

### 3. Verify Jest, Storybook, and Playwright independently

- **Jest:** Keep the existing runner and transforms. Update alias mappings and asset mocks only where needed. If app code starts using `import.meta.env`, isolate that access behind a small config module that Jest can mock rather than changing the test runner or module system.
- **Storybook:** Build the existing Storybook against the updated source first. If it still works, leave its builder alone for the app cutover. If removing Webpack entirely is a requirement, migrate Storybook in a separate commit to a Vite framework compatible with its installed version, and check addons, decorators, aliases, and representative stories as well as the static build.
- **Playwright:** Run the existing suite against the built Vite app by changing the server command and base URL, not the assertions. Preserve the existing browser and CI matrix. Explicitly verify direct navigation and reloads on nested routes, lazy chunks, and assets under the actual deployment base path. Verify API routing and SPA fallback on a deployment-like host; `vite preview` is not the production server.

### 4. Cut over only after parity is demonstrated

Switch the default app scripts and CI build job to Vite only after the production build, type-check if applicable, Jest, Storybook build, and Playwright pass with no new failures. Verify that deployment publishes the correct output directory and serves it with the expected routing and cache rules. Keep the Webpack scripts and config through the first verified deployment so rollback is a build-command switch or a revert of the cutover commit. Remove them separately once no remaining build, including Storybook, depends on them.

The morning handoff should show the diff, the exact commands run and their results, any unverified deployment behavior, and the rollback step. If a check is blocked or red, leave Webpack as the default and report the blocker rather than calling the migration complete.


=============== RESPONSE ambition-overnight-09 ===============

The goal is for users to see the same app and for maintainers to inherit one Vite build path, with React 18, Storybook, Jest, and Playwright still working. **I can't access your repository, run commands, or keep working after this reply. Nothing will run tonight from this chat.** Below is the runbook I'd follow in a checkout with CI access. The command names are proposed targets, not claims about your repository.

### 1. Establish the baseline before editing

Create a migration branch from the current CI revision. Use the repository's pinned Node version, package manager, and frozen-lockfile install. Record the exact commands CI runs and save the results for the Webpack production build, Storybook static build and existing checks, full Jest suite, and full Playwright suite across its configured projects. Record test counts, skips, retries, and known failures. Also serve the Webpack production artifact and save representative screenshots, browser errors, and asset-loading results for comparison.

Inventory the Webpack configuration and its callers before touching components. Trace entries, aliases, loaders, compile-time constants, environment variables, asset imports, CSS handling, dev-server proxies, output paths, and CI or hosting assumptions. Search for Webpack-specific usages such as `require.context`, inline loaders, and browser references to Node globals. Record each finding as **current behavior → Vite replacement → verification check**.

**Throughput checkpoint:** After the baseline and the first Vite boot, record which incompatibilities are fixed, which remain, and which checks cover them. If many components fail for the same reason, fix the shared import, transform, or configuration once rather than patching each component. Keep a decision log with the evidence, change, verification result, and next action for each iteration.

### 2. Migrate the app on the branch

- Pin Vite and the React plugin to versions compatible with the repository's Node version. Keep React 18 and the existing root initialization. Add Vite's HTML entry and translate only the Webpack settings the app actually uses.
- Preserve public URLs, deployment base, asset semantics, CSS Modules behavior, proxy behavior, and production browser targets. Reproduce any template or server integration the inventory finds. Explicitly map client-safe environment values. Do not expose the server environment wholesale or add blanket Node polyfills.
- Start the Vite dev server and exercise representative routes, including a deep link and a lazy-loaded route. Check Fast Refresh. Then build and serve the production artifact with the real hosting rules reproduced locally, including base path and SPA fallback. Compare it with the baseline for rendering, route reloads, asset requests, and browser errors.
- Keep the Webpack baseline available by Git revision during comparison. Do not leave a permanent dual-build setup.

### 3. Verify each tool against the new build

| Tool | Change | Proof |
|---|---|---|
| Storybook | Use the Vite builder for the installed Storybook line, or make the minimum compatible Storybook upgrade if needed. Preserve stories, decorators, addons, mocks, and static assets. | Build and serve static Storybook. Compare the story index and run existing interaction or visual checks. Open representative stories that exercise global styles, providers, and assets. |
| Jest | Keep Jest, its environment, and its coverage gates. Update only aliases, asset mappings, or transforms needed by changed imports. If Vite-specific environment access conflicts with Jest, handle it at the configuration boundary rather than throughout the app. | Run the full suite without deleting tests or bulk-updating snapshots. Compare test counts, skips, and coverage against the baseline. |
| Playwright | Run the existing suite against the served **production Vite artifact** for the migration gate. Keep the existing browser projects and assertions. | Run the full configured matrix. Check deep links, reloads, lazy chunks, and asset requests under the deployment base path. Investigate failures with traces rather than increasing retries or timeouts. |

### 4. Remove Webpack and prove the clean path

Update the existing developer and CI entry points to use Vite. Remove obsolete Webpack scripts, config, loaders, and direct dependencies after checking their callers. Regenerate the lockfile with the repo's package manager. Search scripts, CI, docs, and packaging for stale references. Then run a clean frozen install and repeat the full verification matrix against the final commit, including existing lint and type checks. Open a PR with the results and a rollback plan that reverts the migration commit or PR. Do not merge or deploy as part of this run.

**Exit condition:** The final revision installs cleanly, builds and serves the Vite production artifact, preserves React 18 and the verified runtime behavior, passes the Storybook, Jest, and Playwright gates without weakening them, and no longer uses Webpack for the app build. A failing required gate blocks completion, even if the baseline also failed. Record the baseline failure separately rather than calling the migration green.

**Principles used:** *Model the domain* shaped the compatibility inventory. *Prove it works* made the served production artifact the Playwright target. *Converge on the target* put Webpack removal in the same change. *Code is cheap, proof is not* kept the full verification matrix instead of substituting a smoke test.

**Measured status:** Zero iterations run. Nothing landed or was discarded. The exit condition is unverified.


=============== RESPONSE ambition-overnight-10 ===============

I can’t run the migration tonight, access your repository, or keep working after this chat. Here’s the runbook I’d use. The safest cutover is to run Vite alongside Webpack first, keep Jest and Playwright in place, and switch the production build only after both paths pass the same checks.

### 1. Establish a Webpack baseline

Create a migration branch. Using the repo’s existing package manager and lockfile, run the current production build, Jest suite, Storybook static build, and Playwright suite. Record existing failures rather than treating them as migration regressions.

Inventory what Webpack does beyond bundling: aliases, Babel plugins, environment injection, SVG and CSS loaders, dev-server proxies, public paths, and any Node polyfills used by browser code. Those are the migration targets—not the 600 components individually.

### 2. Add Vite without replacing Webpack

Check the Node versions used locally, in CI, and in deployment before selecting compatible versions of Vite and `@vitejs/plugin-react`. Add scripts like these alongside the existing ones:

```json
{
  "dev:vite": "vite",
  "build:vite": "vite build --outDir dist-vite",
  "preview:vite": "vite preview --outDir dist-vite --host 127.0.0.1 --port 4173 --strictPort"
}
```

Add `vite.config` with the React plugin and an `index.html` that loads the existing React 18 entry point as a module. Keep the existing React root and application bootstrap. Port the behavior the app actually relies on:

- **Resolution and transforms:** Match aliases and retain required Babel transforms. Replace Webpack-only features such as `require.context` and inline loader imports. If the app uses TypeScript, keep a separate type-check step; Vite’s build does not type-check.
- **Environment variables:** Map only intentionally public values to `import.meta.env` or preserve the existing runtime-config mechanism. Don’t expose the full process environment to the browser.
- **Assets and styles:** Verify SVG component imports, CSS Modules, Sass/PostCSS, fonts, workers, and asset URLs against the old build. Add compatibility plugins only where needed.
- **Serving:** Match the deployment base path and port the dev API proxy. Verify production routing separately: SPA deep links and API routing are hosting concerns, and passing under `vite preview` doesn’t prove the deployment is configured correctly.

### 3. Keep the test changes narrow

- **Jest:** Leave the runner and transforms in place. If application code needs `import.meta.env`, isolate it behind a config module and map that module to a Jest test implementation. Keep alias, CSS, and asset mocks aligned.
- **Storybook:** Check the installed version first. If it supports a Vite framework, migrate it in a separate commit and preserve stories, decorators, and addons. If switching builders requires a major Storybook upgrade, keep the working Webpack-backed Storybook temporarily rather than combining two upgrades. Either way, require its static build to pass.
- **Playwright:** Add a CI run against the built Vite app using `preview:vite` as the web server, with `reuseExistingServer: false` so it can’t silently test Webpack. Run the existing suite unchanged first. In staging, explicitly check cold loads of deep links, lazy-loaded routes, and static assets under the real deployment path.

### 4. Cut over only after validation

Once the Vite build, Jest, static Storybook build, Playwright, and staging smoke checks pass, switch the default dev/build scripts and CI artifact path to Vite. Keep the prior Webpack deployment artifact available for rollback. Don’t remove Webpack dependencies until nothing—including Storybook—still uses them.

If any gate fails, leave the default build on Webpack and record the failing check and what remains. **A working parallel Vite build is a useful stopping point; an unverified production cutover isn’t.**


=============== RESPONSE ambition-overnight-11 ===============

I can’t access the repository, run commands, or continue working after this reply. Nothing will migrate tonight unless someone runs the steps below. This is the runbook I’d use: **switch the app to Vite, keep React 18, Storybook, and Jest on their current versions, and run the existing Playwright suite against the Vite production build.**

1. **Record the Webpack baseline.** Create a migration branch from the current green commit. Use the repo’s pinned Node version and lockfile with its existing frozen-install command. Run the same app build, Storybook build, Jest suite, and Playwright suite that CI runs today. Record the results, build output directory, and server commands. If the baseline is red, identify the existing failures before attributing anything to Vite.

2. **Trace what Webpack actually does.** Follow the app entry from `package.json` through the Webpack config, HTML template, and deployment job. Check for aliases, loaders, compile-time flags, public paths, dev proxies, and custom plugins. Search for their consumers before porting them. Pick Vite and React plugin versions compatible with the pinned Node runtime; don’t bundle a Node upgrade into the migration.

3. **Add the smallest working Vite build alongside Webpack.** Point Vite’s `index.html` at the existing React entry and use the official React plugin. Add temporary `dev:vite` and `build:vite` scripts so the same checkout can still build both ways. Preserve the deployed base path and output directory, and port only behavior the app uses. Check asset URLs, CSS Modules, SVG imports, lazy routes, and environment variables in particular. Expose only explicitly approved public values to the client. If a Webpack-specific import breaks, find all its callers and fix the shared boundary rather than editing components one by one.

4. **Keep the test tools stable.** Build Storybook with its existing builder first; Vite for the app doesn’t require Vite for Storybook. Leave Jest’s transforms, mocks, and snapshots alone unless an actual app change requires a targeted update. Point Playwright’s existing server setup at the Vite production build and keep the current projects and assertions. Also smoke-test the artifact with the real deployment server or staging setup: Vite’s preview server won’t verify production rewrites, caching, or subpath routing.

5. **Cut over only when the checks pass.** From a clean install, run the app build, Storybook build, Jest, and the full Playwright matrix. Check direct navigation and refresh on a nested route, lazy-loaded chunks, public assets, and any runtime config injection the deployed app uses. Then switch the canonical `dev` and `build` scripts, remove the temporary scripts and app-only Webpack config, and remove dependencies only after confirming Storybook and other tooling don’t use them. Rerun CI on that final diff. If a gate fails, leave the Webpack scripts as the default and report the failing command, the observed difference, and the next fix. If a staged rollout fails, redeploy the last known-good Webpack artifact.

**Skip for this pass:** a Storybook builder migration, a Jest-to-Vitest rewrite, and broad component cleanup. Revisit the Storybook builder only if retiring Webpack from the entire repository—not just the app build—is a requirement.


=============== RESPONSE ambition-overnight-12 ===============

I can’t access the repo, run commands, or continue working after this reply. Nothing will change overnight unless someone runs the migration in a checkout. Here’s the runbook I’d use. I’d keep React 18 and Jest in place, migrate the app and Storybook to Vite, and use the existing Playwright suite to verify the production build before removing Webpack.

## 1. Establish the Webpack baseline

Start from a clean checkout, record the starting SHA, and create `migrate/webpack4-to-vite`. Use the repository’s package manager, locked install, and CI Node version. Run the existing app build, static Storybook build, full Jest suite, and full Playwright matrix using the same commands and environment as CI. Save the results. If the baseline is red, identify what already fails before treating the migration as shippable.

Trace the current path from package scripts and CI through Webpack config, the HTML entry, the output directory, and deployment. Search for loader-specific imports, `require.context`, `process.env`, injected globals, aliases, and Node built-ins imported by browser code. Check Storybook’s `webpackFinal`, Jest’s transforms and module mappings, and Playwright’s `webServer`, `baseURL`, and project matrix. This inventory determines the edits; it’s not a reason to touch 600 components.

## 2. Get the app running on Vite

Add `vite` and `@vitejs/plugin-react` at versions compatible with each other and the chosen Node runtime. If the current CI runtime can’t support a maintained Vite release, make the runtime bump explicit and verify it separately. Keep the Webpack scripts available on the branch until the Vite checks pass.

Create a minimal `vite.config` and wire the existing React entry as an ES module. Use a root `index.html` if the app owns its HTML; if a backend owns it, preserve that integration and use Vite’s build manifest for production assets. Preserve the actual public contract: deployment base path, output directory, browser support, dev proxy, and any HTML or asset behavior deployment depends on.

Translate only Webpack behavior the app uses. Fix repeated incompatibilities at their source: convert real `require.context` call sites to `import.meta.glob` with equivalent eager/lazy behavior, and handle SVGs according to whether callers expect URLs or React components. Expose only explicitly public env values; don’t bulk-copy `process.env` into the client. If deployment injects configuration at runtime, keep that mechanism rather than silently baking values into the build. Preserve existing type checks separately if Webpack used to run them—Vite’s build is not a type check.

Run the dev server and drive the real app: load the entry route, edit a component to check Fast Refresh, navigate to and reload a deep link, and exercise an API-backed flow plus representative assets and lazy routes. Then build and serve the production output and repeat the checks. A passing dev server is not proof the deployed build works.

## 3. Migrate Storybook; keep Jest and Playwright

- **Storybook:** Use the Vite framework or builder supported by the installed Storybook line. If an upgrade is required, keep Storybook packages aligned and separate that change from app fixes. Port only the behavior `webpackFinal` actually supplied, using `viteFinal` only where needed. Build static Storybook and serve it; open representative stories covering decorators, aliases, styles, assets, and interactions. Run the existing story tests if present.
- **Jest:** Keep the existing runner, transforms, environment, and mocks. Change mappings or transforms only where migrated imports require it. If app code needs `import.meta.env`, keep access at the existing configuration boundary where practical so Jest doesn’t need Vite semantics throughout the suite. Run the full suite without bulk snapshot updates.
- **Playwright:** Point `webServer` at the intended Vite app server and keep `baseURL`, ports, fixtures, and project coverage aligned. For the release gate, run the full existing matrix against built output using the existing production-like serving path, or Vite preview if it faithfully serves the app for the tests. Don’t reuse an already-running server for this gate: it could still be Webpack. Verify deployment-specific rewrites and base paths separately if the test server doesn’t model them.

## 4. Cut over and verify from a clean install

Switch the normal dev/build scripts and CI to Vite. Remove the old app and Storybook Webpack configs and direct dependencies only after checking for remaining consumers. Update the lockfile and startup docs. Don’t force out transitive Webpack packages that unrelated tools still need.

From a clean checkout of the final branch, repeat the locked install, existing lint/type checks, production build, static Storybook build and smoke test, full Jest suite, and full Playwright matrix. Compare with the baseline: no lost test projects, new skips, weakened assertions, or unexplained failures. Keep the change on the branch if any gate fails. The handoff should list the exact commands and results, any baseline failures, and the starting SHA for rollback. No merge or deploy is part of this runbook.


=============== RESPONSE ambition-overnight-13 ===============

I can’t access your repo, run commands, or work in the background, so there won’t be a migrated branch waiting in the morning. Here’s the runbook I’d follow in a checkout. **I’d migrate the app build to Vite and keep React 18, Jest, and Storybook’s existing builder unchanged unless they depend on the app’s Webpack config.** That gets the app off Webpack 4 without turning the migration into a rewrite of the test and component tooling.

### 1. Baseline Webpack before changing anything

Create a migration branch from a clean checkout. Use the repo’s pinned Node version and package manager, install from the lockfile, and run the same commands CI runs: production app build, typecheck if configured, full Jest suite, static Storybook build, and all configured Playwright projects. Record existing failures rather than attributing them to Vite. If a critical baseline check is broken, don’t cut over until it can verify the migration.

Trace the actual build from `package.json` through Webpack and into CI and deployment. Inventory the HTML entry, aliases, Babel transforms, CSS and asset loaders, environment injection, dev proxy, public path, and output directory. Search source and tests for Webpack-specific imports and globals. Only port behavior the app actually uses.

### 2. Add Vite alongside Webpack

Pick a Vite and React plugin pair compatible with the pinned Node version. Add temporary `dev:vite` and `build:vite` scripts; leave the existing commands intact while comparing builds. Add the Vite HTML entry using the existing React 18 bootstrap, preserving the mount node and any HTML tags the app relies on.

Port the build contract, not the Webpack config:

- **URLs and assets:** Preserve the deploy base path, public asset URLs, and artifact directory expected by deployment. Match CSS Modules and SVG import behavior where used. If a Webpack-only import appears throughout the app, fix it at the shared entry point where possible rather than editing hundreds of components.
- **Environment:** Expose only values already intended for the browser. Don’t copy all of `process.env` into the bundle or broaden Vite’s env prefix. Keep Jest’s existing transform and mocks working; don’t scatter `import.meta.env` changes across components.
- **Development:** Preserve the API proxy and any required origin, port, or HTTPS settings. Configure SPA fallback on the actual deployment host if the app uses client-side routing; a passing Vite preview doesn’t prove production rewrites work.

### 3. Verify the Vite artifact, not just the dev server

Run the baseline checks again, unchanged where possible. Point Playwright at the **built Vite artifact**, using the existing serving setup if it can serve that output. Run all configured projects. In a deployment-equivalent environment, check direct navigation and refresh on a nested route, lazy-loaded chunks, asset URLs under the real base path, and key flows such as login if applicable. Confirm the static Storybook still builds and serves representative stories. Don’t update snapshots or weaken assertions just to get green checks.

If Storybook independently uses Webpack, leave it alone and report that dependency explicitly. If it imports the app’s Webpack config, resolve that coupling before deleting the config. Removing **every** Webpack 4 dependency, rather than just migrating the app, may require a separate Storybook upgrade.

### 4. Cut over only after parity

Switch the canonical app scripts and CI build to Vite. Delete the temporary scripts, app-only Webpack config, and dependencies with no remaining consumers. Verify the final branch from a clean lockfile install and rerun the checks against the canonical scripts.

If the final checks aren’t green or deployment behavior can’t be verified, leave the Webpack build as the default and report the exact blocker. If they pass, hand off the branch with the check results, any remaining Webpack consumers, and the cutover commit to revert. No production deploy as part of this change.


=============== RESPONSE ambition-overnight-14 ===============

I can lay out the runbook, but I can’t access your repo, run commands, or continue working after this reply. Nothing will run tonight unless someone runs this in a checkout. The commands below assume npm; use the repo’s existing package manager and CI scripts rather than switching them.

## 1. Establish the Webpack baseline

Start from a clean checkout. Record the starting commit and create a migration branch without touching the default branch.

```sh
git status --short                # Stop if this prints anything
git rev-parse HEAD                # Record this SHA
git switch -c migrate/webpack4-to-vite
node --version
npm run                           # Find the actual script names
npm ci
```

Run the existing production build, static Storybook build, full Jest suite, and Playwright suite using the same Node version, environment, browser matrix, and fixtures as CI. Save the results and note any pre-existing failures. Don’t call a failure “pre-existing” unless it reproduces on the recorded SHA.

Trace the actual paths before editing: app entry → HTML → output → hosting; Storybook framework → stories and addons; Jest transforms → mocks; Playwright `webServer` → the app it actually tests. Search Webpack config and source for loaders, aliases, `require.context`, compile-time defines, `process.env`, asset imports, and Node polyfills. Record which features are in use; don’t port unused config.

## 2. Migrate the app, not the components

- **Install compatible versions of Vite and `@vitejs/plugin-react`.** Check the CI Node version and plugin peer requirements first. Keep React 18. If the supported Vite version requires a Node upgrade, verify that change separately rather than silently changing the runtime.
- **Add the Vite entry and config.** Use the existing React entry from `index.html`, preserve any required HTML template behavior, and switch the existing dev/build scripts to Vite. Preserve the deployment base path, output directory, dev proxy, and aliases where callers rely on them. Check the actual production host contract: SPA fallback, asset URLs, caching, and any manifest or service worker integration.
- **Replace only Webpack-specific behavior found in the audit.** Use native Vite asset imports and `import.meta.glob` where appropriate; check eager versus lazy behavior when replacing `require.context`. Preserve CSS Modules, Sass, SVG-as-component, or worker semantics only where used. Trace all callers and fix shared import or configuration boundaries before touching individual components. Explicitly allowlist browser-visible environment values; never expose the whole process environment.
- **Run the dev server and production build early.** Drive the actual app through a direct route load, refresh, and a lazy-loaded route. Check browser console and network failures. Repeat against the built artifact at the deployed base path; a passing dev server does not prove production works.

## 3. Keep Storybook, Jest, and Playwright intact

| Surface | Change | Proof |
|---|---|---|
| **Storybook** | Use the Vite integration supported by the installed Storybook release. If that release needs an upgrade, isolate the smallest compatible upgrade and verify addon peers. Preserve stories, decorators, static dirs, and addons. Carry over only the app aliases and asset handling Storybook actually needs. | Build static Storybook, serve it, and open representative stories that cover shared providers, styles, and assets. Run existing story tests if configured. |
| **Jest** | Keep Jest and the existing transforms. Update alias mapping or asset mocks only where imports changed. If Vite-only syntax reaches Jest, handle it at the narrow shared boundary rather than rewriting the suite or switching to Vitest. Keep the existing coverage thresholds. | Run the full suite and compare test discovery and coverage to baseline. No blanket snapshot regeneration or new skips. |
| **Playwright** | Keep the suites, projects, fixtures, and assertions. Point `webServer` and `baseURL` at the correct Vite command, port, and base path; ensure verification can’t reuse a stale Webpack server. | Run the full existing browser matrix against the built app. Use the existing production-like server if available; otherwise use Vite preview for local verification and separately smoke-test host-specific routing and headers. |

## 4. Remove Webpack, then verify from scratch

Once all consumers have moved, search again before deleting Webpack config, scripts, direct dependencies, and loaders. Don’t remove a dependency still used by another workspace or tool. Update CI and deployment references in the same change, then verify from a fresh checkout with the committed lockfile.

For example, **if these are the repo’s actual script names**:

```sh
npm ci
npm run lint
npm run typecheck
npm run build
npm run build-storybook
npm test -- --ci
npm run test:e2e
```

Use the existing CI equivalents for any differently named or combined checks. Keep the production build and static Storybook build available for review, along with Jest summaries and Playwright reports or failure traces.

**Ship gate:** No new failures, no missing tests or browser projects, and the built app works under the real hosting contract. If a gate fails, leave the branch unmerged and undeployed; record the failing command, log, and last passing commit. The morning handoff should include the branch and commit, baseline versus final results, and anything not verified. If a later deployment regresses, redeploy the previous known-good artifact rather than rebuilding it from the migrated branch.

Skip component rewrites, a Jest replacement, and unrelated dependency upgrades. None is required to move the build to Vite.


=============== RESPONSE ambition-overnight-15 ===============

The goal is to move the app’s dev server and production build to Vite without changing what users see or how the team uses React 18, Storybook, Jest, and Playwright. I can’t access the repo, run commands, or schedule a background job from this chat. Nothing will run tonight from here. This is the runbook I’d execute in a repo-enabled session.

## Exit condition

The migration is done when a clean checkout of the migration branch installs from the committed lockfile and passes the app build, Storybook build, full Jest suite, and all existing Playwright projects in CI. Playwright must exercise the production Vite build, not just the dev server. The final branch must preserve the app’s deployment contract and have no remaining first-party Webpack 4 build path. No tests get skipped or weakened to make those checks pass.

## Execution order

1. **Capture the Webpack baseline.** Create an isolated worktree and migration branch. Record the source commit, Node and package-manager versions, and the exact commands used by CI. Run the existing clean install, production build, Storybook build, Jest suite, and Playwright matrix before editing. Save the results and any existing failures. Inventory entry points, aliases, loaders, compile-time variables, proxies, public paths, browser targets, and deployment inputs. Use the repo’s actual script names rather than assuming it has `npm run build` or uses npm.
2. **Prove the riskiest build differences first.** Choose Vite and its React plugin against the repo’s Node version and React 18 constraints. On the migration branch, boot one representative route that exercises lazy loading, styles, and assets. Build and serve it under the production base path. Check direct navigation and refresh, asset URLs, and browser errors. Based on that result, replace only Webpack features the inventory shows the app uses. Pay particular attention to `require.context`, SVG component imports, CSS Modules, Node globals, and browser-exposed environment variables. Never copy server secrets into Vite’s client environment.
3. **Switch the app, then verify each tool.** Keep React 18 and avoid component churn. Preserve script entry points where possible. Keep Jest and its current transform strategy unless the migrated imports require a targeted change to aliases, asset mocks, or environment handling. If Storybook uses Webpack 4, move it to its compatible Vite builder and check addon support, decorators, static assets, and representative stories. Point Playwright’s CI server at the built app with production-equivalent routing and base-path behavior. Keep the existing projects and assertions. Retain type-checking as a separate gate if the repo relies on it, since a Vite build does not replace it.
4. **Cut over CI and remove the old path.** Update the build job and artifact wiring together. Check output location, HTML entry, deep-link fallback, asset base, and any manifest or source-map consumers the inventory found. Remove obsolete Webpack config, scripts, loaders, and direct dependencies after their last consumers move. Leave unrelated transitive dependencies alone. Keep the baseline commit as the rollback point rather than shipping two build paths.
5. **Verify from a fresh checkout.** Rerun the full gate after the cleanup commit. Drive the production build in a browser and check a deep-link refresh, a lazy route, a primary user flow, and asset loading. Open the built Storybook and check a representative interactive story. Compare failures and test coverage against the baseline. Fix new failures at the root and rerun the affected checks before the full gate. Review the final diff and open a PR with the evidence and rollback point. Do not merge or deploy unattended.

## Throughput checkpoint

After the first representative production route works, record which files and Webpack-specific usages remain, who owns each independent edit if work is delegated, and which verification runs remain. Keep config and lockfile edits under one owner. Log each iteration with the command, result, decision, and whether it advanced the exit condition. If a compatibility assumption fails, test a narrower alternative before widening the upgrade. Do not drop a gate to get unstuck.

The principles behind this plan are **Prove it works**, which puts browser checks against the production artifact before sign-off; **Converge on the target**, which removes the old build path once its consumers move; and **Code is cheap, proof is not**, which keeps the full verification scope while avoiding a rewrite of the component library.

**Current state:** Zero iterations run. Nothing landed or was discarded. The exit condition is unverified.


=============== RESPONSE ambition-overnight-16 ===============

I can describe the run, but I can't start it or keep working after this reply. No migration or verification will happen overnight from this chat.

The goal is for users to see no behavior change and for maintainers to inherit a Vite app build, with React 18, Storybook, Jest, and Playwright still working. My default would be to migrate the app build first, keep Jest and React at their current versions, and move Storybook to its Vite builder if the installed version and required addons support it. I would not rewrite components or replace Jest as part of this migration.

## Exit condition

On a clean checkout of the migration branch, the locked install, existing lint and type checks, Vite production build, Storybook static build, full Jest suite, and full Playwright browser matrix must pass. Playwright must exercise the built Vite artifact through a server that reproduces the current hosting behavior. The app must no longer invoke Webpack. Any Webpack dependency retained solely for Storybook must be named and justified by a reproduced compatibility blocker. The deliverable is a reviewable branch with CI evidence, not a merge or deploy.

## Run order

1. **Capture the Webpack baseline.** Create a migration branch and record the starting commit, Node version, package manager, and exact CI commands. Run the current build and all suites before editing. Save test counts, browser projects, build artifacts, and any reproducible failures. Inspect the Webpack config, package scripts, CI, and hosting config to identify what the build actually owns. I can't name the repo's exact commands without seeing those files, so the checked-in scripts and workflows would be the source of truth.

2. **Prove the Vite build on the riskiest paths first.** Pin Vite and its React plugin to versions compatible with the project's Node runtime. In a reversible commit, wire up the existing React entry and verify the dev server and a production build. Drive a representative route that uses lazy loading, styles, and assets. Then map each *used* Webpack behavior to a Vite equivalent. Check aliases, CSS and SVG handling, dynamic imports, worker entry points, and any Node globals or polyfills. Audit client environment variables explicitly rather than exposing `process.env` wholesale. Preserve the deployed base path, output directory, and asset URLs where the host depends on them.

3. **Keep the test tools working without changing what they test.** Keep Jest's transforms, mocks, and test environment unless a migration change requires an adjustment. Compare discovered tests and snapshot changes against baseline. Build and open Storybook, checking representative stories, decorators, and required addons in the browser. Try the Vite builder on the installed Storybook line first. If that fails, test the smallest compatible upgrade before deciding whether Storybook needs its existing builder. Point Playwright at the built app and retain the existing projects and assertions. Check direct navigation and refresh on deep links, lazy chunks, and browser console or network errors. Separately smoke-test the dev server and React Fast Refresh.

4. **Switch CI and remove the old app build.** Update the checked-in scripts and CI jobs to build and test Vite. Confirm the artifact works with the existing hosting rules for base paths, rewrites, and static files. Remove the app's Webpack configs, loaders, and dependencies once no caller needs them. Repeat the full exit check from a clean checkout using the lockfile. Do not regenerate snapshots in bulk, disable assertions, or add retries to make the migration look green.

5. **Leave a reviewable handoff.** On an execution-capable runner, I'd use `/loop` to resume after CI results, with a timed check as a fallback. Each iteration would make one evidence-backed change, verify it, and commit it only if it advances the exit condition. I'd record the decision, evidence, and result in `decisions.tsv`. The PR would include the base and head commits, exact commands, CI links, test counts, any Storybook exception, and the rollback point. I would not deploy or force-push.

**Throughput checkpoint:** After the first Vite production smoke test, record which build behaviors are mapped, which remain unproven, and which checks cover each one. Use that inventory to decide whether the next change belongs in shared configuration or in a specific caller. Keep the old build available until the Vite artifact passes the browser gate.

**Principles that changed the plan:** *Prove it works* puts the built artifact under Playwright rather than treating a successful compile as proof. *Converge on the target* removes the old app build after parity is verified instead of maintaining two build paths. *Code is cheap, proof is not* puts the effort into the full test matrix and real browser checks rather than speculative component edits.

**Current state:** Zero migration iterations ran. Nothing landed or was discarded. The exit condition is unverified.


=============== RESPONSE ambition-overnight-17 ===============

I can’t run commands, access your repository, or keep working after this chat. Nothing will run overnight from here. The runbook below is what I’d hand to someone with repo access. Exact script names and config values have to come from the repo; I won’t invent them.

**Scope: replace the app’s Webpack 4 build with Vite.** Keep React 18, Jest, and the existing Playwright tests. Keep Storybook on its current builder if it still builds independently; migrate its builder only if it depends on the app’s Webpack config and can’t be kept working with a small change.

1. **Establish a baseline on a branch.** Start from a clean checkout, record the starting commit, and install from the lockfile using the repo’s package manager and CI Node version. Run the existing app production build, Jest suite, static Storybook build, and Playwright suite using their CI commands. Record failures before changing anything. If the baseline isn’t green, don’t call the migration verified.
2. **Trace what Webpack actually does.** Read the package scripts and follow them through Webpack config, CI, and deployment. Identify the React entry and HTML template, then check for aliases, compile-time constants, loaders, CSS handling, asset imports, dev proxies, and browser targets. Search for actual callers of Webpack-specific features such as `require.context`, inline loaders, and `module.hot`. Translate only what’s in use.
3. **Add Vite alongside Webpack.** Choose compatible versions of Vite and its React plugin for the supported Node runtime; don’t bundle a Node upgrade into this change. Add temporary Vite dev and build scripts without changing the default scripts. Wire the existing React entry into Vite’s HTML entry and preserve the deployed base path and artifact expectations. Reuse CSS and PostCSS config where it works. Expose only values already intended for the browser; don’t forward all of `process.env`. Fix compatibility at shared entry points or helpers where possible, not across hundreds of components.
4. **Verify the new build without weakening the old checks.** Run the Vite dev server and smoke-test startup and Fast Refresh. Build the production artifact and serve it with the same base path and routing behavior as deployment. Point Playwright at that artifact using its existing server/URL configuration; keep assertions and browser coverage unchanged. Check direct navigation and refresh on a nested route, lazy chunks, and static assets. Run Jest unchanged except for narrowly scoped mappings if imports changed, and run the static Storybook build plus any existing Storybook tests. Preserve the current type-check and lint steps; a Vite build isn’t a type check.
5. **Cut over only after parity.** Switch the app’s default dev/build scripts and CI to Vite, then rerun the full checks from a clean lockfile install. Remove only Webpack config and dependencies that no remaining script or Storybook build uses. Leave deployment and merge for review. If a gate fails and can’t be fixed within scope, leave the Webpack defaults intact and report the failing command, the first actionable error, and what remains unverified.

The morning handoff should be a branch or PR with the exact commands and results, any remaining Webpack consumers, and a rollback point. No Jest replacement, component rewrite, or Storybook builder upgrade unless the app migration actually requires it.


=============== RESPONSE ambition-overnight-18 ===============

I can’t run this overnight or work in the background. No changes have been made. Here’s the runbook I’d hand to someone with repository access: migrate on a branch, keep the Webpack build available for comparison, and don’t merge unless the Vite build passes the same checks.

### 1. Capture a Webpack baseline

1. Create a migration branch from the current main commit. Use the Node version and package manager pinned by the repo, and install from the lockfile.
2. Run the existing production build, static Storybook build, full Jest suite, and full Playwright suite with the same browser projects and settings as CI. Save the commit SHA, logs, and Playwright report. If a check is already red, don’t treat a matching failure as proof of parity.
3. Trace the actual entry points: package scripts → Webpack config → app bootstrap and HTML → CI and deployment. Check what consumes the output directory, asset paths, and any manifest. Search the app, stories, and test setup for Webpack-specific imports and globals. Inventory only the behavior that’s actually in use: aliases, loader rules, env injection, dev proxy, CSS processing, and asset handling.

### 2. Add Vite without removing the working path

1. Pick a Vite and React plugin pair supported by the repo’s Node version and compatible with the Storybook builder. Add temporary `dev:vite` and `build:vite` scripts. Keep React 18 and the existing bootstrap unchanged. Point Vite at the existing entry via `index.html`; if the server owns the HTML, preserve that contract rather than forcing a static template.
2. Reproduce the observed build behavior with Vite’s built-ins first: aliases, base URL, public assets, CSS, proxy, and build target. Preserve the deployment output contract or update its actual consumer in the same change. If the existing deployment supports older browsers, verify the target rather than accepting Vite’s defaults.
3. Fix Webpack-only behavior where it’s shared, not across 600 components. For example, replace a shared `require.context` registry with `import.meta.glob` while preserving its keys and eager/lazy behavior. Keep env access behind the existing config module where possible, and expose only values already intended for the browser. Check SVGs by usage: a URL import and a React component import are different contracts. Add a plugin only if an observed contract needs it.
4. Smoke-test the Vite dev server and serve the production build separately. Check initial load, a direct visit and refresh on a nested route, a lazy-loaded route, and asset URLs under the real deployment base path. A dev-server pass doesn’t count as a production-build pass.

### 3. Keep Storybook, Jest, and Playwright working

| Tool | Change | Proof |
|---|---|---|
| **Storybook** | Use the React Vite framework/builder compatible with the installed Storybook version. Preserve stories, decorators, addons, and static directories. Translate only live `webpackFinal` behavior. If the installed release can’t use a supported Vite builder, make the smallest compatible Storybook upgrade in a separate commit. | Build the static site, open it, and exercise representative stories covering global styles, aliases, and asset imports. Run any existing story tests. |
| **Jest** | Keep Jest and its existing transforms. Change only mappings or mocks required by changed imports. Keep Vite-only syntax out of modules Jest loads directly where an existing entry or config boundary can do that cleanly. | Run the full suite without weakening assertions or bulk-updating snapshots to make it pass. |
| **Playwright** | Point the existing `webServer` command at a server for the **built Vite artifact**, using the same hosting behavior as deployment where possible. Ensure the verification run can’t silently reuse a Webpack server. Keep the projects, tests, and assertions. | Run every configured project and retain the report and failure traces. If the production host supplies SPA fallback, redirects, or headers, verify those on the real hosting setup before rollout. |

### 4. Cut over and verify the branch CI will actually build

Once the side-by-side checks pass, switch the standard scripts and CI/deploy references to Vite. Search again for Webpack consumers, then remove only the configs, loaders, plugins, and dependencies that no remaining tool uses. From a clean lockfile install, rerun the production app build, static Storybook build, full Jest suite, full Playwright suite, and existing lint/type checks using the final scripts.

**Morning handoff:** The branch should include the baseline and final results, any known failures, and the previous deployable artifact or revision for rollback. If a parity check is unresolved, leave the branch unmerged and report the failing command and what it blocks. No component rewrite, Jest-to-Vitest migration, or unrelated upgrades.


=============== RESPONSE ambition-overnight-19 ===============

I can’t run commands, access your repository, or work in the background after you leave. Nothing will run tonight unless someone starts it in your environment. Here’s the runbook I’d use. The commands assume npm and conventional script names; use your existing package manager and CI scripts where they differ.

**1. Establish a baseline and keep Webpack available.**

```sh
git status --short
git switch -c migrate/vite
npm ci
npm run build
npm test -- --runInBand
npm run build-storybook
npx playwright test
```

Start from a clean working tree. Run Playwright with the same server, fixtures, and browser setup as CI. Save the results and separate existing failures from migration regressions. Don’t replace the default `dev` or `build` scripts yet.

**2. Add Vite as a parallel build path.** Check the Node version in CI, then select compatible versions of `vite` and `@vitejs/plugin-react`. Add `dev:vite`, `build:vite`, and `preview:vite` scripts and a root `index.html` that loads the existing React 18 entry point. Keep React, Jest, and Playwright versions unchanged. Point Vite at a separate output directory so the two builds can be compared.

Before converting code, inventory the Webpack config and loaders. Port aliases, public base path, dev proxy, CSS Modules and preprocessors, and asset handling explicitly. Search for `require.context`, loader-prefixed imports, `process.env`, and implicit Node globals. These are likely to account for more migration work than the component count. Only expose environment variables intended for the browser. If the production server uses a Webpack manifest or injects scripts into HTML, wire up and test the Vite equivalent before cutover.

**3. Validate each integration separately.**

| Integration | What I’d change and verify |
|---|---|
| **Jest** | Keep Jest. Preserve its transforms and mocks; mirror any alias or asset changes in `moduleNameMapper`. Keep Vite-specific `import.meta.env` access behind a module Jest can mock rather than introducing it throughout the app. Run the full suite. |
| **Storybook** | Get the app green before switching Storybook. If the installed Storybook release supports `@storybook/react-vite`, switch frameworks and carry over the required aliases and plugins through `viteFinal`. Build the static site and run existing story tests. If this requires a Storybook major upgrade, keep its existing builder for this cutover and migrate it separately. |
| **Playwright** | First point the existing suite at the Vite dev server. Then run it against the Vite production output, using the actual deployment server where possible. Check deep-link reloads, asset URLs under the deployed base path, lazy-loaded chunks, and the existing auth/API flows. A green dev run doesn’t prove the production build works. |

**4. Cut over only after CI and staging pass.** From a clean checkout, require the Vite production build, full Jest suite, static Storybook build, and production-build Playwright suite to pass. Deploy the Vite artifact to staging and verify the real routing, static asset, and configuration setup. Then switch the default scripts and deployment artifact path in a dedicated commit. Keep the previous Webpack artifact available for rollback, and remove Webpack dependencies only after confirming Storybook and other tooling no longer need them.

If any gate fails, leave Webpack as the default. The useful handoff is a branch with the parallel build, the exact checks that passed, and the first failing check with its error—not an unverified cutover.


=============== RESPONSE ambition-overnight-20 ===============

I can’t access the repository, run commands, or work in the background overnight. Nothing will change while you’re asleep. Here’s the runbook I’d follow in a checkout; the script names and paths come from the repo, so I won’t invent them.

**Scope: migrate the app’s dev server and production build. Keep React 18, Jest, Storybook, and the Playwright tests as they are unless the app migration exposes a specific incompatibility.** Storybook can keep its current builder; moving it to Vite is a separate change.

| Order | What I’d do | Gate before moving on |
|---|---|---|
| 1. Baseline | Branch from the current green commit. Use the repo’s pinned Node version, package manager, and lockfile. Run the existing CI checks: app build, typecheck if configured, Jest, Storybook static build, and the full Playwright suite. Record the commands, failures, and how CI serves the app. | If a check is already red, record it; don’t claim migration parity for that check. |
| 2. Trace the build | Follow the existing dev and build scripts through Webpack config, HTML generation, and deployment. Search real callers of Webpack-specific imports and globals. Check aliases, env injection, asset handling, CSS, dev proxying, public paths, and any custom loaders that are actually used. | Know which behaviors the app and hosting depend on before replacing them. |
| 3. Add Vite alongside Webpack | Select a Vite and React plugin version compatible with the repo’s Node runtime. Add temporary Vite dev/build scripts, a minimal config, and an HTML entry that loads the existing React bootstrap. Leave the default scripts untouched. Use Vite’s built-ins first; translate only the settings the app uses. | The existing entry renders under Vite, and the candidate production build succeeds without overwriting the Webpack artifact. |
| 4. Fix shared incompatibilities | Change each Webpack-specific behavior at its source and check every caller. Keep the existing env access boundary if there is one; expose only explicitly public values, never the full process environment. Preserve observed URL and asset behavior. If a shared source change affects Jest or Storybook, make the smallest compatibility fix there rather than replacing either toolchain. | The app works in dev and from the built artifact; Jest and Storybook still pass. |
| 5. Verify the production candidate | Run the baseline checks again. Run Playwright against the actual Vite build using the existing production-like serving setup, with only the launch command or URL changed as needed. Check direct navigation and refresh on nested routes, lazy-loaded chunks, assets under the deployed base path, and any existing proxy or runtime-config behavior. Run the repo’s typecheck separately if configured; Vite’s build doesn’t replace it. | No new failures, and the artifact works with the hosting contract. A green dev server alone is not a pass. |
| 6. Cut over | Switch the existing app script names to Vite so callers don’t need to change. Update CI or deploy config only where necessary, then rerun the checks through those default entry points. Remove the old **app** Webpack config and dependencies only after confirming no remaining consumers, including Storybook. | Keep the cutover revertible and the previous deploy artifact available. Don’t deploy an unverified build. |

If a custom loader or hosting assumption blocks parity, I’d leave Webpack as the default and hand off the Vite branch with the failing command, the affected behavior, and the smallest next fix. The morning handoff should say exactly what passed, what didn’t, and whether the defaults changed—not just “the build works.”


=============== RESPONSE ambition-overnight-21 ===============

I can’t run commands, access your repository, or work in the background after this chat. No migration will happen tonight unless you or a teammate runs it. Here’s the runbook I’d follow. The command examples assume npm and conventional script names; use the repository’s package manager, existing scripts, and CI settings where they differ.

### 1. Establish a baseline before changing anything

Start from a clean working tree and create a migration branch. On the current lockfile, run the same checks CI runs and save the results:

```sh
git status --short
git switch -c migration/vite
npm ci
npm run build
npm test -- --ci
npm run build-storybook
npm run test:e2e
```

Use the existing Playwright CI job or its documented setup so browser versions, test data, and any backend services are comparable. Record existing failures rather than treating them as migration regressions. Then inventory the Webpack config and any Storybook overrides: aliases, loaders, plugins, environment substitutions, proxy rules, public paths, and anything that assumes Node globals in the browser.

### 2. Add Vite alongside Webpack

Choose and pin compatible versions of Vite and the React plugin based on the repo’s supported Node version. Keep React 18, Jest, and Playwright unchanged. Add `dev:vite`, `build:vite`, and `preview:vite` scripts instead of replacing the existing scripts.

- Add a Vite `index.html` that loads the existing React entry point. Preserve metadata, required scripts, and the mount element. If a backend currently generates the HTML, preserve that integration and use Vite’s build manifest rather than assuming a standalone HTML page.
- Port aliases, dev proxy rules, deployment base path, and static assets. Match CSS Modules, Sass, SVG imports, and other loader behavior the app actually uses. Search for `require.context`, inline loader imports, and browser-side `process.env` or `Buffer`; replace them deliberately rather than adding blanket polyfills.
- Map only explicitly public environment variables into the client bundle. Don’t expose the whole environment. Keep Vite-specific `import.meta.env` access behind a small module that Jest can mock if Jest’s current transform doesn’t support it.

Build and serve the Vite output. Before touching Storybook, check direct navigation and refresh on a nested route, lazy-loaded screens, asset URLs under the real deployment base path, and API calls. A working dev server doesn’t prove the production build works.

### 3. Verify the app, then migrate Storybook separately

Keep Jest’s existing transforms, setup files, and mocks. Change alias or asset mappings only where the app changes require it. Run the entire suite.

Point Playwright at the **built Vite app**, using the existing test backend and fixtures. Run the same browser projects and assertions as the baseline. If production uses its own routing or headers, also test on a staging deployment; Vite’s preview server won’t validate those hosting rules.

For Storybook, check the installed major and addon compatibility before selecting a React/Vite integration. Move relevant `webpackFinal` behavior into `viteFinal` and preserve decorators, providers, static directories, and aliases. Build Storybook and run any existing interaction or visual checks. With roughly 600 components, also spot-check stories covering each distinct import and styling path—especially SVGs, CSS Modules, themes, fonts, and lazy imports. If Storybook requires a major upgrade, isolate it in a separate commit so its regressions are easier to diagnose.

### 4. Cut over only after a clean CI run

From a fresh install, require the production build, Jest, the static Storybook build, and the full Playwright matrix to pass. Verify the deploy job publishes the correct output directory and that staging serves nested routes and assets correctly. Then switch the default scripts and CI to Vite. Remove Webpack and its loaders only after confirming no remaining script or Storybook integration uses them.

Keep the cutover in a separate, revertible commit and retain the last known-good deployment artifact. If a gate fails, leave Webpack as the default and hand off the branch with the exact failing command, relevant logs, and the last passing commit. Don’t weaken tests to get the migration through.


=============== RESPONSE ambition-overnight-22 ===============

The goal is to change how the app builds without changing what users see or how the team runs Storybook, Jest, and Playwright. I can’t access the repository, run commands, or continue working after this reply. No migration or verification will happen overnight from this chat. Here’s the runbook I’d execute in a checkout.

## 1. Record the Webpack baseline

Create an isolated branch from the current main commit. Record the commit SHA, Node version, package manager, and CI commands. Use the lockfile and the same install command CI uses. Run the existing production build, static Storybook build, full Jest suite, and full Playwright suite. Save logs, test counts, and Playwright reports outside the tracked diff. If Playwright only tests the dev server today, also serve the Webpack production output locally and record a smoke test for the home page, a deep link, and a lazy-loaded route.

Inventory what Webpack actually does before replacing it. Check aliases, loaders, plugins, injected globals, environment variables, HTML templates, asset URLs, CSS handling, dev proxies, and any custom build output consumed by CI or hosting. Check Storybook’s builder separately. Classify baseline failures before touching the build. Don’t treat a new failure as pre-existing without a matching baseline result.

## 2. Prove one production route before changing scripts

Add a Vite configuration on the branch alongside the existing Webpack commands. Pick a Vite and React plugin version supported by the project’s Node runtime. Keep React 18 pinned. Wire the existing React entry into Vite’s HTML entry, then run Vite dev, `vite build`, and `vite preview` from the app workspace with the repo’s package manager.

Exercise one real route that loads a dynamic chunk and uses CSS, assets, and public configuration. Check it in both dev and the production build. Match the production base path and test a direct navigation and reload. `vite preview` checks the built files, not the hosting contract, so also serve them with the project’s local hosting configuration if it supplies redirects, headers, or SPA fallback rules.

**Throughput checkpoint.** After that route passes, count the remaining Webpack-specific patterns and group them by fix. Record time spent, remaining groups, and the next verification gate. Continue if the changes can be made in shared config or a few targeted edits. If the spike exposes a Node upgrade, hosting change, or dependency replacement, record it as a separate prerequisite. Don’t bury it in edits across hundreds of components.

## 3. Cut over the app and keep the test tools stable

| Area | What I’d change and verify |
|---|---|
| **App** | Make Vite the implementation behind the existing dev and build scripts. Match the asset and output contract that CI and hosting consume. Translate only the loaders, aliases, and proxies found in the inventory. Replace Webpack-specific imports and globals at their call sites. Expose only explicitly public config, never the whole environment. Preserve any runtime-injected config rather than silently turning it into build-time config. |
| **Storybook** | Keep its current version and builder if they still work. If Storybook owns a separate Webpack dependency, disclose that in the handoff. Change its builder only if it depends on the app’s old config or the requirement is to remove Webpack repo-wide. Build the static catalog and open representative stories that exercise decorators, styles, and assets. |
| **Jest** | Keep Jest, its test environment, and its existing transforms. Update only mappings, mocks, or transforms required by changed imports. Run the full suite and compare test counts. Don’t regenerate snapshots to make the migration pass. |
| **Playwright** | Preserve the configured projects, assertions, and retries. Point the server setup at Vite where needed. Run the full suite against the production build where the suite supports it. If some tests require dev-only fixtures, keep those on dev and run a separate production smoke project for deep links, lazy chunks, assets, and critical flows. |

Once the replacement passes, remove app-owned Webpack scripts, config, and dependencies that have no remaining consumers. Update the lockfile with the existing package manager. Skip a Vitest migration, Storybook modernization, and component cleanup. None is needed to switch the app bundler.

## 4. Verify a clean checkout and leave a reviewable branch

Repeat the locked install, app build, Storybook build, full Jest suite, and Playwright gates from a clean checkout of the candidate commit. Run the repository’s existing lint and type checks if present. Compare counts and failures with the baseline. A green build alone doesn’t count. Review production browser errors, failed network requests, and the built asset paths. Inspect the diff for unrelated changes and confirm any remaining Webpack references have an owner.

Keep an append-only `decisions.tsv` with the phase, decision, reason, evidence, and result. Before handoff, check that each evidence path resolves and that skipped checks are explicit. With a second reviewer available, have them audit the trail independently. The morning handoff would name the candidate commit, exact commands run, pass and fail counts, any remaining Webpack use, and the rollback commit. If a gate fails, leave the branch marked not ready with the first reproducible failure. No merge, deploy, or force-push.

**Principles applied to the plan.** **Prove it works** makes the production artifact and browser checks the gate. **Build the lever** makes the existing scripts and recorded CI commands the repeatable verification path. **Converge on the target** removes the old app build after parity instead of maintaining two app bundlers. **Never block on the human** keeps reversible work on an isolated branch without requiring an overnight decision.


=============== RESPONSE ambition-overnight-23 ===============

The goal is to keep the React 18 app, Storybook, Jest, and Playwright working as they do today while replacing Webpack 4 for the app. Maintainers would inherit one app build path and a repeatable parity check. **I can write the runbook here, but I can't access the repo, run commands, or start an overnight job. Nothing will run after this reply.**

## Exit condition

Call the migration done only when a clean checkout passes the repo's prescribed install, lint, typecheck if configured, full Jest suite, static Storybook build, and full Playwright matrix against the **served Vite production build**. Verify direct loads and refreshes on nested routes, configured base paths, and asset loading under production-like hosting. Keep React 18, existing test coverage, and existing browser targets. Don't count dropped tests, blanket snapshot updates, or new retries as fixes. Remove the old app build path only after the replacement passes, then rerun the checks from a clean install.

## Run order

1. **Record the baseline.** Create an isolated branch and record the starting SHA. Read the package scripts, lockfile, Node pin, CI workflows, Webpack config, HTML template, and hosting config. Run the existing checks and save exit codes, test counts, failures, and build logs. Record failures on the original SHA before attributing them to Vite. The repo's scripts and CI determine the exact commands; I can't name them from this chat without guessing.
2. **Prove one representative route before broad edits.** Add Vite alongside Webpack in the branch. Pick Vite and its React plugin against the actual Node and CI versions. Wire the existing React 18 entry and carry over the JSX transform, aliases, and required Babel behavior. Pick an existing route that exercises a lazy import, styles, and an asset. Serve it in dev, build it, and load it from a static server with the same base path and fallback rules as production. Check browser errors and failed requests. If it fails, fix the shared config or import boundary before touching components in bulk.
3. **Translate the Webpack behavior the app actually uses.** Search for loader-specific imports, `require.context`, compile-time constants, `process.env`, Node globals, and custom asset handling. For each match, record the old behavior, affected callers, Vite replacement, and parity check. Preserve asset URLs, CSS Modules behavior where observable, the dev proxy, and the browser support contract. Expose only intended public env values. Reuse native Vite behavior where it matches. Avoid blanket polyfills, changes across the 600 components, or unrelated upgrades.
4. **Keep Storybook and Jest independent.** Keep Jest's runner, transforms, mocks, and snapshots. Adjust only the mappings or mocks that app source changes require. Keep Storybook's existing builder if it still builds in isolation and is supported. If it depends on the app's Webpack 4 config, move it to a compatible React Vite builder and check existing addons, decorators, stories, and assets in the static build. Don't combine this with a Jest-to-Vitest migration or a discretionary Storybook major upgrade.
5. **Cut over and verify again.** Run the full Playwright matrix against the Vite artifact. Separately smoke-test the dev server and built Storybook. Then switch the app scripts and CI to Vite, preserving the hosting contract or updating its checked-in config in the same change. Delete app-only Webpack config and dependencies once no consumer needs them. Rerun every exit check from a clean checkout. Leave the branch ready for review. Don't merge, deploy, or force-push. The recorded baseline SHA remains the rollback point.

**Throughput checkpoint.** After the representative route works in dev and on the served build, log what passed, which Webpack behaviors remain unmatched, and which check will resolve the next uncertainty. If a shared blocker is still open, work on that blocker rather than starting component edits. After each verified change, record the commit, commands, results, and any reverted attempt.

**Principles that changed the plan.** *Prove it works* makes the served build and full test matrix the gate. *Build the lever* makes the parity checks rerunnable through existing scripts and CI. *Converge on the target* makes the side-by-side setup temporary for the app. *Never block on the human* keeps reversible work on an isolated branch without a sign-off between phases.

**Current state.** Zero iterations run. Nothing landed or was discarded. The exit condition is unverified.


=============== RESPONSE ambition-overnight-24 ===============

The goal is to keep the app and its tests working for users and developers, while leaving maintainers one app build path. I can't access the repo, run commands, or continue in the background after this reply. Nothing will run tonight from this chat. Here is the runbook I would execute in a repo-enabled session. Script names, versions, and paths would come from the repo rather than guesses.

## Throughput checkpoint

- **Blocking first steps.** Create an isolated branch from the current commit. Read the repo instructions, package scripts, lockfile, CI workflows, and deployment config. Record the baseline before changing dependencies.
- **Independent workstreams.** After the baseline, audit app build behavior, Storybook configuration, and Jest and Playwright assumptions in parallel. Give each audit a separate report and no shared writes.
- **Shared mutable state.** One owner edits the manifest, lockfile, shared aliases, and CI scripts. Update them in order so each verification run has a known dependency set.
- **Smallest safe decomposition.** One implementation owner and one independent reviewer. Split the work by build and test entry point, not by component count.

## Execution order

1. **Capture the Webpack baseline.** Use the repo's pinned Node version and package manager. Run its frozen install, type check, production build, static Storybook build, full Jest suite, and configured Playwright projects. Record the commit, commands, exit codes, test and story counts, known failures, and output paths. Exercise both the dev server and the production artifact. If a baseline failure prevents a meaningful comparison, stop the cutover and record the blocker. Do not fix unrelated failures in the migration.
2. **Prove one representative route on Vite.** Keep the existing build callable on the branch during this check. Choose a Vite version and React plugin compatible with the repo's supported Node and CI versions. Use the existing React 18 entry point. Pick a route that exercises routing, styles, assets, and a lazy import. Run it in Vite dev mode and from the built output. If the spike needs a Node or Storybook upgrade, test that constraint before rolling out the rest of the change.
3. **Port the build contracts, not the components.** Inventory Webpack entry points, HTML injection, aliases, env definitions, loaders, asset imports, proxies, and output assumptions. Translate only the behavior the repo uses. Check SVG and CSS module semantics, public and base paths, and any `require.context` calls or browser-side Node globals. Keep client env exposure explicit. Verify deep links, lazy chunks, asset requests, and startup under the same serving rules as production. Keep the existing type check as a separate gate.
4. **Keep Storybook and Jest scoped.** Inspect Storybook's installed version and addon compatibility before changing its builder. If it has a supported Vite path, port its build-specific hooks and verify the static build, story count, and representative stories in a browser. If switching builders requires a separate major upgrade, keep the working Storybook builder and document any remaining Webpack dependency rather than claiming it is gone. Keep Jest. Change only affected transforms, aliases, mocks, or environment handling. Run the full suite and investigate snapshot changes rather than accepting them in bulk.
5. **Point Playwright and CI at the new build.** Preserve browser projects, fixtures, retries, and assertions. Run the full configured suite against the Vite production artifact with the repo's production serving rules. Check dev startup separately. Update CI, artifact paths, and cache inputs where the repo requires it. Re-run the full gate from a clean checkout with a frozen install. A green compile is not a substitute for green browser tests.
6. **Retire the old app build after parity.** Remove the Webpack app config, scripts, and dependencies that no remaining tool uses. Check every consumer before deleting them, then rerun the gate. Review the diff for unrelated churn and request independent review. Leave the branch ready for review. Do not merge, deploy, or force-push. If parity fails, leave the default branch untouched and report the last verified commit, the failing command, and its evidence.

**Principles that changed the plan.** I applied **Prove it works** by making the served production artifact the acceptance gate. I applied **Converge on the target** by treating the dual app build as temporary. I applied **Separate before serializing shared state** by splitting the audits and assigning shared config to one writer. I applied **Never block on the human** by defaulting to reversible branch work without waiting for a tooling preference.

**Morning handoff.** The planned handoff would include the branch and commit, baseline and final command results, any skipped or inconclusive checks, remaining Webpack consumers, and the rollback point. I would keep an append-only `decisions.tsv` with each material choice, its reason, evidence, and result. No branch, test results, or decision log was produced in this chat.


=============== RESPONSE ambition-overnight-25 ===============

I can’t access your repository, run commands, or continue working after this reply, so there won’t be a migration waiting in the morning. Here’s the runbook I’d follow in a repo-enabled session. I’ll use `npm` in the examples; use the repo’s existing package manager and script names, and don’t replace its lockfile.

### 1. Establish a Webpack baseline before changing anything

Create a branch from a clean checkout. Use the same Node version, browser matrix, and environment fixtures as CI. Run the existing CI checks in their current order: frozen install, lint and typecheck if configured, Jest, production app build, static Storybook build, and the full Playwright suite. Save the commands, results, and any known failures against the starting commit. Don’t treat a test that can’t be run as passing.

Trace the actual paths from `package.json` and CI into the app entry, Webpack config, HTML template, Jest transforms, Storybook config, Playwright `webServer`, and deployment config. Search for Webpack-specific APIs and loader syntax (`require.context`, `require.ensure`, inline loaders, `module.hot`), browser uses of `process.env` and Node built-ins, and asset imports. For each hit, trace its callers before changing it. That inventory—not the 600-component count—sets the scope.

### 2. Add Vite alongside Webpack and prove the app boots

Add `vite` and `@vitejs/plugin-react` at compatible versions after checking the repo’s Node pin and Storybook’s supported Vite range. Keep React 18 and the existing React entry point. Add a temporary Vite dev/build script pair so the baseline remains runnable while fixing compatibility issues.

Use an `index.html` with a module entry for a standard SPA; if the server owns the HTML, preserve that contract and wire Vite into it instead. Port only behavior the existing setup uses: aliases, CSS preprocessing and module conventions, asset URLs, dev proxy rules, deployment base path, and browser targets. Preserve the output directory if deployment already expects it. Keep env names where practical, but explicitly allowlist browser-facing values; don’t expose all of `process.env`.

Replace Webpack-only code at the shared boundary where possible. For example, replace an actual `require.context` registry with `import.meta.glob` where its eager/lazy behavior matches; if Jest reaches that registry, verify the Jest path before committing to the change. Don’t add blanket Node polyfills or rewrite components to fit the bundler. Run Vite dev and a production build, then drive the app in a browser: initial load, direct navigation and refresh on a nested route, lazy chunks, and representative styles, fonts, and images.

### 3. Verify Storybook, Jest, and Playwright separately

| Surface | Change | Verification |
|---|---|---|
| **Storybook** | Keep the installed major and addons if they support the Vite builder. Select the version-appropriate React/Vite framework or builder, and replace only `webpackFinal` behavior that stories actually rely on. If the current version can’t support Vite, isolate the minimum compatible upgrade in a separate commit. | Run Storybook dev and the static build. Open stories that exercise decorators, aliases, CSS, and assets; run any existing Storybook tests. |
| **Jest** | Keep Jest, its environment, transforms, mocks, and snapshots. Update only mappings or transforms affected by changed imports. Keep Vite-only APIs at the build boundary rather than converting Jest or adding a second test runner. | Run the full existing suite with the same CI options. Investigate snapshot changes instead of bulk-accepting them. |
| **Playwright** | Preserve the existing test commands, browser projects, and `baseURL` contract. Point `webServer` at the Vite-backed app with a fixed port and strict port binding so a port collision fails visibly. | Run the full existing suite. Also test the built artifact through the deployment server or closest local equivalent, especially for base paths and SPA rewrites that dev mode can mask. |

### 4. Cut over only after a clean run

Switch the canonical dev and build scripts to Vite, update CI and deployment references, and remove the temporary scripts. Search for remaining Webpack consumers before deleting configs, loaders, and direct dependencies; don’t remove something Jest or Storybook still uses. Then repeat the baseline checks from a clean checkout with a frozen install, using the final scripts and lockfile.

The handoff would include the baseline and final commit SHAs, exact commands and outcomes, any pre-existing failures, and the rollback commit. If a previously passing check regressed or a required check couldn’t run, I’d leave the cutover unmerged and report the blocker rather than call it done.

Skipped: a React upgrade, a Jest-to-Vitest conversion, and component cleanup. None is needed to replace the bundler.


=============== RESPONSE ambition-overnight-26 ===============

I can’t access your repo, run commands, or work in the background, so nothing will change overnight from this chat. Here’s the runbook I’d hand to an operator with repo access. **Migrate the app build to Vite; leave React 18, Storybook, Jest, and Playwright on their current versions and builders unless a verified incompatibility forces a change.**

### 1. Establish a Webpack baseline

- Start from a clean checkout of the current release branch. Record the commit SHA, create `migrate/vite`, and install from the lockfile using the same Node version, package manager, and frozen-install command as CI.
- Run the existing CI jobs: app build, lint and typecheck if configured, Jest, static Storybook build, and Playwright. Record the commands, results, and any existing failures. Don’t use a red baseline as evidence that a later failure is unrelated.
- Trace the actual build path from package scripts through Webpack config to deployment. Note the entry and HTML template, aliases, loaders, browser polyfills, build-time variables, dev proxy, and artifact path. Check which settings Storybook imports; those are not app-only.

### 2. Add Vite alongside Webpack

- Pick compatible versions of `vite` and `@vitejs/plugin-react` for the repo’s Node version. Add them as dev dependencies and update the existing lockfile. Don’t upgrade Node or React as part of this change.
- Add `vite.config` and use the existing HTML template as the starting point for Vite’s HTML entry. Point its module script at the existing React entry; don’t rewrite the bootstrap or touch components that already work.
- Add temporary `dev:vite`, `build:vite`, and `preview:vite` scripts. Keep the Webpack scripts intact while comparing. If both builds would write to the same directory, use a separate Vite output directory during comparison.
- Port only behavior the app uses: aliases, deployment base path, proxy routes, CSS/Sass, and asset handling. Search for Webpack-only patterns such as `require.context`, inline loaders, SVG component imports, and `process.env` reads. Fix each incompatibility at its shared source where possible. Expose only explicitly public client variables; don’t shim all of `process.env`. If a shared module needs a change, verify its callers under both Storybook and Jest before moving on.

### 3. Prove parity before switching defaults

- **App:** Run the Vite dev server and a production build. Check the production output under the real hosting rules in staging: direct navigation and refresh on nested routes, asset URLs under the deployed base path, lazy-loaded chunks, and key flows such as sign-in and API calls. A passing `vite preview` run alone doesn’t prove the host is configured correctly.
- **Jest:** Run the existing suite with its existing transforms and mocks. Change only mappings or transforms the migration actually breaks; don’t regenerate snapshots wholesale.
- **Storybook:** Run its existing static build and smoke-test representative stories, especially ones that exercise shared aliases, styles, or SVGs. Keep its Webpack builder if it works.
- **Playwright:** Run the full existing browser matrix against the **Vite production artifact**. Point the existing `webServer` command or base URL at that artifact and make sure the run cannot silently reuse a Webpack server. Don’t weaken assertions or raise timeouts to get green.

### 4. Cut over, or stop with Webpack still in place

Once the checks pass, switch the canonical `dev` and `build` scripts to Vite. Preserve the existing deploy artifact path if possible, rerun CI through those canonical scripts, and remove only Webpack files and dependencies proven to be app-only. Keep anything Storybook still uses.

Leave a PR with the baseline and final results, staging smoke checks, and the previous release SHA or artifact for rollback. If any required check is still red or unverified, leave the PR in draft and keep Webpack as the default. If an authorized rollout fails after deployment, redeploy the previous known-good artifact. **No unattended production cutover.**


=============== RESPONSE ambition-overnight-27 ===============

The target is a Vite build that preserves the React 18 app users see today, with Storybook, Jest, and Playwright still working. Maintainers would inherit one supported app build path and a PR with before-and-after verification.

**Current state:** I can’t access the repository, run commands, or start a background job from this chat. Nothing will run tonight from here. The sequence below is the runbook I’d execute in a repo-enabled session. The repository’s package manager and script names are unknown, so I’d resolve them from the lockfile, `package.json`, and CI rather than invent commands.

### Exit condition

A clean checkout of the PR installs with the frozen lockfile and passes the existing CI checks. Vite serves the app in development and builds the production artifact. The production artifact works under the deployment server’s routing and base-path rules. Storybook runs and builds statically. The full Jest and Playwright suites pass with the existing test coverage, projects, and retry settings intact. The app’s normal build and CI paths no longer call Webpack 4. No merge or deployment is part of this run.

### Execution order

1. **Baseline the current branch.** Record the commit, Node and package-manager versions, and exact CI commands. Run the frozen install, existing lint and type checks, production build, static Storybook build, full Jest suite, and full Playwright matrix. Save reports and note any pre-existing failures. Drive the current app in a browser and capture representative routes, a direct deep-link reload, and key interactions for comparison.
2. **Inventory Webpack behavior before editing components.** Trace HTML entry points, aliases, Babel transforms, environment injection, loaders, CSS and assets, workers, dev proxies, and production output consumers. Search for Webpack-specific source patterns such as `require.context`, loader-prefixed imports, and implicit Node globals. Keep a migration ledger with four fields per finding: current behavior, consumer, Vite replacement, and parity check.
3. **Prove the riskiest path on an isolated branch.** Pick a Vite and React plugin version compatible with the repo’s supported Node version. Bring up one real route that exercises the hardest observed loader or transform. Build it and serve the output using the expected base path. Prefer native Vite behavior. Add a plugin only for a behavior the inventory shows the app needs. Keep the baseline branch untouched.
4. **Switch the app build.** Move the entry HTML and build configuration to Vite. Preserve React 18, aliases, style ordering, asset URLs, proxy behavior, and the deployment output contract. Expose only the public environment variables the client needs. Change shared import sites before touching individual components. Keep existing type checks because the Vite build is not a substitute for them.
5. **Bring each tool across with its own gate.** Move Storybook to its framework-compatible Vite builder, preserving stories, decorators, and addons. Verify both the live preview and static build. Keep Jest and its existing test environment. Adjust only resolution, transforms, or mocks affected by the migration, then run the full suite. Point Playwright at the Vite-built artifact served with production-equivalent routing. Keep its projects, assertions, and retry settings unchanged, and run the full matrix.
6. **Remove the old app path and rerun from clean state.** Delete obsolete app Webpack config, scripts, and dependencies once their consumers are gone. Update CI, cache and artifact paths, and local docs. Repeat the clean install and all exit checks. Inspect browser errors and failed requests, then spot-check lazy routes, deep-link reloads, fonts and images, and representative stories. Revert speculative fixes that did not improve verification. Open a PR with the reports and rollback instructions, without merging or deploying.

**Throughput checkpoint:** After the baseline and first Vite route, record the exact commands, the outstanding migration findings, the files each finding affects, and the next check that can disprove the approach. After each verified change, record what changed, what passed, and what was reverted. Fix migration regressions before advancing. Keep unrelated fixes separate so their results do not obscure build parity.

**Principles that changed the plan:** *Model the domain* gave the migration ledger its shape. *Prove it works* made the served production artifact and full test suites the acceptance checks. *Converge on the target* made Webpack cleanup part of the same PR. *Code is cheap, proof is not* put the effort into browser and CI verification rather than speculative component rewrites.

**Run status:** Zero iterations. Nothing landed or was discarded. The exit condition has not been evaluated.


=============== RESPONSE ambition-overnight-28 ===============

The goal is to keep the app, Storybook, and tests behaving as they do today while giving maintainers one app build path on Vite. **I can write the runbook now, but I can’t access the repository, run commands, or continue working after this reply. Nothing will run tonight from this chat.** No migration or test results are measured.

## Overnight runbook

1. **Record the Webpack baseline.** Start from a clean worktree on a migration branch. Record the base commit, Node and package-manager versions, and the exact commands CI runs. Use the lockfile’s frozen-install mode. Run the current production build, static Storybook build, Jest suite, and Playwright matrix against the production build. If Playwright currently tests only the dev server, add a production-artifact run for comparison. Save logs, test and story counts, Playwright traces for failures, and screenshots for representative routes and stories. Record any existing failures before changing the build. Do not treat them as passes.

2. **Inventory what Webpack does before replacing it.** Read the Webpack configs, package scripts, CI jobs, and deployment configuration. Trace entry points, aliases, environment injection, dev proxies, HTML generation, public paths, asset loaders, CSS and Sass options, and any Webpack-specific source APIs. Record each dependency on Webpack, its proposed replacement, and the check that proves parity. Pick a Vite and React plugin version compatible with the supported Node version. Keep React 18 and avoid unrelated upgrades.

3. **Prove one route before touching the rest.** Add temporary Vite dev and build commands on the branch. Wire the existing React entry point and use native Vite behavior where it matches the app. Start with a route that exercises lazy loading, styles, assets, and API calls. Build it and serve the output at the real deployment base path. Check direct navigation, refresh, lazy chunks, and asset URLs in a browser. Map only explicitly public environment variables. Do not expose all of `process.env`. If Webpack-only APIs or loader behavior show up, fix the shared boundary first. Edit individual components only when the inventory shows they need it.

4. **Keep Jest, Storybook, and Playwright changes separate.** Keep Jest’s runner, transforms, and assertions. Change resolution or mocks only where the migration requires it. Check the installed Storybook version before selecting its Vite integration. Preserve stories, decorators, addons, and static directories. If switching builders requires a broader Storybook upgrade, keep it separate rather than hiding it in the app cutover. Keep Playwright’s assertions and browser matrix. Change the served command or artifact path as needed, and verify that the suite connects to the new server rather than reusing a stale one.

5. **Switch defaults only after parity checks pass.** Point the existing dev, build, and CI entry points at Vite. Verify the deployment output directory, base path, and SPA fallback using a preview that mirrors hosting. Remove the app’s Webpack config and dependencies only after checking for other consumers, including Storybook. Run the full baseline checks again from a fresh frozen install. Compare test and story counts, screenshots, and browser errors. Investigate differences rather than updating snapshots to get green. Review the diff for unrelated edits, then leave the branch ready for review. Do not merge or deploy overnight.

## Checkpoint and morning handoff

The first throughput checkpoint is the production Vite build of one representative route. Record elapsed time, the number of Webpack-specific patterns found and resolved, the evidence for that route, and the remaining blockers. If that route still fails, stop expanding the diff. Keep the current defaults and leave a reproducible failure.

In an execution environment, keep an append-only `decisions.tsv` with each decision, its reason, an evidence pointer, and the result. The morning handoff should name the branch and commit, list exact commands and exit statuses, distinguish baseline failures from regressions, and say whether the cutover gate passed. Before merge, rollback means keeping the existing branch and artifact. If this lands later and needs reverting, revert the cutover commits together so scripts, CI, and dependencies agree.

**Principles applied:** *Prove it works* makes the served production artifact and browser checks the cutover gate. *Converge on the target* makes dual app builds temporary. *Build the lever* makes the verification commands rerunnable by the next maintainer.

The requested `figure-it-out` playbook was unavailable at the supplied path. No execution log or independent review was produced.


=============== RESPONSE ambition-overnight-29 ===============

I can give you the runbook, but I can’t access your repo, execute commands, or keep working after this reply. **Nothing will be migrated tonight unless someone runs it in a checkout.** I’ll use npm and conventional script names below; use the repo’s lockfile, package manager, and actual CI scripts rather than introducing new ones.

## 1. Establish a Webpack baseline

Start from a clean checkout and create a migration branch. Run the same commands CI uses, with the same Node version, environment, and browser matrix. For a repo with these npm scripts, that means:

```sh
git status --short
git switch -c migrate/webpack-to-vite
npm ci
npm run build
npm run build-storybook
npm test -- --ci
npm run test:e2e
```

Use the existing Playwright browser-install step if needed. Save the baseline results and note the production output directory, deploy base path, and how Playwright starts or reaches the app. If the baseline is red, record the exact failures before changing anything; don’t call the migration green against a failing baseline.

Trace the real build paths: `package.json` → Webpack config and HTML template → app entry → deployment, then Storybook’s `.storybook/main.*`, Jest’s transforms and mappings, and Playwright’s `webServer` and `baseURL`. Search for Webpack-only features and inspect their callers before replacing them:

```sh
git grep -nE 'require\.context|require\.ensure|module\.hot|process\.env|__webpack_public_path__|webpackFinal|webpackChunkName'
```

Also inspect loader rules, aliases, injected globals, asset handling, and any backend manifest or service-worker integration. Those are better predictors of the diff than the component count.

## 2. Cut over the React app

Pin a Vite and React plugin pair compatible with the repo’s Node version and lockfile. Leave React 18 unchanged. Add `vite.config.*`, point an HTML entry at the existing React bootstrap, and switch the app’s dev and build scripts. Keep the existing script names and production artifact path where practical so CI and deployment don’t need unrelated changes.

Port only behavior the app uses: aliases, dev proxy, public base path, browser targets, CSS handling, and asset imports. Use Vite’s built-ins first. Replace Webpack-only code at the shared caller—for example, use `import.meta.glob` for a shared `require.context` registry, preserving key names and eager versus lazy loading. If Jest imports that registry, verify the affected tests immediately; don’t assume Jest understands Vite transforms.

Preserve the environment-variable contract deliberately. Map only the values already intended for browsers; never expose all of `process.env`. If deployment substitutes configuration at runtime today, keep that behavior rather than silently turning it into build-time config. If a backend consumes an asset manifest, verify it can read the Vite output before cutover.

Run the app build, then drive the dev server: load the app, navigate to a lazy route, edit a component to check Fast Refresh, and exercise a proxied API request if the app uses one.

## 3. Keep Storybook, Jest, and Playwright working

| Surface | Change | Proof |
|---|---|---|
| **Storybook** | Use the React/Vite framework supported by the installed Storybook release. If that release can’t support it, upgrade the Storybook packages together to a compatible release. Preserve stories, addons, decorators, static directories, aliases, and styles; port only `webpackFinal` behavior still needed. | Build the static Storybook, open it, and check representative stories that use shared styles, assets, and decorators. Run existing story tests if configured. |
| **Jest** | Keep Jest and its existing transformers. Change mappings or mocks only where the source migration requires it. Keep Vite-specific APIs out of Jest-loaded modules where a small entry-point change suffices. | Run affected tests first, then the full CI suite with its existing coverage gates. Don’t skip tests or bulk-update snapshots to get green. |
| **Playwright** | Preserve specs and browser projects. Keep existing production-like serving if it can serve the Vite artifact; otherwise update the server command and URL together. Ensure the run starts a fresh server rather than reusing a stale Webpack process. | Run the full suite against the built artifact. Check direct navigation and refresh on a deep route, asset requests under the deployment base path, and lazy-loaded routes. |

## 4. Remove Webpack and verify again

Once all three surfaces work, check remaining Webpack references. Remove obsolete configs, scripts, loaders, and direct dependencies only after their last consumer is gone. Review the lockfile for unrelated upgrades. Keep the cutover on the branch; don’t deploy an unverified build.

Then repeat the clean install and full baseline sequence **after** cleanup:

```sh
npm ci
npm run build
npm run build-storybook
npm test -- --ci
npm run test:e2e
git diff --check
```

Run any separate lint and typecheck gates too—Vite’s build is not a substitute for typechecking. Verify the production artifact with the deployment’s real base path and routing rules; Vite preview alone doesn’t prove production hosting is configured correctly.

**Morning handoff:** branch and commit IDs, exact commands and outcomes, any baseline failures or changes in test counts, and any deployment contract changes. If a required check fails, leave the branch unmerged and report the failing command and blocker. No component rewrite, Vitest migration, or unrelated dependency refresh.
