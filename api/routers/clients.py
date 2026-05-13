from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from bankpy import crud, schemas, security
from bankpy.db import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

router = APIRouter()
log = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = security.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.post("/register", response_model=schemas.CustomerSchema)
def register_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    try:
        new_customer = crud.create_customer(
            db,
            name=customer.name,
            cpf=customer.cpf,
            email=customer.email,
            password=customer.password
        )
        db.commit()
        log.info(f"Cliente registrado: {new_customer.cpf}")
        return new_customer
    except Exception as e:
        db.rollback()
        log.error(f"Erro ao registrar cliente: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_client_by_cpf(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = security.create_access_token(data={"sub": user.cpf})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=list[schemas.CustomerSchema])
def list_customers(skip: int = Query(0), limit: int = Query(50), db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(crud.Customer).offset(skip).limit(limit).all()

@router.get("/{cpf}", response_model=schemas.CustomerSchema)
def get_customer(cpf: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    customer = crud.get_client_by_cpf(db, cpf)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
