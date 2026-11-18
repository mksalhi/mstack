#!/usr/bin/env bash
# Run every benchmark on a baseline ref and a candidate ref; results land in bench/results/.
# Needs ANTHROPIC_API_KEY (and OPENAI_API_KEY for the GPT rows).
# Usage: bench/run_all.sh BASE_REF [CAND_REF]   e.g. bench/run_all.sh origin/main HEAD
set -euo pipefail
base=${1:?base ref}; cand=${2:-HEAD}
cd "$(git rev-parse --show-toplevel)"
out=bench/results; mkdir -p "$out"
claude=${BENCH_CLAUDE:-claude-sonnet-5-5}; gpt=${BENCH_GPT:-gpt-5}; runs=${BENCH_RUNS:-3}
export OPENAI_REASONING_EFFORT=${OPENAI_REASONING_EFFORT:-low}
exact=""; [ -n "${ANTHROPIC_API_KEY:-}" ] && exact=--exact
python3 bench/static.py "$base" $exact --json "$out/static-base.json"
python3 bench/static.py "$cand" $exact --json "$out/static-cand.json"
for m in "$claude" "$gpt"; do
  for r in base cand; do ref=$([ $r = base ] && echo "$base" || echo "$cand")
    python3 bench/trigger/run.py --ref "$ref" --model "$m" --runs "$runs" --out "$out/trigger-$m-$r.json" > /dev/null
  done
  python3 bench/tasks/run.py --model "$m" --base "$base" --cand "$cand" --runs "$runs" --out "$out/tasks-$m.json" > /dev/null
done
python3 bench/report.py "$out" > "$out/REPORT.md"
cat "$out/REPORT.md"
