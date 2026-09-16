import os
from prometheus_client import start_http_server, Counter, Histogram

try:
    start_http_server(8000)
except Exception:
    pass

REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP Requests')
ERRORS_TOTAL = Counter('http_request_errors_total', 'Total HTTP Errors')
LLM_LATENCY = Histogram('llm_latency_seconds', 'LLM response latency in seconds')

# Force-initialize time series so Prometheus scrapes '0' instead of empty set
REQUESTS_TOTAL.inc(0)
ERRORS_TOTAL.inc(0)
