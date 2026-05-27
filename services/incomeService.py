# services/incomeService.py
from fastapi import HTTPException, status
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy import desc

import pandas as pd
from schemas.commonSchema import ApiResponse
from models.incomeModel import Income

from utils.date_filter import get_date_range

from schemas.incomeSchema import (
    IncomeCreate,
    IncomeUpdate
)
# =========================================================
# Add Income
# =========================================================
def add_income(
    db: Session,
    user_id: int,
    income: IncomeCreate
):

    if (
        not income.description or
        not income.amount or
        not income.category or
        not income.date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields are required"
        )

    new_income = Income(
        user_id=user_id,
        description=income.description,
        amount=income.amount,
        category=income.category,
        date=income.date,
        type="income"
    )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return ApiResponse(
    success=True,
    message="Income added successfully",
    data={
        "id": new_income.id,
        "description": new_income.description,
        "amount": new_income.amount,
        "category": new_income.category,
        "date": str(new_income.date)
    }
)
  

# =========================================================
# Get All Income
# =========================================================
def get_all_income(
    db: Session,
    user_id: int
):

    incomes = (
        db.query(Income)
        .filter(Income.user_id == user_id)
        .order_by(desc(Income.date))
        .all()
    )
    
    return ApiResponse(
        success=True,
        message="Income fetched successfully",
        data=[
            {
                "id": income.id,
                "description": income.description,
                "amount": income.amount,
                "category": income.category,
                "date": str(income.date)
            }
            for income in incomes
        ]
    )


# =========================================================
# Update Income
# =========================================================
def update_income(
    db: Session,
    user_id: int,
    income_id: int,
    income_data: IncomeUpdate
):

    income = (
        db.query(Income)
        .filter(
            Income.id == income_id,
            Income.user_id == user_id
        )
        .first()
    )

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income not found"
        )

    if income_data.description is not None:
        income.description = income_data.description

    if income_data.amount is not None:
        income.amount = income_data.amount

    # if income_data.category is not None:
    #     income.category = income_data.category

    # if income_data.date is not None:
    #     income.date = income_data.date

    db.commit()
    db.refresh(income)

    return ApiResponse(
        success=True,
        message="Income updated successfully",
        data={
            "id": income.id,
            "description": income.description,
            "amount": income.amount,
            "category": income.category,
            "date": str(income.date)
        }
    )


# =========================================================
# Delete Income
# =========================================================
def delete_income(
    db: Session,
    user_id: int,
    income_id: int
):

    income = (
        db.query(Income)
        .filter(
            Income.id == income_id,
            Income.user_id == user_id
        )
        .first()
    )

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income not found"
        )

    db.delete(income)
    db.commit()

    return ApiResponse(
        success=True,
        message="Income deleted successfully"
    )


# =========================================================
# Download Excel
# =========================================================
def download_excel(
    db: Session,
    user_id: int
):

    try:

        incomes = (
            db.query(Income)
            .filter(Income.user_id == user_id)
            .order_by(desc(Income.date))
            .all()
        )

        plain_data = []

        for inc in incomes:

            plain_data.append({
                "Description": inc.description,
                "Amount": inc.amount,
                "Category": inc.category,
                "Date": inc.date.strftime("%d-%m-%Y") if inc.date else ""
            })

        df = pd.DataFrame(plain_data)

        file_name = "income_details.xlsx"

        df.to_excel(file_name, index=False)

        
        return FileResponse(
            path=file_name,
            filename=file_name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as error:

        print(error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )


# =========================================================
# Get Income Overview
# =========================================================
def get_income_overview(
    db: Session,
    user_id: int,
    range: str = "monthly"
):

    start, end = get_date_range(range)

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == user_id,
            Income.date >= start,
            Income.date <= end
        )
        .order_by(desc(Income.date))
        .all()
    )

    total_income = sum(income.amount for income in incomes)

    average_income = (
        total_income / len(incomes)
        if len(incomes) > 0
        else 0
    )

    number_of_transactions = len(incomes)

    recent_transactions = incomes[:9]

    return ApiResponse(
        success=True,
        message="Income overview fetched successfully",
        data={
            "totalIncome": total_income,
            "averageIncome": average_income,
            "numberOfTransactions": number_of_transactions,
            "recentTransactions": [
                {
                    "id": income.id,
                    "description": income.description,
                    "amount": income.amount,
                    "category": income.category,
                    "date": str(income.date)
                }
                for income in recent_transactions
            ],
            "range": range
        }
    )
