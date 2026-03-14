from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

#The engine is the actual connection to your Supabase/PostgreSQL database. Think of it as the pipeline between your Python code and the database. 
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,    # reconnect on stale connections
    pool_size=10,
    max_overflow=20,
)

#A session is like a conversation with the database — you run queries, make changes, then either commit or roll back. SessionLocal is the factory that creates these sessions.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

#This is the parent class all your SQLAlchemy models inherit from.
Base = declarative_base()


def get_db() -> Generator:
    """FastAPI dependency that provides a per-request DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
