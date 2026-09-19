from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.trial_balance.schemas import (
    TrialBalanceResponse,
)

from app.modules.trial_balance.service import (
    get_trial_balance,
)

router = APIRouter(
    prefix="/trial-balance",
    tags=["Trial Balance"],
)


@router.get(
    "/",
    response_model=TrialBalanceResponse,
)
def trial_balance(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.MANAGER,
        )
    ),
):
    return get_trial_balance(db)