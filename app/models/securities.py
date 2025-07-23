from sqlalchemy import Column, String, Text, Date, Numeric, BigInteger, Integer, Float, DateTime, func

from app.core.database import Base


class Securities(Base):
    __tablename__ = "securities"

    # --- Primary identifiers ---
    ticker = Column(String(10), primary_key=True)
    isin_code = Column(String(20), unique=True)
    company_name = Column(String(255), nullable=False)
    short_name = Column(String(100))
    description = Column(Text)

    # --- Market and classification info ---
    exchange = Column(String(50))
    industry_classification_code = Column(String(10))
    company_type = Column(String(50))
    country_code = Column(String(5))

    # --- Listing information ---
    listing_date = Column(Date)
    initial_listing_price = Column(Numeric(18, 2))
    
    # --- Capital and share information ---
    charter_capital = Column(BigInteger)
    issued_shares = Column(BigInteger)
    outstanding_shares = Column(BigInteger)
    free_float_shares = Column(BigInteger)
    free_float_rate = Column(Float)

    # --- Shareholder information ---
    shareholder_count = Column(Integer)
    shareholder_record_date = Column(Date)

    # --- Status & metadata ---
    margin_status = Column(String(20), default="not_allowed")
    control_status = Column(String(50))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()) 