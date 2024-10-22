from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.settings import pwd_context, settings
from app.models.user import User


def to_camel(string: str) -> str:
    """将字段名转换为驼峰命名法"""
    return ''.join(word.capitalize() if i != 0 else word for i, word in enumerate(string.split('_')))


# 创建密码哈希
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 创建用户
def create_user(db: Session, username: str, password: str, email: str, user_role: str, gender: str):
    hashed_password = get_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email, user_role=user_role, gender=gender)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 验证用户身份
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


# 创建访问令牌 (JWT)
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


# 获取当前用户
def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# 更新用户头像
def update_user_avatar(db: Session, current_user_id: str, avatar_url: str):
    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.avatar = avatar_url  # 更新用户头像字段
    db.commit()  # 提交事务
    db.refresh(user)  # 刷新对象，确保返回最新数据
    return user
