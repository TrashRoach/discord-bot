"""Add sample users, guilds

Revision ID: 846ebfe856c3
Revises: 
Create Date: 2023-07-28 19:13:17.839794+03:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '846ebfe856c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='The user\'s unique ID.'),
        sa.Column('name', sa.String(), nullable=False, comment='The user\'s username.'),
        sa.Column('global_name', sa.String(), nullable=True, comment='The user\'s global nickname.'),
        sa.Column('avatar_url', sa.String(), nullable=True, comment='User avatar url'),
        sa.Column('bot', sa.Boolean(), nullable=False, comment='Specifies if the user is a bot account.'),
        sa.PrimaryKeyConstraint('id'),
        comment='Discord user',
    )
    op.create_table(
        'guilds',
        sa.Column('id', sa.BigInteger(), nullable=False, comment='Unique Discord ID'),
        sa.Column('name', sa.String(), nullable=False, comment='Guild name'),
        sa.Column('owner_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='Discord guild',
    )


def downgrade() -> None:
    op.drop_table('guilds')
    op.drop_table('users')
