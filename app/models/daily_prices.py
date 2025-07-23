from sqlalchemy import Column, String, Numeric, BigInteger, Float, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class DailyPrice(Base):
    __tablename__ = "daily_prices"

    # --- Primary key and foreign key ---
    time = Column(DateTime(timezone=True), nullable=False)
    ticker = Column(String(10), ForeignKey("securities.ticker"), nullable=False)

    # --- Basic price data (OHLC) ---
    open_price = Column(Numeric(18, 2))
    high_price = Column(Numeric(18, 2))
    low_price = Column(Numeric(18, 2))
    close_price = Column(Numeric(18, 2))

    # --- Transaction data ---
    volume = Column(BigInteger)
    price_change = Column(Numeric(18, 2))
    percent_change = Column(Float)

    # --- Foreign trade and cash flow data ---
    buy_order_value = Column(Numeric(20, 2))
    sell_order_value = Column(Numeric(20, 2))
    foreign_net_buy_value = Column(Numeric(20, 2))
    
    buy_order_quantity = Column(BigInteger)
    sell_order_quantity = Column(BigInteger)
    foreign_net_buy_quantity = Column(BigInteger)
    
    # --- Primary key and relationship ---
    __table_args__ = (
        PrimaryKeyConstraint('time', 'ticker'),
    )
    
    security = relationship("Securities") 