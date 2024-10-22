from passlib.context import CryptContext

# 密码加密器
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 配置
SECRET_KEY = "ZZYISYYDS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 3    # 访问令牌过期时间（分钟）

# 智谱ai api key
ZHIPU_AI_API_KEY = "545072b9d1295bbf0b3f6beab6a28f78.s1rr0AALVCTmYzuC"

# 定义图片存储的目录
UPLOAD_DIR = "uploads/"