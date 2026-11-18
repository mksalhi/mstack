#!/usr/bin/env python3
"""List, reply to, and resolve GitHub pull-request review threads."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any

DEFAULT_AI_AUTHORS = ("[bot]", "chatgpt-codex", "cursor", "copilot", "coderabbit")

THREADS_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number title url state baseRefName headRefName baseRefOid headRefOid
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated path line startLine originalLine
          originalStartLine diffSide startDiffSide
          resolvedBy { login }
          comments(first: 100) {
            nodes {
              id body createdAt updatedAt url path line originalLine
              author { login }
              commit { oid }
            }
          }
        }
      }
    }
  }
}
"""

REPLY_MUTATION = """\
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
    comment { id body createdAt author { login } }
  }
}
"""

RESOLVE_MUTATION = """\
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved resolvedBy { login } }
  }
}
"""


def run(cmd: list[str], stdin: str | None = None) -> str:
    result = subprocess.run(cmd, input=stdin, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout


def run_json(cmd: list[str], stdin: str | None = None) -> dict[str, Any]:
    output = run(cmd, stdin)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON from {' '.join(cmd)}\n{output}") from exc


def gh_graphql(query: str, **fields: object) -> dict[str, Any]:
    command = ["gh", "api", "graphql", "-F", "query=@-"]
    for key, value in fields.items():
        if value is not None:
            command.extend(["-F", f"{key}={value}"])
    payload = run_json(command, query)
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload


def parse_pr_ref(value: str | None) -> tuple[str, str, int]:
    if not value:
        value = run_json(["gh", "pr", "view", "--json", "url"])["url"]
    for pattern in (
        r"github\.com/([^/]+)/([^/]+)/pull/(\d+)",
        r"^([^/\s]+)/([^#\s]+)#(\d+)$",
        r"^([^/\s]+)/([^/\s]+)/pull/(\d+)$",
    ):
        if match := re.search(pattern, value):
            owner, repo, number = match.groups()
            return owner, repo, int(number)
    raise ValueError("PR must be a GitHub URL, OWNER/REPO#NUMBER, OWNER/REPO/pull/NUMBER, or omitted on a PR branch")


def fetch_threads(owner: str, repo: str, number: int) -> dict[str, Any]:
    cursor: str | None = None
    metadata: dict[str, Any] | None = None
    threads: list[dict[str, Any]] = []
    while True:
        payload = gh_graphql(THREADS_QUERY, owner=owner, repo=repo, number=number, cursor=cursor)
        pr = payload["data"]["repository"]["pullRequest"]
        if pr is None:
            raise RuntimeError(f"Pull request not found: {owner}/{repo}#{number}")
        if metadata is None:
            metadata = {key: value for key, value in pr.items() if key != "reviewThreads"}
            metadata.update({"owner": owner, "repo": repo})
        page = pr["reviewThreads"]
        threads.extend(page["nodes"] or [])
        if not page["pageInfo"]["hasNextPage"]:
            return {"pull_request": metadata, "review_threads": threads}
        cursor = page["pageInfo"]["endCursor"]


def author_matches(thread: dict[str, Any], authors: tuple[str, ...]) -> bool:
    needles = tuple(author.lower() for author in authors)
    return any(
        any(needle in (((comment.get("author") or {}).get("login") or "").lower()) for needle in needles)
        for comment in (thread.get("comments") or {}).get("nodes", []) or []
    )


def filtered_threads(
    payload: dict[str, Any], authors: tuple[str, ...], include_resolved: bool, all_authors: bool
) -> list[dict[str, Any]]:
    return [
        thread
        for thread in payload["review_threads"]
        if (include_resolved or not thread.get("isResolved"))
        and (all_authors or author_matches(thread, authors))
    ]


def print_text(pr: dict[str, Any], threads: list[dict[str, Any]]) -> None:
    print(f"PR: {pr['owner']}/{pr['repo']}#{pr['number']} - {pr['title']}")
    print(f"Base/head: {pr['baseRefName']} {pr['baseRefOid']} -> {pr['headRefName']} {pr['headRefOid']}")
    print(f"Matching threads: {len(threads)}")
    for index, thread in enumerate(threads, 1):
        line = thread.get("line") or thread.get("originalLine") or "?"
        flags = ["resolved" if thread.get("isResolved") else "unresolved"]
        if thread.get("isOutdated"):
            flags.append("outdated")
        print(f"\n{index}. {thread['id']} [{', '.join(flags)}] {thread.get('path')}:{line}")
        for comment in (thread.get("comments") or {}).get("nodes", []) or []:
            login = (comment.get("author") or {}).get("login") or "unknown"
            body = " ".join((comment.get("body") or "").split())
            print(f"   - {login}: {body[:237] + '...' if len(body) > 240 else body}")


def cmd_list(args: argparse.Namespace) -> None:
    owner, repo, number = parse_pr_ref(args.pr)
    payload = fetch_threads(owner, repo, number)
    authors = tuple(args.author or DEFAULT_AI_AUTHORS)
    threads = filtered_threads(payload, authors, args.include_resolved, args.all_authors)
    result = {"pull_request": payload["pull_request"], "review_threads": threads}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text(payload["pull_request"], threads)


def cmd_reply(args: argparse.Namespace) -> None:
    payload = gh_graphql(REPLY_MUTATION, threadId=args.thread_id, body=args.body)
    print(json.dumps(payload["data"]["addPullRequestReviewThreadReply"]["comment"], indent=2))


def cmd_resolve(args: argparse.Namespace) -> None:
    payload = gh_graphql(RESOLVE_MUTATION, threadId=args.thread_id)
    print(json.dumps(payload["data"]["resolveReviewThread"]["thread"], indent=2))


def cmd_reply_and_resolve(args: argparse.Namespace) -> None:
    reply = gh_graphql(REPLY_MUTATION, threadId=args.thread_id, body=args.body)
    resolved = gh_graphql(RESOLVE_MUTATION, threadId=args.thread_id)
    print(json.dumps({
        "reply": reply["data"]["addPullRequestReviewThreadReply"]["comment"],
        "thread": resolved["data"]["resolveReviewThread"]["thread"],
    }, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="List PR review threads")
    listing.add_argument("pr", nargs="?", help="PR URL or OWNER/REPO#NUMBER; omit for current branch")
    listing.add_argument("--author", action="append", help="AI author substring; repeatable and replaces defaults")
    listing.add_argument("--all-authors", action="store_true", help="include human reviewers too")
    listing.add_argument("--include-resolved", action="store_true")
    listing.add_argument("--json", action="store_true")
    listing.set_defaults(func=cmd_list)

    for name, help_text in (("reply", "Reply to a thread"), ("reply-and-resolve", "Reply, then resolve a thread")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("thread_id")
        command.add_argument("--body", required=True)
        command.set_defaults(func=cmd_reply if name == "reply" else cmd_reply_and_resolve)

    resolve = commands.add_parser("resolve", help="Resolve a thread")
    resolve.add_argument("thread_id")
    resolve.set_defaults(func=cmd_resolve)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        args.func(args)
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
