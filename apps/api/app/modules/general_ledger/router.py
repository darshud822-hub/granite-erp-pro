from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.general_ledger.service import (
    get_general_ledger,
)

router = APIRouter(
    prefix="/general-ledger",
    tags=["General Ledger"],
)


@router.get("/{account_id}")
def ledger(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.MANAGER,
        )
    ),
):
    return get_general_ledger(
        db,
        account_id,
    )