# Encode lessons in structure

**Rule:** When the same instruction or correction comes up twice, encode it as a lint, check or script instead of more text.

If the lesson needs judgment and cannot be encoded, make the instruction more prominent and add an example of the failure mode.

**Corollary:** if the fix is structural, use only the structural fix. The instruction is the symptom.

**Feedback loop:**
- **Capture every correction.** When the human intervenes or tests fail, decide: one-off or pattern.
- **Route to the right layer.** One-off -> note in the mstack store (`~/.claude/mstack/<slug>/`) or repo `AGENTS.md`. Recurring -> skill or lint rule. Systemic -> principle.
- **Close the loop.** Apply now or create a concrete todo.

**Anti-patterns:**
- Acknowledging without recording ("I'll keep that in mind" does not persist).
- Recording without routing (a note that a lint rule should exist is wasted until the rule is built).
- Fixing one instance while leaving the recurring pattern intact.
