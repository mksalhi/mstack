#!/usr/bin/env python3
"""Static skill metrics at a git ref: size, always-loaded cost, pointer graph, lint.

Usage: python3 bench/static.py [REF] [--json out.json]
REF defaults to the working tree. Token counts are chars/4 unless ANTHROPIC_API_KEY
is set, in which case SKILL.md bodies and descriptions are counted with the
count_tokens endpoint (--exact).
"""
import json, os, re, subprocess, sys, tempfile, collections, urllib.request

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def tree_at(ref):
    if ref in (None, "WORKTREE"):
        return os.path.join(ROOT, "plugin")
    d = tempfile.mkdtemp(prefix="skills-")
    tar = subprocess.check_output(["git", "-C", ROOT, "archive", ref, "plugin"])
    subprocess.run(["tar", "-x", "-C", d], input=tar, check=True)
    return os.path.join(d, "plugin")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm, body = m.group(1), text[m.end():]
    out = {}
    for line in fm.splitlines():
        km = re.match(r"([a-z_-]+):\s*(.*)", line)
        if km:
            v = km.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            out[km.group(1)] = v
    return out, body


LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)|`([^`\s]+\.(?:md|sh|py|mjs|js|tsv|json|yaml|tla|cfg))`")


def pointers(path, text, plugin):
    """Files a document points at: markdown links and backticked paths that resolve."""
    found, broken = set(), set()
    here = os.path.dirname(path)
    skill_root = path.split("/skills/")[0] + "/skills/" + path.split("/skills/")[1].split("/")[0]
    for m in LINK.finditer(text):
        raw = m.group(1) or m.group(2)
        if raw.startswith(("http", "mailto:", "~", "$", "/")):
            continue
        raw = raw.replace("${CLAUDE_SKILL_DIR}", skill_root)
        cands = []
        if raw.startswith("<mstack>/"):
            cands = [os.path.join(plugin, raw[len("<mstack>/"):])]
        else:
            cands = [os.path.join(here, raw), os.path.join(skill_root, raw)]
        if "<" in raw.replace("<mstack>/", "") or "*" in raw:
            # pattern pointer such as playbooks/<title>.md: reaches every file it can match
            import glob
            for c in cands:
                found |= {os.path.normpath(g) for g in glob.glob(re.sub(r"<[^>]+>|\*+", "*", c))}
            continue
        hit = next((os.path.normpath(c) for c in cands if os.path.exists(c)), None)
        if hit:
            found.add(hit)
        elif m.group(1) or raw.startswith("<mstack>/"):
            broken.add(raw)
    return found, broken


def count_tokens_api(texts):
    key = os.environ.get("ANTHROPIC_API_KEY")
    out = []
    for t in texts:
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages/count_tokens",
            data=json.dumps({"model": os.environ.get("BENCH_COUNT_MODEL", "claude-sonnet-5-5"),
                             "messages": [{"role": "user", "content": t or "."}]}).encode(),
            headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
        out.append(json.load(urllib.request.urlopen(req))["input_tokens"])
    return out


def shingles(text, n=8):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def analyze(ref=None, exact=False):
    plugin = tree_at(ref)
    sk = os.path.join(plugin, "skills")
    skills, all_shingles = {}, collections.defaultdict(set)
    for name in sorted(os.listdir(sk)):
        sp = os.path.join(sk, name, "SKILL.md")
        if not os.path.isfile(sp):
            continue
        text = open(sp).read()
        fm, body = frontmatter(text)
        files = [os.path.normpath(os.path.join(dp, f)) for dp, _, fs in os.walk(os.path.join(sk, name)) for f in fs]
        docs = [f for f in files if f.endswith(".md")]
        # BFS over pointers, staying inside this skill
        depth, broken, q = {os.path.normpath(sp): 0}, set(), [os.path.normpath(sp)]
        while q:
            cur = q.pop(0)
            if not cur.endswith(".md"):
                continue
            found, br = pointers(cur, open(cur).read(), plugin)
            broken |= br
            for f in found:
                if f.startswith(os.path.join(sk, name) + "/") and f not in depth:
                    depth[f] = depth[cur] + 1
                    q.append(f)
        chars_docs = {f: len(open(f).read()) for f in docs}
        orphans = [os.path.relpath(f, os.path.join(sk, name)) for f in docs if f not in depth]
        long_no_toc = [os.path.relpath(f, os.path.join(sk, name)) for f in docs
                       if open(f).read().count("\n") > 300 and not re.search(r"(?im)^#+\s*(contents|table of contents)", open(f).read())]
        for f in docs:
            for s in shingles(open(f).read()):
                all_shingles[s].add(name)
        desc = fm.get("description", "")
        skills[name] = {
            "desc_chars": len(desc),
            "desc_tokens": len(desc) / 4,
            "skill_lines": body.count("\n"),
            "skill_words": len(body.split()),
            "skill_tokens": len(body) / 4,
            "ref_files": len(docs) - 1,
            "ref_tokens": (sum(chars_docs.values()) - chars_docs[os.path.normpath(sp)]) / 4,
            "max_depth": max(depth.values()),
            "deep_files": sum(1 for v in depth.values() if v >= 2),
            "orphans": orphans,
            "broken_links": sorted(broken),
            "long_no_toc": long_no_toc,
            "lint": [m for m, bad in [
                ("name!=dir", fm.get("name") != name),
                ("desc>1024", len(desc) > 1024),
                ("desc empty", not desc),
                ("skill>500 lines", body.count("\n") > 500),
                ("skill>5000 tokens", len(body) / 4 > 5000),
            ] if bad],
            "_desc": desc, "_body": body,
        }
    if exact:
        names = list(skills)
        bt = count_tokens_api([skills[n]["_body"] for n in names])
        dt = count_tokens_api([skills[n]["_desc"] for n in names])
        for n, b, d in zip(names, bt, dt):
            skills[n]["skill_tokens"], skills[n]["desc_tokens"] = b, d
    dup = collections.Counter()
    for s, owners in all_shingles.items():
        if len(owners) > 1:
            for o in owners:
                dup[o] += 1
    for n in skills:
        skills[n]["shared_8grams"] = dup[n]
        del skills[n]["_desc"], skills[n]["_body"]
    hook = os.path.join(plugin, "hooks")
    tot = lambda k: sum(s[k] for s in skills.values())
    summary = {
        "ref": ref or "WORKTREE",
        "skills": len(skills),
        "listing_chars": sum(len(n) + 4 + s["desc_chars"] for n, s in skills.items()),
        "desc_tokens": tot("desc_tokens"),
        "skill_tokens_total": tot("skill_tokens"),
        "skill_tokens_median": sorted(s["skill_tokens"] for s in skills.values())[len(skills) // 2],
        "ref_tokens_total": tot("ref_tokens"),
        "files_at_depth>=2": tot("deep_files"),
        "orphan_files": sum(len(s["orphans"]) for s in skills.values()),
        "broken_links": sum(len(s["broken_links"]) for s in skills.values()),
        "lint_failures": sum(len(s["lint"]) for s in skills.values()),
        "shared_8grams": tot("shared_8grams"),
    }
    return {"summary": summary, "skills": skills}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = analyze(args[0] if args else None, exact="--exact" in sys.argv)
    if "--json" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    s = out["summary"]
    for k, v in s.items():
        print(f"{k:22} {round(v) if isinstance(v, float) else v}")
