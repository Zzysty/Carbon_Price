from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # 加密配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 3  # 3小时过期

    # API Key
    zhipu_ai_api_key: str

    # 图片上传目录
    upload_dir: str

    # 数据库配置
    db_username: str
    db_password: str
    db_host: str
    db_name: str

    class Config:
        # 动态加载不同环境的 .env 文件
        env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"
        env_file_encoding = 'utf-8'


# 初始化 Settings
settings = Settings()

# 密码加密器
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
