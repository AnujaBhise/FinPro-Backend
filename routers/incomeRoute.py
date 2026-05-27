# routes/income_route.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.incomeSchema import (
    IncomeCreate,
    IncomeUpdate
)

from services.incomeService import (
    add_income,
    get_all_income,
    update_income,
    delete_income,
    download_excel,
    get_income_overview
)

from middleware import get_db, get_current_user

from utils.date_filter import get_date_range
router = APIRouter(
    prefix="/api/income",
    tags=["Income"]
)


# =========================================================
# Add Income
# =========================================================
@router.post(
    "/add",
    summary="Add new income"
)
def create_income(
    income_data: IncomeCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new income record.

    - **description**: Income description
    - **amount**: Income amount
    - **category**: Income category
    - **date**: Income date
    """

    return add_income(
        db,
        current_user.id,
        income_data
    )


# =========================================================
# Get All Income
# =========================================================
@router.get(
    "/get",
    summary="Get all income records"
)
def fetch_all_income(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetch all income records for logged-in user.
    """

    return get_all_income(
        db,
        current_user.id
    )


# =========================================================
# Update Income
# =========================================================
@router.put(
    "/update/{income_id}",
    summary="Update income by ID"
)
def edit_income(
    income_id: int,
    income_data: IncomeUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update income details.

    - **description**: Updated income description
    - **amount**: Updated income amount
    - **category**: Updated income category
    - **date**: Updated income date
    """

    return update_income(
        db,
        current_user.id,
        income_id,
        income_data
    )


# =========================================================
# Delete Income
# =========================================================
@router.delete(
    "/delete/{income_id}",
    summary="Delete income by ID"
)
def remove_income(
    income_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete income record using income ID.
    """

    return delete_income(
        db,
        current_user.id,
        income_id
    )


# =========================================================
# Download Excel Report
# =========================================================
@router.get(
    "/downloadexcel",
    summary="Download income Excel report"
)
def export_income_excel(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download income records as Excel file.
    """

    return download_excel(
        db,
        current_user.id
    )


# =========================================================
# Income Overview
# =========================================================
@router.get(
    "/overview",
    summary="Get income dashboard overview"
)
def income_overview(
    range: str = "monthly",
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get income overview statistics.

    Available ranges:
    - daily
    - weekly
    - monthly
    - yearly
    """

    return get_income_overview(
        db,
        current_user.id,
        range
    )