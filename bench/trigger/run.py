#!/usr/bin/env python3
"""Skill-trigger accuracy: does the model pick the right skill from the listing alone?

Usage: python3 bench/trigger/run.py --ref REF --model MODEL [--runs 3] [--out results.json]

Each query goes to a fresh agent whose system prompt lists every mstack skill at REF
plus distractor skills (bench/trigger/distractors.json), the way a harness lists them.
Claude models get a Claude Code style Skill tool; OpenAI models get a Codex style
listing with file paths and a shell tool, and "picking" means reading that SKILL.md.
The first action decides the pick; no tool call means NONE.
"""
import argparse, concurrent.futures as cf, hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import llm
from static import tree_at, frontmatter, skill_at

HERE = os.path.dirname(os.path.abspath(__file__))
AGENT = ("You are a coding agent working in the user's git repository. Use the tools when they help; "
         "otherwise answer directly. Before acting on a task, load a skill when one applies.")


def listing(ref):
    sk = os.path.join(tree_at(ref), "skills")
    skills, user_only = {}, set()
    for n in sorted(os.listdir(sk)):
        p = os.path.join(sk, n, "SKILL.md")
        if os.path.isfile(p):
            fm = frontmatter(open(p).read())[0]
            if str(fm.get("disable-model-invocation", "")).lower() == "true":
                user_only.add(n)  # the harness never lets the model pick these
            else:
                skills[n] = fm.get("description", "")
    skills.update(json.load(open(os.path.join(HERE, "distractors.json"))))
    return skills, user_only


def setup(model, skills):
    names = sorted(skills)
    if llm.provider(model) == "anthropic":
        lst = "\n".join(f"- {n}: {skills[n]}" for n in names)
        system = AGENT + "\n\nThe following skills are available for use with the Skill tool:\n\n" + lst
        tools = [{"name": "Skill", "description": "Execute a skill within the main conversation. Pass the exact skill name.",
                  "schema": {"type": "object", "properties": {"skill": {"type": "string"}}, "required": ["skill"]}},
                 {"name": "Bash", "description": "Run a shell command.",
                  "schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}]
    else:
        lst = "\n".join(f"- {n}: {skills[n]} (file: /skills/{n}/SKILL.md)" for n in names)
        system = (AGENT + "\n\n## Skills\nA skill is a set of instructions in a SKILL.md file. To use one, read its file "
                  "with the shell tool before doing the task.\n### Available skills\n" + lst)
        tools = [{"name": "shell", "description": "Run a shell command and return its output.",
                  "schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}]
    return system, tools


def pick(resp, names):
    for c in resp["tool_calls"]:
        if c["name"] == "Skill":
            return c["input"].get("skill", "").split(":")[-1]
        cmd = c["input"].get("command", "")
        m = re.search(r"skills/([a-z0-9-]+)/SKILL\.md", cmd)
        if m:
            return m.group(1)
    return "NONE"


def split(q):
    return "val" if int(hashlib.sha1(q.encode()).hexdigest(), 16) % 5 < 2 else "train"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default=None)
    ap.add_argument("--model", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out")
    a = ap.parse_args()
    skills, user_only = listing(a.ref)
    mstack = set(skills) - set(json.load(open(os.path.join(HERE, "distractors.json"))))
    system, tools = setup(a.model, skills)
    qs = []
    for l in open(os.path.join(HERE, "queries.jsonl")):
        q = json.loads(l)
        acc = [n for n in q["accept"] if skill_at(mstack | user_only, n) not in user_only]
        if q["accept"] and not acc:
            continue  # only a user-only skill answers it: the user types the command
        qs.append({**q, "accept": acc})
    jobs = [(i, r) for i, q in enumerate(qs) for r in range(a.runs)]

    def one(job):
        i, _ = job
        resp = llm.chat(a.model, system, [{"role": "user", "content": qs[i]["q"]}], tools, max_tokens=4000)
        return i, pick(resp, skills), resp["usage"]

    picks = {i: [] for i in range(len(qs))}
    usage = {"in": 0, "out": 0}
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, p, u in ex.map(one, jobs):
            picks[i].append(p)
            usage["in"] += u["in"]; usage["out"] += u["out"]
    rows = []
    for i, q in enumerate(qs):
        acc = {skill_at(mstack, n) for n in q["accept"]}
        positive = bool(acc & mstack)
        correct = [p in acc for p in picks[i]]
        rows.append({"q": q["q"], "accept": q["accept"], "picks": picks[i], "split": split(q["q"]),
                     "positive": positive, "rate": sum(correct) / len(correct),
                     "false_mstack": sum(p in mstack and p not in acc for p in picks[i]) / len(correct)})

    def agg(sel):
        sel = list(sel)
        return {"n": len(sel), "accuracy": sum(r["rate"] for r in sel) / max(1, len(sel)),
                "pass@0.5": sum(r["rate"] > 0.5 for r in sel) / max(1, len(sel)),
                "wrong_mstack_pick": sum(r["false_mstack"] for r in sel) / max(1, len(sel))}
    summary = {"ref": a.ref or "WORKTREE", "model": a.model, "runs": a.runs,
               "all": agg(rows), "positives": agg(r for r in rows if r["positive"]),
               "negatives": agg(r for r in rows if not r["positive"]),
               "train": agg(r for r in rows if r["split"] == "train"),
               "val": agg(r for r in rows if r["split"] == "val"),
               "system_prompt_tokens_per_call": usage["in"] / len(jobs), "usage": usage}
    print(json.dumps(summary, indent=1))
    if a.out:
        json.dump({"summary": summary, "rows": rows}, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
