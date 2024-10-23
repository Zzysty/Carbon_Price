from contextlib import asynccontextmanager

import aioredis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from app.api.ai import routes as ai_routes
from app.api.carbon_market import routes as carbon_market_routes
from app.api.user import routes as user_routes
from app.config.redis_client import get_redis_pool
from app.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在应用启动时初始化 Redis 连接池
    app.state.redis = await get_redis_pool()

    yield  # 在此处可以让请求处理继续

    # 在应用关闭时关闭 Redis 连接池
    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://carbon-price.vercel.app"
    ],
    # 允许前端地址进行跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（GET, POST 等）
    allow_headers=["*"],  # 允许所有请求头
)

# 使得 FastAPI 可以服务静态文件
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


@app.get("/")
async def root():
    # 重定向到docs，fastapi的接口文档节目
    return RedirectResponse(url="/docs")


"""注册登录接口"""
app.include_router(user_routes.router, prefix="/api/user", tags=["User"])

"""上传文件导入数据接口"""
app.include_router(carbon_market_routes.router, prefix="/api/carbon_market", tags=["Carbon Market"])

"""AI 接口"""
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI"])


@app.get("/test-redis/")
async def test_redis_connection():
    redis_client = app.state.redis
    try:
        # 使用异步 Redis 客户端操作
        await redis_client.set("test_key", "test_value")
        value = await redis_client.get("test_key")

        if value == "test_value":
            return {"message": "Redis connection successful", "value": value}
        else:
            return {"message": "Redis connection failed", "error": "Incorrect value retrieved"}
    except Exception as e:
        return {"message": "Redis connection failed", "error": str(e)}
