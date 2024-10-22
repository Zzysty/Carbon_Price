from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from api.ai import routes as ai_routes
from api.carbon_market import routes as carbon_market_routes
from api.user import routes as user_routes
from core.config import UPLOAD_DIR

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
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


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
