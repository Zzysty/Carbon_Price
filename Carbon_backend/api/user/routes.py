from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas.user as schemas
from api.user import crud
from api.user.crud import get_current_user
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from db.session import get_db
from models import User

router = APIRouter()

# OAuth2 密码流模式，用户登录时请求 /token 接口
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


# 注册接口
@router.post("/register", response_model=schemas.UserResponse)
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
@router.post("/token", response_model=schemas.Token)
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
@router.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    return user
