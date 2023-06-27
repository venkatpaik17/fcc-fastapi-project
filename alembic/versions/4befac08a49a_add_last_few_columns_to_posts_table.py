"""add last few columns to posts table

Revision ID: 4befac08a49a
Revises: faf7822bc92d
Create Date: 2023-06-27 12:01:01.848422

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4befac08a49a"
down_revision = "faf7822bc92d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
