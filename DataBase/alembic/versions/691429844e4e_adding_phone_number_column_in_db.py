"""Adding phone number column in db

Revision ID: 691429844e4e
Revises: 
Create Date: 2026-09-23 16:02:48.923956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '691429844e4e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users' , sa.Column('phone_number' , sa.String() ,nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users' , 'phone_number')
