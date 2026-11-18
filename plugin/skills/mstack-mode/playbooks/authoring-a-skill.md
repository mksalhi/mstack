### Authoring or modifying a skill

**You own the skill's voice.**

1. Write under the `writing` skill, including its `agents.md` and `SKILL-MECHANICS.md`. Frontmatter fields: https://code.claude.com/docs/en/skills.
2. Validate: frontmatter has `name` and `description`, referenced files exist, cross-skill links resolve.
3. Add test cases if structural. Skip if subjective.
4. Run **Opening a PR**.

When in doubt, delete. Keep only prose that changes a decision. State the rule, and give a reason only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) per Encode lessons in structure. Delegate to other skills by path instead of restating them. A recurring uncaptured workflow → propose a new skill.

**Reply:** skill summary, key design decisions, validation notes.
