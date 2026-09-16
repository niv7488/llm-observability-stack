import os
import time
import requests
import streamlit as st
from prometheus_client import start_http_server, Counter, Histogram

# Initialize Prometheus Metrics Server on Port 8000
@st.cache_resource
def init_prometheus():
    try:
        start_http_server(8000)
    except Exception:
        pass

init_prometheus()

# Metric definitions
REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP Requests')
ERRORS_TOTAL = Counter('http_request_errors_total', 'Total HTTP Errors')
LLM_LATENCY = Histogram('llm_latency_seconds', 'LLM response latency in seconds')

st.set_page_config(page_title="Autonomous Weather Agent", page_icon="☀️", layout="centered")

st.title("☀️ Autonomous Weather Activity Agent")

city = st.selectbox("Select Target City", ["London", "New York", "Tokyo", "Paris", "Tel Aviv"])
user_query = st.text_input("Ask about weather, sports activities, or tourism itinerary:", 
                           "what is the weather right now and what good football games there are in this week?")

if st.button("Query Agent"):
    start_time = time.time()
    REQUESTS_TOTAL.inc()
    
    try:
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        prompt = f"Target City: {city}. User Query: {user_query}. Provide a helpful, friendly recommendations summary."
        
        response = requests.post(
            f"{ollama_host}/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=60
        )
        
        latency = time.time() - start_time
        LLM_LATENCY.observe(latency)
        
        if response.status_code == 200:
            result = response.json().get("response", "No answer received.")
            st.subheader("Agent Answer:")
            st.write(result)
        else:
            ERRORS_TOTAL.inc()
            st.error(f"Error from LLM: {response.status_code}")
            
    except Exception as e:
        ERRORS_TOTAL.inc()
        st.error(f"Failed to process query: {e}")
