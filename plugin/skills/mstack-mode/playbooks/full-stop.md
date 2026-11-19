### Full stop

**Nobody is watching. Take one change from its current state to a PR that is ready to merge, then stop. Merge only when the user said "full send".**

"full stop" or "full send" is the grant. Without one of those words, follow the normal playbooks and ask as usual.

**What the grant covers.**
- Commit, push, rebase and fix conflicts on this task's branch. Force-push only that branch, with `--force-with-lease` pinned to the head you last saw.
- Use any test method that step 2 needs (computer use, browser automation, simulators, a dev server, screenshots), even where `AGENTS.md` says to ask first. Rules about *how* to test still apply. List each gated method in the reply.
- "full send" only: merge once the merge gate passes, with the method the repo uses. Never `--admin` or another bypass.
- Nothing else. Deleting data, production, anything outside the repo, closing a PR, or force-pushing another branch still needs the user.

1. **Finish the change.** Branch off trunk if you are on it. Make the smallest change that meets the user's goal. Fix the case that happened, not every case that could. Under "full stop", turn off auto-merge and leave any merge queue before the first push, and check again before each later push.
2. **Prove it.** Evidence you saw yourself in this session, per Prove it works (`principles`): reproduce the failure, fix, watch the same repro pass; run the checks CI runs; add one focused test that fails without the fix when the repo has a test setup; for UI or runtime behavior, drive the real surface (project `verify-*` skill, `playwright`, or Bash). Done when every change in the diff has its own proof. No way to prove a change means asking (step 7).
3. **Review it.** Run `council` on the diff. Done when council stops with agreement. If it stops stuck with a blocker or should still open, that is a question for the user (step 7), never something to merge past.
4. **Open the PR** per `playbooks/opening-a-pr.md`, rebased on the latest trunk. Add one line to the body naming how you proved it. Done when the PR is open, not a draft, and its URL is in hand.
5. **Babysit** per `playbooks/babysit.md` in `drive` mode. Prove each fix before you push it. Never end the turn while checks or bots are pending, because nobody will prompt you again; wait on the watcher.
6. **Check the merge gate** on the latest head. Every item must hold:
   - Your proof covers every change in the diff.
   - Council agreed on the current behavior diff, with no blocker or should open.
   - Required checks are green.
   - Review bots finished; each finding is fixed or dismissed with a written reason.
   - No human review requests changes.
   - The branch is up to date with trunk and GitHub reports it mergeable.

   "full stop": stop here, PR open and unmerged. If only a required human approval remains, say that is the blocker. "full send": merge, then confirm GitHub reports it merged (a queue or auto-merge request is not merged).
7. **Ask only when stuck.** Ask when you can't prove the change, the gate can't pass and you can't fix it, council is stuck on a blocker or should, the next step is outside the grant, the goal is ambiguous in a way that changes the result, or another PR makes this one obsolete. Use the harness's question tool so the thread shows it is waiting, with the PR link, the blocker and your recommended option first. No question tool: leave the PR open and unmerged, and open the reply with the question. Decide everything else with sensible defaults and list them.

**Reply:** the PR link, its final head, merged or open-and-unmerged, the merge commit if merged, your proof, council's outcome, each decision you made for the user, and remaining risks.
