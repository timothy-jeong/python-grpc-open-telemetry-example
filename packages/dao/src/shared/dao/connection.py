import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_env_var(name: str) -> str:
    """Gets an environment variable or raises a ValueError if it's not set."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


DB_USER = get_env_var("DB_USER")
DB_PASSWORD = get_env_var("DB_PASSWORD")
DB_HOST = get_env_var("DB_HOST")
DB_PORT = get_env_var("DB_PORT")
DB_NAME = get_env_var("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
