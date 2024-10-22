from app.db.session import Base, engine

# 创建所有模型对应的数据库表
Base.metadata.create_all(bind=engine)
