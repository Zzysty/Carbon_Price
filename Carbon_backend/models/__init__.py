from db.session import Base, engine
from models.user import User  # 导入用户模型
from models.carbon_market import CarbonMarketHB, CarbonMarketGD, CarbonMarketTJ, CarbonMarketBJ  # 导入碳市场模型

# 创建所有模型对应的数据库表
Base.metadata.create_all(bind=engine)
