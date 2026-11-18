- `search_issues` using exception classes, target function, checked error strings, file path.
- Narrow with `search_issue_events`, `get_issue_tag_values` by release/time/env; compare last-seen to ship date; identify fixing release.
- Use `get_sentry_resource` for full event; confirm stack trace passes through target.
- `find_releases` near commit date to map version to PR.
Return per issue: ID, title, project, first/last seen, event count, affected releases, stack trace excerpt through target, correlation with ship date, link.
