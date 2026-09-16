import os
import streamlit as st
import psycopg2
import requests
from prometheus_client import Counter, start_http_server, REGISTRY

# Define Prometheus Metric safely to prevent re-registration crash in Streamlit
try:
    REQUEST_COUNTER = Counter('agent_queries_total', 'Total AI Agent queries answered')
except ValueError:
    # If already registered on Streamlit rerun, retrieve existing metric from registry
    REQUEST_COUNTER = REGISTRY._names_to_collectors['agent_queries_total']

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'weather_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'password')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

# Start metrics server safely
try:
    start_http_server(8000)
except Exception:
    pass

def get_db_data(city):
    """Fetch recent weather and recommendation context from PostgreSQL."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute("SELECT city, temperature, condition, llm_recommendation FROM weather_recommendations WHERE LOWER(city) = LOWER(%s) ORDER BY created_at DESC LIMIT 1;", (city,))
        row = cur.fetchone()
        conn.close()
        return row
    except Exception:
        return None

def query_ollama(prompt):
    """Query local Llama 3 LLM instance."""
    try:
        res = requests.post(f"{OLLAMA_HOST}/api/generate", json={"model": "llama3", "prompt": prompt, "stream": False}, timeout=60)
        return res.json().get('response', 'No response generated.')
    except Exception as e:
        return f"Error contacting Ollama: {str(e)}"

# Frontend UI
st.title("☀️ Autonomous Weather Activity Agent")

city = st.selectbox("Select Target City", ["London", "Paris", "Tokyo", "New York", "Tel Aviv"])
user_query = st.text_input("Ask about weather, sports activities, or tourism itinerary:")

if st.button("Query Agent"):
    REQUEST_COUNTER.inc()
    context_row = get_db_data(city)
    
    if context_row:
        context = f"City: {context_row[0]}, Temp: {context_row[1]}°C, Condition: {context_row[2]}. Recommendation: {context_row[3]}"
    else:
        context = f"Target city is {city}."

    prompt = f"Context: {context}\nUser Question: {user_query}\nProvide a concise recommendation regarding outdoor activity, sports, or tourism."
    
    with st.spinner("Analyzing context and querying local LLM..."):
        response = query_ollama(prompt)
        st.write("### Agent Answer:")
        st.write(response)
