"""add content column to posts table

Revision ID: 6b2c5d21b0f9
Revises: 4ba5099a96c6
Create Date: 2023-06-27 11:21:59.192634

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "6b2c5d21b0f9"
down_revision = "4ba5099a96c6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("p_content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "p_content")
    pass
