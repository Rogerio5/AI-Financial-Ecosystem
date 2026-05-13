-- 01-create-superset.sql
-- Cria banco superset (idempotente). Não cria role com senha.

-- Criar o banco superset (se já existir, este comando falhará uma vez, mas não compromete o pipeline)
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'superset') THEN
      EXECUTE 'CREATE DATABASE superset WITH ENCODING = ''UTF8'' TEMPLATE template0';
   END IF;
END
$$;

-- As próximas instruções devem ser executadas dentro do banco superset.
-- Para o PostgresOperator, configure a conexão para usar o schema 'superset'
-- ou rode manualmente uma vez via pgAdmin/psql.

-- Criar extensão útil de forma idempotente
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Criar schema public se não existir
CREATE SCHEMA IF NOT EXISTS public;
