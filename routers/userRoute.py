# routers/userRoute.py - User API routes
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.userSchema import PasswordUpdate, UserLogin, UserRegister, UserUpdate
from services.userService import get_user_profile, login_user, register_user, update_user_password, update_user_profile
from middleware import get_db, get_current_user

router = APIRouter(prefix="/api/user", tags=["User"])


@router.post("/register", status_code=201)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    - **name**: User's full name
    - **email**: User's email address (must be unique)
    - **password**: User's password (minimum 6 characters)
    """
    print("ROUTE HIT")

    print(user_data)

    return register_user(db, user_data)



@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login existing user   
    - **email**: User's email address
    - **password**: User's password
    """
    return login_user(db, user_data.email, user_data.password)


@router.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    """
    Get current logged-in user  
    Requires JWT token in Authorization header.
    """
    return get_user_profile(current_user)


@router.put("/profile")
async def update_profile(
    user_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile   
    - **name**: User's full name
    - **email**: User's email address (must be unique) 
    Requires JWT token in Authorization header.
    """
    return update_user_profile(db, current_user, user_data)


@router.put("/password")
async def change_password(
    password_data: PasswordUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user password
    - **currentPassword**: Current password for verification
    - **newPassword**: New password (minimum 6 characters)   
    Requires JWT token in Authorization header.
    """
    return update_user_password(db, current_user, password_data)
