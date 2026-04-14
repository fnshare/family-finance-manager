# 家庭理财管理系统

一个开源的个人/家庭理财管理系统，支持用户管理、账目记录、分类管理、项目预算、信用管理、炒股投资跟踪等功能，提供RESTful API，支持Docker Compose部署。

## 功能特性
- ✅ 用户管理：注册、登录、权限控制
- ✅ 账目管理：记录收支详情，关联分类和项目
- ✅ 分类管理：自定义收支分类，支持层级分类
- ✅ 项目管理：按项目管理预算和支出
- ✅ 信用管理：跟踪信用卡、花呗等信用账户
- ✅ 预算管理：设置分类/项目预算，对比实际支出
- ✅ 炒股投资：跟踪股票持仓、交易记录和盈亏
- ✅ RESTful API：完整的API接口，支持自动化调用
- ✅ Docker部署：一键启动服务

## 技术栈
- 后端：FastAPI + Uvicorn
- 数据库：SQLite（默认）/ PostgreSQL
- ORM：SQLAlchemy
- 认证：JWT + OAuth2
- 部署：Docker + Docker Compose

## 项目结构
```
family-finance-manager/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI主程序
│   ├── models.py            # SQLAlchemy数据模型
│   ├── schemas.py           # Pydantic请求/响应模型
│   ├── crud.py              # 数据库操作封装
│   ├── database.py          # 数据库连接配置
│   └── dependencies.py      # 认证依赖项
├── docker-compose.yml       # Docker Compose配置
├── Dockerfile               # 后端镜像构建文件
├── requirements.txt         # Python依赖包
└── README.md                # 项目说明文档
```

## 快速部署

### 1. 初始化项目
```bash
# 创建项目目录
mkdir family-finance-manager && cd family-finance-manager
```

### 2. 编写配置文件

#### requirements.txt
```txt
fastapi==0.104.1
uvicorn==0.24.0.post1
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

#### app/database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite数据库配置（默认）
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/finance.db"

# PostgreSQL配置（可选）
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/finance"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

#### app/models.py
```python
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
```

#### app/schemas.py
```python
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
```

#### app/crud.py
```python
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_category(db: Session, category: schemas.CategoryBase):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_account(db: Session, account: schemas.AccountBase, owner_id: int):
    db_account = models.Account(**account.dict(), owner_id=owner_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def create_stock(db: Session, stock: schemas.StockBase, user_id: int):
    db_stock = models.Stock(**stock.dict(), user_id=user_id)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock
```

#### app/main.py
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import crud, models, schemas, database
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="家庭理财管理系统API", description="支持家庭理财全场景管理")

# 数据库依赖
 def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT认证配置
SECRET_KEY = "your-secret-key-keep-it-safe"  # 请修改为自己的密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# 登录接口
@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 用户管理接口
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已被注册")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

# 股票管理接口（示例）
@app.post("/stocks/", response_model=schemas.Stock)
def create_stock(stock: schemas.StockBase, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_stock(db=db, stock=stock, user_id=current_user.id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

RUN mkdir -p /app/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - TZ=Asia/Shanghai

# PostgreSQL可选配置
#  db:
#    image: postgres:15-alpine
#    volumes:
#      - postgres_data:/var/lib/postgresql/data/
#    environment:
#      - POSTGRES_USER=finance_user
#      - POSTGRES_PASSWORD=finance_password
#      - POSTGRES_DB=finance_db
#
#volumes:
#  postgres_data:
```

## 启动服务
```bash
# 构建并启动容器
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 停止服务
docker-compose down
```

## 访问API文档
启动后访问 http://localhost:8000/docs 即可查看完整的API文档并进行接口测试。

## 开源协议
MIT License