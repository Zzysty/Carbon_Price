from fastapi import FastAPI
from api.user import routes as user_routes
from api.carbon_market import routes as carbon_market_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
]

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（GET, POST, etc.）
    allow_headers=["*"],  # 允许所有的请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""注册登录接口"""

app.include_router(user_routes.router, prefix="/api/user", tags=["User"])

"""上传文件导入数据接口"""
app.include_router(carbon_market_routes.router, prefix="/api/carbon_market", tags=["Upload Carbon Market"])
