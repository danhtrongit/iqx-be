"""add_daily_prices_table

Revision ID: 4009a35da2f7
Revises: af7eb6952751
Create Date: 2025-07-17 11:36:35.330050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4009a35da2f7'
down_revision: Union[str, Sequence[str], None] = 'af7eb6952751'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'daily_prices',
        sa.Column('time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ticker', sa.String(10), nullable=False),
        sa.Column('open_price', sa.Numeric(18, 2), nullable=True),
        sa.Column('high_price', sa.Numeric(18, 2), nullable=True),
        sa.Column('low_price', sa.Numeric(18, 2), nullable=True),
        sa.Column('close_price', sa.Numeric(18, 2), nullable=True),
        sa.Column('volume', sa.BigInteger(), nullable=True),
        sa.Column('price_change', sa.Numeric(18, 2), nullable=True),
        sa.Column('percent_change', sa.Float(), nullable=True),
        sa.Column('buy_order_value', sa.Numeric(20, 2), nullable=True),
        sa.Column('sell_order_value', sa.Numeric(20, 2), nullable=True),
        sa.Column('foreign_net_buy_value', sa.Numeric(20, 2), nullable=True),
        sa.Column('buy_order_quantity', sa.BigInteger(), nullable=True),
        sa.Column('sell_order_quantity', sa.BigInteger(), nullable=True),
        sa.Column('foreign_net_buy_quantity', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['ticker'], ['securities.ticker'], ),
        sa.PrimaryKeyConstraint('time', 'ticker')
    )
    op.execute("SELECT create_hypertable('daily_prices', 'time');")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('daily_prices')
