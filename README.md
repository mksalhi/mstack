# mstack

An agent plugin for Claude Code and Codex: playbooks, principles, review and parallel-work skills, UI review, and code-rendered films, with every role on Opus 5.5. By [Mohammed Al Salhi](https://github.com/mksalhi).

- **The plugin** (`plugin/`): `skills/`, `agents/`, `hooks/` and the Claude Code, Codex and Cursor manifests. The marketplace manifests stay at the repo root.
- **Templates** (`templates/project-AGENTS.md`): a skeleton for a project's own AGENTS.md.

## Install

```bash
claude plugin marketplace add mksalhi/mstack
claude plugin install mstack@mstack
codex plugin marketplace add mksalhi/mstack
codex plugin add mstack@mstack
```

In Codex, `plugin/.codex-plugin/plugin.json` points at the same `skills/` and `hooks/`, so the two never drift. The scripts need Node 24.2+ and pnpm 10+.

Then run `/mstack:setup-mstack` once to write `~/.claude/rules/mstack-models.md`. If you skip it, the skills fall back to the same Opus 5.5 defaults.

If you keep personal copies of skills that mstack bundles, remove them, or agents get every instruction twice.

## Adding a skill

Add `plugin/skills/<name>/SKILL.md`. Give a skill its own folder when a model would reach for it on its own. Fold it into an existing skill's table only when it is one area of that skill, like a `ui` area or a `principles` rule.

## Use

Start any task that needs rigor with `/mstack:mstack-mode`:

```
/mstack:mstack-mode the nightly cleanup job skips rows deleted exactly 72h ago. repro first, then fix and verify.
```

It matches the task to one of 24 playbooks (bug fix, feature, refactoring, investigation, babysit, shipping, full stop, autonomous run, and more), opens a todo list from that playbook's steps, and routes to the other skills as steps need them. The playbook index is in [`skills/mstack-mode/SKILL.md`](./plugin/skills/mstack-mode/SKILL.md).

You can also call a skill directly. For example, `/mstack:how` gives a subsystem walkthrough, `/mstack:why` explains why something was built that way, `/mstack:interrogate` has several models try to break a diff, `/mstack:council` reviews in rounds and fixes until the models agree, `/mstack:arena` runs parallel attempts and takes the best, and `/mstack:arena` in swarm mode runs parallel workers over slices.

## What's inside

**Repo conventions.** Each repo's own `AGENTS.md` wins over mstack-mode wherever they disagree.

**Models.** Every configured role defaults to `claude-opus-5-5`. Steps that need a different model family (cross-judge, trail review, verifiers) use fable or sonnet. Re-run `/mstack:setup-mstack` and pick `mixed` for an opus/fable/sonnet table, or change single roles by hand in `~/.claude/rules/mstack-models.md`.

**Skills.** One folder per skill under `plugin/skills/`, flat. Two skills hold several areas behind a table: `ui` (`/mstack:ui <area>`: review, accessibility, layout, copy, typography, colors, polish, animate, animate-expo, mobile-web, break, sonner, prototype) and `principles` (13 rules stated inline, detail files under `references/`).

| Group | Skills |
|---|---|
| Understand | `how` (walkthroughs, teaching, research), `why` |
| Plan | `architect`, `blast-radius`, `figure-it-out` |
| Parallel | `arena` (best-of and swarm), `interrogate`, `council` (review rounds until agreement) |
| Verify | `debug`, `test-audit`, `playwright`, `verifier`, `formal-verification` |
| Ship | `pr` (body, cutting comments, bot review threads), `takeover` (finish someone's PR, modernize an old one), `scoper` (always on; `/mstack:scoper lite\|full\|ultra\|review\|debt`), `writing` (prose, unslop, plain, sharpen) |
| Session | `handoff` (write, resume, catch up), `decision-log`, `retro`, `automate-me` |
| Design | `ui`, `principles` |
| Other | `mstack-mode` (playbooks), `setup-mstack`, `motion-video` (with the `motion-critic` agent), `write-swift` |

**Tags.** Every `SKILL.md` carries machine tags under `metadata` (the Agent Skills spec's free-form field, so validators accept it):

```yaml
metadata:
  harness: "claude codex"      # which harnesses get it
  platform: "darwin linux"     # which OSes
  scope: universal             # universal | command-center | <machine-name>
  requires: "npx"              # optional; if missing, tell the user instead of guessing
```

Today every skill is `universal`.

The store lives at `~/.claude/mstack/<slug>/`.

## License

MIT, © 2026 Mohammed Al Salhi. [LICENSE](./LICENSE) also carries the third-party notices.
