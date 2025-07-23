from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class SecuritiesBase(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol", max_length=10)
    isin_code: Optional[str] = Field(None, description="ISIN code", max_length=20)
    company_name: str = Field(..., description="Full company name", max_length=255)
    short_name: Optional[str] = Field(None, description="Company short name", max_length=100)
    description: Optional[str] = Field(None, description="Company description")
    exchange: Optional[str] = Field(None, description="Stock exchange", max_length=50)
    industry_classification_code: Optional[str] = Field(None, description="Industry classification code", max_length=10)
    company_type: Optional[str] = Field(None, description="Company type", max_length=50)
    country_code: Optional[str] = Field(None, description="Country code", max_length=5)
    listing_date: Optional[date] = Field(None, description="Listing date")
    initial_listing_price: Optional[float] = Field(None, description="Initial listing price")
    charter_capital: Optional[int] = Field(None, description="Charter capital")
    issued_shares: Optional[int] = Field(None, description="Number of issued shares")
    outstanding_shares: Optional[int] = Field(None, description="Number of outstanding shares")
    free_float_shares: Optional[int] = Field(None, description="Number of free float shares")
    free_float_rate: Optional[float] = Field(None, description="Free float rate")
    shareholder_count: Optional[int] = Field(None, description="Number of shareholders")
    shareholder_record_date: Optional[date] = Field(None, description="Date of shareholder record")
    margin_status: Optional[str] = Field("not_allowed", description="Margin status", max_length=20)
    control_status: Optional[str] = Field(None, description="Control status", max_length=50)
    status: Optional[str] = Field("active", description="Status", max_length=20)


class SecuritiesCreate(SecuritiesBase):
    pass


class SecuritiesUpdate(BaseModel):
    isin_code: Optional[str] = Field(None, description="ISIN code", max_length=20)
    company_name: Optional[str] = Field(None, description="Full company name", max_length=255)
    short_name: Optional[str] = Field(None, description="Company short name", max_length=100)
    description: Optional[str] = Field(None, description="Company description")
    exchange: Optional[str] = Field(None, description="Stock exchange", max_length=50)
    industry_classification_code: Optional[str] = Field(None, description="Industry classification code", max_length=10)
    company_type: Optional[str] = Field(None, description="Company type", max_length=50)
    country_code: Optional[str] = Field(None, description="Country code", max_length=5)
    listing_date: Optional[date] = Field(None, description="Listing date")
    initial_listing_price: Optional[float] = Field(None, description="Initial listing price")
    charter_capital: Optional[int] = Field(None, description="Charter capital")
    issued_shares: Optional[int] = Field(None, description="Number of issued shares")
    outstanding_shares: Optional[int] = Field(None, description="Number of outstanding shares")
    free_float_shares: Optional[int] = Field(None, description="Number of free float shares")
    free_float_rate: Optional[float] = Field(None, description="Free float rate")
    shareholder_count: Optional[int] = Field(None, description="Number of shareholders")
    shareholder_record_date: Optional[date] = Field(None, description="Date of shareholder record")
    margin_status: Optional[str] = Field(None, description="Margin status", max_length=20)
    control_status: Optional[str] = Field(None, description="Control status", max_length=50)
    status: Optional[str] = Field(None, description="Status", max_length=20)


class SecuritiesResponse(SecuritiesBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SecuritiesList(BaseModel):
    items: List[SecuritiesResponse]
    total: int 