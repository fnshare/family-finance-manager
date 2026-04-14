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