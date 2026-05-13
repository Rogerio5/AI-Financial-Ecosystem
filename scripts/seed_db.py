# scripts/seed_db.py
from bankpy.db import SessionLocal
from bankpy.models import Customer

def run_seed():
    """Aplica o seed no banco de teste."""
    session = SessionLocal()
    try:
        # Exemplo de dados iniciais
        customers = [
            Customer(cpf="12345678901", name="Rogério", email="rogerio@example.com"),
            Customer(cpf="98765432100", name="Maria", email="maria@example.com"),
        ]
        session.add_all(customers)
        session.commit()
        print("Seed aplicada com sucesso no banco PostgreSQL.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao aplicar seed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_seed()
