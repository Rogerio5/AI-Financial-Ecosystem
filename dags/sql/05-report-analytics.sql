-- 05-report-analytics.sql
-- Relatórios analíticos consolidados: clientes + contas + transações + resultados ML

-- =========================
-- 1) Saldo atual por cliente
-- =========================
SELECT cl.id AS cliente_id,
       cl.nome,
       cl.email,
       c.account_id,
       c.saldo_inicial AS saldo_atual
FROM clientes cl
JOIN contas c ON c.cliente_id = cl.id
ORDER BY cl.id;

-- =========================
-- 2) Últimas 5 transações por cliente
-- =========================
SELECT cl.id AS cliente_id,
       cl.nome,
       t.account_id,
       t.date,
       t.type,
       t.amount,
       t.balance_after,
       t.description
FROM clientes cl
JOIN contas c ON c.cliente_id = cl.id
JOIN transacoes t ON t.account_id = c.account_id
WHERE t.date IS NOT NULL
ORDER BY cl.id, t.date DESC
LIMIT 50;

-- =========================
-- 3) Total de depósitos e saques por cliente
-- =========================
SELECT cl.id AS cliente_id,
       cl.nome,
       SUM(CASE WHEN t.type = 'deposit' THEN t.amount ELSE 0 END) AS total_depositos,
       SUM(CASE WHEN t.type = 'withdraw' THEN t.amount ELSE 0 END) AS total_saques,
       COUNT(t.id) AS qtd_transacoes
FROM clientes cl
JOIN contas c ON c.cliente_id = cl.id
JOIN transacoes t ON t.account_id = c.account_id
GROUP BY cl.id, cl.nome
ORDER BY total_depositos DESC;

-- =========================
-- 4) Relatório consolidado com resultados de ML
-- =========================
SELECT cl.id AS cliente_id,
       cl.nome,
       cl.email,
       c.account_id,
       c.saldo_inicial AS saldo_atual,
       mr.model_name,
       mr.run_date,
       mr.prediction
FROM clientes cl
JOIN contas c ON c.cliente_id = cl.id
LEFT JOIN ml_results mr ON mr.customer_id = cl.id
ORDER BY mr.run_date DESC NULLS LAST;

-- =========================
-- 5) Clientes com maior risco (exemplo de filtro em ML)
-- =========================
SELECT cl.id AS cliente_id,
       cl.nome,
       mr.model_name,
       mr.prediction
FROM clientes cl
JOIN ml_results mr ON mr.customer_id = cl.id
WHERE mr.model_name = 'fraude_detect'
  AND mr.prediction->>'risk' = 'high';
