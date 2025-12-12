from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./beauty.db"   # or postgres/mysql

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}   # only for SQLite
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
