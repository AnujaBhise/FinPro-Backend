# schemas/incomeSchema.py - Pydantic models for data validation
from pydantic import BaseModel, Field
from datetime import datetime


class IncomeCreate(BaseModel):
    """Schema for creating income"""
    description: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    date: datetime
    # user_id: int
    # type: str = "income"


class IncomeUpdate(BaseModel):
    """Schema for updating income"""
    description: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    # category: str = Field(..., min_length=1)
    # date: datetime
    # type: str = "income"


class IncomeResponse(BaseModel):
    """Schema for income response"""
    id: int
    description: str
    amount: float
    category: str
    date: datetime
    user_id: int
    type: str

    class Config:
        from_attributes = True
