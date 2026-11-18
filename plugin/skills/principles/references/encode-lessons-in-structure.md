- Encode repeated corrections as a lint/check/script, not more text.
- If the fix is structural, only implement the structural fix.

Feedback loop:
- Capture every correction; decide: one-off, recurring, or systemic.
- Route: one-off -> ~/.claude/mstack/<slug>/ or AGENTS.md; recurring -> skill or lint rule; systemic -> principle.
- Close the loop: apply now or create a concrete todo.

Anti-patterns:
- Acknowledge without recording.
- Record without routing.
- Fix one instance while leaving the recurring pattern.
