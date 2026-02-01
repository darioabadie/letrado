"""add user timezone

Revision ID: 0002_timezone
Revises: 0001_init
Create Date: 2026-02-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_timezone"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("timezone", sa.String(length=80), nullable=False, server_default="UTC"))
    op.alter_column("users", "timezone", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "timezone")
