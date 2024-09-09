import uuid

from sqlalchemy import Column, String, Date, DECIMAL, Integer

from db.session import Base


class CarbonMarketHB(Base):
    __tablename__ = 'carbon_market_hb'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    product = Column(String(255))
    date = Column(Date)
    latest_price = Column(DECIMAL(10, 2))
    price_change = Column(DECIMAL(10, 4))
    highest_price = Column(DECIMAL(10, 2))
    lowest_price = Column(DECIMAL(10, 2))
    volume = Column(Integer)
    turnover = Column(DECIMAL(15, 2))
    previous_close_price = Column(DECIMAL(10, 2))


class CarbonMarketGD(Base):
    __tablename__ = 'carbon_market_gd'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    date = Column(Date)
    product = Column(String(255))
    opening_price = Column(DECIMAL(10, 2))
    closing_price = Column(DECIMAL(10, 2))
    highest_price = Column(DECIMAL(10, 2))
    lowest_price = Column(DECIMAL(10, 2))
    price_change = Column(DECIMAL(10, 2))
    price_change_percentage = Column(DECIMAL(10, 4))
    volume = Column(Integer)
    turnover = Column(DECIMAL(15, 2))


class CarbonMarketTJ(Base):
    __tablename__ = 'carbon_market_tj'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    date = Column(Date)
    product = Column(String(255))
    volume_auction = Column(Integer)
    volume_daily_summary = Column(Integer)
    turnover_auction = Column(DECIMAL(15, 2))
    turnover_daily_summary = Column(DECIMAL(15, 2))
    average_price_auction = Column(DECIMAL(10, 2))


class CarbonMarketBJ(Base):
    __tablename__ = 'carbon_market_bj'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    date = Column(Date)
    volume = Column(Integer)
    average_price = Column(DECIMAL(10, 2))
    turnover = Column(DECIMAL(15, 2))

