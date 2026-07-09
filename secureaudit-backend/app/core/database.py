from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
#database.py — Connecting to the PostgreSQL database
#This file configures the SQLAlchemy connection to PostgreSQL.

engine = create_engine(settings.DATABASE_URL)

# Session factory — each API request will have its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class from which all models will inherit 
Base = declarative_base()


def get_db():
    #FastAPI dependency — provides a database session.
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
