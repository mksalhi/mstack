# Code Archaeology (git + in-repo)

## What this source contains

The most trustworthy and complete source, tied directly to the code: commits (messages, dates, authors, diffs); PR descriptions, reviews, and threads (via `gh`); inline comments, TODOs, FIXMEs, deprecation notes; ADRs; tests (names and assertions encode motivating edge cases); co-changed files; CHANGELOG and release notes; ticket IDs in commits and PR bodies.

## How to search it

Expand the seed commit list:

```bash
git log --follow --oneline -- <file>            # history through renames
git log -S '<exact_string_from_code>' -- <file> # pickaxe: added/removed this text
git log -G '<regex>' -- <file>                  # pattern pickaxe
git blame -L <start>,<end> <file>               # who wrote each line, when
git show <hash>                                 # one commit's full diff
git log <old>..<new> -p -- <file>               # commits between two points
```

Out-of-band docs:

```bash
rg -l -i 'architecture.decision' --glob '*.md'        # ADRs (often docs/adr/)
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>   # markers near the target
rg -l '<symbol>' --glob '*test*'                       # related tests
```
