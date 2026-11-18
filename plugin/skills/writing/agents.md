# Writing for agents

For any document an agent consumes: a skill, an `AGENTS.md` / `CLAUDE.md`, a doc reached by a pointer. Packaging differs; the writing does not. The goal is predictability: the agent takes the same _process_ every run, not the same output.

For a skill, also read [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md) (invocation choice, router skills).

## Context pointers

A **context pointer** is an in-context reference naming out-of-context material and the condition for reaching it: a skill description, or an `AGENTS.md` line naming a doc. The pointer's _wording_, not its target, decides when and how reliably the agent reaches it. A must-have target behind a weak pointer is a variance bug: sharpen the wording first; inline the material only if that fails.

A pointer states what the material is and lists the **branches** that trigger it (a branch is a distinct case the document handles). Always-loaded words cost every turn, so prune pointers harder than bodies:
- **Front-load the leading word**; the pointer is where it triggers.
- **One trigger per branch.** Synonyms renaming one branch collapse to one.
- **Cut identity the body already carries.**

## The two loads

- **Context load:** always-loaded material (an `AGENTS.md` line, a skill description) spends tokens and attention every turn, fired or not.
- **Cognitive load:** the human as index, remembering which documents exist and when to use each. It is the price of human agency: spend it where human judgement matters, remove it elsewhere.

Material behind a pointer costs only the pointer's line of context load; material with no pointer rides entirely on cognitive load.

## Information hierarchy

Content is **steps** (ordered actions) and **reference** (definitions, rules, facts consulted on demand), mixed freely. Place each piece on the **information hierarchy**, ranked by how immediately the agent needs it:

1. **In-file step:** what the agent does, in order.
2. **In-file reference:** consulted on demand. A flat peer-set (every review rule on one rung) is fine.
3. **Disclosed reference:** in a separate file behind a context pointer, loaded only when it fires; from a sibling file to fully external reference any document can point at.

Push too little down and the top bloats; too much and you hide what the agent needs.

**Progressive disclosure** moves material down the ladder to keep the top legible; it protects the hierarchy more than it saves tokens. Test by branching: inline what every branch needs, disclose what only some reach. Undisclosed reference that buries steps makes attending to them a coin-flip, a variance lever.

**Co-location:** keep a concept's definition, rules, and caveats under one heading so reading one part brings its neighbours. The document should read like documentation written for the agent. (Scattering fragments one meaning across places; duplication repeats it.)

**Sprawl:** a document too long even when every line is live and unique; attention thins. Cure: disclose reference behind pointers, split by branch or sequence.

## Steps and completion criteria

Every step ends on a **completion criterion** telling the agent the work is done.

- **Clarity:** can the agent tell done from not-done? A vague bound ("understanding reached") invites **premature completion**, pulled by the visible **post-completion steps**. Defend in order: **sharpen the bound first**; only if it is irreducibly fuzzy _and_ you observe the rush, hide later steps by splitting the sequence. Hiding works only across a real context boundary (hand-off or subagent dispatch; an inline call clears nothing).
- **Demand:** how much it requires. "Every modified model accounted for" forces thoroughness that "produce a change list" doesn't. Demand drives **legwork** (digging latent in the wording, not written as a step) and binds reference too: "every rule applied" gives an all-reference document an exhaustiveness bar.

The strongest criteria are checkable and exhaustive.

## When to split

Splitting spends one of the two loads; split only when the cut earns it:
- **By sequence:** when post-completion steps tempt the agent to rush the current one; hiding them drives more legwork. Merging sequences does the reverse.
- **By invocation**, skill-specific: see [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md).

## Leading words

A **leading word** is a compact pretrained concept the agent thinks with (_lesson_, _fog of war_, _tracer bullets_). Repeated as a token, never as a sentence, it anchors a region of behaviour in the fewest tokens by recruiting existing priors. A coined word recruits none and must be paid for in definition tokens: reach for an existing word first.

It anchors _execution_ in the body (same behaviour wherever the word appears; in flat reference, a class of thing to look for) and _invocation_ in a pointer (shared language across prompts, docs, and codebase makes reaching it more reliable).

Hunt restatements to collapse into one token: a triad spelled out at three sites, a pointer spending a sentence on one idea.
- "fast, deterministic, low-overhead" → _tight_ (a _tight_ loop).
- "a loop you believe in" → _red_, a binary observable state (the loop goes _red_ on the bug, or doesn't).

**Negation** backfires: a prohibition puts the forbidden behaviour in context and makes it _more_ available. Prompt the **positive** target ("write one-line comments"). Use a prohibition only as a hard guardrail you cannot phrase positively, and pair it with the positive target.

## Pruning

- **Single source of truth:** one authoritative place per meaning, so a behaviour change is a one-place edit. **Duplication** costs maintenance and tokens and inflates the meaning's rank. (A leading word repeats a token on purpose, never the meaning.)
- The **environment** (`package.json` scripts, config files, directory layout, `--help` output) is a source of truth; restating it is a **cache**, worth its load only when the lookup is expensive. Cache what looking can't find: unwritten conventions, the reason behind a choice, gotchas no config confesses.
- Check every line for **relevance**: lines lose it by never bearing on the task (exposition, or a branch to disclose) or by going stale. Without pruning, **sediment** settles: stale layers kept because adding feels safe and removing risky.
- Hunt **no-ops** sentence by sentence: instructions the model already follows by default. The test (does it change behaviour versus the default?) is model-relative; settle disagreements by running the document. Delete the whole failing sentence, don't trim it. A leading word too weak to beat the default (_be thorough_) is a no-op; fix with a stronger word (_relentless_).
