"""Widen patient password hash column."""
from alembic import op
import sqlalchemy as sa


revision = 'f17a8c2d9b40'
down_revision = '0bba1a45e13a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'patients',
        'password',
        existing_type=sa.String(length=100),
        type_=sa.String(length=255),
        existing_nullable=False,
        nullable=False,
    )


def downgrade():
    op.alter_column(
        'patients',
        'password',
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
        existing_nullable=False,
        nullable=False,
    )