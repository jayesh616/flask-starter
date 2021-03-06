""" User

Revision ID: 3a9f65801ff9
Revises: 
Create Date: 2018-10-25 17:37:03.538311

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime


# revision identifiers, used by Alembic.
revision = '3a9f65801ff9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('password', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=80), nullable=False),
        sa.Column('is_active', sa.BOOLEAN, nullable=False, default=False),
        sa.Column('is_email_verified', sa.BOOLEAN, nullable=False, default=False),
        sa.Column('created_at', DateTime(timezone=True)),
        sa.Column('updated_at', DateTime(timezone=True)),
        sa.Column('deleted_at', DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    )
    op.create_unique_constraint(op.f('uq_users_email'), 'users', ['email'])


def downgrade():
    op.drop_table('users')
