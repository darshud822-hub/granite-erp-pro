from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.cash_flow.schemas import (
    CashFlowResponse,
)
from app.modules.cash_flow.service import (
    get_cash_flow,
)

router = APIRouter(
    prefix="/cash-flow",
    tags=["Cash Flow"],
)


@router.get(
    "/",
    response_model=CashFlowResponse,
)
def cash_flow(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.MANAGER,
        )
    ),
):
    return get_cash_flow(db)