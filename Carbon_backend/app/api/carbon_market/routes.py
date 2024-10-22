from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import asc, func
from sqlalchemy.orm import Session

from app.api.carbon_market.crud import get_columns_map, process_file, get_data, market_to_table, market_price_field_map, \
    market_response_model_map, market_name_map
from app.db.session import get_db
from app.models.carbon_market import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ, OtherFactors
from app.schemas.carbon_market import CarbonMarketHBQueryParams, CarbonMarketResponseWithTotal, \
    CarbonMarketDatePriceResponse, CarbonMarketDatePriceResponseList, CarbonAllCountResponseList
from app.schemas.response import success_response, error_response, ResponseBase
from app.utils.utils import fill_null_with_average

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


@router.get("/latest", response_model=ResponseBase[CarbonMarketResponseWithTotal])
def query_market_daily_data(db: Session = Depends(get_db)):
    """
    查询四个市场的最新数据
    """
    global unified_record
    markets_data = []

    # 对于每个市场查询最新的数据
    for market, table_model in market_to_table.items():
        # 跳过不需要返回的市场
        if market == 'factors':
            continue

        response_model = market_response_model_map.get(market)

        if response_model:
            # 查询最新记录
            record = db.query(table_model).order_by(table_model.date.desc()).first()

            # 如果找到了数据，存入 markets_data
            if record:
                record_dict = response_model.from_orm(record).dict()

                # 根据市场对字段进行统一处理
                if market in ['hb', 'gd']:
                    unified_record = {
                        "market": "湖北" if market == 'hb' else "广东",
                        "date": record_dict.get("date"),
                        "price": record_dict.get("latest_price") or record_dict.get("closing_price"),
                        "volume": record_dict.get("volume"),
                        "turnover": record_dict.get("turnover"),
                        "price_change": record_dict.get("price_change")
                    }
                elif market in ['tj', 'bj']:
                    unified_record = {
                        "market": "天津" if market == 'tj' else "北京",
                        "date": record_dict.get("date"),
                        "price": record_dict.get("average_price_auction") or record_dict.get("average_price"),
                        "volume": record_dict.get("volume_auction") or record_dict.get("volume"),
                        "turnover": record_dict.get("volume_auction") or record_dict.get("turnover"),
                        "price_change": None  # 天津和北京没有涨跌幅字段，设置为 None
                    }
                markets_data.append(unified_record)
        else:
            return error_response(message="Market not supported", code=404)

    # 如果没有找到四个市场的数据，返回错误
    if not markets_data:
        return error_response(message="Failed to find data for all markets", code=404)

    # 返回四个市场的数据
    return success_response(data={"total": len(markets_data), "items": markets_data})


@router.get("/carbon_count", response_model=ResponseBase[CarbonAllCountResponseList])
def carbon_num_vis(db: Session = Depends(get_db)):
    """
        遍历所有数据库模型类，查询各自表中数据总数以及总的数据条数
    """
    total_count = 0
    table_counts = []

    for market, table_model in market_to_table.items():
        count = db.query(func.count(table_model.id)).scalar()
        total_count += count
        table_counts.append({"market": market_name_map.get(market, market), "count": count})

    return success_response(data={"total": total_count, "items": table_counts})
