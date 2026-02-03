"""add onboarding fields to users

Revision ID: 0003_add_user_onboarding_fields
Revises: 0002_timezone
Create Date: 2026-02-03 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0003_add_user_onboarding_fields"
down_revision = "0002_timezone"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("onboarding_step", sa.String(length=40), nullable=True))
    op.add_column(
        "users",
        sa.Column("preferred_hour", sa.Integer(), nullable=False, server_default="9"),
    )
    op.alter_column("users", "preferred_hour", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "preferred_hour")
    op.drop_column("users", "onboarding_step")
