from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    user_role: str
    gender: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    user_role: str
    gender: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
