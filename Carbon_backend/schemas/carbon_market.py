from datetime import date
from decimal import Decimal
from typing import Optional, List, Union

from pydantic import BaseModel


class CarbonMarketOtherFactorsResponse(BaseModel):
    """外部因素返回类"""
    id: str
    date: Optional[date]
    gas_price: Optional[Decimal]
    coal_price: Optional[Decimal]
    oil_price: Optional[Decimal]
    hs300: Optional[Decimal]
    aql_sh: Optional[int]
    aql_gd: Optional[int]
    aql_hb: Optional[int]
    si: Optional[Decimal]
    eua_price: Optional[Decimal]

    class Config:
        from_attributes = True
        orm_mode = True  # 启用 orm_mode

class HBCarbonMarketResponse(BaseModel):
    """湖北碳市场返回类"""
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
        orm_mode = True  # 启用 orm_mode


class GDCarbonMarketResponse(BaseModel):
    """广东碳市场返回类"""
    id: str
    product: Optional[str]
    date: Optional[date]
    opening_price: Optional[Decimal]
    closing_price: Optional[Decimal]
    highest_price: Optional[Decimal]
    lowest_price: Optional[Decimal]
    price_change: Optional[Decimal]
    price_change_percentage: Optional[Decimal]
    volume: Optional[int]
    turnover: Optional[Decimal]

    class Config:
        from_attributes = True
        orm_mode = True


class TJCarbonMarketResponse(BaseModel):
    """天津碳市场返回类"""
    id: str
    product: Optional[str]
    date: Optional[date]
    volume_auction: Optional[int]
    volume_daily_summary: Optional[int]
    turnover_auction: Optional[Decimal]
    turnover_daily_summary: Optional[Decimal]
    average_price_auction: Optional[Decimal]

    class Config:
        from_attributes = True
        orm_mode = True


class BJCarbonMarketResponse(BaseModel):
    """北京碳市场返回类"""
    id: str
    date: Optional[date]
    volume: Optional[int]
    average_price: Optional[Decimal]
    turnover: Optional[Decimal]

    class Config:
        from_attributes = True
        orm_mode = True


# 查询返回类,包含总条数
class CarbonMarketResponseWithTotal(BaseModel):
    total: int
    items: Union[List[HBCarbonMarketResponse], List[GDCarbonMarketResponse], List[TJCarbonMarketResponse], List[
        BJCarbonMarketResponse]]

    class Config:
        orm_mode = True

# 查询请求类
class CarbonMarketHBQueryParams(BaseModel):
    dateRange: Optional[List[date]] = None


class CarbonMarketDatePriceResponse(BaseModel):
    """日期与碳价格"""
    x: Optional[date]  # 日期
    y: Optional[Decimal]  # 最新成交价格

    class Config:
        from_attributes = True

# 查询返回类，只查询日期与碳价格
class CarbonMarketDatePriceResponseList(BaseModel):
    total: int
    items: List[CarbonMarketDatePriceResponse]