import uuid

from sqlalchemy import Column, String, Enum, TIMESTAMP, func

from db.session import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    user_role = Column(Enum('admin', 'user', 'guest'), nullable=False)
    gender = Column(Enum('male', 'female'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())