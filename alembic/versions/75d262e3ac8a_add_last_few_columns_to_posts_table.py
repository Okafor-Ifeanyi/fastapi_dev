"""add last few columns to posts table

Revision ID: 75d262e3ac8a
Revises: 266993bf09eb
Create Date: 2022-04-07 22:15:06.323298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75d262e3ac8a'
down_revision = '266993bf09eb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, Server_default= sa.text('now()') ))  
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
""