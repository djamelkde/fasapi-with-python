"""add foreign key to posts table

Revision ID: 2fe635b10cbb
Revises: c66b2a6000d8
Create Date: 2022-05-11 11:30:50.006613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fe635b10cbb'
down_revision = 'c66b2a6000d8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users",
    local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
