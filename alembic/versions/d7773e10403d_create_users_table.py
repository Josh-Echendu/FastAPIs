"""create users table

Revision ID: d7773e10403d
Revises: 06ba28eb8e3d
Create Date: 2025-06-25 19:24:18.131020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = 'd7773e10403d'
down_revision: Union[str, Sequence[str], None] = '06ba28eb8e3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema: Create the 'users' table."""
    op.create_table(
        "users",
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
