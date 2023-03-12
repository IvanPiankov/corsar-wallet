"""init db

Revision ID: defae579ae42
Revises: 
Create Date: 2023-03-12 09:47:48.469150

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'defae579ae42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('wallet_currency', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )

    op.create_table('wallets',
    sa.Column('wallet_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('wallet_type', postgresql.ENUM('CASH', 'CARD', 'SAVINGS_ACCOUNT', 'DEPOSIT_ACCOUNT', name='account_types'), nullable=False),
    sa.Column('balance', sa.DECIMAL(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('wallet_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallets')
    op.drop_table('users')
    # ### end Alembic commands ###
