from fastapi import FastAPI
from api.user import routes as user_routes
from api.carbon_market import routes as carbon_market_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许前端地址进行跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（GET, POST 等）
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""注册登录接口"""

app.include_router(user_routes.router, prefix="/api/user", tags=["User"])

"""上传文件导入数据接口"""
app.include_router(carbon_market_routes.router, prefix="/api/carbon_market", tags=["Upload Carbon Market"])
