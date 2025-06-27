"""create a new table called posts

Revision ID: 21a1f5b5b568
Revises: 
Create Date: 2025-06-25 18:33:26.745832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21a1f5b5b568'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts",  sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
