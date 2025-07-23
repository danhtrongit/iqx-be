from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.crud import daily_prices as daily_prices_crud
from app.crud import securities as securities_crud
from app.schemas.daily_prices import (
    DailyPriceCreate,
    DailyPriceList,
    DailyPriceResponse,
    DailyPriceUpdate,
    TimeRange,
    ExtendedDailyPriceResponse,
    ExtendedDailyPriceList,
)

router = APIRouter(tags=["daily-prices"])


@router.post(
    "/daily-prices",
    response_model=ExtendedDailyPriceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_daily_price(
    daily_price: DailyPriceCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new daily price record.
    """
    # Check if the associated security exists
    db_security = securities_crud.get_security_by_ticker(db, ticker=daily_price.ticker)
    if not db_security:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security with ticker {daily_price.ticker} not found",
        )

    # Check if a daily price for this ticker and time already exists
    db_daily_price = daily_prices_crud.get_daily_price_by_ticker_and_time(
        db, ticker=daily_price.ticker, time=daily_price.time
    )
    if db_daily_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Daily price for ticker {daily_price.ticker} at {daily_price.time} already exists",
        )

    return daily_prices_crud.create_daily_price(db=db, daily_price=daily_price)


@router.get("/daily-prices", response_model=ExtendedDailyPriceList)
def list_daily_prices(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ticker: Optional[str] = Query(None, description="Filter by ticker symbol"),
) -> Any:
    """
    Retrieve daily prices with optional filtering.
    """
    filters = {}
    if ticker:
        filters["ticker"] = ticker

    items = daily_prices_crud.get_daily_prices(
        db=db, skip=skip, limit=limit, filters=filters
    )
    total = daily_prices_crud.count_daily_prices(db=db, filters=filters)

    return {"items": items, "total": total}


@router.get("/daily-prices/{ticker}/range/{time_range}", response_model=ExtendedDailyPriceList)
def get_daily_prices_by_time_range(
    ticker: str = Path(..., description="Ticker symbol of the security"),
    time_range: TimeRange = Path(..., description="Time range for data retrieval"),
    limit: int = Query(10000, ge=1, le=50000, description="Maximum number of data points to return"),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get daily prices for a specific ticker based on predefined time range.
    
    Available time ranges:
    - 1d: Last 24 hours
    - 1m: Last 30 days
    - 3m: Last 90 days
    - 6m: Last 180 days
    - 1y: Last 365 days
    - 5y: Last 5 years
    - all: All available data
    """
    # Check if the security exists
    db_security = securities_crud.get_security_by_ticker(db, ticker=ticker)
    if not db_security:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security with ticker {ticker} not found",
        )
    
    items = daily_prices_crud.get_daily_prices_by_time_range(
        db=db, ticker=ticker, time_range=time_range, limit=limit
    )
    
    # Count items for response
    total = len(items)
    
    return {"items": items, "total": total}


@router.get("/daily-prices/{ticker}/{time}", response_model=ExtendedDailyPriceResponse)
def get_daily_price(
    ticker: str,
    time: datetime,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific daily price by ticker and time.
    """
    db_daily_price = daily_prices_crud.get_daily_price_by_ticker_and_time(
        db=db, ticker=ticker, time=time
    )
    if not db_daily_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Daily price for ticker {ticker} at {time} not found",
        )
    return db_daily_price


@router.put("/daily-prices/{ticker}/{time}", response_model=ExtendedDailyPriceResponse)
def update_daily_price(
    ticker: str,
    time: datetime,
    daily_price_update: DailyPriceUpdate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Update a daily price record.
    """
    updated_daily_price = daily_prices_crud.update_daily_price(
        db=db, ticker=ticker, time=time, daily_price=daily_price_update
    )
    if not updated_daily_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Daily price for ticker {ticker} at {time} not found",
        )
    return updated_daily_price


@router.delete("/daily-prices/{ticker}/{time}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_price(
    ticker: str,
    time: datetime,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a daily price record.
    """
    success = daily_prices_crud.delete_daily_price(db=db, ticker=ticker, time=time)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Daily price for ticker {ticker} at {time} not found",
        )
    return None 