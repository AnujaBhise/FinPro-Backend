
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import SessionLocal
from models.userModel import User
from utils.auth import decode_token


# JWT bearer token handler
security = HTTPBearer()


# Database connection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Get logged-in user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # Get token from Authorization header
    token = credentials.credentials

    # Decode JWT token
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # Get user id from token
    user_id = payload.get("id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Find user in database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user