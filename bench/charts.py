#!/usr/bin/env python3
"""Chart a multi-version run (bench/versions.sh) and write VERSIONS.md next to the PNGs.

Usage: python3 bench/charts.py RESULTS_DIR REF1 REF2 ...   (refs in chronological order)
Error bars are the standard deviation of the per-run means across the repeated runs.
"""
import glob, json, os, statistics, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d, refs = sys.argv[1], sys.argv[2:]
labels = [r.split("/")[-1] for r in refs]
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]  # fixed categorical order: model 1, model 2, ...
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10,
                     "lines.linewidth": 2, "lines.markersize": 8, "legend.frameon": False})
J = lambda p: json.load(open(os.path.join(d, p)))
tasks = {json.load(open(p))["summary"]["model"]: json.load(open(p)) for p in sorted(glob.glob(os.path.join(d, "tasks-*.json")))}
models = list(tasks)
color = {m: SERIES[i] for i, m in enumerate(models)}
md = ["# Skill benchmark across versions", "",
      f"Versions, oldest first: {', '.join(f'`{l}`' for l in labels)}. Every version is scored on the same tasks and trigger queries. "
      "\"none\" is the same task with no skill loaded. Error bars and ± are the standard deviation across repeated runs.", ""]


def per_run(rows, key, runs):
    """Mean of key per run index, then mean and sd across runs."""
    means = [statistics.mean(r[key] for r in rows if r["run"] == k) for k in range(runs) if any(r["run"] == k for r in rows)]
    return statistics.mean(means), (statistics.pstdev(means) if len(means) > 1 else 0.0)


def save(fig, name, alt):
    fig.tight_layout()
    fig.savefig(os.path.join(d, name), dpi=160, bbox_inches="tight")
    plt.close(fig)
    md.extend([f"![{alt}]({name})", ""])


# Task outcomes: score and all-pass by version, one line per model, no-skill as a dashed reference.
stats = {}
for m, t in tasks.items():
    runs = t["summary"]["runs"]
    for c in ["none"] + refs:
        rs = [r for r in t["rows"] if r["cond"] == c]
        stats[m, c] = {"score": per_run(rs, "score", runs), "all": per_run(rs, "all_pass", runs),
                       "in": statistics.mean(r["usage"]["in"] for r in rs), "out": statistics.mean(r["usage"]["out"] for r in rs)}
if tasks:
    n_tasks = len(next(iter(tasks.values()))["summary"]["by_task"])
    md += ["## Task outcomes", "", f"{n_tasks} tasks, {next(iter(tasks.values()))['summary']['runs']} runs per cell, "
           f"graded by regex checks plus judge `{next(iter(tasks.values()))['summary']['judge']}`.", ""]
    for key, title, fname in [("score", "Assertion pass rate", "task_score.png"), ("all", "Tasks with every assertion passed", "task_all_pass.png")]:
        fig, ax = plt.subplots(figsize=(7.5, 4.2))
        for i, m in enumerate(models):
            ys = [stats[m, c][key] for c in refs]
            ax.errorbar(labels, [y[0] * 100 for y in ys], yerr=[y[1] * 100 for y in ys], color=color[m], marker="o", capsize=4, label=m)
            ax.axhline(stats[m, "none"][key][0] * 100, color=color[m], ls="--", lw=1.2, alpha=.7)
            ax.annotate(f"{m} no skill", (len(refs) - 1, stats[m, "none"][key][0] * 100), textcoords="offset points", xytext=(0, 4 if i % 2 else -12),
                        ha="right", fontsize=8, color=MUTED)
        ax.set_ylim(0, 102); ax.set_ylabel("%"); ax.set_title(title, loc="left")
        ax.legend(loc="lower left")
        save(fig, fname, title)
    md += ["| Model | none | " + " | ".join(labels) + " |", "|---|---|" + "---|" * len(labels)]
    for key, name in [("score", "pass rate"), ("all", "all pass")]:
        for m in models:
            md.append(f"| {m} {name} | " + " | ".join(f"{stats[m, c][key][0]:.1%} ± {stats[m, c][key][1]:.1%}" for c in ["none"] + refs) + " |")
    for m in models:
        md.append(f"| {m} input tokens | " + " | ".join(f"{stats[m, c]['in']:.0f}" for c in ["none"] + refs) + " |")
    errs = {m: t["summary"].get("errors", 0) for m, t in tasks.items()}
    md += ["", "Dropped jobs (API or judge failure after a retry): " + ", ".join(f"{m} {n}" for m, n in errs.items()) + ".", ""]

    # Input tokens per task by version.
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    w = 0.8 / len(models)
    for i, m in enumerate(models):
        xs = [k + (i - (len(models) - 1) / 2) * w for k in range(len(refs))]
        ax.bar(xs, [stats[m, c]["in"] for c in refs], w * 0.92, color=color[m], label=m)
    ax.set_xticks(range(len(refs)), labels); ax.set_ylabel("input tokens per task"); ax.legend()
    ax.set_title("Input tokens per task (skill body plus files read)", loc="left")
    save(fig, "task_tokens.png", "Input tokens per task")

    # Per-task heatmap per model.
    for m, t in tasks.items():
        bt = t["summary"]["by_task"]
        names = list(bt)
        cols = ["none"] + refs
        grid = [[(bt[n][c] if bt[n][c] is not None else float("nan")) for c in cols] for n in names]
        fig, ax = plt.subplots(figsize=(1.3 * len(cols) + 2.5, 0.28 * len(names) + 1.2))
        ax.imshow(grid, cmap="Blues", vmin=0, vmax=1, aspect="auto")
        ax.grid(False)
        ax.set_xticks(range(len(cols)), ["none"] + labels); ax.set_yticks(range(len(names)), names, fontsize=8)
        ax.xaxis.tick_top()
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                if v == v:
                    ax.text(j, i, f"{v:.0%}", ha="center", va="center", fontsize=7, color="white" if v > .6 else INK)
        ax.set_title(f"Per-task pass rate, {m}", loc="left", pad=24)
        save(fig, f"task_heatmap-{m}.png", f"Per-task heatmap {m}")

    # Change per task, latest version vs first version.
    if len(refs) > 1:
        names = list(next(iter(tasks.values()))["summary"]["by_task"])
        delta = {m: [(tasks[m]["summary"]["by_task"][n][refs[-1]] or 0) - (tasks[m]["summary"]["by_task"][n][refs[0]] or 0) for n in names] for m in models}
        order = sorted(range(len(names)), key=lambda i: sum(delta[m][i] for m in models))
        fig, ax = plt.subplots(figsize=(7.5, 0.3 * len(names) + 1.2))
        h = 0.8 / len(models)
        for i, m in enumerate(models):
            ax.barh([k + (i - (len(models) - 1) / 2) * h for k in range(len(names))], [delta[m][j] * 100 for j in order], h * 0.9, color=color[m], label=m)
        ax.set_yticks(range(len(names)), [names[j] for j in order], fontsize=8)
        ax.axvline(0, color=MUTED, lw=1); ax.set_xlabel(f"points, {labels[-1]} minus {labels[0]}"); ax.legend(loc="lower right")
        ax.set_title(f"Per-task change, {labels[0]} to {labels[-1]}", loc="left")
        save(fig, "task_delta.png", "Per-task change")

