# Datadog Telemetry

## What this source contains

The runtime record of what actually happened in production: metrics (a metric's existence shows someone thought it worth watching), monitors and alerts (a monitor on `rate_limit_hit > 10/min` is direct evidence the team worried about that threshold), dashboards, APM traces and spans (slowness, timeouts), logs (error conditions behind defensive code), incidents with timelines and postmortems, notebooks with exploratory analyses.

## How to search it

Use the Datadog MCP, broad then narrow.

1. **Owning services:** `search_datadog_services` (name or team), `search_datadog_service_dependencies` (upstream/downstream).
2. **Dashboards and monitors first:** `search_datadog_dashboards`, `search_datadog_monitors` (feature, service, symbol). Note their queries and thresholds; a threshold often answers "why is this clamped at N?"
3. **Metrics:** `search_datadog_metrics` (name pattern), `get_datadog_metric_context` (description, units, tags), `get_datadog_metric` (timeseries). Correlate the trajectory with the target's change date: "the `payment_timeout` metric spiked 2023-11-03, and the retry logic merged 2023-11-06."
4. **Logs, narrow not dumped:** `search_datadog_logs` with `use_log_patterns=true`, by symbol, error string, or feature; `analyze_datadog_logs` only for counts. **Strongly prefer time-bounded queries** (e.g. 30 days around the change).
5. **APM:** `aggregate_spans` (how often does this endpoint fail?), `search_datadog_spans`, `get_datadog_trace` (one trace ID). For timeouts, retries, slow paths, cross-service behavior.
6. **Incidents:** `search_datadog_incidents` (title, team, date range), `get_datadog_incident`. Defensive target: search incidents around when it was added; a timeline entry "added defensive check for X" is near-direct evidence.

## What good evidence looks like here

- A monitor whose query and threshold match the code's constraint (code clamps to 100, monitor alerts above 100/min).
- A dashboard by the target's author with widgets matching what the code measures or guards.
- A production spike right before the merge and stable values after.
- An incident or log pattern referencing the target's symbols or error strings, timestamped before the change.

## Common pitfalls

- **Correlation is not causation:** other changes may have landed in the window; check neighboring PRs.
- **A chart reflects its maker's framing:** "retry success rate" shows the team cared about retries, not why a specific line exists.
- **Vanished telemetry** (renamed, deleted, short retention): a gap, not a null result.
- **Noise:** narrow by service, tag, and time; aggregate with `analyze_datadog_logs` rather than dumping logs.

## What to return

Per relevant item: type (dashboard / monitor / metric / log pattern / trace / incident / notebook); title or name; identifier (dashboard ID, monitor ID, metric name, incident ID); owner and created/modified date; the verbatim condition, query, or quote bearing on the question; relevance and connection strength.
