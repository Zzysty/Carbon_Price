from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from db.session import get_db
from models import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ
from utils.file_processing import get_columns_map, process_file

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
