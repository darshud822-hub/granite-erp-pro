"""add user role

Revision ID: 2a20ab084064
Revises: d84ae3144ded
Create Date: 2026-07-18 14:10:28.783857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "2a20ab084064"
down_revision = "d84ae3144ded"
branch_labels = None
depends_on = None

userrole = sa.Enum(
    "ADMIN",
    "MANAGER",
    "SALES",
    "PRODUCTION",
    "PURCHASE",
    "ACCOUNTANT",
    name="userrole",
)

def upgrade():
    bind = op.get_bind()

    # Create enum type
    userrole.create(bind, checkfirst=True)

    # Add column
    op.add_column(
        "users",
        sa.Column(
            "role",
            userrole,
            nullable=False,
            server_default="SALES",
        ),
    )

    # Remove temporary default
    op.alter_column("users", "role", server_default=None)


def downgrade():
    op.drop_column("users", "role")
    userrole.drop(op.get_bind(), checkfirst=True)
