# Datadog telemetry

## Searching (Datadog MCP, broad then narrow)
1. Services: search_datadog_services, search_datadog_service_dependencies.
2. Dashboards/monitors first: search_datadog_dashboards, search_datadog_monitors by feature/service/symbol. Monitor thresholds often answer “why clamped at N?”.
3. Metrics: search_datadog_metrics, get_datadog_metric_context, get_datadog_metric; correlate trajectories with change dates.
4. Logs: search_datadog_logs with use_log_patterns=true, bounded ~30 days around the change; analyze_datadog_logs for counts. Never dump raw logs.
5. APM: aggregate_spans, search_datadog_spans, get_datadog_trace for timeouts, retries, slow paths.
6. Incidents: search_datadog_incidents, get_datadog_incident near when defensive code was added.

## Pitfalls
- Neighboring PRs may confound.
- Charts show attention, not motive.
- Renamed/deleted/expired telemetry is a gap, not a null.

## Return
Per item: type, name, identifier, owner, dates, verbatim query/condition/quote, strength.
