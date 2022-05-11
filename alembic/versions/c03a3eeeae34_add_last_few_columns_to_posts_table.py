"""add last few columns to posts table

Revision ID: c03a3eeeae34
Revises: 2fe635b10cbb
Create Date: 2022-05-11 11:39:45.415751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c03a3eeeae34'
down_revision = '2fe635b10cbb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("published", sa.Boolean(), nullable=False, server_default="True"))
    op.add_column("posts", sa.Column("creation_date", sa.TIMESTAMP(timezone=True), 
                          server_default=sa.text("now()"), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "creation_date")
    pass
