# Databricks analytics and system tables

The product view (Datadog is the runtime view): what users did, which experiments ran, where a threshold came from.

## Tables

- **Product events:** raw `your_warehouse.events.analytics_track_event`, or the typed, deduplicated dbt models `<your_analytics_db>.<schema>.stg_<source>_<event_name>` (`<source>` is `app`, `backend`, `website` or `cli`). Typed models carry `_timestamp`, `_id`, `_auth_id`, `_request_id`, `event_name`, `properties_<name>` and `context_*` columns. Prefer them; use raw only when no model exists or within the dbt refresh lag (dedupe raw by `_id`).
- **Usage and billing:** `events.usage_event` / `stg_usage_events`, `events.raw_model_event` / `stg_raw_model_events`.
- **Experiments and flags:** company-specific; find them with `SHOW TABLES ... LIKE '*experiment*'`.
- **System tables:** `system.query.history`, `system.compute.warehouses`, `system.billing.*`, `system.access.audit`.
- **Notebooks** aren't queryable through the SQL MCP; if the answer likely lives in one, report a gap.

## Querying

Use `execute_sql_read_only`; if it returns a `statement_id`, poll with `poll_sql_result` rather than rerunning. Confirm every table with `SHOW TABLES` / `DESCRIBE TABLE` before reporting from it. Bound every query to about 30 days either side of the ship date (`_timestamp`, or `start_time` for query history); unbounded scans time out.

## Patterns that pay off

1. **Usage trajectory:** daily counts ±30 days around the merge. Zero to steady in a day or two means the PR launched it; decay to zero means deprecation.
2. **Threshold origin:** median, p99 and max of the relevant `properties_<name>` in the 14 days before the PR. A p99 matching the constant suggests a data-chosen number.
3. **Experiment:** exposure counts by variant for the flag key near the PR date.
4. **Migrations and perf rewrites:** `system.query.history` with `statement_text ILIKE '%<table>%'`, sorted by `total_duration_ms` or summed `read_bytes`.
5. **dbt lineage:** if the target reads or writes a model, hand that model's git history to the git investigator.

## Pitfalls

- An event correlating with the ship date isn't causation; pair it with a PR citation.
- A volume step may be a new event, not new behavior; look for instrumentation PRs in the window.
- Older data may hold a field only in raw `properties_json`.
- A window before retention or model creation is a gap, not zero activity. Say so.

## Return

Per finding: type, fully qualified table, the exact query, the window, a numeric summary (counts, percentiles, first and last seen; never raw rows), the correlation with the ship date ("first row 2024-08-15, PR #49074 merged 2024-08-14"), and strength (direct, circumstantial, weak).
