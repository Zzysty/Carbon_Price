from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.user import crud
from api.user.crud import get_current_user
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from db.session import get_db
from models import User
from schemas.response import success_response, error_response, ResponseBase
from schemas.user import UserResponse, UserCreate, Token

router = APIRouter()

# OAuth2 密码流模式，用户登录时请求 /token 接口
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


# 注册接口
@router.post("/register", response_model=ResponseBase[UserResponse])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return error_response("Username already registered", code=400)

    # 创建用户
    new_user = crud.create_user(
        db=db,
        username=user.username,
        password=user.password,
        email=user.email,
        user_role=user.user_role,
        gender=user.gender
    )

    return success_response(new_user, message="User successfully registered")


# 登录接口，返回 JWT token
@router.post("/login", response_model=ResponseBase[Token])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 验证用户身份
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return error_response("Incorrect username or password", code=400)

    # 生成 JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return success_response({"access_token": access_token, "token_type": "bearer"})


# 获取当前用户信息的接口
@router.get("/me", response_model=ResponseBase[UserResponse])
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    return success_response(user)
