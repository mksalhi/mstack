# sidebar

One side pane for everything, drawn in the `token-rate` style: titled tiles gathered at the bottom of the docked pane, level with the prompt bar, with label and value rows inside and no borders. A Claude Code mod (a plugin with a hooks module).

It replaces `session-pane`, `all-agents`, `doubt`, `quick-commit` and `prompt-cache-control` from this repository, and takes over what the separate `token-rate` mod draws.

## Use

The pane opens by itself from a window 144 columns wide. Below that, type `/sidebar`. `/sidebar cache` (or any tab name) opens it on that tab. Click a tab name under the tiles to switch.

Three commands jump straight to a tab and act:

| Command | Does |
| --- | --- |
| `/cache` | Opens the cache tab |
| `/doubt` | Opens the doubt tab and asks for a second opinion on the last answer |
| `/quick-commit` | Drafts a commit message and opens the commit tab |

The status line shows `ctx 45% · cache 98% 3:41` at all times.

Where the app can't dock the pane at the side it sits above the prompt as one compact row: live rate, context percent, cache hit rate and countdown, session cost.

## Tabs

| Tab | Tiles | Click does |
| --- | --- | --- |
| tokens | Output live (tokens per second with a 20-second chart), Last response (input, cached, output, speed, cost), Session (output, average, peak, cost) | |
| cache | Prompt cache (read, wrote, new, time left, advice), Requests (the last eight, with hit rate) | |
| context | Context window (percent, tokens, compaction threshold, model), By category | |
| turn | This turn (calls, time in tools, slowest), Tool calls with durations | |
| files | Edits (files, edits), Edited this session, hottest marked | |
| todos | `TODO` and `FIXME` lines Claude wrote this session | Sends the item back as a prompt to resolve |
| prompts | The last 100 distinct prompts, newest first | Puts the prompt back in the prompt box |
| agents | Agent types with a task field, Runs | Starts that agent type on the task |
| doubt | The model's argument against its last answer; the conversation never sees it | Ask, or ask again |
| commit | A drafted commit message and the changed files | Draft, then Commit all |

On desktop the tokens, cache and context tabs draw a chart and rings; a terminal gets text bars.

## Limits

- The live rate is estimated from characters until a response ends, as in `token-rate`.
- Cost per response uses a hand-kept price table at the top of `hooks/register.tsx`; a model not in it shows "no price for model".
- The cache lifetime is a guess: one hour when the account reports a five-hour or weekly window under 100%, five minutes otherwise. Environment overrides and gateways are not read, and it does not correct itself from request timing as `prompt-cache-control` did.
- Edits made through Bash are not counted in files or todos.
- Starting an agent with an empty task only shows a toast.
- Commit all runs `git add -A` and commits on the current branch, whatever it is.
- `/doubt` and each commit draft cost one model call.
- Run it instead of `token-rate`, not beside it: both would open a pane with the same figures.

## Files

- `hooks/register.tsx`
- `types/index.d.ts` (state contract)

## Install

See the [repository README](../README.md).
