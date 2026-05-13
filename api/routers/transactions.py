from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from bankpy import crud, schemas, security
from bankpy.db import get_db
from fastapi.security import OAuth2PasswordBearer
import logging

router = APIRouter()
log = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = security.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.post("/accounts", response_model=schemas.AccountSchema)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        new_account = crud.create_account(db, account_id=account.id, owner_cpf=account.owner_cpf, initial_balance=account.balance)
        db.commit()
        log.info(f"Conta criada: {new_account.id}")
        return new_account
    except Exception as e:
        db.rollback()
        log.error(f"Erro ao criar conta: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/deposit", response_model=schemas.AccountSchema)
def deposit_money(account_id: str, amount: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    acc = crud.deposit(db, account_id, amount, description="API deposit")
    db.commit()
    log.info(f"Depósito de {amount} na conta {account_id}")
    return acc

@router.post("/withdraw", response_model=schemas.AccountSchema)
def withdraw_money(account_id: str, amount: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    acc = crud.withdraw(db, account_id, amount, description="API withdraw")
    db.commit()
    log.info(f"Saque de {amount} na conta {account_id}")
    return acc

@router.post("/transfer")
def transfer_money(from_id: str, to_id: str, amount: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    crud.transfer(db, from_id, to_id, amount, description="API transfer")
    db.commit()
    log.info(f"Transferência de {amount} de {from_id} para {to_id}")
    return {"status": "success"}

@router.get("/transactions", response_model=list[schemas.TransactionSchema])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(crud.Transaction).offset(skip).limit(limit).all()
