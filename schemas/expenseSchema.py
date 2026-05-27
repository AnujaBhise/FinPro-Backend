from pydantic import BaseModel, Field
from datetime import datetime


class ExpenseCreate(BaseModel):
    """Schema for creating expense"""

    description: str = Field(
        ...,
        min_length=1
    )

    amount: float = Field(
        ...,
        gt=0
    )

    category: str = Field(
        ...,
        min_length=1
    )

    date: datetime

    # user_id: int
    # type: str = "expense"


class ExpenseUpdate(BaseModel):
    """Schema for updating expense"""

    description: str = Field(
        ...,
        min_length=1
    )

    amount: float = Field(
        ...,
        gt=0
    )

    # category: str = Field(..., min_length=1)
    # date: datetime
    # type: str = "expense"


class ExpenseResponse(BaseModel):
    """Schema for expense response"""

    id: int
    description: str
    amount: float
    category: str
    date: datetime
    user_id: int
    type: str

    class Config:
        from_attributes = True