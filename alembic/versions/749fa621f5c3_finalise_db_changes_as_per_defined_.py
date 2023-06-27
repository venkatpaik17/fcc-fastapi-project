"""finalise db changes as per defined models. Adds votes table.

Revision ID: 749fa621f5c3
Revises: 4befac08a49a
Create Date: 2023-06-27 12:18:15.400280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '749fa621f5c3'
down_revision = '4befac08a49a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.p_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.u_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
