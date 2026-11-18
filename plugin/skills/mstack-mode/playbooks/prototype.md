### Prototype

**You own the design decision, not the code. The prototype is throwaway; the real build follows Feature.** Scoper's smallest change and the verification bar invert here: speed over polish, code quality irrelevant, no planning. Propose variations the user didn't ask for; throw approaches away freely.

1. Scope the decision: which layout, interaction, density, or for an empirical fork which behavior, timing, or approach. No decision means no prototype; route to Feature.
2. Open design space: gather prior art, summarize a moodboard of themes, palettes, and layouts, and let the user pick directions before building. Skip when the direction is set.
3. Build throwaway in an isolated scratch dir outside production source. Visual: vanilla HTML/CSS/JS or the lightest stack that renders it, CDN deps, hot-reload dev server. Behavioral or timing: the smallest script that exercises the question. No production framework, tests, or abstractions.
4. Compare alternatives behind one labeled switcher (buttons or a keypress). For a component inside an existing app, follow the `ui` skill's prototype area (`<mstack>/skills/ui/references/prototype/index.md`), which builds them into the real page behind its picker (Exhaust the design space).
5. Verify on the matching surface. Visual: screenshot each variant via the control skill and drive the interaction. Behavioral: observe the thing decided (log timing, print output, watch the render). The observation is the test.
6. Present alternatives, tradeoffs, and a recommendation. Hand the chosen direction to **Feature** (or `architect` for the shape).

**Reply:** variants explored, the evidence (screenshots, or observed output or timing), tradeoffs, recommendation, scratch path. Say plainly the prototype is throwaway.
