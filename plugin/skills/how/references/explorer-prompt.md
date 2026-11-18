# Explorer Prompt Template

Fill in the placeholders.

---

Other explorers cover other slices of this subsystem in parallel. Go deep on your angle only.

## Question

> {QUESTION}

## Your Exploration Angle

{EXPLORATION_ANGLE}

## Output

### Components Found
Key types, services, classes, abstractions: name, file path, one-sentence role.

### Flow
Step by step: function/method, file, what it does, what it calls next, and the data passed between steps.

### Files Read
Every file you read.

### Boundaries
Where this subsystem connects to the rest of the codebase: inputs and outputs.

### Non-Obvious Things
Surprising, historically motivated, or easy-to-get-wrong behavior.

### Open Questions
What you couldn't fully trace. Be honest about gaps.
