
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.expenseSchema import (
    ExpenseCreate,
    ExpenseUpdate
)

from services.expenseService import (
    add_expense,
    get_all_expense,
    update_expense,
    delete_expense,
    download_excel,
    get_expense_overview
)

from middleware import get_db, get_current_user


router = APIRouter(
    prefix="/api/expense",
    tags=["Expense"]
)


# =========================================================
# Add Expense
# =========================================================
@router.post(
    "/add",
    summary="Add new expense"
)
def create_expense(
    expense_data: ExpenseCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new expense record.

    - **description**: Expense description
    - **amount**: Expense amount
    - **category**: Expense category
    - **date**: Expense date
    """

    return add_expense(
        db,
        current_user.id,
        expense_data
    )


# =========================================================
# Get All Expense
# =========================================================
@router.get(
    "/get",
    summary="Get all expense records"
)
def fetch_all_expense(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetch all expense records for logged-in user.
    """

    return get_all_expense(
        db,
        current_user.id
    )


# =========================================================
# Update Expense
# =========================================================
@router.put(
    "/update/{expense_id}",
    summary="Update expense by ID"
)
def edit_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update expense details.

    - **description**: Updated expense description
    - **amount**: Updated expense amount
    - **category**: Updated expense category
    - **date**: Updated expense date
    """

    return update_expense(
        db,
        current_user.id,
        expense_id,
        expense_data
    )


# =========================================================
# Delete Expense
# =========================================================
@router.delete(
    "/delete/{expense_id}",
    summary="Delete expense by ID"
)
def remove_expense(
    expense_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete expense record using expense ID.
    """

    return delete_expense(
        db,
        current_user.id,
        expense_id
    )


# =========================================================
# Download Excel Report
# =========================================================
@router.get(
    "/downloadexcel",
    summary="Download expense Excel report"
)
def export_expense_excel(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download expense records as Excel file.
    """

    return download_excel(
        db,
        current_user.id
    )


# =========================================================
# Expense Overview
# =========================================================
@router.get(
    "/overview",
    summary="Get expense dashboard overview"
)
def expense_overview(
    range: str = "monthly",
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get expense overview statistics.

    Available ranges:
    - daily
    - weekly
    - monthly
    - yearly
    """

    return get_expense_overview(
        db,
        current_user.id,
        range
    )