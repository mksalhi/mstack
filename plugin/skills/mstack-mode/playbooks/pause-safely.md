### Pause safely

**You own a clean stop. Leave a checkpoint a cold-start agent can resume from.** Explicit only. On "keep going", "going to bed, keep going", or "don't stop", do not pause.

1. Stop at a safe boundary. Finish or back out of the current atomic step. Start nothing new. Cancel nested subagents.
2. Take no irreversible action to pause. No PR and no push unless one was already out.
3. Commit uncommitted edits as one `wip:` commit on the current branch. If the tree is broken, say so in one line of the commit body.
4. Write the resume note in the Write mode output shape of the `handoff` skill (`<mstack>/skills/handoff/SKILL.md`): intent, progress and what's verified, key files, gotchas, the next step. For the compaction trigger write it to `~/.claude/mstack/<slug>/resume.md`. If a decision-log trail exists, point at it instead of duplicating it.

**Reply:** where you are in the loop, what's on disk versus still in your head (paths, no diff dumps), the commits made and whether the tree is clean, the first action on resume. A pause, not a final report.
