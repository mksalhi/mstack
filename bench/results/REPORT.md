# Skill benchmark

## Static (origin/main → a0ef016)

| Metric | Before | After | Delta |
|---|---|---|---|
| scoper_hook_tokens | 1132 | 897 | -236 (-21%) |
| listing_chars | 5673 | 5570 | -103 (-2%) |
| desc_tokens | 2189 | 2149 | -40 (-2%) |
| skill_tokens_total | 55109 | 43704 | -11405 (-21%) |
| skill_tokens_median | 1430 | 1099 | -331 (-23%) |
| ref_tokens_total | 103521 | 63592 | -39929 (-39%) |
| files_at_depth>=2 | 40 | 11 | -29 (-72%) |
| orphan_files | 5 | 4 | -1 (-20%) |
| broken_links | 1 | 0 | -1 (-100%) |
| lint_failures | 1 | 0 | -1 (-100%) |
| shared_8grams | 280 | 285 | +5 (+2%) |

## Trigger accuracy

Share of runs where the model picked an accepted skill (or none, for queries no mstack skill should take).

| Model | Slice | Before | After | Delta |
|---|---|---|---|---|
| claude-sonnet-5-5 | all (n=116) | 100.0% | 99.4% | -0.6% |
| claude-sonnet-5-5 | positives (n=101) | 100.0% | 99.3% | -0.7% |
| claude-sonnet-5-5 | negatives (n=15) | 100.0% | 100.0% | +0.0% |
| claude-sonnet-5-5 | val (n=42) | 100.0% | 100.0% | +0.0% |
| claude-sonnet-5-5 | wrong mstack pick | 0.0% | 0.6% | +0.6% |
| claude-sonnet-5-5 | input tokens per call | 3702 | 3662 | -40 |
| gpt-6.2-sol | all (n=116) | 57.5% | 60.9% | +3.4% |
| gpt-6.2-sol | positives (n=101) | 54.8% | 59.7% | +5.0% |
| gpt-6.2-sol | negatives (n=15) | 75.6% | 68.9% | -6.7% |
| gpt-6.2-sol | val (n=42) | 56.3% | 57.9% | +1.6% |
| gpt-6.2-sol | wrong mstack pick | 3.2% | 3.4% | +0.3% |
| gpt-6.2-sol | input tokens per call | 2781 | 2759 | -22 |

## Task outcomes, claude-sonnet-5-5 (3 runs per task, judge claude-opus-5-5)

| | No skill | Old skill | New skill |
|---|---|---|---|
| Assertion pass rate | 65.8% ± 1.4% | 90.4% ± 0.4% | 91.1% ± 0.6% |
| Every assertion passed | 30.6% | 63.9% | 66.7% |
| Input tokens per task | 248 | 3949 | 3028 |
| Output tokens per task | 1241 | 1468 | 1408 |
| Skill files read | 0.0 | 0.3 | 0.2 |

| Task | No skill | Old | New |
|---|---|---|---|
| unslop-readme | 76% | 81% | 76% |
| pr-body | 41% | 100% | 100% |
| test-audit | 100% | 100% | 100% |
| pr-comments | 100% | 100% | 100% |
| debug-flaky | 42% | 100% | 100% |
| grill-plan | 58% | 67% | 75% |
| handoff-write | 90% | 100% | 100% |
| decision-log | 25% | 100% | 100% |
| scoper-cache | 50% | 100% | 100% |
| swift-modernize | 100% | 67% | 67% |
| ketchup | 57% | 95% | 100% |
| blast-radius | 50% | 75% | 75% |

## Task outcomes, gpt-6.2-sol (3 runs per task, judge claude-opus-5-5)

| | No skill | Old skill | New skill |
|---|---|---|---|
| Assertion pass rate | 73.3% ± 1.8% | 93.8% ± 1.1% | 95.1% ± 1.0% |
| Every assertion passed | 25.0% | 69.4% | 77.8% |
| Input tokens per task | 170 | 2012 | 1614 |
| Output tokens per task | 279 | 369 | 370 |
| Skill files read | 0.0 | 0.1 | 0.1 |

| Task | No skill | Old | New |
|---|---|---|---|
| unslop-readme | 86% | 90% | 100% |
| pr-body | 44% | 100% | 100% |
| test-audit | 92% | 100% | 100% |
| pr-comments | 100% | 93% | 100% |
| debug-flaky | 83% | 100% | 100% |
| grill-plan | 75% | 75% | 83% |
| handoff-write | 90% | 100% | 100% |
| decision-log | 25% | 100% | 100% |
| scoper-cache | 92% | 100% | 100% |
| swift-modernize | 72% | 83% | 83% |
| ketchup | 62% | 100% | 100% |
| blast-radius | 58% | 83% | 75% |

