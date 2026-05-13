"""add_score_per_section_to_test_results

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-05-01

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('test_results',
        sa.Column('score_simple_present', sa.Integer(), nullable=True, server_default='0')
    )
    op.add_column('test_results',
        sa.Column('score_simple_past', sa.Integer(), nullable=True, server_default='0')
    )
    op.add_column('test_results',
        sa.Column('score_irregular_verbs', sa.Integer(), nullable=True, server_default='0')
    )
    op.add_column('test_results',
        sa.Column('score_imperative', sa.Integer(), nullable=True, server_default='0')
    )


def downgrade() -> None:
    op.drop_column('test_results', 'score_imperative')
    op.drop_column('test_results', 'score_irregular_verbs')
    op.drop_column('test_results', 'score_simple_past')
    op.drop_column('test_results', 'score_simple_present')