from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.crud import securities as securities_crud
from app.schemas.securities import (
    SecuritiesCreate,
    SecuritiesResponse,
    SecuritiesList,
    SecuritiesUpdate,
)

router = APIRouter(tags=["securities"])


@router.post("/securities", response_model=SecuritiesResponse, status_code=status.HTTP_201_CREATED)
def create_security(
    security: SecuritiesCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new security.
    """
    # Check if security with same ticker already exists
    db_security = securities_crud.get_security_by_ticker(db, ticker=security.ticker)
    if db_security:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Security with ticker {security.ticker} already exists",
        )

    # Check if ISIN code is unique if provided
    if security.isin_code:
        db_security_isin = securities_crud.get_security_by_isin(db, isin_code=security.isin_code)
        if db_security_isin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Security with ISIN {security.isin_code} already exists",
            )

    return securities_crud.create_security(db=db, security=security)


@router.get("/securities", response_model=SecuritiesList)
def list_securities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ticker: Optional[str] = None,
    exchange: Optional[str] = None,
    status: Optional[str] = None,
    margin_status: Optional[str] = None,
) -> Any:
    """
    Retrieve securities with optional filtering.
    """
    # Build filter dict from parameters
    filters = {}
    if ticker:
        filters["ticker"] = ticker
    if exchange:
        filters["exchange"] = exchange
    if status:
        filters["status"] = status
    if margin_status:
        filters["margin_status"] = margin_status

    items = securities_crud.get_securities(db=db, skip=skip, limit=limit, filters=filters)
    total = securities_crud.count_securities(db=db, filters=filters)
    
    return {"items": items, "total": total}


@router.get("/securities/{ticker}", response_model=SecuritiesResponse)
def get_security(
    ticker: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get security details by ticker.
    """
    db_security = securities_crud.get_security_by_ticker(db=db, ticker=ticker)
    if not db_security:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security with ticker {ticker} not found",
        )
    return db_security


@router.put("/securities/{ticker}", response_model=SecuritiesResponse)
def update_security(
    ticker: str,
    security_update: SecuritiesUpdate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Update a security by ticker.
    """
    # Check if security exists
    db_security = securities_crud.get_security_by_ticker(db=db, ticker=ticker)
    if not db_security:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security with ticker {ticker} not found",
        )

    # Check if ISIN code is unique if being updated
    if security_update.isin_code:
        db_security_isin = securities_crud.get_security_by_isin(db=db, isin_code=security_update.isin_code)
        if db_security_isin and db_security_isin.ticker != ticker:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Security with ISIN {security_update.isin_code} already exists",
            )

    updated_security = securities_crud.update_security(
        db=db, ticker=ticker, security=security_update
    )
    return updated_security


@router.delete("/securities/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
def delete_security(
    ticker: str,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a security by ticker.
    """
    success = securities_crud.delete_security(db=db, ticker=ticker)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security with ticker {ticker} not found",
        )
    return None 