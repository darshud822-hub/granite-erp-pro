from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.profit_and_loss.schemas import (
    ProfitLossResponse,
)
from app.modules.profit_and_loss.service import (
    get_profit_and_loss,
)

router = APIRouter(
    prefix="/profit-and-loss",
    tags=["Profit & Loss"],
)


@router.get(
    "/",
    response_model=ProfitLossResponse,
)
def profit_and_loss(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.MANAGER,
        )
    ),
):
    return get_profit_and_loss(db)