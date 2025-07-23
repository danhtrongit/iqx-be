from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.securities import Securities
from app.schemas.securities import SecuritiesCreate, SecuritiesUpdate


def get_securities(db: Session, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[Securities]:
    """
    Get a list of securities with optional filtering, pagination
    """
    query = db.query(Securities)
    
    # Apply filters if provided
    if filters:
        filter_conditions = []
        for key, value in filters.items():
            if hasattr(Securities, key) and value is not None:
                filter_conditions.append(getattr(Securities, key) == value)
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))
    
    return query.offset(skip).limit(limit).all()


def count_securities(db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
    """
    Count total number of securities with optional filtering
    """
    query = db.query(func.count(Securities.ticker))
    
    # Apply filters if provided
    if filters:
        filter_conditions = []
        for key, value in filters.items():
            if hasattr(Securities, key) and value is not None:
                filter_conditions.append(getattr(Securities, key) == value)
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))
    
    return query.scalar()


def get_security_by_ticker(db: Session, ticker: str) -> Optional[Securities]:
    """
    Get a security by its ticker
    """
    return db.query(Securities).filter(Securities.ticker == ticker).first()


def get_security_by_isin(db: Session, isin_code: str) -> Optional[Securities]:
    """
    Get a security by its ISIN code
    """
    return db.query(Securities).filter(Securities.isin_code == isin_code).first()


def create_security(db: Session, security: SecuritiesCreate) -> Securities:
    """
    Create a new security
    """
    db_security = Securities(**security.dict())
    db.add(db_security)
    db.commit()
    db.refresh(db_security)
    return db_security


def update_security(db: Session, ticker: str, security: SecuritiesUpdate) -> Optional[Securities]:
    """
    Update a security by ticker
    """
    db_security = db.query(Securities).filter(Securities.ticker == ticker).first()
    if not db_security:
        return None
    
    update_data = security.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_security, key, value)
    
    db.commit()
    db.refresh(db_security)
    return db_security


def delete_security(db: Session, ticker: str) -> bool:
    """
    Delete a security by ticker
    """
    db_security = db.query(Securities).filter(Securities.ticker == ticker).first()
    if not db_security:
        return False
    
    db.delete(db_security)
    db.commit()
    return True 