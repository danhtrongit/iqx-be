"""add_securities_table

Revision ID: af7eb6952751
Revises: 11dc74dc385b
Create Date: 2025-07-17 08:45:26.835096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af7eb6952751'
down_revision: Union[str, Sequence[str], None] = '11dc74dc385b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'securities',
        # --- Primary identifiers ---
        sa.Column('ticker', sa.String(10), primary_key=True),
        sa.Column('isin_code', sa.String(20), unique=True),
        sa.Column('company_name', sa.String(255), nullable=False),
        sa.Column('short_name', sa.String(100)),
        sa.Column('description', sa.Text()),

        # --- Market and classification info ---
        sa.Column('exchange', sa.String(50)),
        sa.Column('industry_classification_code', sa.String(10)),
        sa.Column('company_type', sa.String(50)),
        sa.Column('country_code', sa.String(5)),

        # --- Listing information ---
        sa.Column('listing_date', sa.Date()),
        sa.Column('initial_listing_price', sa.Numeric(18, 2)),
        
        # --- Capital and share information ---
        sa.Column('charter_capital', sa.BigInteger()),
        sa.Column('issued_shares', sa.BigInteger()),
        sa.Column('outstanding_shares', sa.BigInteger()),
        sa.Column('free_float_shares', sa.BigInteger()),
        sa.Column('free_float_rate', sa.Float()),

        # --- Shareholder information ---
        sa.Column('shareholder_count', sa.Integer()),
        sa.Column('shareholder_record_date', sa.Date()),

        # --- Status & metadata ---
        sa.Column('margin_status', sa.String(20), server_default='not_allowed'),
        sa.Column('control_status', sa.String(50)),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('securities')
