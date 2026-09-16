import os
from prometheus_client import start_http_server, Counter, Histogram

# Starts HTTP Metrics server once on port 8000
try:
    start_http_server(8000)
except Exception:
    pass

# Global metric declarations (registered only once during import)
REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP Requests')
ERRORS_TOTAL = Counter('http_request_errors_total', 'Total HTTP Errors')
LLM_LATENCY = Histogram('llm_latency_seconds', 'LLM response latency in seconds')
