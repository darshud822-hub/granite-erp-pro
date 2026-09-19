from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.journal_entries.schemas import (
    JournalEntryCreate,
    JournalEntryResponse,
)

from app.modules.journal_entries.service import (
    create_journal_entry,
    get_journal_entries,
    get_journal_entry,
    post_journal,
    delete_journal,
)

router = APIRouter(
    prefix="/journal-entries",
    tags=["Journal Entries"],
)


@router.post("/", response_model=JournalEntryResponse)
def create(
    data: JournalEntryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
        )
    ),
):
    try:
        return create_journal_entry(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[JournalEntryResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_journal_entries(db)


@router.get("/{journal_id}", response_model=JournalEntryResponse)
def get_one(
    journal_id: UUID,
    db: Session = Depends(get_db),
):
    journal = get_journal_entry(db, journal_id)

    if not journal:
        raise HTTPException(
            status_code=404,
            detail="Journal Entry not found",
        )

    return journal


@router.post("/{journal_id}/post")
def post(
    journal_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
        )
    ),
):
    journal = post_journal(
        db,
        journal_id,
    )

    if not journal:
        raise HTTPException(
            status_code=404,
            detail="Journal Entry not found",
        )

    return {
        "message": "Journal posted successfully"
    }


@router.delete("/{journal_id}")
def delete(
    journal_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        deleted = delete_journal(
            db,
            journal_id,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Journal Entry not found",
            )

        return {
            "message": "Journal deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )