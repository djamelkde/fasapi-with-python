"""create posts table

Revision ID: b8548b922485
Revises: 
Create Date: 2022-05-11 10:57:11.894531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8548b922485'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))


def downgrade():
    op.drop_table("posts")
    pass
