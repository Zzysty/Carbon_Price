from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import asc
from sqlalchemy.orm import Session

from api.carbon_market.crud import get_columns_map, process_file, get_data
from db.session import get_db
from models import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ
from schemas.carbon_market import CarbonMarketHBQueryParams, CarbonMarketResponseWithTotal, \
    CarbonMarketDatePriceResponse, CarbonMarketDatePriceResponseList
from schemas.response import success_response, error_response, ResponseBase
from utils.utils import fill_null_with_average

router = APIRouter()


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
    'bj': CarbonMarketBJ
}


@router.post("/{market}", response_model=ResponseBase[CarbonMarketResponseWithTotal])
def query_market_data(market: str, query_params: CarbonMarketHBQueryParams, db: Session = Depends(get_db)):
    """
    通用查询接口，支持不同的市场
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


@router.get("/content-data/{market}", response_model=ResponseBase[CarbonMarketDatePriceResponseList])
def query_market_date_price_data(market: str, db: Session = Depends(get_db)):
    """
    通用日期、碳价格查询接口，支持不同的市场
    """
    # 根据路径参数中的市场标识，确定表模型
    table_model = market_to_table.get(market)
    if not table_model:
        return error_response(message="Invalid market type", code=404)

    # 市场与碳价格字段的映射
    market_price_field_map = {
        'hb': 'latest_price',
        'gd': 'closing_price',
        'tj': 'average_price_auction',
        'bj': 'average_price',
    }

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
