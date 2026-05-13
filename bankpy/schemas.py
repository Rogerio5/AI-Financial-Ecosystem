from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

# -------------------
# Customer
# -------------------
class CustomerBase(BaseModel):
    cpf: str = Field(..., max_length=11, min_length=11, regex=r"^\d{11}$")
    name: str
    email: Optional[EmailStr] = None

class CustomerCreate(CustomerBase):
    password: str  # para autenticação

class CustomerSchema(CustomerBase):
    accounts: List["AccountSchema"] = []
    class Config:
        from_attributes = True

# -------------------
# Account
# -------------------
class AccountBase(BaseModel):
    id: str
    owner_cpf: str
    balance: float = 0.0

class AccountCreate(AccountBase):
    pass

class AccountSchema(AccountBase):
    transactions: List["TransactionSchema"] = []
    class Config:
        from_attributes = True

# -------------------
# Transaction
# -------------------
class TransactionBase(BaseModel):
    account_id: str
    type: str
    amount: float
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionSchema(TransactionBase):
    id: int
    date: datetime
    balance_after: float
    class Config:
        from_attributes = True
