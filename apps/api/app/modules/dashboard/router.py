from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.dashboard.schemas import DashboardResponse
from app.modules.dashboard.service import get_dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=DashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.ACCOUNTANT,
            UserRole.SALES,
        )
    ),
):
    return get_dashboard(db)