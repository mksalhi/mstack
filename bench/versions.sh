#!/usr/bin/env bash
# Score every skill version on the same tasks and queries, then chart the trend.
# Usage: bench/versions.sh REF1 REF2 ...   e.g. bench/versions.sh origin/main c1b557a a0ef016 HEAD
# Results land in bench/results/versions/. Needs ANTHROPIC_API_KEY or ANT_API_KEY, and OPENAI_API_KEY.
set -euo pipefail
[ $# -ge 1 ] || { echo "usage: $0 REF..." >&2; exit 2; }
cd "$(git rev-parse --show-toplevel)"
out=${BENCH_OUT:-bench/results/versions}; mkdir -p "$out"; rm -f "$out"/*.json
claude=${BENCH_CLAUDE:-claude-sonnet-5-5}; gpt=${BENCH_GPT:-gpt-5}; runs=${BENCH_RUNS:-3}
export OPENAI_REASONING_EFFORT=${OPENAI_REASONING_EFFORT:-low}
[ -z "${ANTHROPIC_API_KEY:-}" ] && [ -n "${ANT_API_KEY:-}" ] && export ANTHROPIC_API_KEY=$ANT_API_KEY
label() { echo "${1##*/}"; }
for r in "$@"; do python3 bench/static.py "$r" --exact --json "$out/static-$(label "$r").json" > /dev/null; done
refs=$(IFS=,; echo "$*")
for m in "$claude" "$gpt"; do
  ([ -n "${BENCH_NO_TRIGGER:-}" ] || for r in "$@"; do  # triggers run one ref at a time, alongside the task run
    python3 bench/trigger/run.py --ref "$r" --model "$m" --runs "$runs" --out "$out/trigger-$m-$(label "$r").json" > /dev/null
  done) & trig=$!
  python3 bench/tasks/run.py --model "$m" --refs "$refs" --runs "$runs" --workers "${BENCH_WORKERS:-12}" --out "$out/tasks-$m.json" > /dev/null
  wait "$trig"  # fail the run if any trigger pass failed
done
python3 bench/charts.py "$out" "$@"
