# Explainer Prompt Template

Fill in the placeholders.

---

Write an architectural explanation that leaves a senior engineer new to this area with a solid mental model, enough to start working in it confidently. Explorer agents traced different slices of the codebase in parallel.

## Original Question

> {QUESTION}

## Explorer Findings

{EXPLORER_FINDINGS_ALL}

## Instructions

- Merge overlapping findings into one picture; resolve contradictions by checking the code yourself.
- You have read-only access (Read, Grep, Glob) to verify details or fill gaps; don't re-explore from scratch.

## Output Format

Adapt to the question; drop sections that don't apply.

### Overview
1-2 paragraphs: what it is, what it does, why it exists. Enough to decide whether to keep reading.

### Key Concepts
Brief definitions of the types, services, or abstractions needed to follow the rest.

### How It Works
The longest section. Walk the flow: trigger, steps, where data goes, decision points. Prose, not pseudocode; name specific files and functions; code snippets only when essential. When components talk to each other or data moves through stages, add a mermaid diagram (sequence, flowchart, component graph) or ASCII art for simpler relationships; skip it if prose covers the flow.

### Where Things Live
Brief map of the files and directories needed to start working here.

### Gotchas
Non-obvious behavior, historical context, pitfalls. Skip if none.

## Communication Style

- Concrete: "the `UserService` calls `AuthClient.refresh()`", not "the service delegates to the client".
- Explain why complex things are complex; don't pad simple ones.
- Analogies only when they help.
- Acknowledge explorers' open questions and gaps.
