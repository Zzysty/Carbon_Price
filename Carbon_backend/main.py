from fastapi import FastAPI

from api.user import routes as user_routes
from api.carbon_market import routes as carbon_market_routes

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""注册登录接口"""

app.include_router(user_routes.router, prefix="/api/user", tags=["User"])

"""上传文件导入数据接口"""
app.include_router(carbon_market_routes.router, prefix="/api/carbon_market", tags=["Upload Carbon Market"])