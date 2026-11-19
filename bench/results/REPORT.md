# Skill benchmark

## Static (origin/main → HEAD)

| Metric | Before | After | Delta |
|---|---|---|---|
| scoper_hook_tokens | 576 | 607 | +32 (+6%) |
| listing_chars | 5414 | 5018 | -396 (-7%) |
| desc_tokens | 1262 | 1170 | -92 (-7%) |
| skill_tokens_total | 22127 | 21150 | -978 (-4%) |
| skill_tokens_median | 529 | 530 | +1 (+0%) |
| ref_tokens_total | 52018 | 52425 | +406 (+1%) |
| files_at_depth>=2 | 11 | 11 | +0 (+0%) |
| orphan_files | 2 | 2 | +0 (+0%) |
| broken_links | 0 | 0 | +0 |
| lint_failures | 0 | 0 | +0 |
| shared_8grams | 194 | 185 | -9 (-5%) |

## Trigger accuracy

Share of runs where the model picked an accepted skill (or none, for queries no mstack skill should take).

| Model | Slice | Before | After | Delta |
|---|---|---|---|---|
| gpt-6.2-sol | all (n=108) | 63.3% | 63.0% | -0.3% |
| gpt-6.2-sol | positives (n=93) | 61.6% | 61.6% | +0.0% |
| gpt-6.2-sol | negatives (n=15) | 73.3% | 71.1% | -2.2% |
| gpt-6.2-sol | val (n=40) | 60.8% | 57.5% | -3.3% |
| gpt-6.2-sol | wrong mstack pick | 4.0% | 3.4% | -0.6% |
| gpt-6.2-sol | input tokens per call | 2639 | 2511 | -128 |

## Task outcomes, gpt-6.2-sol (3 runs per task, judge gpt-6.2-sol)

| | No skill | Old skill | New skill |
|---|---|---|---|
| Assertion pass rate | 58.5% ± 0.8% | 87.5% ± 0.9% | 86.6% ± 0.9% |
| Every assertion passed | 15.4% | 60.7% | 57.3% |
| Input tokens per task | 139 | 2078 | 2285 |
| Output tokens per task | 462 | 625 | 627 |
| Skill files read | 0.0 | 0.8 | 0.9 |

| Task | No skill | Old | New |
|---|---|---|---|
| unslop-readme | 71% | 95% | 90% |
| pr-body | 44% | 100% | 100% |
| test-audit | 83% | 100% | 100% |
| pr-comments | 100% | 100% | 100% |
| debug-flaky | 67% | 83% | 75% |
| handoff-write | 95% | 100% | 100% |
| decision-log | 25% | 100% | 100% |
| scoper-cache | 75% | 75% | 75% |
| swift-modernize | 78% | 83% | 83% |
| ketchup | 67% | 95% | 100% |
| blast-radius | 67% | 75% | 75% |
| ui-a11y-review | 83% | 100% | 100% |
| ui-copy | 93% | 87% | 60% |
| principles-types | 80% | 80% | 80% |
| architect-sketch | 40% | 80% | 67% |
| how-explain | 93% | 100% | 87% |
| mstack-reply | 83% | 100% | 94% |
| formal-choose | 40% | 87% | 80% |
| playwright-script | 87% | 53% | 53% |
| motion-brief | 0% | 100% | 100% |
| arena-frame | 50% | 92% | 100% |
| automate-me-draft | 17% | 89% | 83% |
| figure-it-out-migration | 42% | 100% | 100% |
| interrogate-synthesize | 52% | 100% | 100% |
| principles-shared-state | 67% | 89% | 89% |
| principles-new-requirement | 0% | 67% | 44% |
| retro-session | 83% | 100% | 100% |
| setup-mstack-mixed | 0% | 100% | 100% |
| swarm-perf | 33% | 100% | 100% |
| verifier-create | 29% | 100% | 100% |
| why-timeout | 58% | 100% | 100% |
| scoper-review | 40% | 60% | 67% |
| council-round | 62% | 100% | 100% |
| takeover-modernize | 80% | 100% | 100% |
| ambition-estimate | 33% | 33% | 100% |
| ambition-game | 100% | 89% | 78% |
| ambition-rewrite | 25% | 33% | 50% |
| ambition-overnight | 40% | 67% | 47% |
| ambition-scope | 100% | 100% | 100% |

