"""add content column to posts table

Revision ID: 76c301a8e546
Revises: b8548b922485
Create Date: 2022-05-11 11:08:14.863199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c301a8e546'
down_revision = 'b8548b922485'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
