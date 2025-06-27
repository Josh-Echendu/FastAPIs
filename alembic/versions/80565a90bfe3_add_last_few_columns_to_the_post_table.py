"""add last few columns to the post table

Revision ID: 80565a90bfe3
Revises: 368d3e7041a4
Create Date: 2025-06-25 20:05:33.877717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80565a90bfe3'
down_revision: Union[str, Sequence[str], None] = '368d3e7041a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Add 'published' and 'created_at' columns to the 'posts' table."""
    # Add 'published' column
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False)
    )
    # Add 'created_at' column
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
    pass
