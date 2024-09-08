from sqlalchemy.orm import Session

from passlib.context import CryptContext
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, username: str, password: str, email: str, user_role: str, gender: str):
    hashed_password = get_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email, user_role=user_role, gender=gender)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def  authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
