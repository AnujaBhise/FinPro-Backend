

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.userModel import User

from schemas.userSchema import (
    PasswordUpdate,
    UserRegister,
    UserResponse,
    UserUpdate
)

from schemas.commonSchema import ApiResponse

from utils.auth import (
    hash_password,
    verify_password,
    create_token
)


# Get user by email
def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(
        User.email == email
    ).first()


# Get user by id
def get_user_by_id(db: Session, user_id: int):

    return db.query(User).filter(
        User.id == user_id
    ).first()


# Register user
def register_user(db: Session, user_data: UserRegister):

    # Check existing user
    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    # Hash password
    hashed_password = hash_password(
        user_data.password
    )

    # Create user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )

    # Save user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create JWT token
    token = create_token(new_user.id)

    # Common response
    return ApiResponse(
        success=True,
        message="User registered successfully",
        data={
            "token": token,
            "user": UserResponse(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email
            )
        }
    )


# Login user
def login_user(db: Session, email: str, password: str):

    # Find user
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate token
    token = create_token(user.id)

    return ApiResponse(
        success=True,
        message="Login successful",
        data={
            "token": token,
            "user": UserResponse(
                id=user.id,
                name=user.name,
                email=user.email
            )
        }
    )


# Get current user profile
def get_user_profile(user: User):

    return ApiResponse(
        success=True,
        message="User profile fetched successfully",
        data=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    )


# Update profile
def update_user_profile(
    db: Session,
    user: User,
    user_data: UserUpdate
):

    # Check duplicate email
    existing_user = db.query(User).filter(
        User.email == user_data.email,
        User.id != user.id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # Update user
    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return ApiResponse(
        success=True,
        message="Profile updated successfully",
        data=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    )


# Update password
def update_user_password(
    db: Session,
    user: User,
    password_data: PasswordUpdate
):

    # Verify current password
    if not verify_password(
        password_data.currentPassword,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Current password is incorrect"
        )

    # Update password
    user.password = hash_password(
        password_data.newPassword
    )

    db.commit()

    return ApiResponse(
        success=True,
        message="Password updated successfully"
    )