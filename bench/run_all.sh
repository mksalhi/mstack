#!/usr/bin/env bash
# Run every benchmark on a baseline ref and a candidate ref; results land in bench/results/.
# GPT only by default (OPENAI_API_KEY). BENCH_MODELS="claude-sonnet-5-5 gpt-6.2-sol" adds Claude rows (needs ANTHROPIC_API_KEY or ANT_API_KEY).
# Usage: bench/run_all.sh BASE_REF [CAND_REF]   e.g. bench/run_all.sh origin/main HEAD
set -euo pipefail
base=${1:?base ref}; cand=${2:-HEAD}
cd "$(git rev-parse --show-toplevel)"
out=bench/results; mkdir -p "$out"
rm -f "$out"/trigger-*.json "$out"/tasks-*.json  # never mix in another run's refs or models
models=${BENCH_MODELS:-gpt-6.2-sol}; judge=${BENCH_JUDGE:-gpt-6.2-sol}; runs=${BENCH_RUNS:-3}
export OPENAI_REASONING_EFFORT=${OPENAI_REASONING_EFFORT:-low}
[ -z "${ANTHROPIC_API_KEY:-}" ] && [ -n "${ANT_API_KEY:-}" ] && export ANTHROPIC_API_KEY=$ANT_API_KEY
exact=""; [ -n "${ANTHROPIC_API_KEY:-}" ] && exact=--exact
python3 bench/static.py "$base" $exact --json "$out/static-base.json"
python3 bench/static.py "$cand" $exact --json "$out/static-cand.json"
for m in $models; do
  for r in base cand; do ref=$([ $r = base ] && echo "$base" || echo "$cand")
    python3 bench/trigger/run.py --ref "$ref" --model "$m" --runs "$runs" --out "$out/trigger-$m-$r.json" > /dev/null
  done
  python3 bench/tasks/run.py --model "$m" --base "$base" --cand "$cand" --runs "$runs" --judge "$judge" --out "$out/tasks-$m.json" > /dev/null
done
python3 bench/report.py "$out" > "$out/REPORT.md"
cat "$out/REPORT.md"
