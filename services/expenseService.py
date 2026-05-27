# services/expenseService.py

from fastapi import HTTPException, status
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy import desc

import pandas as pd

from schemas.commonSchema import ApiResponse

from models.expenseModel import Expense

from utils.date_filter import get_date_range

from schemas.expenseSchema import (
    ExpenseCreate,
    ExpenseUpdate
)


# =========================================================
# Add Expense
# =========================================================
def add_expense(
    db: Session,
    user_id: int,
    expense: ExpenseCreate
):

    if (
        not expense.description or
        not expense.amount or
        not expense.category or
        not expense.date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields are required"
        )

    new_expense = Expense(
        user_id=user_id,
        description=expense.description,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        type="expense"
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return ApiResponse(
        success=True,
        message="Expense added successfully",
        data={
            "id": new_expense.id,
            "description": new_expense.description,
            "amount": new_expense.amount,
            "category": new_expense.category,
            "date": str(new_expense.date)
        }
    )


# =========================================================
# Get All Expense
# =========================================================
def get_all_expense(
    db: Session,
    user_id: int
):

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(desc(Expense.date))
        .all()
    )

    return ApiResponse(
        success=True,
        message="Expense fetched successfully",
        data=[
            {
                "id": expense.id,
                "description": expense.description,
                "amount": expense.amount,
                "category": expense.category,
                "date": str(expense.date)
            }
            for expense in expenses
        ]
    )


# =========================================================
# Update Expense
# =========================================================
def update_expense(
    db: Session,
    user_id: int,
    expense_id: int,
    expense_data: ExpenseUpdate
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    if expense_data.description is not None:
        expense.description = expense_data.description

    if expense_data.amount is not None:
        expense.amount = expense_data.amount

    db.commit()
    db.refresh(expense)

    return ApiResponse(
        success=True,
        message="Expense updated successfully",
        data={
            "id": expense.id,
            "description": expense.description,
            "amount": expense.amount,
            "category": expense.category,
            "date": str(expense.date)
        }
    )


# =========================================================
# Delete Expense
# =========================================================
def delete_expense(
    db: Session,
    user_id: int,
    expense_id: int
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return ApiResponse(
        success=True,
        message="Expense deleted successfully"
    )


# =========================================================
# Download Excel
# =========================================================
def download_excel(
    db: Session,
    user_id: int
):

    try:

        expenses = (
            db.query(Expense)
            .filter(Expense.user_id == user_id)
            .order_by(desc(Expense.date))
            .all()
        )

        plain_data = []

        for exp in expenses:

            plain_data.append({
                "Description": exp.description,
                "Amount": exp.amount,
                "Category": exp.category,
                "Date": exp.date.strftime("%d-%m-%Y") if exp.date else ""
            })

        df = pd.DataFrame(plain_data)

        file_name = "expense_details.xlsx"

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
# Get Expense Overview
# =========================================================
def get_expense_overview(
    db: Session,
    user_id: int,
    range: str = "monthly"
):

    start, end = get_date_range(range)

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id,
            Expense.date >= start,
            Expense.date <= end
        )
        .order_by(desc(Expense.date))
        .all()
    )

    total_expense = sum(expense.amount for expense in expenses)

    average_expense = (
        total_expense / len(expenses)
        if len(expenses) > 0
        else 0
    )

    number_of_transactions = len(expenses)

    recent_transactions = expenses[:9]

    return ApiResponse(
        success=True,
        message="Expense overview fetched successfully",
        data={
            "totalExpense": total_expense,
            "averageExpense": average_expense,
            "numberOfTransactions": number_of_transactions,
            "recentTransactions": [
                {
                    "id": expense.id,
                    "description": expense.description,
                    "amount": expense.amount,
                    "category": expense.category,
                    "date": str(expense.date)
                }
                for expense in recent_transactions
            ],
            "range": range
        }
    )