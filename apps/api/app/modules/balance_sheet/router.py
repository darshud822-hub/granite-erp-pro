from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.balance_sheet.schemas import (
    BalanceSheetResponse,
)
from app.modules.balance_sheet.service import (
    get_balance_sheet,
)

router = APIRouter(
    prefix="/balance-sheet",
    tags=["Balance Sheet"],
)


@router.get(
    "/",
    response_model=BalanceSheetResponse,
)
def balance_sheet(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.MANAGER,
        )
    ),
):
    return get_balance_sheet(db)