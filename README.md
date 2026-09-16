
# 🌤️ Autonomous Weather Activity Recommendation Engine & AI Agent

A containerized microservices stack designed to fetch weather data across multiple cities, perform local LLM inferences (Ollama/Llama 3) for activity recommendations, stream data through RabbitMQ and PostgreSQL, and present an interactive RAG-enabled Tourism & Sports AI Agent with integrated observability.

---

## 📐 Architecture Overview

```text
  +---------------------------------------------------------------------------------------+
  |                                   🐳 Docker Network                                   |
  |                                                                                       |
  |   +-------------------+      API Fetch       +-------------------+                    |
  |   | OpenWeather API   | <------------------ |    n8n Workflow   |                    |
  |   +-------------------+                      |    Automation     |                    |
  |                                              +---------+---------+                    |
  |                                                        |                              |
  |                                                        v Ingestion Pipeline           |
  |   +-------------------+   Local Prompting   +----------+--------+                     |
  |   |   Ollama LLM      | <------------------ |    RabbitMQ       |                     |
  |   |   (Llama 3)       |                     |  Message Queue    |                     |
  |   +-------------------+                     +----------+--------+                     |
  |                                                        |                              |
  |                                                        v Data Persistence             |
  |                                             +----------+--------+                     |
  |                                             |    PostgreSQL     |                     |
  |                                             |    Database       |                     |
  |                                             +----------+--------+                     |
  |                                                        ^                              |
  |                                                        | RAG Query Context            |
  |   +-------------------+   Scrape Metrics    +----------+--------+                     |
  |   |    Prometheus     | <------------------ |   Agent UI        |                     |
  |   |   (Collector)     |    (/metrics)       | (Streamlit/FastAPI|                     |
  |   +---------+---------+                     +-------------------+                     |
  |             | PromQL                                                                  |
  |             v                                                                         |
  |   +-------------------+                                                               |
  |   |     Grafana       |                                                               |
  |   |   (Dashboard)     |                                                               |
  |   +-------------------+                                                               |
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
🛠️ Tech Stack & Key Choices
Workflow Ingestion (n8n): Automates scheduled weather data extraction for 5 key cities without exposing external API dependencies to down-stream services.

Queueing & Processing (RabbitMQ): Ensures fault tolerance and temporary failure recovery so no weather payload is lost during peaks or database downtime.

Local LLM Engine (Ollama / Llama 3): Performs zero-cost, private open-weights inference to generate activity recommendations (e.g., surfing, running, outdoor leisure) based on real-time weather metrics.

Storage Layer (PostgreSQL): Stores structured metrics and generated recommendations to enable context retrieval for RAG queries.

User Agent (Streamlit + Python): Interactive frontend enabling users to ask weather, sports, and tourism questions powered by historical DB context and local LLM logic.

Observability Stack (Prometheus & Grafana): Provides real-time metrics tracking request counts, errors, and system response times.

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
Verify Ingestion: Access n8n at http://localhost:5678 to trigger or inspect the weather ingestion pipeline.

Interact with AI Agent: Open http://localhost:8501, select a target city, and ask tourism/sports itinerary questions.

Monitor Metrics: Open http://localhost:3000 (Grafana) to view real-time request counts and system health metrics.

🛑 Tear Down
To stop all services and remove volumes:

Bash
./stop.sh
