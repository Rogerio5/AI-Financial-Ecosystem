-- 02-init.sql
-- Inicializa esquema e dados (idempotente)

-- Garantir privilégios
GRANT CONNECT ON DATABASE airflow29 TO postgres;
GRANT USAGE, CREATE ON SCHEMA public TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO postgres;

-- =========================
-- Tabela Clientes
-- =========================
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_cadastro DATE DEFAULT CURRENT_DATE,
    cidade VARCHAR(100),
    estado VARCHAR(50),
    telefone VARCHAR(20),
    ativo BOOLEAN DEFAULT TRUE,
    data_nascimento DATE,
    genero VARCHAR(20),
    profissao VARCHAR(100),
    renda_estimada NUMERIC(12,2)
);

-- Inserção de clientes (idempotente por email)
INSERT INTO clientes (nome, email, data_cadastro, cidade, estado, telefone, ativo, data_nascimento, genero, profissao, renda_estimada) VALUES
('Rogerio Sabino', 'rogerio.sabino@example.com', '2026-03-01', 'Agudos', 'SP', '19991111222', TRUE, '1994-04-10', 'Masculino', 'Engenheiro de IA/Dados', 12000.00),
('Ronaldo Sabino', 'ronaldo.sabino@example.com', '2026-03-02', 'Agudos', 'SP', '19993333444', TRUE, '1994-08-15', 'Masculino', 'Engenheiro de Dados', 11500.00),
('Mariana Silva', 'mariana.silva@example.com', '2026-01-12', 'Campinas', 'SP', '19988887777', TRUE, '1990-05-12', 'Feminino', 'Analista de Dados', 6500.00),
('Carlos Pereira', 'carlos.pereira@example.com', '2026-01-20', 'Rio de Janeiro', 'RJ', '21977776666', TRUE, '1985-11-03', 'Masculino', 'Engenheiro', 12000.00),
('Ana Costa', 'ana.costa@example.com', '2026-02-02', 'Belo Horizonte', 'MG', '31966665555', TRUE, '1992-07-21', 'Feminino', 'Designer', 4800.00),
('Felipe Rocha', 'felipe.rocha@example.com', '2026-02-10', 'São Paulo', 'SP', '11955554444', TRUE, '1991-02-02', 'Masculino', 'Cientista de Dados', 14000.00),
('Beatriz Almeida', 'beatriz.almeida@example.com', '2026-02-15', 'Curitiba', 'PR', '41944443333', TRUE, '1993-09-30', 'Feminino', 'Product Manager', 9800.00),
('Lucas Fernandes', 'lucas.fernandes@example.com', '2026-02-18', 'Porto Alegre', 'RS', '51933332222', TRUE, '1990-12-05', 'Masculino', 'Desenvolvedor', 8200.00),
('Sofia Martins', 'sofia.martins@example.com', '2026-02-20', 'Recife', 'PE', '81922221111', TRUE, '1995-06-18', 'Feminino', 'Analista Financeiro', 7200.00),
('Pedro Gomes', 'pedro.gomes@example.com', '2026-02-22', 'Fortaleza', 'CE', '85911110000', TRUE, '1988-10-09', 'Masculino', 'Consultor', 9000.00)
ON CONFLICT (email) DO NOTHING;

-- =========================
-- Tabela Contas
-- =========================
CREATE TABLE IF NOT EXISTS contas (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(20) UNIQUE NOT NULL,
    cliente_id INT REFERENCES clientes(id),
    tipo VARCHAR(50),
    saldo_inicial NUMERIC(12,2),
    data_abertura DATE DEFAULT CURRENT_DATE
);

-- =========================
-- Tabela Acessos
-- =========================
CREATE TABLE IF NOT EXISTS acessos (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    data_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_acesso VARCHAR(50),
    duracao_minutos INT,
    localizacao VARCHAR(100)
);

-- =========================
-- Tabela Transações
-- =========================
CREATE TABLE IF NOT EXISTS transacoes (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(20),
    owner_cpf VARCHAR(11),
    date TIMESTAMP,
    type VARCHAR(50),
    amount NUMERIC(12,2),
    balance_after NUMERIC(12,2),
    description TEXT
);

-- Carregar CSV de transações (se existir)
-- Incluímos a coluna 'id' porque o CSV já traz essa informação
-- TRUNCATE garante que não haverá duplicação se rodar mais de uma vez
TRUNCATE TABLE transacoes;

COPY transacoes(id, account_id, owner_cpf, date, type, amount, balance_after, description)
FROM '/app/data/transactions_flat.csv'
DELIMITER ','
CSV HEADER;
