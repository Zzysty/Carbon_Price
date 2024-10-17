from typing import Generic, TypeVar, Optional, Union

from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

T = TypeVar("T")


# 通用响应基类
class ResponseBase(BaseModel, Generic[T]):
    code: int = Field(..., description="响应状态码")
    msg: str = Field(..., description="响应信息")
    data: Optional[Union[T, dict]] = Field(None, description="响应数据")


# 通用成功响应
def success_response(data: Optional[Union[T, dict]] = None, message: str = "Success") -> ResponseBase[T]:
    if data is None:
        data = {}
    return ResponseBase(code=200, msg=message, data=data)


# 通用错误响应
def error_response(message: str, code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "msg": message,
            "data": None
        }
    )
