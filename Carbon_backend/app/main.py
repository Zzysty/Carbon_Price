import aioredis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from app.api.ai import routes as ai_routes
from app.api.carbon_market import routes as carbon_market_routes
from app.api.user import routes as user_routes
from app.config.redis_client import get_redis_client
from app.config.settings import settings

app = FastAPI()

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
async def test_redis_connection(redis_client: aioredis.Redis = Depends(get_redis_client)):
    """测试 Redis 连接是否成功"""
    try:
        # 设置一个测试值
        await redis_client.set("test_key", "test_value")
        # 获取该测试值
        value = await redis_client.get("test_key")

        # 检查是否成功
        if value == "test_value":
            return {"message": "Redis connection successful", "value": value}
        else:
            return {"message": "Redis connection failed", "error": "Incorrect value retrieved"}
    except Exception as e:
        # 捕获连接异常
        return {"message": "Redis connection failed", "error": str(e)}
