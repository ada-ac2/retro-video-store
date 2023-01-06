"""add get_by_id cls method

Revision ID: 339d00a1251d
Revises: bee1f9af5c8f
Create Date: 2023-01-05 21:46:11.311294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '339d00a1251d'
down_revision = 'bee1f9af5c8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer_video', sa.Column('due_date', sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer_video', 'due_date')
    # ### end Alembic commands ###
