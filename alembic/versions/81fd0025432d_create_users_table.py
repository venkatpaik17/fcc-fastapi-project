"""create users table

Revision ID: 81fd0025432d
Revises: 6b2c5d21b0f9
Create Date: 2023-06-27 11:34:42.376462

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "81fd0025432d"
down_revision = "6b2c5d21b0f9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("u_id", sa.Integer(), nullable=False),
        sa.Column("u_email", sa.String(), nullable=False),
        sa.Column("u_password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("u_id"),
        sa.UniqueConstraint("u_email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
