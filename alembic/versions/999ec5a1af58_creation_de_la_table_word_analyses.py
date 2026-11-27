"""Creation de la table word_analyses

Revision ID: 999ec5a1af58
Revises: 
Create Date: 2026-11-26 23:57:11.717364

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '999ec5a1af58'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'word_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('analysis_result', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_word_analyses_id'), 'word_analyses', ['id'], unique=False)
    op.create_index(op.f('ix_word_analyses_word'), 'word_analyses', ['word'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_word_analyses_word'), table_name='word_analyses')
    op.drop_index(op.f('ix_word_analyses_id'), table_name='word_analyses')
    op.drop_table('word_analyses')