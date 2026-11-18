#!/usr/bin/env python3
"""Chart a stack comparison (bench/compare/run.py) and write COMPARE.md next to the PNGs.

Usage: python3 bench/compare/charts.py RESULTS_DIR
Error bars and ± are the standard deviation of the per-run means across repeated runs.
"""
import glob, json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = sys.argv[1]
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SERIES = ["#2a78d6", "#eb6834"]  # fixed order: model 1, model 2
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10,
                     "lines.markersize": 8, "legend.frameon": False})
res = {json.load(open(p))["summary"]["model"]: json.load(open(p)) for p in sorted(glob.glob(os.path.join(d, "compare-*.json")))}
models = list(res)
color = {m: SERIES[i] for i, m in enumerate(models)}
first = next(iter(res.values()))["summary"]
stacks = sorted(first["by_stack"], key=lambda s: (s != "none", -sum(res[m]["summary"]["by_stack"][s]["score"] for m in models)))
md = ["# Skill stacks compared", "",
      f"{first['tasks']} stack-neutral tasks, {first['runs']} runs per cell, judge `{first['judge']}`. Each agent sees one stack's skill "
      "listing, chooses whether and which skill to load, and may read the stack's files. \"none\" has no skills. "
      "Error bars and ± are the standard deviation across runs.", ""]


def save(fig, name, alt):
    fig.tight_layout()
    fig.savefig(os.path.join(d, name), dpi=160, bbox_inches="tight")
    plt.close(fig)
    md.extend([f"![{alt}]({name})", ""])


fig, ax = plt.subplots(figsize=(8.5, 4.2))
w = 0.8 / len(models)
for i, m in enumerate(models):
    bs = res[m]["summary"]["by_stack"]
    xs = [k + (i - (len(models) - 1) / 2) * w for k in range(len(stacks))]
    ax.bar(xs, [bs[s]["score"] * 100 for s in stacks], w * 0.92, yerr=[bs[s]["score_sd_over_runs"] * 100 for s in stacks],
           capsize=3, color=color[m], label=m, error_kw={"ecolor": MUTED, "lw": 1})
ax.set_xticks(range(len(stacks)), stacks, rotation=15)
ax.set_ylim(0, 100); ax.set_ylabel("assertion pass rate, %")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.06), ncol=len(models))
ax.set_title("Task score by skill stack", loc="left")
save(fig, "compare_score.png", "Task score by stack")

fig, ax = plt.subplots(figsize=(8.5, 4.6))
for m in models:
    bs = res[m]["summary"]["by_stack"]
    ax.scatter([bs[s]["in_tokens"] for s in stacks], [bs[s]["score"] * 100 for s in stacks], color=color[m], label=m, zorder=3)
    for s in stacks:
        ax.annotate(s, (bs[s]["in_tokens"], bs[s]["score"] * 100), textcoords="offset points", xytext=(5, 4), fontsize=8, color=MUTED)
ax.set_xscale("symlog", linthresh=500); ax.set_xlabel("input tokens per task"); ax.set_ylabel("assertion pass rate, %")
ax.set_title("Score against token cost", loc="left"); ax.legend(loc="center left")
save(fig, "compare_cost.png", "Score against token cost")

for m in models:
    bt = res[m]["summary"]["by_task"]
    names = list(bt)
    grid = [[bt[n][s] if bt[n][s] is not None else float("nan") for s in stacks] for n in names]
    fig, ax = plt.subplots(figsize=(1.25 * len(stacks) + 2.8, 0.3 * len(names) + 1.4))
    ax.imshow(grid, cmap="Blues", vmin=0, vmax=1, aspect="auto"); ax.grid(False)
    ax.set_xticks(range(len(stacks)), stacks, rotation=20, ha="left"); ax.set_yticks(range(len(names)), names, fontsize=8)
    ax.xaxis.tick_top()
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if v == v:
                ax.text(j, i, f"{v:.0%}", ha="center", va="center", fontsize=7, color="white" if v > .6 else INK)
    ax.set_title(f"Per-task pass rate, {m}", loc="left", pad=40)
    save(fig, f"compare_heatmap-{m}.png", f"Per-task heatmap {m}")

md += ["| Stack | skills | " + " | ".join(f"{m} score | {m} all pass | {m} tokens | {m} loaded a skill" for m in models) + " |",
       "|---|---|" + "---|---|---|---|" * len(models)]
for s in stacks:
    cells = []
    for m in models:
        b = res[m]["summary"]["by_stack"][s]
        cells.append(f"{b['score']:.1%} ± {b['score_sd_over_runs']:.1%} | {b['all_pass_rate']:.1%} | {b['in_tokens']:.0f} | {b['load_rate']:.0%}")
    md.append(f"| {s} | {first['stacks'][s]['skills']} | " + " | ".join(cells) + " |")
md += ["", "Dropped jobs (API or judge failure after a retry): " + ", ".join(f"{m} {res[m]['summary']['errors']}" for m in models) + ".", ""]
open(os.path.join(d, "COMPARE.md"), "w").write("\n".join(md))
print("\n".join(md))
