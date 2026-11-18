#!/usr/bin/env python3
"""Render bench/results/*.json as one Markdown report with before/after deltas."""
import glob, json, os, sys

d = sys.argv[1] if len(sys.argv) > 1 else "bench/results"
J = lambda p: json.load(open(os.path.join(d, p)))
out = ["# Skill benchmark", ""]


def row(name, a, b, fmt="{:.0f}", lower_better=True):
    delta = b - a
    pct = f" ({delta / a:+.0%})" if a else ""
    return f"| {name} | {fmt.format(a)} | {fmt.format(b)} | {fmt.format(delta) if delta < 0 else '+' + fmt.format(delta)}{pct} |"


if os.path.exists(os.path.join(d, "static-base.json")):
    a, b = J("static-base.json")["summary"], J("static-cand.json")["summary"]
    out += [f"## Static ({a['ref']} → {b['ref']})", "", "| Metric | Before | After | Delta |", "|---|---|---|---|"]
    for k in ["scoper_hook_tokens", "listing_chars", "desc_tokens", "skill_tokens_total", "skill_tokens_median", "ref_tokens_total",
              "files_at_depth>=2", "orphan_files", "broken_links", "lint_failures", "shared_8grams"]:
        out.append(row(k, a[k], b[k]))
    out.append("")

trig = sorted(glob.glob(os.path.join(d, "trigger-*-base.json")))
if trig:
    out += ["## Trigger accuracy", "", "Share of runs where the model picked an accepted skill (or none, for queries no mstack skill should take).", "",
            "| Model | Slice | Before | After | Delta |", "|---|---|---|---|---|"]
    for p in trig:
        m = os.path.basename(p)[len("trigger-"):-len("-base.json")]
        a, b = J(f"trigger-{m}-base.json")["summary"], J(f"trigger-{m}-cand.json")["summary"]
        for sl in ["all", "positives", "negatives", "val"]:
            out.append(f"| {m} | {sl} (n={a[sl]['n']}) | {a[sl]['accuracy']:.1%} | {b[sl]['accuracy']:.1%} | {b[sl]['accuracy'] - a[sl]['accuracy']:+.1%} |")
        out.append(f"| {m} | wrong mstack pick | {a['all']['wrong_mstack_pick']:.1%} | {b['all']['wrong_mstack_pick']:.1%} | {b['all']['wrong_mstack_pick'] - a['all']['wrong_mstack_pick']:+.1%} |")
        out.append(f"| {m} | input tokens per call | {a['system_prompt_tokens_per_call']:.0f} | {b['system_prompt_tokens_per_call']:.0f} | {b['system_prompt_tokens_per_call'] - a['system_prompt_tokens_per_call']:+.0f} |")
    out.append("")

for p in sorted(glob.glob(os.path.join(d, "tasks-*.json"))):
    s = json.load(open(p))["summary"]
    c = s["by_cond"]
    out += [f"## Task outcomes, {s['model']} ({s['runs']} runs per task, judge {s['judge']})", "",
            "| | No skill | Old skill | New skill |", "|---|---|---|---|",
            "| Assertion pass rate | " + " | ".join(f"{c[k]['score']:.1%} ± {c[k]['score_sd_over_runs']:.1%}" for k in ["none", "old", "new"]) + " |",
            "| Every assertion passed | " + " | ".join(f"{c[k]['all_pass_rate']:.1%}" for k in ["none", "old", "new"]) + " |",
            "| Input tokens per task | " + " | ".join(f"{c[k]['in_tokens']:.0f}" for k in ["none", "old", "new"]) + " |",
            "| Output tokens per task | " + " | ".join(f"{c[k]['out_tokens']:.0f}" for k in ["none", "old", "new"]) + " |",
            "| Skill files read | " + " | ".join(f"{c[k]['file_reads']:.1f}" for k in ["none", "old", "new"]) + " |",
            "", "| Task | No skill | Old | New |", "|---|---|---|---|"]
    out += [f"| {t} | {v['none']:.0%} | {v['old']:.0%} | {v['new']:.0%} |" for t, v in s["by_task"].items()]
    out.append("")
print("\n".join(out))
