"""Add guild members

Revision ID: 66321ac7bf19
Revises: 846ebfe856c3
Create Date: 2023-08-09 17:01:36.873784+03:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '66321ac7bf19'
down_revision = '846ebfe856c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'members',
        sa.Column('guild_id', sa.BigInteger(), nullable=False, comment="The guild's unique ID"),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment="The user's unique ID"),
        sa.Column('display_name', sa.String(), nullable=True, comment="Discord guild member's name"),
        sa.Column('active', sa.Boolean(), nullable=False, comment='Currently in guild'),
        sa.ForeignKeyConstraint(['guild_id'], ['guilds.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('guild_id', 'user_id'),
        comment='Discord guild member',
    )


def downgrade() -> None:
    op.drop_table('members')
