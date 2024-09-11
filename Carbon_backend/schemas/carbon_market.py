from datetime import date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel


# 查询返回类
class CarbonMarketHBResponse(BaseModel):
    id: str
    product: Optional[str]
    date: Optional[date]
    latest_price: Optional[Decimal]
    price_change: Optional[Decimal]
    highest_price: Optional[Decimal]
    lowest_price: Optional[Decimal]
    volume: Optional[int]
    turnover: Optional[Decimal]
    previous_close_price: Optional[Decimal]

    class Config:
        from_attributes = True


# 查询返回类,包含总条数
class CarbonMarketHBResponseWithTotal(BaseModel):
    total: int  # 返回数据总数
    items: List[CarbonMarketHBResponse]  # 返回的数据列表


# 查询请求类
class CarbonMarketHBQueryParams(BaseModel):
    dateRange: Optional[List[date]] = None
