# Skill benchmark

## Static (origin/main → c1b557a)

| Metric | Before | After | Delta |
|---|---|---|---|
| scoper_hook_tokens | 1132 | 897 | -236 (-21%) |
| listing_chars | 5673 | 5570 | -103 (-2%) |
| desc_tokens | 1319 | 1293 | -26 (-2%) |
| skill_tokens_total | 38569 | 33393 | -5176 (-13%) |
| skill_tokens_median | 1050 | 792 | -259 (-25%) |
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
| gpt-6.2-sol | all (n=116) | 59.2% | 58.6% | -0.6% |
| gpt-6.2-sol | positives (n=101) | 57.4% | 56.4% | -1.0% |
| gpt-6.2-sol | negatives (n=15) | 71.1% | 73.3% | +2.2% |
| gpt-6.2-sol | val (n=42) | 57.1% | 54.8% | -2.4% |
| gpt-6.2-sol | wrong mstack pick | 3.2% | 2.9% | -0.3% |
| gpt-6.2-sol | input tokens per call | 2781 | 2759 | -22 |

