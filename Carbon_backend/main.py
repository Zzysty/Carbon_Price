from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db
from app.models import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ
from utils.file_processing import get_columns_map, process_file

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""注册登录接口"""


@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user.username, user.password, user.email, user.user_role, user.gender)
    return db_user


@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticated_user = crud.authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": authenticated_user.id}


"""上传文件导入数据接口"""


# 上传并导入湖北碳市场表数据
@app.post("/upload/hb/")
async def upload_hb(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('hb')
    table_model = CarbonMarketHB
    return await process_file(file, db, columns, table_model)


# 上传并导入广东碳市场表数据
@app.post("/upload/gd/")
async def upload_gd(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('gd')
    table_model = CarbonMarketGD
    return await process_file(file, db, columns, table_model)


# 上传并导入天津碳市场表数据
@app.post("/upload/tj/")
async def upload_tj(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('tj')
    table_model = CarbonMarketTJ
    return await process_file(file, db, columns, table_model)


# 上传并导入北京碳市场表数据
@app.post("/upload/bj/")
async def upload_bj(file: UploadFile = File(...), db: Session = Depends(get_db)):
    columns = get_columns_map('bj')
    table_model = CarbonMarketBJ
    return await process_file(file, db, columns, table_model)
