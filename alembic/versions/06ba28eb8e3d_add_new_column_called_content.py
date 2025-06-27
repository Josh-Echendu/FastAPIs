"""add new column called content

Revision ID: 06ba28eb8e3d
Revises: 21a1f5b5b568
Create Date: 2025-06-25 19:07:33.052460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06ba28eb8e3d'
down_revision: Union[str, Sequence[str], None] = '21a1f5b5b568'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
