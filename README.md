
# 🌤️ Autonomous Weather Activity Recommendation Engine & AI Agent

A containerized microservices stack featuring a local LLM inference engine (Ollama/Llama 3), an interactive RAG-enabled Tourism & Sports AI Agent, and an integrated observability stack with Prometheus and Grafana.

---

## 📐 Architecture Overview

```text
  +---------------------------------------------------------------------------------------+
  |                                   🐳 Docker Network                                   |
  |                                                                                       |
  |   +-------------------+                                                               |
  |   |    Ollama LLM     | <-------------------------------------------------+           |
  |   |     (Llama 3)     |                                                   |           |
  |   +-------------------+                                                   |           |
  |                                                                           |           |
  |   +-------------------+   Scrape Metrics    +-------------------+         |           |
  |   |    Prometheus     | <------------------ |     Agent UI      | <-------+           |
  |   |    (Collector)    |    (/metrics)       |  (Streamlit App)  |  Direct Prompting |
  |   +---------+---------+                     +-------------------+                     |
  |             | PromQL                                                                  |
  |             v                                                                         |
  |   +-------------------+                                                               |
  |   |      Grafana      |                                                               |
  |   |    (Dashboard)    |                                                               |
  |   +-------------------+                                                               |
  |                                                                                       |
  |   --- [Infrastructure-Ready / Standby Components] ----------------------------------  |
  |   | n8n Workflow Engine | ---> | RabbitMQ Queue | ---> | PostgreSQL Database |          |
  |   ----------------------------------------------------------------------------------  |
  +---------------------------------------------------------------------------------------+

🌐 Services & Access Endpoints
Plaintext
Service          | Protocol / Port | Endpoint URL           | Credentials   | Description
-----------------+-----------------+------------------------+---------------+--------------------------------------------------
AI Agent UI      | HTTP / 8501     | http://localhost:8501  | N/A           | Streamlit RAG Agent for tourism & sports queries
App Metrics      | HTTP / 8000     | http://localhost:8000  | N/A           | Prometheus exporter endpoint for agent metrics
n8n Workflow     | HTTP / 5678     | http://localhost:5678  | User Setup    | Data ingestion & automation workflow engine
RabbitMQ Manager | HTTP / 15672    | http://localhost:15672 | guest / guest | Message queue management console
Ollama API       | HTTP / 11434    | http://localhost:11434 | N/A           | Local open-weights LLM inference engine (Llama 3)
Prometheus UI    | HTTP / 9090     | http://localhost:9090  | N/A           | Metrics collector & PromQL query engine
Grafana UI       | HTTP / 3000     | http://localhost:3000  | admin / admin | Pre-configured observability dashboards

🛠️ Tech Stack & Architecture Choices
User Agent & Inference (Streamlit + Ollama): The interactive frontend communicates directly with the local Ollama LLM runtime running Llama 3. This ensures low-latency benchmarking, robust direct-to-model prompt execution, and clean Prometheus metric collection.

Local LLM Engine (Ollama / Llama 3): Performs zero-cost, private open-weights inference to generate activity recommendations (e.g., surfing, running, outdoor leisure) based on real-time parameters, ensuring complete data privacy and air-gapped security.

Infrastructure-Ready Components (n8n, RabbitMQ, PostgreSQL): Positioned within the Docker network as an advanced orchestration and persistence layer designed for scheduled future ingestion pipelines and automated webhooks.

Observability Stack (Prometheus & Grafana): Provides real-time metrics tracking request counts, errors, and system response times directly from the application layer.

🚀 Quick Start
Prerequisites
Docker & Docker Compose installed and running.

Launch the Stack
Run the automated startup script:

Bash
chmod +x start.sh stop.sh
./start.sh
The startup script will automatically build the containers, configure networks, initialize database tables, and pull the llama3 model into Ollama.


🧪 Testing & Verification
Interact with AI Agent: Open http://localhost:8501, select a target city, and ask tourism/sports itinerary questions.

Monitor Metrics: Open http://localhost:3000 (Grafana) to view real-time request counts and system health metrics.

Check Standby Infrastructure: Access n8n at http://localhost:5678 or RabbitMQ at http://localhost:15672 to inspect the pre-configured orchestration containers.

🛑 Tear Down
To stop all services and remove volumes:


❓ FAQ & Troubleshooting
Q: Why does the Streamlit UI communicate directly with Ollama instead of routing through n8n?

A: The architecture is designed for modularity and immediate performance benchmarking. The Streamlit UI communicates directly with the local Ollama instance for fast, reliable text generation and clean metric collection. Meanwhile, n8n, RabbitMQ, and PostgreSQL reside in the stack as an infrastructure-ready pipeline for future automated data syncing and multi-tool workflows.

Q: Why am I getting a DuplicateTimeseries error in Streamlit?

A: Streamlit re-runs its entire script from top to bottom on every user interaction. If Prometheus metrics are instantiated directly inside the main app.py, they are re-registered on every click, causing a conflict.

Fix: We separated the metric definitions into a standalone module (metrics.py). This ensures the Prometheus client registers the metrics into memory only once during the initial import.

Q: Why do my Grafana Stat Panels display "No Data"?

A: This typically happens when Prometheus hasn't recorded any data for a metric yet (e.g., zero requests have been made since startup).

Fix: Initialize your counters at startup using .inc(0) in your Python code. Additionally, use the or vector(0) fallback in your Grafana PromQL queries (e.g., sum(http_requests_total) or vector(0)) to gracefully display 0 instead of "No data".

Q: The LLM agent times out and throws a ReadTimeout error. How do I fix it?

A: Local LLMs (like Ollama running llama3) can take a moment to load into memory during a "Cold Start", often exceeding default HTTP request timeouts.

Fix: Increase the timeout parameter in your requests.post() call (e.g., timeout=180). It is also recommended to use a visual loading state (like st.status or st.spinner) to provide clear feedback to the user while the model generates the response.

🚀 Future Improvements (Production Readiness)
Taking this stack from a local Docker Compose environment to a production-grade deployment requires a few architectural upgrades. If you plan to deploy this in a real-world scenario, consider the following enhancements:

Kubernetes (K8s) Orchestration: Migrate from Docker Compose to Helm Charts or native K8s manifests. Utilize the Prometheus Operator and ServiceMonitor resources for dynamic metric scraping. For optimal inference speed, ensure the Ollama workloads are scheduled on GPU-enabled nodes.

Persistent Storage: Attach Persistent Volumes (PV/PVCs) to Prometheus and Grafana. This ensures that historical metric data and custom dashboard configurations survive pod/container restarts.

Secrets & Configuration Management: Decouple hardcoded environment variables. Use Kubernetes Secrets, HashiCorp Vault, or a robust external Secrets Manager to safely store and inject sensitive data.

Security & Authentication: Implement TLS/SSL to encrypt internal communication between microservices. Secure the Grafana dashboard and Streamlit UI from unauthorized access using an authentication proxy (like OAuth2 Proxy) or Ingress-level authentication.

Bash
./stop.sh
