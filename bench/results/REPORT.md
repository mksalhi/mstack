# Skill benchmark

## Static (origin/main → c1b557a)

| Metric | Before | After | Delta |
|---|---|---|---|
| scoper_hook_tokens | 1132 | 897 | -236 (-21%) |
| listing_chars | 5673 | 5570 | -103 (-2%) |
| desc_tokens | 2189 | 2149 | -40 (-2%) |
| skill_tokens_total | 55109 | 47667 | -7442 (-14%) |
| skill_tokens_median | 1430 | 1105 | -325 (-23%) |
| ref_tokens_total | 103521 | 105438 | +1917 (+2%) |
| files_at_depth>=2 | 40 | 39 | -1 (-2%) |
| orphan_files | 5 | 5 | +0 (+0%) |
| broken_links | 1 | 1 | +0 (+0%) |
| lint_failures | 1 | 0 | -1 (-100%) |
| shared_8grams | 280 | 289 | +9 (+3%) |

## Trigger accuracy

Share of runs where the model picked an accepted skill (or none, for queries no mstack skill should take).

| Model | Slice | Before | After | Delta |
|---|---|---|---|---|
| claude-sonnet-5-5 | all (n=116) | 99.4% | 99.1% | -0.3% |
| claude-sonnet-5-5 | positives (n=101) | 99.3% | 99.0% | -0.3% |
| claude-sonnet-5-5 | negatives (n=15) | 100.0% | 100.0% | +0.0% |
| claude-sonnet-5-5 | val (n=42) | 98.4% | 100.0% | +1.6% |
| claude-sonnet-5-5 | wrong mstack pick | 0.3% | 0.9% | +0.6% |
| claude-sonnet-5-5 | input tokens per call | 3702 | 3662 | -40 |
| gpt-6.2-sol | all (n=116) | 60.6% | 58.6% | -2.0% |
| gpt-6.2-sol | positives (n=101) | 58.7% | 56.8% | -2.0% |
| gpt-6.2-sol | negatives (n=15) | 73.3% | 71.1% | -2.2% |
| gpt-6.2-sol | val (n=42) | 57.9% | 54.0% | -4.0% |
| gpt-6.2-sol | wrong mstack pick | 3.4% | 3.4% | +0.0% |
| gpt-6.2-sol | input tokens per call | 2781 | 2759 | -22 |

## Task outcomes, claude-sonnet-5-5 (3 runs per task, judge claude-opus-5-5)

| | No skill | Old skill | New skill |
|---|---|---|---|
| Assertion pass rate | 65.8% ± 1.0% | 89.0% ± 0.4% | 92.1% ± 1.0% |
| Every assertion passed | 33.3% | 55.6% | 72.2% |
| Input tokens per task | 248 | 4059 | 3253 |
| Output tokens per task | 1190 | 1481 | 1439 |
| Skill files read | 0.0 | 0.4 | 0.2 |

| Task | No skill | Old | New |
|---|---|---|---|
| unslop-readme | 71% | 81% | 71% |
| pr-body | 44% | 100% | 100% |
| test-audit | 100% | 100% | 100% |
| pr-comments | 100% | 93% | 100% |
| debug-flaky | 42% | 100% | 100% |
| grill-plan | 50% | 67% | 75% |
| handoff-write | 100% | 100% | 100% |
| decision-log | 25% | 100% | 100% |
| scoper-cache | 50% | 100% | 100% |
| swift-modernize | 100% | 67% | 67% |
| ketchup | 57% | 86% | 100% |
| blast-radius | 50% | 75% | 92% |

## Task outcomes, gpt-6.2-sol (3 runs per task, judge claude-opus-5-5)

| | No skill | Old skill | New skill |
|---|---|---|---|
| Assertion pass rate | 70.2% ± 1.7% | 92.4% ± 0.0% | 93.1% ± 2.0% |
| Every assertion passed | 22.2% | 66.7% | 72.2% |
| Input tokens per task | 170 | 1820 | 1586 |
| Output tokens per task | 288 | 366 | 375 |
| Skill files read | 0.0 | 0.0 | 0.0 |

| Task | No skill | Old | New |
|---|---|---|---|
| unslop-readme | 81% | 100% | 100% |
| pr-body | 44% | 100% | 100% |
| test-audit | 92% | 100% | 100% |
| pr-comments | 100% | 100% | 100% |
| debug-flaky | 67% | 100% | 83% |
| grill-plan | 67% | 75% | 75% |
| handoff-write | 90% | 100% | 100% |
| decision-log | 25% | 100% | 100% |
| scoper-cache | 83% | 75% | 100% |
| swift-modernize | 78% | 83% | 83% |
| ketchup | 57% | 100% | 100% |
| blast-radius | 58% | 75% | 75% |

