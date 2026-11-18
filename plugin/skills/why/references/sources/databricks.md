# Databricks Analytics & System Tables

## What this source contains

The product/data view (Datadog is infra/runtime): what users did, which experiments ran, how usage evolved, where a threshold came from.

- **Product analytics events:** `your_warehouse.events.analytics_track_event` (raw) and typed, deduplicated per-event dbt models in `<your_analytics_db>.<schema>.<table>`: feature invocations, clicks, accepts/rejects, submissions, client errors.
- **Usage & billing events:** `your_warehouse.events.usage_event` / `<your_analytics_db>.<schema>.stg_usage_events`, `your_warehouse.events.raw_model_event` / `<your_analytics_db>.<schema>.stg_raw_model_events`, for cost- or volume-driven decisions.
- **Experiment / feature-flag tables:** **company-specific schema**; probe with `SHOW TABLES` first.
- **System tables:** `system.query.history`, `system.compute.warehouses`, `system.billing.*`, `system.access.audit` ("was this query expensive?", "how often was it run?", "when did load spike?").
- **dbt lineage:** models in `<your_analytics_db>.<schema>` show what depends on a table or field; upstream changes often motivate consumer code.
- **Notebooks:** **not queryable via the SQL MCP**; if the rationale likely lives in one, return a gap.

## How to search it

Use the Databricks SQL MCP: `execute_sql_read_only`; if it returns a `statement_id`, poll with `poll_sql_result` instead of re-running.

- **Orient first:** schemas are company-specific; never report from a table you didn't confirm.

  ```sql
  SHOW TABLES IN <your_analytics_db>.<schema> LIKE '*<keyword>*';
  DESCRIBE TABLE <your_analytics_db>.<schema>.stg_<event>;
  ```

- **Time-bound every query** (unbounded scans time out): `_timestamp` (events) or `start_time` (`system.query.history`), ~30 days either side of the ship date, wider only with strong reason.
- **Prefer typed dbt models** (deduplicated, typed, liquid-clustered) over the raw table (duplicates, untyped `properties_json`). Name pattern `stg_<source>_<event_name_with_underscores>`, `<source>` ∈ `app`, `backend`, `website`, `cli`; confirm with `SHOW TABLES`. Use raw only when no model exists or for events inside the refresh lag.
- **Typed model columns:** `_timestamp`, `_id`, `_auth_id`, `_request_id`, `event_name` on every model; `properties_<name>` (typed event properties, e.g. `properties_entrypoint`, `properties_size_bytes`); `context_team_id`, `context_client_version`, `context_country`, `context_client_os`.

### Investigation patterns that tend to pay off

1. **Usage trajectory:** daily counts on the `stg_*` model over ±30d around the merge. Zero to steady within a day or two suggests the PR launched it; decay to zero suggests deprecation.
2. **Guard-rail origin:** median / p99 / max of the relevant `properties_<name>` in the 14 days *before* the PR. A p99 matching the threshold constant suggests a data-chosen number.
3. **Experiment / flag:** `SHOW TABLES ... LIKE '*experiment*'`, then exposure counts by variant for the flag key near the PR date.
4. **Migrations, backfills, perf rewrites:** `system.query.history` with `statement_text ILIKE '%<table_or_symbol>%'` and a tight `start_time` window; sort by `total_duration_ms` or aggregate `SUM(read_bytes)`, `COUNT(*)`.
5. **dbt lineage:** if the target reads or writes a model, the model's git history holds the rationale; hand that lead to the git investigator.

## What good evidence looks like here

- An error-classifying event dropping to near zero after a defensive-code PR.
- An exposure table naming the target's flag key with a "shipped" / "concluded" decision near the ship date.

## Common pitfalls

- **Instrumented ≠ caused:** pair with a PR/commit citation from the git investigator before claiming causation.
- **Silent instrumentation changes:** a volume step may be a new event, not new behavior; check for instrumentation PRs in the window.
- **Schema drift:** a typed column may postdate the target; older data may hold it only in raw `properties_json`.
- **dbt refresh lag** (hourly/daily): for the last few hours use `your_warehouse.events.*`, deduplicated by `_id`.
- **Retention cliff:** a window before retention or model creation is a *gap*, not a null; name it so "no results" isn't read as "no activity".

## What to return

Per finding: type (product event / experiment exposure / usage or billing event / system-table row / dbt model); fully-qualified table and the exact query; time window; compact numeric summary (counts, percentiles, first/last-seen), **never raw rows**; correlation with the ship date (e.g. "first row 2024-08-15, PR #49074 merged 2024-08-14"); relevance and strength (direct / circumstantial / weak).
