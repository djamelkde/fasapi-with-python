"""add users table

Revision ID: c66b2a6000d8
Revises: 76c301a8e546
Create Date: 2022-05-11 11:18:24.471910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c66b2a6000d8'
down_revision = '76c301a8e546'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                sa.Column("id", sa.Integer(), nullable=False),
                sa.Column("email", sa.String(), nullable=False),
                sa.Column("password", sa.String(), nullable=False),
                sa.Column("creation_date", sa.String(), nullable=False),
                sa.Column("creation_date", sa.TIMESTAMP(timezone=True), 
                          server_default=sa.text("now()"), nullable=False),
                sa.PrimaryKeyConstraint("id"),
                sa.UniqueConstraint("email")
                )
            
    pass


def downgrade():
    op.drop_table("users")
    pass
