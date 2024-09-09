from datetime import timedelta

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.crud import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app import schemas, crud
from app.database import get_db
from app.models import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ, User
from utils.file_processing import get_columns_map, process_file

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""注册登录接口"""

# OAuth2 密码流模式，用户登录时请求 /token 接口
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 注册接口
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 创建用户
    new_user = crud.create_user(
        db=db,
        username=user.username,
        password=user.password,
        email=user.email,
        user_role=user.user_role,
        gender=user.gender
    )

    return new_user


# 登录接口，返回 JWT token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 验证用户身份
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

    # 生成 JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# 获取当前用户信息的接口
@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 解析和验证 token
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 获取用户信息
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user


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
