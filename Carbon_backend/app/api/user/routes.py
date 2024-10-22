import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.user import crud
from app.api.user.crud import get_current_user
from app.config.settings import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.response import success_response, error_response, ResponseBase
from app.schemas.user import UserResponse, UserCreate, Token, UserBasicInfo

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
    crud.create_user(
        db=db,
        username=user.username,
        password=user.password,
        email=user.email,
        user_role=user.user_role,
        gender=user.gender
    )

    return success_response(data=None, message="User successfully registered")


# 登录接口，返回 JWT token
@router.post("/login", response_model=ResponseBase[Token])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 验证用户身份
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return error_response("Incorrect username or password", code=400)

    # 生成 JWT token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return success_response({"access_token": access_token, "token_type": "bearer"})


# 获取当前用户信息的接口
@router.get("/me", response_model=ResponseBase[UserResponse])
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    # 确保密码字段不会包含在响应中
    user_dict = user.__dict__.copy()  # 将SQLAlchemy对象转为字典
    if 'password' in user_dict:
        del user_dict['password']  # 删除密码字段

    return success_response(user_dict)


# 用户注销接口
@router.post("/logout", response_model=ResponseBase[str])
def logout(token: str = Depends(oauth2_scheme)):
    """
    简单的无状态注销接口，只是提示客户端丢弃 JWT token。
    """
    # 理论上，不需要在服务器端执行任何操作，前端丢弃 token 即完成注销
    return success_response(None, message="Successfully logged out")


# 修改用户基础信息接口
@router.put("/update", response_model=ResponseBase[UserResponse])
def update_user_basic(user_update: UserBasicInfo, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    更新用户的基本信息，用户名、权限、性别、电话、邮箱、个人简介
    """
    # 获取当前用户
    current_user = get_current_user(db, token)

    # 查找用户
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        return error_response("User not found", code=404)

    # 更新用户信息（这里只更新非空的字段）
    db_user.username = user_update.username if user_update.username else db_user.username
    db_user.email = user_update.email if user_update.email else db_user.email
    db_user.phone = user_update.phone if user_update.phone else db_user.phone
    db_user.user_role = user_update.user_role if user_update.user_role else db_user.user_role
    db_user.gender = user_update.gender if user_update.gender else db_user.gender
    db_user.description = user_update.description if user_update.description else db_user.description

    # 如果用户传入了新的密码，则更新密码
    # if user_update.password:
    #     db_user.password = crud.get_password_hash(user_update.password)  # 更新加密后的密码

    # 提交更改到数据库
    db.commit()
    db.refresh(db_user)

    # 确保密码字段不会包含在响应中
    user_dict = db_user.__dict__.copy()
    if 'password' in user_dict:
        del user_dict['password']

    return success_response(user_dict, message="User info updated successfully")


# 用户头像上传接口
@router.post("/upload", response_model=ResponseBase[str])
async def upload_user_avatar(file: UploadFile = File(...), db: Session = Depends(get_db),
                             token: str = Depends(oauth2_scheme)):
    # 校验文件类型（可以根据需要扩展，如限制为图片格式）
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    # 检查文件夹是否存在，如果不存在则创建文件夹
    if not os.path.exists(settings.upload_dir):
        os.makedirs(settings.upload_dir)

    # 读取文件内容，保存文件，或者上传到云存储
    try:
        file_location = f"{settings.upload_dir}{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())  # 保存文件到本地

        # 更新用户头像相对路径到数据库中
        current_user = get_current_user(db, token)
        crud.update_user_avatar(db, current_user_id=current_user.id, avatar_url=file_location)
        # 返回可以访问图片的 URL
        avatar_url = f"/uploads/{file.filename}"
        return success_response(avatar_url, message="Avatar uploaded successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while uploading file: {str(e)}")
