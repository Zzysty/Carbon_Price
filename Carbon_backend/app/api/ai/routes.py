from fastapi import APIRouter
from starlette.responses import StreamingResponse
from zhipuai import ZhipuAI

from app.config.settings import settings

router = APIRouter()

client = ZhipuAI(api_key=settings.zhipu_ai_api_key)


@router.get("/chat/sse")
async def chat_stream():
    response = client.chat.completions.create(
        model="glm-4-plus",  # 填写需要调用的模型编码
        messages=[
            {"role": "user", "content": "你好！你叫什么名字"},
        ],
        stream=True,
    )

    # 生成器函数，用于逐块返回流式响应
    def generate():
        for chunk in response:
            # 将 delta 转换为字符串
            yield chunk.choices[0].delta.content

    return StreamingResponse(generate(), media_type="text/plain")
