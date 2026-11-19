# Sources

- Monperrus, "Coding agents have a completely wrong sense of time": agents quote human-scale durations; pre-task estimates overshoot 4 to 7x; a concrete unit (tool calls, files) beats "you are fast". https://www.monperrus.net/martin/coding-agents-sense-of-time
- Anthropic, "Measuring AI agent autonomy in practice": models "are capable of more autonomy than they exercise"; on complex tasks Claude Code stops to ask over twice as often as humans interrupt. https://www.anthropic.com/research/measuring-agent-autonomy
- Anthropic prompting best practices: ask explicitly for a fully featured result; `default_to_action`; soften CAPS wording, which overtriggers on current models. https://platform.claude.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices
- OpenAI GPT-5 prompting guide: persistence block, don't ask the user to confirm assumptions. https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- Kaddour et al., "Agentic Uncertainty Reveals Agentic Overconfidence": agents overrate their success; reframing self-review as bug-finding improves calibration. https://www.arxiv.org/pdf/2602.06948
- Digital Applied, "Define done, not effort": give the agent a check it runs and a done predicate. https://www.digitalapplied.com/blog/define-done-acceptance-criteria-agent-prompts-2026
- Hacker News thread on why LLMs overestimate implementation time (anecdotal). https://news.ycombinator.com/item?id=48230861
