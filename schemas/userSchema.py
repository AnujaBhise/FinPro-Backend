# schemas/user.py - Pydantic models for data validation
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration"""
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    name: str = Field(..., min_length=1)
    email: EmailStr


class PasswordUpdate(BaseModel):
    """Schema for updating password"""
    currentPassword: str
    newPassword: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    success: bool
    token: str | None = None
    user: UserResponse | None = None
    message: str | None = None
