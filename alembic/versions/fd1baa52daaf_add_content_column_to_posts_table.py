"""add content column to posts table

Revision ID: fd1baa52daaf
Revises: e11d373b47e0
Create Date: 2025-06-10 17:53:26.949967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd1baa52daaf'
down_revision: Union[str, None] = 'e11d373b47e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
