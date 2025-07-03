"""Database connection management."""
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/tasks"
)

# Create PostgreSQL engine
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Function to create and manage database sessions.
    
    This function creates a database session, yields it for use,
    and ensures proper cleanup even if an exception occurs.
    
    Yields:
        Session: SQLAlchemy session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """Function to create and manage database sessions.
    
    This function creates a database session, yields it for use,
    and ensures proper cleanup even if an exception occurs.
    
    Yields:
        Session: SQLAlchemy session object
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine) 