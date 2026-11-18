### Authoring or modifying a skill

**You own the skill's voice.**

1. Before writing, run the task without the skill and note where the agent goes wrong; the skill exists to fix those misses, not to restate what the agent already does.
2. Write under the `writing` skill, including its `agents.md`. Frontmatter fields: https://code.claude.com/docs/en/skills.
3. Validate: frontmatter has `name` and `description`, referenced files exist, cross-skill links resolve.
4. Check triggering: 8-10 prompts that should fire it (some never naming the skill's domain) and 8-10 near-misses that share its words but need something else. Rerun the misses after each description change.
5. For a behaviour-shaping change, compare task results with no skill, the old skill and the new one (the **Eval** playbook).
6. Run **Opening a PR**.

When in doubt, delete. Keep only prose that changes a decision. State the rule, and give a reason only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) per Encode lessons in structure. Delegate to other skills by path instead of restating them. A recurring uncaptured workflow → propose a new skill.

**Reply:** skill summary, key design decisions, validation notes.
