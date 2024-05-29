"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-05-15 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '0001_initial_migration'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=25), nullable=False),
        sa.Column('sub_directory', sa.String(length=150), nullable=False),
        sa.Column('first_name', sa.String(length=25), nullable=False),
        sa.Column('last_name', sa.String(length=25), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_sub_directory'), 'user', ['sub_directory'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table(
        'shortener_url',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('short_url', sa.String(length=5), nullable=False),
        sa.Column('original_url', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('short_url', 'user_id', name='unique_short_url_user_id')
    )
    op.create_index(
        'index_short_url_user_id', 'shortener_url', ['short_url', 'user_id'], unique=False
    )
    op.create_index(op.f('ix_shortener_url_id'), 'shortener_url', ['id'], unique=False)
    op.create_index(op.f('ix_shortener_url_short_url'), 'shortener_url', ['short_url'], unique=False)
    op.create_index(op.f('ix_shortener_url_user_id'), 'shortener_url', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_shortener_url_user_id'), table_name='shortener_url')
    op.drop_index(op.f('ix_shortener_url_short_url'), table_name='shortener_url')
    op.drop_index(op.f('ix_shortener_url_id'), table_name='shortener_url')
    op.drop_index('index_short_url_user_id', table_name='shortener_url')
    op.drop_table('shortener_url')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_sub_directory'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
