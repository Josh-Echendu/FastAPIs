"""add foreign key column to the posts table

Revision ID: f0195fd6a3b1
Revises: d7773e10403d
Create Date: 2025-06-25 19:41:57.626220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0195fd6a3b1'
down_revision: Union[str, Sequence[str], None] = 'd7773e10403d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table='users',
    local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
