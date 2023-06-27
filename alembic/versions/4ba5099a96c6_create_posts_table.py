"""create posts table

Revision ID: 4ba5099a96c6
Revises: 
Create Date: 2023-06-27 10:56:32.512162

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4ba5099a96c6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("p_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("p_title", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
