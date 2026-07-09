"""
This file manages two main things:
1. Hashing passwords with bcrypt
2. Creating and verifying JWT tokens
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Background: bcrypt — an algorithm used to hash passwords
# bcrypt is irreversible — it is impossible to recover the original password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    
    Example:
        hash_password(‘password123’) 
        → ‘$2b$12$KIXx...’ (unreadable hash)
    
    Args:
        password: the plaintext password
    Returns:
        the hashed password — this is what is stored in the database
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks whether a plaintext password matches its hash.
    
    Example:
        verify_password(‘password123’, ‘$2b$12$KIXx...’) → True
        verify_password(‘wrongpassword’, ‘$2b$12$KIXx...’) → False
    
    Args:
        plain_password: the password entered by the user
        hashed_password: the hash stored in the database
    Returns:
        True if the password is correct, False otherwise

Translated with DeepL.com (free version)
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token using the data provided.
    
    The token contains:
    - the data (e.g. user_id)
    - an expiry date (default 1440 minutes = 24 hours)
    - a secret signature to prevent forgery
    
    Example:
        create_access_token({‘sub’: ‘1’}) 
        → ‘eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.abc123’
    
    Args:
        data: the data to be encoded in the token (e.g. {‘sub’: ‘1’})
        expires_delta: the token’s validity period
    Returns:
        the JWT token as a string

Translated with DeepL.com (free version)
    """
    to_encode = data.copy()
    
    # Calculates the expiry date
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Adds the expiry date to the data
    to_encode.update({"exp": expire})
    
    # Creates and returns the signed token
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_token(token: str) -> Optional[str]:
    """
    Verifies and decodes a JWT token.
    
    Example:
        verify_token("eyJhbGciOiJIUzI1NiJ9...") → "1" (user_id)
        verify_token("token_invalide") → None
    
    Args:
        token: the JWT token to verify
    Returns:
        the user_id if the token is valid, None otherwise
    """
    try:
        # Decodes the token with the secret key
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        # Retrieves the user_id from the payload
        user_id: str = payload.get("sub")
        
        if user_id is None:
            return None
            
        return user_id
        
    except JWTError:
        # Invalid or expired token
        return None