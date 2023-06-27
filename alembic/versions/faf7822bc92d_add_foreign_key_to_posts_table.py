"""add foreign-key to posts table

Revision ID: faf7822bc92d
Revises: 81fd0025432d
Create Date: 2023-06-27 11:48:29.291960

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "faf7822bc92d"
down_revision = "81fd0025432d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["u_id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
