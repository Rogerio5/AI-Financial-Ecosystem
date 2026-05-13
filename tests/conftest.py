# tests/conftest.py
import pytest
import sys
import os

# Garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bankpy.db import Base, engine, SessionLocal
from scripts.seed_db import run_seed

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Recria tabelas antes da suíte
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Aplica seed automaticamente
    run_seed()

    yield

    # Limpa tabelas depois da suíte
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
