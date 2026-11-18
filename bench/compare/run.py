#!/usr/bin/env python3
"""Score whole skill stacks (mstack and other public ones) on the same stack-neutral tasks.

Usage: python3 bench/compare/run.py --model MODEL [--stacks mstack,gstack,...] [--runs 3] [--out f.json]

Each run is a fresh agent that sees one stack's skill listing (name and description, the way
Claude Code lists skills), a Skill tool that loads a SKILL.md body, and a read_file tool over
that stack's files. It chooses whether and which skill to load, then answers. "none" is the
same agent with no skills. Answers are graded by tasks/run.py's checks and judge.
Stacks are pinned in stacks.json and cloned into bench/compare/.stacks/ on first use.
"""
import argparse, concurrent.futures as cf, json, os, re, statistics, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tasks"))
import llm
from static import tree_at
from run import check, judge  # bench/tasks/run.py

SYSTEM = ("You are a coding agent helping a user in a chat. You cannot run commands or see their repository; "
          "everything you need is in the message. Answer the request directly. Before acting on a task, load a skill when one applies.")
SKILL = {"name": "Skill", "description": "Load a skill's instructions by its exact name. Follow them for this request.",
         "schema": {"type": "object", "properties": {"skill": {"type": "string"}}, "required": ["skill"]}}
