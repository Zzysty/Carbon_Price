from datetime import timedelta, date

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import asc
from sqlalchemy.orm import Session

from api.carbon_market.crud import get_columns_map, process_file, get_data
from db.session import get_db
from models import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ, OtherFactors
from schemas.carbon_market import CarbonMarketHBQueryParams, CarbonMarketResponseWithTotal, \
    CarbonMarketDatePriceResponse, CarbonMarketDatePriceResponseList, HBCarbonMarketResponse, GDCarbonMarketResponse, \
    TJCarbonMarketResponse, BJCarbonMarketResponse, CarbonMarketOtherFactorsResponse
from schemas.response import success_response, error_response, ResponseBase
from utils.utils import fill_null_with_average

router = APIRouter()


@router.post("/upload/factors")
async def upload_factors(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    上传并导入外部因素数据
    """
    columns = get_columns_map('factors')
    table_model = OtherFactors
    return await process_file(file, db, columns, table_model)


@router.post("/upload/hb")
async def upload_hb(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    上传并导入湖北碳市场表数据
    """
    columns = get_columns_map('hb')
    table_model = CarbonMarketHB
    return await process_file(file, db, columns, table_model)


@router.post("/upload/gd")
async def upload_gd(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    上传并导入广东碳市场表数据
    """
    columns = get_columns_map('gd')
    table_model = CarbonMarketGD
    return await process_file(file, db, columns, table_model)


# 上传并导入天津碳市场表数据
@router.post("/upload/tj")
async def upload_tj(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    上传并导入天津碳市场表数据
    """
    columns = get_columns_map('tj')
    table_model = CarbonMarketTJ
    return await process_file(file, db, columns, table_model)


@router.post("/upload/bj")
async def upload_bj(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    上传并导入北京碳市场表数据
    """
    columns = get_columns_map('bj')
    table_model = CarbonMarketBJ
    return await process_file(file, db, columns, table_model)


# 根据市场类型动态选择表模型
market_to_table = {
    'hb': CarbonMarketHB,
    'gd': CarbonMarketGD,
    'tj': CarbonMarketTJ,
    'bj': CarbonMarketBJ,
    'factors': OtherFactors,
}


@router.post("/{market}", response_model=ResponseBase[CarbonMarketResponseWithTotal])
def query_market_data(market: str, query_params: CarbonMarketHBQueryParams, db: Session = Depends(get_db)):
    """
    通用查询接口，支持不同的市场，补充外部因素
    """
    # 根据路径参数中的市场标识，确定表模型
    table_model = market_to_table.get(market)
    if not table_model:
        return error_response(message="Invalid market type", code=404)

    # 调用通用查询函数
    data = get_data(db, table_model, query_params.dateRange)

    if not data:
        return error_response(message="No data found", code=404)

    return success_response(data=data)


# 市场与碳价格字段的映射
market_price_field_map = {
    'hb': 'latest_price',
    'gd': 'closing_price',
    'tj': 'average_price_auction',
    'bj': 'average_price',
}


@router.get("/content-data/{market}", response_model=ResponseBase[CarbonMarketDatePriceResponseList])
def query_market_date_price_data(market: str, db: Session = Depends(get_db)):
    """
    通用日期、碳价格查询接口，支持不同的市场
    """
    # 根据路径参数中的市场标识，确定表模型
    table_model = market_to_table.get(market)
    if not table_model:
        return error_response(message="Invalid market type", code=404)

    # 获取市场对应的价格字段
    price_field = market_price_field_map.get(market)
    if not price_field:
        return error_response(message="Market not supported", code=404)

    # 动态获取字段，确保该字段在表模型中存在
    try:
        price_field = getattr(table_model, price_field)
    except AttributeError:
        return error_response(message=f"{market} market does not have the attribute {price_field}", code=500)

    # 查询数据
    records = db.query(table_model.date, price_field).order_by(asc(table_model.date)).all()
    if not records:
        return error_response(message="No data found", code=404)

    # 对天津市场进行单独处理，处理null值
    if market == 'tj':
        records = fill_null_with_average(records)

    # 将元组列表转换为 Pydantic 模型列表
    data = [CarbonMarketDatePriceResponse(x=record[0], y=record[1]) for record in records]

    return success_response(data={"total": len(data), "items": data})


# 市场与响应模型映射
market_response_model_map = {
    'hb': HBCarbonMarketResponse,
    'gd': GDCarbonMarketResponse,
    'tj': TJCarbonMarketResponse,
    'bj': BJCarbonMarketResponse,
    'factors': CarbonMarketOtherFactorsResponse,
}


@router.get("/latest", response_model=ResponseBase[CarbonMarketResponseWithTotal])
def query_market_daily_data(db: Session = Depends(get_db)):
    """
    查询四个市场的最新数据
    """
    markets_data = []

    # 对于每个市场查询最新的数据
    for market, table_model in market_to_table.items():
        response_model = market_response_model_map.get(market)

        if response_model:
            # 查询最新记录
            record = db.query(table_model).order_by(table_model.date.desc()).first()

            # 如果找到了数据，存入 markets_data
            if record:
                markets_data.append(response_model.from_orm(record))
        else:
            return error_response(message="Market not supported", code=404)

    # 如果没有找到四个市场的数据，返回错误
    if not markets_data:
        return error_response(message="Failed to find data for all markets", code=404)

    # 返回四个市场的数据
    return success_response(data={"total": len(markets_data), "items": markets_data})
