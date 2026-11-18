#!/usr/bin/env python3
"""Task outcomes with no skill, the skill at a baseline ref, and the skill at a candidate ref.

Usage: python3 bench/tasks/run.py --model MODEL --base REF [--cand REF] [--runs 3] [--judge MODEL] [--out f.json]

Each run is a fresh agent. Skill conditions get the SKILL.md body the way a harness injects
it after the skill fires, plus a read_file tool over that ref's plugin tree so the agent can
open references on demand. The final answer is graded by regex checks and by a judge model
that never sees which condition produced it.
"""
import argparse, concurrent.futures as cf, json, os, re, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import llm
from static import tree_at, frontmatter

HERE = os.path.dirname(os.path.abspath(__file__))
SYSTEM = ("You are a coding agent helping a user in a chat. You cannot run commands or see their repository; "
          "everything you need is in the message. Answer the request directly.")
READ = {"name": "read_file", "description": "Read a file from the loaded skill's directory or the plugin tree "
        "(paths like references/x.md, <mstack>/skills/name/file.md, or /plugin/...).",
        "schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}


def resolve(plugin, skill, path):
    p = path.replace("${CLAUDE_SKILL_DIR}", f"/plugin/skills/{skill}").replace("<mstack>", "/plugin")
    p = p if p.startswith("/plugin/") else f"/plugin/skills/{skill}/{p}"
    real = os.path.normpath(os.path.join(plugin, p[len("/plugin/"):]))
    if not real.startswith(plugin) or not os.path.isfile(real):
        return None
    return real


def run_agent(model, task, plugin, max_turns=8):
    user = task["prompt"]
    tools, reads = (), []
    if plugin:
        body = frontmatter(open(os.path.join(plugin, "skills", task["skill"], "SKILL.md")).read())[1]
        user += (f"\n\n<skill name=\"{task['skill']}\">\nBase directory for this skill: /plugin/skills/{task['skill']} "
                 f"(`<mstack>` is /plugin). Follow it for this request.\n\n{body}\n</skill>")
        tools = (READ,)
    msgs = [{"role": "user", "content": user}]
    usage = {"in": 0, "out": 0}
    for _ in range(max_turns):
        r = llm.chat(model, SYSTEM, msgs, tools, max_tokens=6000)
        usage["in"] += r["usage"]["in"]; usage["out"] += r["usage"]["out"]
        if not r["tool_calls"]:
            return r["text"], usage, reads
        msgs.append({"role": "assistant", "text": r["text"], "tool_calls": r["tool_calls"]})
        results = []
        for c in r["tool_calls"]:
            real = resolve(plugin, task["skill"], c["input"].get("path", ""))
            reads.append(c["input"].get("path", ""))
            results.append({"id": c["id"], "content": open(real).read() if real else "error: no such file"})
        msgs.append({"role": "tool", "results": results})
    return r["text"], usage, reads


def check(c, text):
    if c.get("scope") == "code":
        text = "\n".join(re.findall(r"```[^\n]*\n(.*?)```", text, re.S))
    if c["type"] == "present":
        return bool(re.search(c["pattern"], text))
    if c["type"] == "absent":
        return not re.search(c["pattern"], text)
    if c["type"] == "count_min":
        return len(re.findall(c["pattern"], text)) >= c["min"]
    if c["type"] == "max_words":
        return len(text.split()) <= c["max"]
    if c["type"] == "tsv_rows":
        rows = [l for l in text.splitlines() if l.count("\t") >= 1 and not l.startswith("ts\t")]
        return len(rows) >= c["min"] and all(l.count("\t") == c["cols"] - 1 for l in rows)


def judge(model, task, text):
    if not task["judge"]:
        return []
    items = "\n".join(f"{i + 1}. {a}" for i, a in enumerate(task["judge"]))
    prompt = (f"Grade a response to a user request against each assertion. Require concrete evidence in the "
              f"response for a pass; a label without substance fails.\n\n<request>\n{task['prompt']}\n</request>\n\n"
              f"<response>\n{text}\n</response>\n\n<assertions>\n{items}\n</assertions>\n\n"
              'Reply with only JSON: {"results": [{"n": 1, "pass": true, "evidence": "short quote or reason"}, ...]}')
    for _ in range(3):
        r = llm.chat(model, "You are a strict, fair grader.", [{"role": "user", "content": prompt}], max_tokens=2000)
        m = re.search(r"\{.*\}", r["text"], re.S)
        try:
            got = {x["n"]: x["pass"] for x in json.loads(m.group(0))["results"]}
            want = range(1, len(task["judge"]) + 1)
            if set(got) == set(want) and all(isinstance(got[n], bool) for n in want):
                return [got[n] for n in want]
        except Exception:
            pass
    raise RuntimeError("judge returned no valid result for every assertion")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--base", required=True, help="git ref for the old skills")
    ap.add_argument("--cand", default=None, help="git ref for the new skills (default: working tree)")
    ap.add_argument("--judge", default="claude-opus-5-5")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out")
    a = ap.parse_args()
    tasks = [t for t in json.load(open(os.path.join(HERE, "tasks.json"))) if not a.only or t["id"] in a.only.split(",")]
    conds = {"none": None, "old": tree_at(a.base), "new": tree_at(a.cand)}
    jobs = [(t, c, r) for t in tasks for c in conds for r in range(a.runs)]

    def one(job):
        t, c, r = job
        text, usage, reads = run_agent(a.model, t, conds[c])
        checks = [check(x, text) for x in t["checks"]]
        judged = judge(a.judge, t, text)
        allv = checks + judged
        return {"task": t["id"], "cond": c, "run": r, "score": sum(allv) / len(allv), "all_pass": all(allv),
                "checks": checks, "judged": judged, "usage": usage, "reads": reads, "text": text}

    with cf.ThreadPoolExecutor(a.workers) as ex:
        rows = list(ex.map(one, jobs))
    summary = {"model": a.model, "base": a.base, "cand": a.cand or "WORKTREE", "runs": a.runs, "judge": a.judge, "by_cond": {}, "by_task": {}}
    for c in conds:
        rs = [r for r in rows if r["cond"] == c]
        summary["by_cond"][c] = {"score": statistics.mean(r["score"] for r in rs),
                                 "score_sd_over_runs": statistics.pstdev([statistics.mean(r["score"] for r in rs if r["run"] == k) for k in range(a.runs)]),
                                 "all_pass_rate": statistics.mean(r["all_pass"] for r in rs),
                                 "in_tokens": statistics.mean(r["usage"]["in"] for r in rs),
                                 "out_tokens": statistics.mean(r["usage"]["out"] for r in rs),
                                 "file_reads": statistics.mean(len(r["reads"]) for r in rs)}
    for t in tasks:
        summary["by_task"][t["id"]] = {c: round(statistics.mean(r["score"] for r in rows if r["task"] == t["id"] and r["cond"] == c), 3) for c in conds}
    print(json.dumps(summary, indent=1))
    if a.out:
        json.dump({"summary": summary, "rows": rows}, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
