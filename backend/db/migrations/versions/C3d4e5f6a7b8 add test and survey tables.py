"""add_test_and_survey_tables

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-04-24

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'test_results',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('test_type', sa.String(10), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('correct', sa.Integer(), nullable=False),
        sa.Column('total', sa.Integer(), nullable=False),
        sa.Column('answers', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_test_results_id_user', 'test_results', ['id_user'])

    op.create_table(
        'survey_results',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('answers', sa.JSON(), nullable=False),
        sa.Column('saran', sa.Text(), nullable=True),
        sa.Column('avg_context', sa.Float(), nullable=False),
        sa.Column('avg_usability', sa.Float(), nullable=False),
        sa.Column('avg_learning', sa.Float(), nullable=False),
        sa.Column('avg_total', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_survey_results_id_user', 'survey_results', ['id_user'])


def downgrade() -> None:
    op.drop_index('ix_survey_results_id_user', table_name='survey_results')
    op.drop_table('survey_results')
    op.drop_index('ix_test_results_id_user', table_name='test_results')
    op.drop_table('test_results')