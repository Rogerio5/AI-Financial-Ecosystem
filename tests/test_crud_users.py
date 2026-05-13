import pytest
from sqlalchemy.orm import Session
from bankpy.models import Customer

@pytest.fixture
def new_customer():
    # CPF diferente do seed para evitar colisão
    return Customer(cpf="55555555555", name="Cliente Teste", email="cliente.teste@example.com")

def test_create_customer(db_session: Session, new_customer):
    db_session.add(new_customer)
    db_session.commit()
    customer = db_session.query(Customer).filter_by(cpf="55555555555").first()
    assert customer is not None
    assert customer.name == "Cliente Teste"

def test_update_customer(db_session: Session, new_customer):
    db_session.add(new_customer)
    db_session.commit()
    new_customer.name = "Cliente Atualizado"
    db_session.commit()
    updated = db_session.query(Customer).filter_by(cpf="55555555555").first()
    assert updated.name == "Cliente Atualizado"

def test_delete_customer(db_session: Session, new_customer):
    db_session.add(new_customer)
    db_session.commit()
    db_session.delete(new_customer)
    db_session.commit()
    deleted = db_session.query(Customer).filter_by(cpf="55555555555").first()
    assert deleted is None
