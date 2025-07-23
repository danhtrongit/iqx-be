from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.daily_prices import DailyPrice
from app.schemas.daily_prices import DailyPriceCreate, DailyPriceUpdate


def get_daily_prices(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None,
) -> List[DailyPrice]:
    """
    Get a list of daily prices with optional filtering, pagination.
    Results are ordered by time descending (newest first).
    """
    query = db.query(DailyPrice)

    if filters:
        filter_conditions = []
        for key, value in filters.items():
            if hasattr(DailyPrice, key) and value is not None:
                filter_conditions.append(getattr(DailyPrice, key) == value)
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

    return query.order_by(DailyPrice.time.desc()).offset(skip).limit(limit).all()


def get_daily_prices_by_time_range(
    db: Session,
    ticker: str,
    time_range: str,
    limit: int = 10000,
) -> List[DailyPrice]:
    """
    Get daily prices for a specific ticker filtered by time range.
    Time range can be: 1d, 1m, 3m, 6m, 1y, 5y, all
    Results are ordered by time descending (newest first).
    """
    query = db.query(DailyPrice).filter(DailyPrice.ticker == ticker)
    
    # Get current date for calculations
    now = datetime.utcnow()
    
    # Apply time range filter
    if time_range == "1d":
        one_day_ago = now - timedelta(days=1)
        query = query.filter(DailyPrice.time >= one_day_ago)
    elif time_range == "1m":
        one_month_ago = now - timedelta(days=30)
        query = query.filter(DailyPrice.time >= one_month_ago)
    elif time_range == "3m":
        three_months_ago = now - timedelta(days=90)
        query = query.filter(DailyPrice.time >= three_months_ago)
    elif time_range == "6m":
        six_months_ago = now - timedelta(days=180)
        query = query.filter(DailyPrice.time >= six_months_ago)
    elif time_range == "1y":
        one_year_ago = now - timedelta(days=365)
        query = query.filter(DailyPrice.time >= one_year_ago)
    elif time_range == "5y":
        five_years_ago = now - timedelta(days=365*5)
        query = query.filter(DailyPrice.time >= five_years_ago)
    # For "all", no time filtering needed
    
    return query.order_by(DailyPrice.time.desc()).limit(limit).all()


def count_daily_prices(db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
    """
    Count total number of daily prices with optional filtering.
    """
    query = db.query(func.count(DailyPrice.time))

    if filters:
        filter_conditions = []
        for key, value in filters.items():
            if hasattr(DailyPrice, key) and value is not None:
                filter_conditions.append(getattr(DailyPrice, key) == value)
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

    return query.scalar()


def get_daily_price_by_ticker_and_time(
    db: Session, ticker: str, time: datetime
) -> Optional[DailyPrice]:
    """
    Get a daily price by its ticker and time.
    """
    return (
        db.query(DailyPrice)
        .filter(DailyPrice.ticker == ticker, DailyPrice.time == time)
        .first()
    )


def create_daily_price(db: Session, daily_price: DailyPriceCreate) -> DailyPrice:
    """
    Create a new daily price.
    """
    db_daily_price = DailyPrice(**daily_price.dict())
    db.add(db_daily_price)
    db.commit()
    db.refresh(db_daily_price)
    return db_daily_price


def update_daily_price(
    db: Session, ticker: str, time: datetime, daily_price: DailyPriceUpdate
) -> Optional[DailyPrice]:
    """
    Update a daily price by ticker and time.
    """
    db_daily_price = get_daily_price_by_ticker_and_time(db, ticker, time)
    if not db_daily_price:
        return None

    update_data = daily_price.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_daily_price, key, value)

    db.commit()
    db.refresh(db_daily_price)
    return db_daily_price


def delete_daily_price(db: Session, ticker: str, time: datetime) -> bool:
    """
    Delete a daily price by ticker and time.
    """
    db_daily_price = get_daily_price_by_ticker_and_time(db, ticker, time)
    if not db_daily_price:
        return False

    db.delete(db_daily_price)
    db.commit()
    return True 