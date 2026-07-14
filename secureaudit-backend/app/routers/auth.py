from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

# Create a router - group all auth routes together
router = APIRouter(prefix="/api/auth", tags=["Authentication"])
# System for verifying the Bearer token in the Authorization header
security = HTTPBearer()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    Args:
        user_data: { email, password } sent by the frontend
        db: database session (automatically injected)
    """
    # Check if the email is already registered in the database
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = hash_password(user_create.password)
    
    # Create the sqlalchemy User object — this will be stored in the database
    new_user = User(email=user_create.email, password_hash=hashed_password)
    
    # Add to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    #  # Generates the JWT token using the user_id
    token = create_access_token(data={"sub": str(new_user.id)})
    
    # Return the token and user info to the frontend
    return {
        "token": token,
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "plan": new_user.plan,
            "created_at": new_user.created_at
        }
    }

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login an existing user.
    
    Args:
        user_data: {email, password}
        db: database session (automatically injected)
        
    Returns:
        {token, user} if successful

        Raises:
            401 if the email is not found or the password is incorrect
        """
    # Find the user by email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # Generate a JWT token for the user
    token = create_access_token(data={"sub": str(user.id)})
    return Token(token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            plan=user.plan,
            created_at=user.created_at
        )
    )

@router.get("/me", response_model=UserResponse)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get the currently logged-in user's information.
    
    Args:
        credentials: Bearer token from the Authorization header
        db: database session (automatically injected)
    Returns:
        User information if the token is valid

    Raises:
        401 if the token is invalid or expired
    """
    # Retrieve and check the token 
    token = credentials.credentials
    user_id = verify_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Fetch the user from the database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
