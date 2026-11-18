### Eval

**You own the experiment design. Plan, blind, run, synthesize.**

**Blinding:**

- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in any directory, file, or prompt the candidate sees. Use project-shaped dir and slug names.
- The candidate prompt is an organic user request stating the goal, not the meta. Never mention other candidates.
- No chain-eliciting cues: never ask which skills, principles, or files they applied. Ask for design notes generally.
- The judge may know it is judging but sees outputs by sanitized label only, never model name.
- Comparing two variants: one judge scores both sets in one pass on one scale, blind to set.

**Steps:**

1. **Frame.** Name the variant under test and what counts as success. Write a 3-6 criterion rubric for the judge only.
2. **Set up sanitized environments.** One working dir per candidate with the variant in place, plus the context an organic task would have (project skeleton, skills it would naturally read).
3. **Author one organic prompt**, with no leakage of what is measured.
4. **Spawn N parallel candidates** on different models per `arena` Phase B, each in its own sanitized dir, same prompt.
5. **Spawn one blinded judge** on a different model family per `arena` Phase C, with the rubric.
6. **Verify the chain from transcripts, not self-report.** Read each candidate's transcript per `<mstack>/skills/mstack-mode/references/transcripts.md`; never glob ~/.claude/projects/*/. Grade chain-following from the files it actually opened plus code shape.
7. **Read every candidate output yourself** end to end and compare to the judge. Disagreement means model bias or an ambiguous rubric. Synthesize.

**Reply:** variant under test, rubric, per-candidate notes, judge's verdict, your synthesis, and whether to promote the variant.
