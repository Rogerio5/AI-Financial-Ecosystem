import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Prometheus client para métricas
from prometheus_client import Counter, Histogram

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Usar DATABASE_URL do ambiente se presente
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Importar target metadata do seu projeto
try:
    from bankpy.db import Base  # exemplo: banco de dados em bankpy/db.py
    target_metadata = Base.metadata
except Exception:
    target_metadata = None

# -----------------------------
# Métricas Prometheus
# -----------------------------
migrations_counter = Counter("alembic_migrations_total", "Total de migrations executadas")
migrations_duration = Histogram("alembic_migrations_duration_seconds", "Tempo de execução das migrations em segundos")
migrations_failures = Counter("alembic_migrations_failures_total", "Total de falhas em migrations")

def run_migrations_offline() -> None:
    """Executa migrations em modo offline (gera SQL sem conexão)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        try:
            with migrations_duration.time():
                context.run_migrations()
                migrations_counter.inc()
        except Exception:
            migrations_failures.inc()
            raise

def run_migrations_online() -> None:
    """Executa migrations em modo online (com conexão)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            try:
                with migrations_duration.time():
                    context.run_migrations()
                    migrations_counter.inc()
            except Exception:
                migrations_failures.inc()
                raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
