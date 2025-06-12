"""add foreign-key to post table

Revision ID: f9899444a56f
Revises: 68335c1d688f
Create Date: 2025-06-11 22:48:01.956061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9899444a56f'
down_revision: Union[str, None] = '68335c1d688f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_users', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('fk_posts_users', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
