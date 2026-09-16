-- Database Initialization Script
CREATE TABLE IF NOT EXISTS weather_recommendations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    temperature NUMERIC(5, 2),
    condition VARCHAR(100),
    humidity INT,
    llm_recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_city ON weather_recommendations(city);
