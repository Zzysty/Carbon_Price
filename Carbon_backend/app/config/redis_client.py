import aioredis
from app.config.settings import settings


# 创建 Redis 异步客户端
async def get_redis_pool():
    return await aioredis.from_url(
        f"redis://{settings.redis_host}:{settings.redis_port}",
        db=settings.redis_db,
        password=settings.redis_password,
        encoding="utf-8",
        decode_responses=True
    )