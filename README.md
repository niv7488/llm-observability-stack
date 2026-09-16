# 🚀 LLM Observability & Monitoring Stack

A production-ready reference architecture for monitoring LLM Microservices and Infrastructure using Prometheus, Grafana, and FastAPI.

---

## 📐 Architecture Overview

```text
  +------------------------------------------------------------------------+
  |                         🐳 Docker Network                              |
  |                                                                        |
  |   +----------------+      Scrape      +----------------+               |
  |   |    agent-ui    |  <------------>  |   Prometheus   |               |
  |   |   (FastAPI)    |    (/metrics)    |  (Collector)   |               |
  |   +----------------+                  +-------+--------+               |
  |           ^                                   | PromQL                 |
  |           |                                   v                        |
  |           | Traffic                   +----------------+               |
  |           |                           |    Grafana     |               |
  |           |                           |  (Dashboard)   |               |
  |           |                           +-------+--------+               |
  +-----------+-----------------------------------+------------------------+
              |                                   |
              |                                   | http://localhost:3000
       +------+-------+                  +--------+--------+
       | 👤 End User  |                  | 👨‍💻 Engineer    |
       +--------------+                  +-----------------+


🌐 Access Services & Endpoints
Service             | Protocol / Port | Endpoint URL                  | Credentials   | Description
--------------------+-----------------+-------------------------------+---------------+--------------------------------------------------
LLM Agent API       | HTTP / 8000     | http://localhost:8000         | N/A           | Core FastAPI application handling requests
App Metrics         | HTTP / 8000     | http://localhost:8000/metrics | N/A           | Raw Prometheus format metrics endpoint
Prometheus UI       | HTTP / 9090     | http://localhost:9090         | N/A           | Prometheus target status and PromQL query console
Grafana UI          | HTTP / 3000     | http://localhost:3000         | admin / admin | Pre-configured visualization dashboards

🛠️ Stack Components
Agent Service (agent-ui): Python FastAPI application exposing standard metrics (/metrics) including request counts, response codes, and LLM latency buckets.

Metrics Engine (Prometheus): Scrapes the application metrics every 5 seconds.

Visualization Platform (Grafana): Pre-configured with automated data sources and dashboards for instant observability upon launch.

🚀 Quick Start
Prerequisites
Docker & Docker Compose installed.

Start the Stack
Run the automated startup script:

Bash
chmod +x start.sh stop.sh
./start.sh
📊 Pre-built Grafana Metrics
The stack comes out-of-the-box with a pre-provisioned Grafana dashboard tracking:

Total HTTP Requests: Real-time counter of incoming traffic.

HTTP 5xx Error Rates: Error tracking across application endpoints.

LLM Latency (p95): 95th percentile latency calculation for model responses.

🛑 Tear Down
To stop all services and clean up network resources and volumes:

Bash
./stop.sh

