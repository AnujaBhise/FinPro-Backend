# crud/user.py - Business logic for user operations
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import traceback
from models.userModel import User
from schemas.userSchema import AuthResponse, PasswordUpdate, UserRegister, UserResponse, UserUpdate
from utils.auth import hash_password, verify_password, create_token


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def register_user(db: Session, user_data: UserRegister):

    try:
        print("REGISTER STARTED")

        existing_user = get_user_by_email(db, user_data.email)

        print("CHECK USER DONE")

        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")

        hashed_password = hash_password(user_data.password)

        print("PASSWORD HASHED")

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )

        print("USER OBJECT CREATED")

        db.add(new_user)

        print("USER ADDED")

        db.commit()

        print("DB COMMIT DONE")

        db.refresh(new_user)

        print("REFRESH DONE")

        token = create_token(new_user.id)

        print("TOKEN CREATED")

        response = {
            "success": True,
            "token": token,
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }
        }

        print("SUCCESS RESPONSE")

        return response

    except Exception as e:
        print("REGISTER ERROR")
    
        print("========== ERROR ==========")
        traceback.print_exc()

        raise HTTPException(
         status_code=500,
         detail=str(e)
        )

def login_user(db: Session, email: str, password: str) -> AuthResponse:
    """Login a user"""
    # Find user
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "message": "Invalid Email or Password"}
        )
    
    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "message": "Password is incorrect. Please try again"}
        )
    
    # Create token
    token = create_token(user.id)
    
    return AuthResponse(
        success=True,
        token=token,
        user=UserResponse(id=user.id, name=user.name, email=user.email)
    )


def get_user_profile(user: User) -> dict:
    """Get current user profile"""
    return {
        "success": True,
        "user": UserResponse(id=user.id, name=user.name, email=user.email)
    }


def update_user_profile(db: Session, user: User, user_data: UserUpdate) -> dict:
    """Update user profile"""
    # Check if email is already in use by another user
    existing_user = db.query(User).filter(
        User.email == user_data.email,
        User.id != user.id
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"success": False, "message": "Email already in use"}
        )
    
    # Update user
    user.name = user_data.name
    user.email = user_data.email
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "user": UserResponse(id=user.id, name=user.name, email=user.email)
    }


def update_user_password(db: Session, user: User, password_data: PasswordUpdate) -> dict:
    """Update user password"""
    # Verify current password
    if not verify_password(password_data.currentPassword, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "message": "Current password is incorrect"}
        )
    
    # Hash new password
    user.password = hash_password(password_data.newPassword)
    db.commit()
    
    return {
        "success": True,
        "message": "Password updated successfully"
    }
