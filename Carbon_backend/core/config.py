from passlib.context import CryptContext

# 密码加密器
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 配置
SECRET_KEY = "ZZYISYYDS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # 访问令牌过期时间（分钟）
