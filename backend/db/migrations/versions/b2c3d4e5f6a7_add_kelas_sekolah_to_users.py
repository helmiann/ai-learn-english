"""add_kelas_sekolah_to_users

Revision ID: b2c3d4e5f6a7
Revises: 
Create Date: 2026-04-20

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = '006762e43fe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',
        sa.Column('kelas', sa.String(20), nullable=True)
    )
    op.add_column('users',
        sa.Column('sekolah', sa.String(100), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('users', 'sekolah')
    op.drop_column('users', 'kelas')