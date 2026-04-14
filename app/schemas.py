from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    type: str
    parent_id: Optional[int] = None

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    budget: Optional[float] = 0.0

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: int
    project_id: Optional[int] = None
    date: Optional[datetime] = None

class Account(AccountBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class CreditBase(BaseModel):
    name: str
    bill_date: int
    repayment_date: int
    credit_limit: float
    current_bill: Optional[float] = 0.0

class Credit(CreditBase):
    id: int
    class Config:
        orm_mode = True

class StockBase(BaseModel):
    code: str
    name: str
    quantity: int
    cost_price: float
    current_price: Optional[float] = None

class Stock(StockBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True