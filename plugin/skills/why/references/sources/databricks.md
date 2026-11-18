# Databricks analytics and system tables

Tables
- Product events: prefer typed dbt models <your_analytics_db>.<schema>.stg_<source>_<event_name> (<source>: app, backend, website, cli). Use raw your_warehouse.events.analytics_track_event only if no model or within dbt refresh lag; dedupe raw by _id.
- Usage/billing: events.usage_event / stg_usage_events; events.raw_model_event / stg_raw_model_events.
- System: system.query.history, system.billing.*, system.access.audit.
- Notebooks aren’t queryable via SQL MCP; report a gap.

Querying
- Use execute_sql_read_only; if it returns statement_id, poll with poll_sql_result.
- Confirm with SHOW TABLES/DESCRIBE TABLE before using.
- Time-bound queries to ±30 days of ship (_timestamp; start_time for query history).

Patterns
1) Usage trajectory: daily counts ±30d around merge.
2) Thresholds: median, p99, max of properties_<name> in 14d pre-PR; p99≈constant => data-chosen.
3) Experiments: exposure by variant near PR date.
4) Migrations/perf: system.query.history WHERE statement_text ILIKE '%<table>%'; sort total_duration_ms or sum read_bytes.
5) If a dbt model is touched, hand its git history to the git investigator.

Pitfalls
- Correlation ≠ causation; cite the PR.
- Volume steps may be new events; check instrumentation PRs.
- Older fields may be only in raw properties_json.
- Pre-retention/pre-model windows are gaps, not zero.

Return
- Per finding: type; FQ table; exact query; window; numeric summary (counts, percentiles, first/last seen; never raw rows); ship-date correlation; strength.
