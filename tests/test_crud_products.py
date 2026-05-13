import pytest
from sqlalchemy.orm import Session
from bankpy.models import Account

@pytest.fixture
def new_account():
    return Account(id="ACC123", owner_cpf="12345678901", balance=100.0)

def test_create_account(db_session: Session, new_account):
    db_session.add(new_account)
    db_session.commit()
    account = db_session.query(Account).filter_by(id="ACC123").first()
    assert account is not None
    assert account.balance == 100.0

def test_update_account(db_session: Session, new_account):
    db_session.add(new_account)
    db_session.commit()
    new_account.balance = 250.0
    db_session.commit()
    updated = db_session.query(Account).filter_by(id="ACC123").first()
    assert updated.balance == 250.0

def test_delete_account(db_session: Session, new_account):
    db_session.add(new_account)
    db_session.commit()
    db_session.delete(new_account)
    db_session.commit()
    deleted = db_session.query(Account).filter_by(id="ACC123").first()
    assert deleted is None
