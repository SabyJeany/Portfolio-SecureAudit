"""
models/user.py — SQLAlchemy model for the users table

This file defines the structure of the 'users' table in PostgreSQL.
SQLAlchemy automatically translates this Python class into a SQL table.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """
    SQLAlchemy model representing a SecureAudit user.
    
    Inherits from Base — SQLAlchemy therefore knows that it must create
    a table for this class in PostgreSQL.
    """
    
    # Table name in PostgreSQL
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,  # Primary key —  unique identifier 
        index=True         # Index to speed up searches by id
    )
    
    email = Column(
        String(255),
        unique=True,   # two users cannot have the same email address
        nullable=False, #  The ‘email’ field is mandatory
        index=True     # Index to speed up searches by email
    )
    
    password_hash = Column(
        String(255),
        nullable=False  # Required — you cannot create an account without a password
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()  # Date automatique à la création
    )
    
    plan = Column(
        String(50),
        default="free"  # default plan is "free".
    )
    
    def __repr__(self):
        """
        Représentation lisible de l'objet User.
        Utile pour le débogage.
        
        Exemple : <User id=1 email=jeany@example.com plan=free>
        """
        return f"<User id={self.id} email={self.email} plan={self.plan}>"