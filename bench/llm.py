"""Minimal Anthropic and OpenAI clients over urllib: one chat turn with tools, plus usage.

No SDK dependency so the benchmark runs anywhere Python 3.9+ does.
Keys come from ANTHROPIC_API_KEY and OPENAI_API_KEY.
"""
import json, os, random, time, urllib.error, urllib.request


def _post(url, headers, body, tries=6):
    for i in range(tries):
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
        try:
            return json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:500]
            if e.code in (429, 500, 502, 503, 504, 529) and i < tries - 1:
                time.sleep(2 ** i + random.random())
                continue
            raise RuntimeError(f"{e.code} {msg}") from None
        except (urllib.error.URLError, TimeoutError):
            if i < tries - 1:
                time.sleep(2 ** i)
                continue
            raise


def provider(model):
    return "openai" if model.startswith(("gpt", "o1", "o3", "o4", "codex")) else "anthropic"


def chat(model, system, messages, tools=(), max_tokens=2000):
    """messages: neutral list of {role: user|assistant|tool, ...}. Returns
    {text, tool_calls: [{id, name, input}], usage: {in, out}, raw_assistant}."""
    if provider(model) == "anthropic":
        body = {"model": model, "max_tokens": max_tokens, "system": system,
                "messages": [_to_anthropic(m) for m in messages]}
        if tools:
            body["tools"] = [{"name": t["name"], "description": t["description"], "input_schema": t["schema"]} for t in tools]
        r = _post("https://api.anthropic.com/v1/messages",
                  {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                   "content-type": "application/json"}, body)
        text = "".join(b.get("text", "") for b in r["content"] if b["type"] == "text")
        calls = [{"id": b["id"], "name": b["name"], "input": b["input"]} for b in r["content"] if b["type"] == "tool_use"]
        u = r["usage"]
        return {"text": text, "tool_calls": calls,
                "usage": {"in": u["input_tokens"] + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0),
                          "out": u["output_tokens"]}}
    msgs = [{"role": "system", "content": system}]
    for m in messages:
        if m["role"] == "tool":
            msgs += [{"role": "tool", "tool_call_id": r["id"], "content": r["content"]} for r in m["results"]]
        else:
            msgs.append(_to_openai(m))
    body = {"model": model, "messages": msgs, "max_completion_tokens": max_tokens}
    if os.environ.get("OPENAI_REASONING_EFFORT"):
        body["reasoning_effort"] = os.environ["OPENAI_REASONING_EFFORT"]
    if tools:
        body["tools"] = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                            "parameters": t["schema"]}} for t in tools]
    r = _post("https://api.openai.com/v1/chat/completions",
              {"authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "content-type": "application/json"}, body)
    m = r["choices"][0]["message"]
    calls = [{"id": c["id"], "name": c["function"]["name"], "input": json.loads(c["function"]["arguments"] or "{}")}
             for c in m.get("tool_calls") or []]
    return {"text": m.get("content") or "", "tool_calls": calls,
            "usage": {"in": r["usage"]["prompt_tokens"], "out": r["usage"]["completion_tokens"]}}


def _to_anthropic(m):
    if m["role"] == "user":
        return {"role": "user", "content": m["content"]}
    if m["role"] == "assistant":
        content = ([{"type": "text", "text": m["text"]}] if m.get("text") else []) + [
            {"type": "tool_use", "id": c["id"], "name": c["name"], "input": c["input"]} for c in m.get("tool_calls", [])]
        return {"role": "assistant", "content": content}
    return {"role": "user", "content": [{"type": "tool_result", "tool_use_id": r["id"], "content": r["content"]}
                                        for r in m["results"]]}


def _to_openai(m):
    if m["role"] == "user":
        return {"role": "user", "content": m["content"]}
    if m["role"] == "assistant":
        out = {"role": "assistant", "content": m.get("text") or None}
        if m.get("tool_calls"):
            out["tool_calls"] = [{"id": c["id"], "type": "function",
                                  "function": {"name": c["name"], "arguments": json.dumps(c["input"])}} for c in m["tool_calls"]]
        return out
