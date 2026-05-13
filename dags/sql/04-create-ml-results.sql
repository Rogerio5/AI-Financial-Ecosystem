-- 04-create-ml-results.sql
-- Cria tabela para armazenar resultados dos modelos de ML

CREATE TABLE IF NOT EXISTS ml_results (
    id SERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,
    run_date TIMESTAMP DEFAULT NOW(),
    customer_id BIGINT,
    prediction JSONB
);
