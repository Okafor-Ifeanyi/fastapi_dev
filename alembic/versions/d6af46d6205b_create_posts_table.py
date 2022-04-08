"""create posts table

Revision ID: d6af46d6205b
Revises: 
Create Date: 2022-04-07 20:25:35.708889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6af46d6205b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, 
                        primary_key=True), sa.Column('title', sa.String(), nullable=False))
    
    pass


def me():
    op.drop_table('posts')
    pass
