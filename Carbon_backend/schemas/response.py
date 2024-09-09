from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


# 通用响应基类
class ResponseBase(BaseModel, Generic[T]):
    code: int
    msg: str
    data: Optional[T]


# 通用成功响应
def success_response(data: T, message: str = "Success") -> ResponseBase[T]:
    return ResponseBase[T](code=200, msg=message, data=data)


# 通用错误响应
def error_response(message: str, code: int = 400) -> ResponseBase[None]:
    return ResponseBase[None](code=code, msg=message, data=None)
