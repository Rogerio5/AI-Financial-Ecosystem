import pytest
from sqlalchemy.orm import Session
from bankpy.models import Customer, Account
from bankpy import crud

@pytest.fixture
def setup_accounts(db_session: Session):
    # Cria dois clientes e contas para teste
    c1 = Customer(cpf="11111111111", name="Alice", email="alice@example.com")
    c2 = Customer(cpf="22222222222", name="Bob", email="bob@example.com")
    db_session.add_all([c1, c2])
    db_session.commit()

    acc1 = crud.create_account(db_session, "ACC1", c1.cpf, initial_balance=500.0)
    acc2 = crud.create_account(db_session, "ACC2", c2.cpf, initial_balance=100.0)
    db_session.commit()

    return acc1, acc2

def test_transfer_success(db_session: Session, setup_accounts):
    acc1, acc2 = setup_accounts

    # Executa transferência
    result = crud.transfer(db_session, from_id="ACC1", to_id="ACC2", amount=200.0, description="Teste")
    db_session.commit()

    assert result is True

    # Verifica saldos
    updated_acc1 = db_session.get(Account, "ACC1")
    updated_acc2 = db_session.get(Account, "ACC2")
    assert updated_acc1.balance == 300.0
    assert updated_acc2.balance == 300.0

def test_transfer_insufficient_funds(db_session: Session, setup_accounts):
    acc1, acc2 = setup_accounts

    # Tenta transferir mais do que o saldo
    with pytest.raises(ValueError, match="Insufficient funds"):
        crud.transfer(db_session, from_id="ACC1", to_id="ACC2", amount=1000.0)
