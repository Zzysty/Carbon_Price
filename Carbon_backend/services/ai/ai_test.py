from zhipuai import ZhipuAI

from core.config import ZHIPU_AI_API_KEY

# 示例
# client = ZhipuAI(api_key=ZHIPU_AI_API_KEY)  # 请填写您自己的API Key
# response = client.chat.completions.create(
#   model="glm-4-0520",  # 填写需要调用的模型编码
#   messages=[
#       {"role": "user", "content": "你好！你叫什么名字"},
#   ],
#   stream=True,
# )
# for chunk in response:
#     print(chunk.choices[0].delta)


# 同步
# client = ZhipuAI(api_key=ZHIPU_AI_API_KEY) # 填写您自己的APIKey
# response = client.chat.completions.create(
#     model="glm-4-0520",  # 填写需要调用的模型编码
#     messages=[
#         {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
#         {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
#         {"role": "user", "content": "智谱AI开放平台"},
#         {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
#         {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
#     ],
# )
# print(response.choices[0].message)


# 异步
# client = ZhipuAI(api_key=ZHIPU_AI_API_KEY)  # 请填写您自己的APIKey
# response = client.chat.asyncCompletions.create(
#     model="glm-4-0520",  # 填写需要调用的模型编码
#     messages=[
#         {
#             "role": "user",
#             "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"
#         }
#     ],
# )
# print(response)


# SSE 流式调用
client = ZhipuAI(api_key=ZHIPU_AI_API_KEY) # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4-plus",  # 填写需要调用的模型编码
    messages=[
        {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
        {"role": "user", "content": "我对太阳系的行星非常感兴趣，特别是土星。请提供关于土星的基本信息，包括其大小、组成、环系统和任何独特的天文现象。"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)