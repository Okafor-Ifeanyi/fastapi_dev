"""add content column to post table

Revision ID: f62cc16c6ec4
Revises: d6af46d6205b
Create Date: 2022-04-07 21:23:50.760854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f62cc16c6ec4'
down_revision = 'd6af46d6205b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
