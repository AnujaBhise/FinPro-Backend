from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from middleware import get_db, get_current_user

from services.dashboardService import get_dashboard_overview

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard_overview(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_dashboard_overview(
        db,
        current_user.id
    )