READ = {"name": "read_file", "description": "Read a file from the stack: a path relative to the loaded skill's directory, or an absolute /stack/... path.",
        "schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}


def frontmatter(text):
    """name and description, including folded (>-) and literal (|) YAML descriptions."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    out, lines = {}, m.group(1).splitlines()
    for i, line in enumerate(lines):
        km = re.match(r"(name|description):\s*(.*)", line)
        if not km:
            continue
        v = km.group(2).strip()
        if v in ("", ">", ">-", "|", "|-"):
            more = []
            for nxt in lines[i + 1:]:
                if nxt and not nxt[0].isspace():
                    break
                more.append(nxt.strip())
            v = " ".join(x for x in more if x)
        out[km.group(1)] = v.strip("\"'")
    return out, text[m.end():]


def stack_root(name, spec):
    if spec.get("git_ref"):
        return tree_at(spec["git_ref"]).rsplit("/plugin", 1)[0]
    d = os.path.join(HERE, ".stacks", name)
    if not os.path.isdir(d):
        subprocess.run(["git", "clone", "-q", "--filter=blob:none", spec["repo"], d], check=True)
    if subprocess.check_output(["git", "-C", d, "rev-parse", "HEAD"], text=True).strip() != spec["sha"]:
        subprocess.run(["git", "-C", d, "checkout", "-q", spec["sha"]], check=True)
    return d


def load_stack(name, spec):
    """{skill name: (dir relative to root, description, body)} for every SKILL.md the stack ships."""
    root = stack_root(name, spec)
    skills = {}
    for pat in spec["skills"]:  # glob patterns relative to root, e.g. "skills/*/SKILL.md"
        import glob
        for p in sorted(glob.glob(os.path.join(root, pat))):
            rel = os.path.relpath(os.path.dirname(p), root)
            if any(re.search(x, rel) for x in spec.get("exclude", [])):
                continue
            fm, body = frontmatter(open(p, errors="replace").read())
            n = fm.get("name") or os.path.basename(os.path.dirname(p))
            skills.setdefault(n, (rel, fm.get("description", ""), body))
    return root, skills


def resolve(root, cur, p):
    """A path the skill text names, in whatever convention the stack uses (/stack/..., relative,
    <mstack>/..., ${CLAUDE_SKILL_DIR}/..., ~/.claude/skills/<stack>/...): try it as given, then
    ever-shorter tails of it against the skill directory and the stack root."""
    p = p.replace("${CLAUDE_SKILL_DIR}", "").replace("<mstack>", "plugin")
    p = p[len("/stack/"):] if p.startswith("/stack/") else p
    parts = [x for x in p.split("/") if x not in ("", ".", "~")]
    for i in range(len(parts)):
        if i and len(parts) - i < 2:  # a bare filename tail like SKILL.md would match the wrong file
            break
        for base in ((cur or ""), ""):
            real = os.path.normpath(os.path.join(root, base, *parts[i:]))
            if real.startswith(root + os.sep) and os.path.isfile(real):
                return real
    return None


def run_agent(model, task, stack, max_turns=10):
    root, skills = stack or (None, {})
    system, tools = SYSTEM, ()
    if skills:
        system += "\n\nThe following skills are available for use with the Skill tool:\n\n" + "\n".join(
            f"- {n}: {d}" for n, (_, d, _) in sorted(skills.items()))
        tools = (SKILL, READ)
    msgs = [{"role": "user", "content": task["prompt"]}]
    usage, loaded, reads, cur = {"in": 0, "out": 0}, [], [], None
    for _ in range(max_turns):
        r = llm.chat(model, system, msgs, tools, max_tokens=6000)
        usage["in"] += r["usage"]["in"]; usage["out"] += r["usage"]["out"]
        if not r["tool_calls"]:
            return r["text"], usage, loaded, reads
        msgs.append({"role": "assistant", "text": r["text"], "tool_calls": r["tool_calls"]})
        results = []
        for c in r["tool_calls"]:
            if c["name"] == "Skill":
                n = c["input"].get("skill", "").split(":")[-1].strip("/")
                if n in skills:
                    cur = skills[n][0]; loaded.append(n)
                    out = f"Base directory for this skill: /stack/{cur}\n\n{skills[n][2]}"
                else:
                    out = f"error: no skill named {n}"
            else:
                p = c["input"].get("path", "")
                reads.append(p)
                real = resolve(root, cur, p)
                out = open(real, errors="replace").read()[:60000] if real else "error: no such file"
            results.append({"id": c["id"], "content": out})
        msgs.append({"role": "tool", "results": results})
    return r["text"], usage, loaded, reads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--stacks", default="", help="comma-separated names from stacks.json (default: all)")
    ap.add_argument("--judge", default="claude-opus-5-5")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out")
    a = ap.parse_args()
    specs = json.load(open(os.path.join(HERE, "stacks.json")))
    names = a.stacks.split(",") if a.stacks else list(specs)
    stacks = {"none": None, **{n: load_stack(n, specs[n]) for n in names}}
    tasks = [t for t in json.load(open(os.path.join(HERE, "tasks.json"))) if not a.only or t["id"] in a.only.split(",")]
    jobs = [(t, s, r) for t in tasks for s in stacks for r in range(a.runs)]

    def one(job):
        t, s, r = job
        err = None
        for _ in range(2):
            try:
                text, usage, loaded, reads = run_agent(a.model, t, stacks[s])
                allv = [check(x, text) for x in t["checks"]] + judge(a.judge, t, text)
                return {"task": t["id"], "stack": s, "run": r, "score": sum(allv) / len(allv), "all_pass": all(allv),
                        "usage": usage, "loaded": loaded, "reads": reads, "text": text}
            except Exception as e:
                err = f"{type(e).__name__}: {e}"[:300]
        return {"task": t["id"], "stack": s, "run": r, "error": err}

    with cf.ThreadPoolExecutor(a.workers) as ex:
        rows = list(ex.map(one, jobs))
    errors = [r for r in rows if "error" in r]
    rows = [r for r in rows if "error" not in r]
    summary = {"model": a.model, "judge": a.judge, "runs": a.runs, "errors": len(errors), "tasks": len(tasks),
               "stacks": {n: {"skills": len(stacks[n][1]) if stacks[n] else 0} for n in stacks}, "by_stack": {}, "by_task": {}}
    for s in stacks:
        rs = [r for r in rows if r["stack"] == s]
        if not rs:
            continue
        per_run = [statistics.mean(g) for k in range(a.runs) if (g := [r["score"] for r in rs if r["run"] == k])]
        summary["by_stack"][s] = {"score": statistics.mean(r["score"] for r in rs), "score_sd_over_runs": statistics.pstdev(per_run),
                                  "all_pass_rate": statistics.mean(r["all_pass"] for r in rs),
                                  "in_tokens": statistics.mean(r["usage"]["in"] for r in rs),
                                  "load_rate": statistics.mean(bool(r["loaded"]) for r in rs)}
    for t in tasks:
        summary["by_task"][t["id"]] = {s: round(statistics.mean(g), 3) if (g := [r["score"] for r in rows if r["task"] == t["id"] and r["stack"] == s]) else None for s in stacks}
    print(json.dumps(summary, indent=1))
    if a.out:
        json.dump({"summary": summary, "rows": rows, "errors": errors}, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
