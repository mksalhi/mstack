# Datadog telemetry

The runtime record. A metric's existence shows someone thought it worth watching; a monitor on `rate_limit_hit > 10/min` is direct evidence the team worried about that threshold.

## Searching (Datadog MCP, broad then narrow)

1. **Services:** `search_datadog_services`, `search_datadog_service_dependencies`.
2. **Dashboards and monitors first:** `search_datadog_dashboards`, `search_datadog_monitors` by feature, service or symbol. A monitor threshold often answers "why is this clamped at N?"
3. **Metrics:** `search_datadog_metrics`, `get_datadog_metric_context`, `get_datadog_metric`. Correlate the trajectory with the change date ("`payment_timeout` spiked 2023-11-03; retry logic merged 2023-11-06").
4. **Logs:** `search_datadog_logs` with `use_log_patterns=true`, bounded to about 30 days around the change; `analyze_datadog_logs` for counts. Never dump raw logs.
5. **APM:** `aggregate_spans`, `search_datadog_spans`, `get_datadog_trace` for timeouts, retries and slow paths.
6. **Incidents:** `search_datadog_incidents`, `get_datadog_incident` around when defensive code was added; a timeline entry naming the check is near-direct evidence.

## Pitfalls

- Other changes may have landed in the same window; check neighboring PRs.
- A chart shows what its maker cared about, not why a specific line exists.
- Renamed, deleted or expired telemetry is a gap, not a null result.

## Return

Per item: type, name, identifier (dashboard, monitor or incident ID, metric name), owner and dates, the verbatim query, condition or quote that bears on the question, and strength.
