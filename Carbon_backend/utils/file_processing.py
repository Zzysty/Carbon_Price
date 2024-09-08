import io

import numpy as np
import pandas as pd
from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

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

        # 将 DataFrame 中的 pd.NA 和 NaN 替换为 None，这样 SQLAlchemy 会将其插入为 NULL
        df = df.replace({pd.NA: None, np.nan: None})

        # 进行增量更新：只导入数据库中未存在日期的数据
        existing_dates = db.query(table_model.date).all()
        existing_dates = {date[0] for date in existing_dates}

        new_data = df[~df['date'].isin(existing_dates)]

        if new_data.empty:
            return {
                "code": 200,
                "message": "No new data."
            }

            # 导入新数据
        import_data_to_table(db, new_data, table_model)

        return {
            "code": 200,
            "file_size": len(new_data),
            "message": f"{table_model.__tablename__} Success"
        }
    except pd.errors.ParserError as e:
        return {
            "code": 40100,
            "message": f"Pandas excel error: {str(e)}"
        }
    except SQLAlchemyError as e:
        return {
            "code": 40200,
            "message": f"Database error: {str(e)}"
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"Exception error: {str(e)}"
        }


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
    }
    return column_maps.get(market, {})
