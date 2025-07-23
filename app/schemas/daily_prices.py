from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, computed_field


class TimeRange(str, Enum):
    ONE_DAY = "1d"
    ONE_MONTH = "1m"
    THREE_MONTHS = "3m"
    SIX_MONTHS = "6m"
    ONE_YEAR = "1y"
    FIVE_YEARS = "5y"
    ALL = "all"


class DailyPriceBase(BaseModel):
    time: datetime = Field(..., description="Timestamp of the trading day")
    ticker: str = Field(..., description="Stock ticker symbol", max_length=10)

    open_price: Optional[float] = Field(None, description="Opening price")
    high_price: Optional[float] = Field(None, description="Highest price")
    low_price: Optional[float] = Field(None, description="Lowest price")
    close_price: Optional[float] = Field(None, description="Closing price")

    volume: Optional[int] = Field(None, description="Trading volume")
    price_change: Optional[float] = Field(None, description="Price change from previous day")
    percent_change: Optional[float] = Field(None, description="Percentage change")

    buy_order_value: Optional[float] = Field(None, description="Total buy order value")
    sell_order_value: Optional[float] = Field(None, description="Total sell order value")
    foreign_net_buy_value: Optional[float] = Field(None, description="Foreign net buy value")

    buy_order_quantity: Optional[int] = Field(None, description="Total buy order quantity")
    sell_order_quantity: Optional[int] = Field(None, description="Total sell order quantity")
    foreign_net_buy_quantity: Optional[int] = Field(None, description="Foreign net buy quantity")


class DailyPriceCreate(DailyPriceBase):
    pass


class DailyPriceUpdate(BaseModel):
    open_price: Optional[float] = Field(None, description="Opening price")
    high_price: Optional[float] = Field(None, description="Highest price")
    low_price: Optional[float] = Field(None, description="Lowest price")
    close_price: Optional[float] = Field(None, description="Closing price")

    volume: Optional[int] = Field(None, description="Trading volume")
    price_change: Optional[float] = Field(None, description="Price change from previous day")
    percent_change: Optional[float] = Field(None, description="Percentage change")

    buy_order_value: Optional[float] = Field(None, description="Total buy order value")
    sell_order_value: Optional[float] = Field(None, description="Total sell order value")
    foreign_net_buy_value: Optional[float] = Field(None, description="Foreign net buy value")

    buy_order_quantity: Optional[int] = Field(None, description="Total buy order quantity")
    sell_order_quantity: Optional[int] = Field(None, description="Total sell order quantity")
    foreign_net_buy_quantity: Optional[int] = Field(None, description="Foreign net buy quantity")


class DailyPriceResponse(DailyPriceBase):
    class Config:
        orm_mode = True


class ExtendedDailyPriceResponse(DailyPriceResponse):
    @computed_field
    def change(self) -> Optional[float]:
        """Mức độ thay đổi (tính theo phần trăm)."""
        if self.percent_change is not None:
            return self.percent_change * 100
        return None
    
    @computed_field
    def currentPrice(self) -> Optional[float]:
        """Giá hiện tại."""
        return self.close_price
    
    @computed_field
    def openPrice(self) -> Optional[float]:
        """Giá mở cửa."""
        return self.open_price
    
    @computed_field
    def highPrice(self) -> Optional[float]:
        """Giá cao nhất trong phiên."""
        return self.high_price
    
    @computed_field
    def lowPrice(self) -> Optional[float]:
        """Giá thấp nhất trong phiên."""
        return self.low_price
    
    @computed_field
    def totalVolume(self) -> Optional[int]:
        """Tổng khối lượng giao dịch."""
        return self.volume
    
    @computed_field
    def totalValue(self) -> Optional[float]:
        """Tổng giá trị giao dịch."""
        if self.volume is not None and self.close_price is not None:
            return self.volume * self.close_price
        return None
    
    class Config:
        orm_mode = True


class DailyPriceList(BaseModel):
    items: List[DailyPriceResponse]
    total: int


class ExtendedDailyPriceList(BaseModel):
    items: List[ExtendedDailyPriceResponse]
    total: int 