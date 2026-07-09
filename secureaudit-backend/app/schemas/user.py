from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.
    
    This model is used to validate the data received when a new user is created.
    """
    email: EmailStr # Pydantic will validate that the email is in a proper format
    password: str   # the password will be hashed before storing in the database


class UserLogin(BaseModel):
    """
    Data received from the frontend for user login.
    
    This model is used to validate the data received when a user attempts to log in.
    """
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    """
    Data returned to the frontend after a user is created or logged in.
    NEVER contains the password — not even in hashed form.
    Example of renturned json:
    {
        "id": 1,
        "email": "jeany@example.com",
        "plan": "free",
        "created_at": "2026-05-28T10:00:00."
    """
    id: int
    email: EmailStr
    plan: str
    created_at: datetime

class Config:
    """
    Configure Pydantics to read data from an SQLAlchemy object (not just a dictionary)
    """
    from_attributes = True

class Token(BaseModel):
    """
    JWT Token retturned to the frontend after a successful login or registration.

    Example of returned json:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsIn.....",
        "user": {
            "id": 1,
            "email": "jeany@example.com",
            "plan": "free",
            "created_at": "2026-05-28T10:00:00."
        }
    }
    """
    token: str
    user: UserResponse

class userInDB(BaseModel):
    """
    Internal representation of the user, including the password hash.
    Used internally only — never returned to the frontend.
    """
    id: int
    email: EmailStr
    password_hash: str
    plan: str

    class Config:
        from_attributes = True
