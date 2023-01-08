"""empty message

Revision ID: 79ef0ca35da0
Revises: 9a6246de8b65
Create Date: 2023-01-07 09:55:40.612083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79ef0ca35da0'
down_revision = '9a6246de8b65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('available_inventory', sa.Integer(), nullable=True))
    op.add_column('rental', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('rental', sa.Column('name', sa.String(), nullable=True))
    op.add_column('rental', sa.Column('videos_checked_out_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental', 'videos_checked_out_count')
    op.drop_column('rental', 'name')
    op.drop_column('rental', 'due_date')
    op.drop_column('rental', 'available_inventory')
    # ### end Alembic commands ###
