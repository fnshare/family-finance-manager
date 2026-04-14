from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    accounts = relationship("Account", back_populates="owner")
    stocks = relationship("Stock", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # income/expense
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    budget = Column(Float, default=0.0)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="accounts")

class Credit(Base):
    __tablename__ = "credits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    bill_date = Column(Integer)  # 账单日（每月几号）
    repayment_date = Column(Integer)  # 还款日（每月几号）
    credit_limit = Column(Float)
    current_bill = Column(Float, default=0.0)

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)  # 股票代码
    name = Column(String)  # 股票名称
    quantity = Column(Integer)  # 持仓数量
    cost_price = Column(Float)  # 成本价
    current_price = Column(Float, nullable=True)  # 当前价格
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="stocks")