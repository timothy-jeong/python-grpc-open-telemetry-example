"""Database connection management."""
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 환경 변수에서 데이터베이스 URL을 가져오거나 기본값 사용
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/tasks"
)

# PostgreSQL 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션을 생성하고 관리하는 함수.
    
    FastAPI의 의존성 주입에서 사용됩니다.
    
    Yields:
        Session: SQLAlchemy 세션 객체
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """데이터베이스 세션을 생성하고 관리하는 컨텍스트 매니저.
    
    gRPC 서비스에서 사용하기 위한 컨텍스트 매니저 버전입니다.
    
    Yields:
        Session: SQLAlchemy 세션 객체
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 