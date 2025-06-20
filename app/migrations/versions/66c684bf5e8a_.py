"""empty message

Revision ID: 66c684bf5e8a
Revises: 
Create Date: 2025-06-08 19:14:39.152533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66c684bf5e8a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'server_configs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('keyword', sa.String(), nullable=True),
        sa.Column('status_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )
    op.create_table(
        'leads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('phonecc', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('user_ip', sa.String(), nullable=True),
        sa.Column('aff_sub', sa.String(), nullable=True),
        sa.Column('aff_sub2', sa.String(), nullable=True),
        sa.Column('aff_sub3', sa.String(), nullable=True),
        sa.Column('aff_sub4', sa.String(), nullable=True),
        sa.Column('aff_id', sa.String(), nullable=True),
        sa.Column('offer_id', sa.String(), nullable=True),
        sa.Column('status_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('leads', schema='public')
    op.drop_table('server_configs', schema='public')
