from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from api.carbon_market.crud import get_columns_map, process_file, get_hb_data
from db.session import get_db
from models import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ
from schemas.carbon_market import CarbonMarketHBQueryParams, CarbonMarketHBResponseWithTotal
from schemas.response import success_response, error_response, ResponseBase

router = APIRouter()


# 上传并导入湖北碳市场表数据
@router.post("/upload/hb/")
async def upload_hb(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('hb')
    table_model = CarbonMarketHB
    return await process_file(file, db, columns, table_model)


# 上传并导入广东碳市场表数据
@router.post("/upload/gd/")
async def upload_gd(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('gd')
    table_model = CarbonMarketGD
    return await process_file(file, db, columns, table_model)


# 上传并导入天津碳市场表数据
@router.post("/upload/tj/")
async def upload_tj(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('tj')
    table_model = CarbonMarketTJ
    return await process_file(file, db, columns, table_model)


# 上传并导入北京碳市场表数据
@router.post("/upload/bj/")
async def upload_bj(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('bj')
    table_model = CarbonMarketBJ
    return await process_file(file, db, columns, table_model)


# 全量查询接口，支持根据前端给定条件筛选数据
@router.post("/hb", response_model=ResponseBase[CarbonMarketHBResponseWithTotal])
def query_hb_data(query_params: CarbonMarketHBQueryParams, db: Session = Depends(get_db)):
    hb_data = get_hb_data(db, query_params.dateRange)
    if not hb_data:
        return error_response(message="No data found", code=404)

    return success_response(data=hb_data)
