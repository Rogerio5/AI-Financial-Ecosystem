-- 03-create-accounts-and-generate-transacoes.sql
-- 1) cria contas idempotentes para os 20 clientes
-- 2) gera transações até 20 por conta (apenas as que faltarem)
-- 3) atribui CPFs fictícios por cliente
-- 4) atualiza saldo_inicial com último balance_after
-- 5) adiciona constraints e índices extras

-- 1) Criar contas idempotentes (account_id 0001-CC ... 0020-CC)
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0001-CC', id, 'corrente', 0.00 FROM clientes WHERE email='rogerio.sabino@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0002-CC', id, 'corrente', 0.00 FROM clientes WHERE email='ronaldo.sabino@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0003-CC', id, 'corrente', 0.00 FROM clientes WHERE email='mariana.silva@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0004-CC', id, 'corrente', 0.00 FROM clientes WHERE email='carlos.pereira@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0005-CC', id, 'corrente', 0.00 FROM clientes WHERE email='ana.costa@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0006-CC', id, 'corrente', 0.00 FROM clientes WHERE email='felipe.rocha@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0007-CC', id, 'corrente', 0.00 FROM clientes WHERE email='beatriz.almeida@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0008-CC', id, 'corrente', 0.00 FROM clientes WHERE email='lucas.fernandes@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0009-CC', id, 'corrente', 0.00 FROM clientes WHERE email='sofia.martins@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0010-CC', id, 'corrente', 0.00 FROM clientes WHERE email='pedro.gomes@example.com' ON CONFLICT (account_id) DO NOTHING;

INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0011-CC', id, 'corrente', 0.00 FROM clientes WHERE email='alice.silva@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0012-CC', id, 'corrente', 0.00 FROM clientes WHERE email='bruno.costa@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0013-CC', id, 'corrente', 0.00 FROM clientes WHERE email='carla.souza@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0014-CC', id, 'corrente', 0.00 FROM clientes WHERE email='daniel.lima@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0015-CC', id, 'corrente', 0.00 FROM clientes WHERE email='fernanda.alves@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0016-CC', id, 'corrente', 0.00 FROM clientes WHERE email='sandra.cardenas@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0017-CC', id, 'corrente', 0.00 FROM clientes WHERE email='silvio.sabino@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0018-CC', id, 'corrente', 0.00 FROM clientes WHERE email='priscilla.costa@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0019-CC', id, 'corrente', 0.00 FROM clientes WHERE email='joao.santos@example.com' ON CONFLICT (account_id) DO NOTHING;
INSERT INTO contas (account_id, cliente_id, tipo, saldo_inicial)
SELECT '0020-CC', id, 'corrente', 0.00 FROM clientes WHERE email='maria.oliveira@example.com' ON CONFLICT (account_id) DO NOTHING;

-- 2) Gerar transações até 20 por conta (idempotente)
DO
$$
DECLARE
  r RECORD;
  existing_count INTEGER;
  to_insert INTEGER;
  i INTEGER;
  last_balance NUMERIC;
  amt NUMERIC;
  typ TEXT;
  dt TIMESTAMP;
  desc_txt TEXT;
BEGIN
  FOR r IN SELECT account_id FROM contas LOOP
    SELECT COUNT(*) INTO existing_count FROM transacoes WHERE account_id = r.account_id;
    to_insert := GREATEST(0, 20 - existing_count);

    SELECT (ARRAY_AGG(balance_after ORDER BY date DESC, id DESC))[1] INTO last_balance
    FROM transacoes WHERE account_id = r.account_id;

    IF last_balance IS NULL THEN
      last_balance := 0;
    END IF;

    FOR i IN 1..to_insert LOOP
      amt := round((random() * 2995.0 + 5.0)::numeric, 2);

      IF random() < 0.55 THEN
        typ := 'deposit';
        last_balance := last_balance + amt;
        desc_txt := 'Depósito automático';
      ELSE
        typ := 'withdraw';
        -- Evitar saldo negativo
        IF last_balance - amt < 0 THEN
          amt := last_balance; -- limita saque ao saldo disponível
        END IF;
        last_balance := last_balance - amt;
        desc_txt := 'Saque automático';
      END IF;

      dt := now() - (floor(random() * 365) || ' days')::interval
               - (floor(random() * 86400) || ' seconds')::interval;

      INSERT INTO transacoes (account_id, owner_cpf, date, type, amount, balance_after, description)
      VALUES (r.account_id, '00000000000', dt, typ, amt, last_balance, desc_txt);
    END LOOP;
  END LOOP;
END
$$;

-- 3) Mapear CPFs fictícios por cliente e atualizar transacoes
CREATE TEMP TABLE tmp_cpf_map (email text, cpf text);

INSERT INTO tmp_cpf_map (email, cpf) VALUES
('rogerio.sabino@example.com','11111111111'),
('ronaldo.sabino@example.com','22222222222'),
('mariana.silva@example.com','33333333333'),
('carlos.pereira@example.com','44444444444'),
('ana.costa@example.com','55555555555'),
('felipe.rocha@example.com','66666666666'),
('beatriz.almeida@example.com','77777777777'),
('lucas.fernandes@example.com','88888888888'),
('sofia.martins@example.com','99999999999'),
('pedro.gomes@example.com','00000000001'),
('alice.silva@example.com','00000000002'),
('bruno.costa@example.com','00000000003'),
('carla.souza@example.com','00000000004'),
('daniel.lima@example.com','00000000005'),
('fernanda.alves@example.com','00000000006'),
('sandra.cardenas@example.com','00000000007'),
('silvio.sabino@example.com','00000000008'),
('priscilla.costa@example.com','00000000009'),
('joao.santos@example.com','00000000010'),
('maria.oliveira@example.com','00000000011');

UPDATE transacoes t
SET owner_cpf = m.cpf
FROM contas c
JOIN clientes cl ON cl.id = c.cliente_id
JOIN tmp_cpf_map m ON m.email = cl.email
WHERE t.account_id = c.account_id
  AND (t.owner_cpf IS NULL OR t.owner_cpf = '00000000000');

-- 4) Atualizar saldo_inicial em contas com o último balance_after
WITH last_bal AS (
  SELECT t.account_id,
         (ARRAY_AGG(t.balance_after ORDER BY t.date DESC, t.id DESC))[1] AS last_balance
  FROM transacoes t
  GROUP BY t.account_id
)
UPDATE contas c
SET saldo_inicial = lb.last_balance
FROM last_bal lb
WHERE c.account_id = lb.account_id;

-- 5) Constraints e índices extras
ALTER TABLE contas
  ADD CONSTRAINT saldo_inicial_nonnegative CHECK (saldo_inicial >= 0);

ALTER TABLE transacoes
  ADD CONSTRAINT amount_nonnegative CHECK (amount >= 0),
  ADD CONSTRAINT balance_nonnegative CHECK (balance_after >= 0);

CREATE INDEX IF NOT EXISTS idx_transacoes_owner_cpf ON transacoes(owner_cpf);
CREATE INDEX IF NOT EXISTS idx_transacoes_date ON transacoes(date);
CREATE INDEX IF NOT EXISTS idx_contas_cliente_id ON contas(cliente_id);