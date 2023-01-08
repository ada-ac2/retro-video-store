"""empty message

Revision ID: 9a6246de8b65
Revises: 66b1b8ce0a47
Create Date: 2023-01-07 07:30:58.186185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a6246de8b65'
down_revision = '66b1b8ce0a47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental', 'videos_checked_out_count')
    op.drop_column('rental', 'name')
    op.drop_column('rental', 'due_date')
    op.drop_column('rental', 'available_inventory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('available_inventory', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('rental', sa.Column('due_date', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('rental', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('rental', sa.Column('videos_checked_out_count', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
