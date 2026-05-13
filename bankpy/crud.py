from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .models import Customer, Account, Transaction
from datetime import datetime, timezone
from typing import Optional
from .security import hash_password

def create_customer(db: Session, name: str, cpf: str, email: Optional[str] = None, password: str = ""):
    existing = db.get(Customer, cpf)
    if existing:
        return existing
    c = Customer(cpf=cpf, name=name, email=email or "")
    c.hashed_password = hash_password(password) if password else None
    db.add(c)
    try:
        db.flush()
        db.refresh(c)
        return c
    except SQLAlchemyError:
        db.rollback()
        raise

def get_client_by_cpf(db: Session, cpf: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.cpf == cpf).first()

def create_account(db: Session, account_id: str, owner_cpf: str, initial_balance: float = 0.0):
    existing = db.get(Account, account_id)
    if existing:
        return existing
    owner = db.get(Customer, owner_cpf)
    if not owner:
        raise ValueError(f"Owner (customer) with cpf={owner_cpf} not found")
    acc = Account(id=account_id, owner_cpf=owner_cpf, balance=initial_balance)
    db.add(acc)
    try:
        db.flush()
        if initial_balance > 0:
            t = Transaction(
                account_id=account_id,
                date=datetime.now(timezone.utc),
                type="deposit",
                amount=initial_balance,
                balance_after=initial_balance,
                description="Initial deposit"
            )
            db.add(t)
            db.flush()
        db.refresh(acc)
        return acc
    except IntegrityError:
        db.rollback()
        return db.get(Account, account_id)
    except SQLAlchemyError:
        db.rollback()
        raise

def deposit(db: Session, account_id: str, amount: float, description: str = ""):
    acc = db.get(Account, account_id)
    if not acc:
        raise ValueError("Account not found")
    acc.balance += amount
    t = Transaction(
        account_id=account_id,
        date=datetime.now(timezone.utc),
        type="deposit",
        amount=amount,
        balance_after=acc.balance,
        description=description
    )
    db.add(t)
    db.flush()
    db.refresh(acc)
    return acc

def withdraw(db: Session, account_id: str, amount: float, description: str = ""):
    acc = db.get(Account, account_id)
    if not acc:
        raise ValueError("Account not found")
    if amount > acc.balance:
        raise ValueError("Insufficient funds")
    acc.balance -= amount
    t = Transaction(
        account_id=account_id,
        date=datetime.now(timezone.utc),
        type="withdraw",
        amount=amount,
        balance_after=acc.balance,
        description=description
    )
    db.add(t)
    db.flush()
    db.refresh(acc)
    return acc

def transfer(db: Session, from_id: str, to_id: str, amount: float, description: str = ""):
    from_acc = db.get(Account, from_id)
    to_acc = db.get(Account, to_id)
    if not from_acc or not to_acc:
        raise ValueError("One or both accounts not found")
    if amount > from_acc.balance:
        raise ValueError("Insufficient funds")
    from_acc.balance -= amount
    t1 = Transaction(
        account_id=from_id,
        date=datetime.now(timezone.utc),
        type="withdraw",
        amount=amount,
        balance_after=from_acc.balance,
        description=f"transfer to {to_id}: {description}"
    )
    db.add(t1)
    to_acc.balance += amount
    t2 = Transaction(
        account_id=to_id,
        date=datetime.now(timezone.utc),
        type="deposit",
        amount=amount,
        balance_after=to_acc.balance,
        description=f"transfer from {from_id}: {description}"
    )
    db.add(t2)
    db.flush()
    db.refresh(from_acc)
    db.refresh(to_acc)
    return True
