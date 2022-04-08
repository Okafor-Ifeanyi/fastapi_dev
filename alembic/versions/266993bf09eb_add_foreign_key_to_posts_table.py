"""add foreign-key to posts table

Revision ID: 266993bf09eb
Revises: 512dc1c9b2e1
Create Date: 2022-04-07 22:05:44.098683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '266993bf09eb'
down_revision = '512dc1c9b2e1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", 
                local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column('posts', "owner_id")
    pass
