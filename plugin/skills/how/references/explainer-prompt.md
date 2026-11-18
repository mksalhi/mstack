## Original Question
> {QUESTION}

## Explorer Findings
{EXPLORER_FINDINGS_ALL}

## Instructions
- Merge overlapping findings into one model; resolve contradictions by checking the code yourself.
- You have read-only access (Read, Grep, Glob) to verify or fill gaps; don't re-explore from scratch.
- Adapt to the question; omit sections that don't apply.

### Overview
1–2 paragraphs: what it is/does and why.

### How It Works
Primary section: walk triggers, steps, data paths, decisions. Only include code snippets if essential. Use a mermaid or ASCII diagram for inter-component or data flows; skip if prose suffices.

### Where Things Live
Brief map of files/directories to work in.

### Gotchas
Non-obvious behavior or pitfalls; skip if none.

## Style
- Be concrete (e.g., the `UserService` calls `AuthClient.refresh()`); name specific files/functions.
- Explain why complex parts are complex.
- Acknowledge explorers' open questions and gaps.
