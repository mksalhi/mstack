Blinding:
- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in any directory, file, or prompt the candidate sees. Use project-shaped dir and slug names.
- Organic user prompt stating the goal; never mention other candidates.
- No chain-eliciting cues; don’t ask which skills/principles/files.
- Judge sees sanitized labels only, never model names.
- Comparing variants: one judge, one pass, blind.

1) Frame: name variant + success; 3–6-criterion rubric for judge only.
2) One sanitized working dir per candidate with variant.
3) Spawn N candidates on different models; same prompt; isolated dirs.
4) One blinded judge from a different model family, with rubric.
5) Verify via transcripts, not self-report: read per `<mstack>/skills/mstack-mode/references/transcripts.md`; never glob ~/.claude/projects/*/; grade from opened files + code shape.
6) Read all outputs; compare to judge; disagreement => bias or ambiguous rubric; synthesize.

Reply: variant, rubric, per-candidate notes, judge’s verdict, synthesis, promote?
