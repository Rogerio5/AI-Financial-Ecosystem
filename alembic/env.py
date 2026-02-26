import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# garantir que o pacote do projeto seja importável
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Alembic Config object
config = context.config

# Interpretar o arquivo ini para logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Usar DATABASE_URL do ambiente se presente
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Importar target metadata do seu projeto
# Ajuste o import abaixo conforme a estrutura do seu projeto
try:
    from bankpy.db import Base  # exemplo: banco de dados em bankpy/db.py
    target_metadata = Base.metadata
except Exception:
    target_metadata = None

def run_migrations_offline():
    """Executa migrations em modo offline (gera SQL sem conexão)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Executa migrations em modo online (com conexão)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,        # ajuda autogenerate a detectar mudanças de tipo
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
