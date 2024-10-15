import io
from datetime import date
from typing import Optional, List

import numpy as np
import pandas as pd
from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ, OtherFactors
from schemas.carbon_market import HBCarbonMarketResponse, GDCarbonMarketResponse, TJCarbonMarketResponse, \
    BJCarbonMarketResponse, CarbonMarketOtherFactorsResponse
from schemas.response import success_response, error_response
from utils.utils import clean_numeric_column


# 读取 Excel 文件并导入到数据库
def import_data_to_table(db: Session, df: pd.DataFrame, table_model):
    try:
        for _, row in df.iterrows():
            data = table_model(**row.to_dict())
            db.add(data)
        db.commit()
    except Exception as e:
        db.rollback()  # 回滚事务
        raise e  # 抛出异常以便上层处理


# 处理上传文件
async def process_file(file: UploadFile, db: Session, columns: dict, table_model):
    """
    处理excel文件内容
    湖北、广东默认处理，天津需要删除最后一列，北京需要对turnover列做提取
    """
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), parse_dates=['日期'])

        # 根据表名判断市场类型
        table_name = table_model.__tablename__

        # 天津市场处理：删除最后一列
        if table_name == 'carbon_market_tj':
            df = df.iloc[:, :-1]  # 删除最后一列

        # 列名映射
        df.columns = columns

        # 选择清理数据
        numeric_columns = [col for col in columns.values() if col not in ['date', 'product']]
        df = clean_numeric_column(df, numeric_columns)

        # 确保 'date' 列格式为日期
        try:
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce').dt.date  # 按指定格式解析
        except ValueError as e:
            return error_response(f"Date parsing error: {str(e)}", code=403)

        # 将 DataFrame 中的 pd.NA 和 NaN 替换为 None，这样 SQLAlchemy 会将其插入为 NULL
        df = df.replace({pd.NA: None, np.nan: None})

        # 进行增量更新：只导入数据库中未存在日期的数据
        existing_dates = db.query(table_model.date).all()
        existing_dates = {date[0] for date in existing_dates}

        new_data = df[~df['date'].isin(existing_dates)]

        if new_data.empty:
            return error_response("No new data", 200)

        # 导入新数据
        import_data_to_table(db, new_data, table_model)

        return success_response({"file_size": len(new_data)}, f"{table_model.__tablename__} Success")
    except pd.errors.ParserError as e:
        return error_response(f"Pandas excel error: {str(e)}", code=401)
    except SQLAlchemyError as e:
        return error_response(f"Database error: {str(e)}", code=402)
    except Exception as e:
        return error_response(f"Exception error: {str(e)}", code=500)


# 获取列名映射
def get_columns_map(market: str) -> dict:
    column_maps = {
        'hb': {
            'product': 'product',
            'date': 'date',
            'latest_price': 'latest_price',
            'price_change': 'price_change',
            'highest_price': 'highest_price',
            'lowest_price': 'lowest_price',
            'volume': 'volume',
            'turnover': 'turnover',
            'previous_close_price': 'previous_close_price',
        },
        'gd': {
            'date': 'date',
            'product': 'product',
            'opening_price': 'opening_price',
            'closing_price': 'closing_price',
            'highest_price': 'highest_price',
            'lowest_price': 'lowest_price',
            'price_change': 'price_change',
            'price_change_percentage': 'price_change_percentage',
            'volume': 'volume',
            'turnover': 'turnover',
        },
        'tj': {
            'date': 'date',
            'product': 'product',
            'volume_auction': 'volume_auction',
            'volume_daily_summary': 'volume_daily_summary',
            'turnover_auction': 'turnover_auction',
            'turnover_daily_summary': 'turnover_daily_summary',
            'average_price_auction': 'average_price_auction',
        },
        'bj': {
            'date': 'date',
            'volume': 'volume',
            'average_price': 'average_price',
            'turnover': 'turnover',
        },
        'factors': {
            'date': 'date',
            'gas_price': 'gas_price',
            'coal_price': 'coal_price',
            'oil_price': 'oil_price',
            'hs300': 'hs300',
            'aql_hb': 'aql_hb',
            'aql_gd': 'aql_gd',
            'aql_sh': 'aql_sh',
            'si': 'si',
            'eua_price': 'eua_price',
        },
    }
    return column_maps.get(market, {})


# 查询全量数据，根据查询条件
def get_data(db: Session, table_model, date_range: Optional[List[date]] = None):
    query = db.query(table_model)

    # 按日期范围过滤
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        query = query.filter(and_(table_model.date >= start_date, table_model.date <= end_date))

    items = query.all()  # 获取查询结果列表
    total = len(items)  # 计算总数

    return {"total": total, "items": items}


# 根据市场类型动态选择表模型
market_to_table = {
    'hb': CarbonMarketHB,
    'gd': CarbonMarketGD,
    'tj': CarbonMarketTJ,
    'bj': CarbonMarketBJ,
    'factors': OtherFactors,
}

# 市场名称映射
market_name_map = {
    'hb': '湖北',
    'gd': '广东',
    'tj': '天津',
    'bj': '北京',
    'factors': '外部因素',
}

# 市场与碳价格字段的映射
market_price_field_map = {
    'hb': 'latest_price',
    'gd': 'closing_price',
    'tj': 'average_price_auction',
    'bj': 'average_price',
}

# 市场与响应模型映射
market_response_model_map = {
    'hb': HBCarbonMarketResponse,
    'gd': GDCarbonMarketResponse,
    'tj': TJCarbonMarketResponse,
    'bj': BJCarbonMarketResponse,
    'factors': CarbonMarketOtherFactorsResponse,
}