# Trigger accuracy by version.
trig = {(m, c): J(f"trigger-{m}-{l}.json") for m in models for c, l in zip(refs, labels) if os.path.exists(os.path.join(d, f"trigger-{m}-{l}.json"))}
if trig:
    def trig_stat(t, sel):
        rows = [r for r in t["rows"] if sel(r)]
        runs = t["summary"]["runs"]
        means = [statistics.mean(r["picks"][k] in r["accept"] for r in rows) for k in range(runs)]
        return statistics.mean(means), statistics.pstdev(means)
    slices = [("all queries", lambda r: True), ("should trigger", lambda r: r["positive"]), ("should not trigger", lambda r: not r["positive"])]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
    for ax, (name, sel) in zip(axes, slices):
        for m in models:
            pts = [(l, trig_stat(trig[m, c], sel)) for c, l in zip(refs, labels) if (m, c) in trig]
            ax.errorbar([p[0] for p in pts], [p[1][0] * 100 for p in pts], yerr=[p[1][1] * 100 for p in pts], color=color[m], marker="o", capsize=4, label=m)
        ax.set_title(name, loc="left"); ax.tick_params(axis="x", labelsize=8)
    axes[0].set_ylim(0, 102); axes[0].set_ylabel("% correct pick")
    axes[0].legend(loc="lower left")
    md += ["## Trigger accuracy", "", "Share of runs where the model, given only the skill listing, picked an accepted skill (or none when no mstack skill fits).", ""]
    save(fig, "trigger.png", "Trigger accuracy")
    md += ["| Model | Slice | " + " | ".join(labels) + " |", "|---|---|" + "---|" * len(labels)]
    for m in models:
        for name, sel in slices:
            md.append(f"| {m} | {name} | " + " | ".join(f"{trig_stat(trig[m, c], sel)[0]:.1%} ± {trig_stat(trig[m, c], sel)[1]:.1%}" if (m, c) in trig else "n/a" for c in refs) + " |")
    md.append("")

# Static size by version.
st = {l: J(f"static-{l}.json")["summary"] for l in labels if os.path.exists(os.path.join(d, f"static-{l}.json"))}
if st:
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    keys = [("skill_tokens_total", "SKILL.md bodies"), ("ref_tokens_total", "reference files")]
    w = 0.38
    for i, (k, name) in enumerate(keys):
        xs = [j + (i - .5) * w for j in range(len(st))]
        ax.bar(xs, [st[l][k] / 1000 for l in st], w * 0.92, color=SERIES[2 + i], label=name)
    ax.set_xticks(range(len(st)), list(st)); ax.set_ylabel("thousand tokens"); ax.legend()
    ax.set_title("Skill text size", loc="left")
    md += ["## Size", ""]
    save(fig, "size.png", "Skill text size")
    ks = ["skill_tokens_total", "skill_tokens_median", "ref_tokens_total", "desc_tokens", "scoper_hook_tokens", "broken_links", "lint_failures"]
    md += ["| Metric | " + " | ".join(st) + " |", "|---|" + "---|" * len(st)]
    md += [f"| {k} | " + " | ".join(f"{st[l][k]:.0f}" for l in st) + " |" for k in ks]
    md.append("")

open(os.path.join(d, "VERSIONS.md"), "w").write("\n".join(md))
print("\n".join(md))
