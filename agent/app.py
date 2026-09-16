import os
import streamlit as st
import psycopg2
import requests
from prometheus_client import Counter, start_http_server

# Prometheus Metrics
REQUEST_COUNTER = Counter('agent_queries_total', 'Total AI Agent queries answered')

# Environment Setup
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'weather_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'password')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

# Start Metrics Server on port 8000
try:
    start_http_server(8000)
except Exception:
    pass

def get_db_data(city):
    """Fetch stored weather and recommendation context from PostgreSQL."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute("SELECT city, temperature, condition, llm_recommendation FROM weather_recommendations WHERE LOWER(city) = LOWER(%s) ORDER BY created_at DESC LIMIT 1;", (city,))
        row = cur.fetchone()
        conn.close()
        return row
    except Exception as e:
        return None

def query_ollama(prompt):
    """Query local Llama 3 model."""
    try:
        res = requests.post(f"{OLLAMA_HOST}/api/generate", json={"model": "llama3", "prompt": prompt, "stream": False})
        return res.json().get('response', 'Error generating response.')
    except Exception as e:
        return f"Error contacting Ollama LLM: {str(e)}"

# Streamlit UI
st.title("☀️ AI Weather & Travel Recommendation Agent")

city = st.selectbox("Select City", ["London", "Paris", "Tokyo", "New York", "Tel Aviv"])
user_query = st.text_input("Ask a travel/activity question about this city:")

if st.button("Ask Agent"):
    REQUEST_COUNTER.inc()
    context_row = get_db_data(city)
    
    if context_row:
        context = f"Weather in {context_row[0]}: {context_row[1]}°C, {context_row[2]}. Recommendation: {context_row[3]}"
    else:
        context = "No recent weather data available for this city."

    full_prompt = f"Context: {context}\nUser Question: {user_query}\nProvide a helpful travel and activity recommendation."
    
    with st.spinner("Agent is thinking..."):
        answer = query_ollama(full_prompt)
        st.write("### Agent Answer:")
        st.write(answer)
