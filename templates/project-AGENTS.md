# <!-- Project name -->

## Glossary

Each word below has exactly one meaning in this file.

- **you**: the agent reading this file.
- **I / me**: <!-- project owner -->
- **we / maintainers**: <!-- who maintains the project -->
- **user**: <!-- who uses the product, not the developer -->
- **<!-- term -->**: <!-- one meaning; add the words this project overloads -->

## What this is

<!-- Two or three sentences: what the project does, who uses it, and how it ships
     (app, library, service, CLI). -->

## Never compromise on

- <!-- the 2–4 qualities that make this project worth using -->
- User experience over implementation convenience: fewer, polished features beat many rough ones.

## A note from me

- Ambitious ideas, simple systems. Don't preserve complexity for its own sake: when a requirement
  changes the design, build the target design, migrate every caller, and delete the old path.
- Fix only what the task needs. Anything else you notice goes in a follow-up, not this change.
- These are defaults, not hard rules. A maintainer's stated preference overrides them.
- <!-- project-specific note -->

## Ways agents have hurt this project

<!-- Fill from real mistakes, not guesses. Run the `retro` skill after a thread goes
     wrong, and add each repeat failure here with what to do instead. When the same correction
     comes up twice, turn it into a lint, check, or script instead of more text. -->

1. <!-- failure -->: <!-- what to do instead -->

## Hit every surface

A change is done when it reaches every place below that it touches. Grep every caller before
editing a shared function.

- [ ] <!-- entry points (CLI, routes, jobs) -->
- [ ] <!-- each client (web, mobile, extension) -->
- [ ] <!-- shared types / contracts package -->
- [ ] <!-- docs: user-facing and maintainer-facing -->

## Dev servers

- Start: `<!-- exact command -->` in its own terminal session, never as a blocking foreground
  command. Report the command, URL/port, and how to stop it.
- Don't use: `<!-- commands that look right but aren't -->`
- Parallel worktrees each get their own ports and data: <!-- how this project isolates a stack -->.
  Never run a stack in my primary checkout.
- Save the PID of anything you start, and only ever kill your own processes.

## Verification

- Verify against the real artifact, not a proxy, before calling work done: run the app, the
  command, or the test that exercises the change.
- Verify skill: `<!-- path to this project's verify skill, made with the `verifier` skill -->`
- Gate before a PR: `<!-- lint / typecheck / test commands -->`
- Test data: <!-- fixtures or seed command; never real user data -->
- New or changed tests pass the `test-audit` gate.

## Where code lives, and taste

- Complexity lives at the boundaries (adapters, parsers, I/O). Business logic stays in pure
  functions, and UI stays dumb.
- Make illegal states unrepresentable, and no casts.
- <!-- where each kind of code goes in this repo: packages, folders, layers -->
- <!-- project taste rules: naming, styling, libraries to prefer or avoid -->
- If a change fights these rules, push back and get my sign-off instead of working around them.

## Security

- Validate input at trust boundaries, and never simplify away security, data-loss handling, or
  accessibility basics.
- Don't over-engineer protection for dev-only or maintainer-only tooling.
- Never write secrets, tokens, or credentials into files. <!-- where this project's secrets live -->
