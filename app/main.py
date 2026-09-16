import time
import random
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="LLM Agent Service")

# Prometheus Metrics Definitions
REQUEST_COUNT = Counter(
    "http_requests_total", 
    "Total HTTP Requests", 
    ["method", "endpoint", "status"]
)

LLM_LATENCY = Histogram(
    "llm_request_duration_seconds", 
    "LLM API Latency in seconds",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

@app.get("/")
def read_root():
    REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
    return {"message": "LLM Agent Service is running"}

@app.post("/generate")
def generate_llm_response():
    start_time = time.time()
    
    # Simulate LLM processing time
    processing_time = random.uniform(0.2, 3.5)
    time.sleep(processing_time)
    
    # Simulate random errors (5% rate)
    if random.random() < 0.05:
        REQUEST_COUNT.labels(method="POST", endpoint="/generate", status="500").inc()
        return Response(content="Internal LLM Error", status_code=500)
    
    duration = time.time() - start_time
    LLM_LATENCY.observe(duration)
    REQUEST_COUNT.labels(method="POST", endpoint="/generate", status="200").inc()
    
    return {"status": "success", "latency": duration}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
