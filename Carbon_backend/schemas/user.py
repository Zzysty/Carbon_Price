from pydantic import BaseModel


# 用户创建请求模型
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    user_role: str
    gender: str


# 用户登录请求模型
class UserLogin(BaseModel):
    username: str
    password: str


# 用户响应模型
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    user_role: str
    gender: str

    class Config:
        from_attributes = True  # 启用 ORM 模式以兼容 SQLAlchemy 模型


# 登录成功后的 Token 响应模型
class Token(BaseModel):
    access_token: str
    token_type: str
