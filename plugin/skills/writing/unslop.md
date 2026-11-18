# Unslop

Scan the text for the patterns below, then rewrite. Preserve meaning and intended tone.

## Patterns to detect and fix

Rule numbers are stable ids other skills cite. A removed rule leaves a gap.

### Content

3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.

### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Use plain words.
8. **Fancy "is".** "serves as", "stands as", "boasts", "features". Say "is" or "has".
9. **"Not just X, but Y."** State the point directly.
10. **Rule of three.** Use the natural number, not forced triads.
11. **Synonym cycling.** Protagonist, main character, central figure, hero in one paragraph. Pick one, repeat it.
12. **False ranges.** "from X to Y" without a meaningful scale. List topics directly.

### Style

13. **Em dashes.** Never. End the sentence or use a comma (no parentheses, en dashes, or hyphen-as-dash instead).
14. **Colon overuse.** Colons go before a list or example, not as mid-sentence connectors. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" becomes "Describing when the scheduler should fire works best as plain English": the point stands alone, no comparison framing.
15. **Boldface overuse.** Don't bold every proper noun or acronym.
16. **Inline-header lists.** A bold label and colon restating the line ("**Performance:** Performance improved...") becomes prose. A bold lead-in ending in a period, naming the item, followed by new detail ("**Schema in TypeScript.** Tables live in one file.") is fine.
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Remove from headings and bullets.
19. **Curly quotes.** Use straight quotes.

### Communication artifacts

20. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove.
22. **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly.

### Filler

23. **Filler phrases.** "In order to" becomes "To"; "Due to the fact that" becomes "Because"; delete "It is important to note that".
24. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
25. **Generic conclusions.** "The future looks bright." State specific plans or facts.

### Jargon

26. **Abstract metaphor nouns.** Substrate (base), wedge, wedge in (add), vector (way, method), locus, vantage, nexus, primitive as a noun, harness as a metaphor, surface as in "API surface", bedrock, scaffolding as a metaphor, modality, paradigm, gold-plating (more than the job needs), ratchet as a metaphor (the mechanism's real name, or a limit that only tightens), evacuate for moving code (move out), endgame (the last phase), north star, flywheel. Pick the concrete word.

### Plain speech

27. **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read" name a feeling; name the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". If a sentence can't be restated as a concrete instruction, fact, or number, or could appear unchanged in another project's docs, cut it.
28. **Dense sentences.** If the reader must backtrack, split it or drop clauses. One idea per sentence.
29. **Active voice.** Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries". Passive only when the actor is unknown or irrelevant.
30. **Adverbs.** Cut, or use a stronger verb or the number: "runs quickly" becomes "is fast"; "significantly improves" becomes the measured delta.
31. **Plain word.** "utilize"/"leverage" become "use", "facilitate" "help", "numerous" "many", "in the event that" "if".
32. **Mannered prose.** Flourish where a literal phrase exists: aphorisms ("wire it or delete it"), rhetorical fragments, personified code ("the plan holds it"), figurative verbs ("rides along", "stands on"), stock framing. "A dial worth turning" becomes "a parameter worth varying". Rule 26 covers metaphor nouns.
33. **Over-compression.** Dropped articles, verbless fragments, symbol-speak, and abbreviations that make the reader decode. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing." Write whole sentences; spell out arrows and abbreviations.
