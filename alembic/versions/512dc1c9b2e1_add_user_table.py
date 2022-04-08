"""add user table

Revision ID: 512dc1c9b2e1
Revises: f62cc16c6ec4
Create Date: 2022-04-07 21:45:27.248843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '512dc1c9b2e1'
down_revision = 'f62cc16c6ec4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()') , nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
                )

    pass


def downgrade():
    op.drop_table('users')
    pass
