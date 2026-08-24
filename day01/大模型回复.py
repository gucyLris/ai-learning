import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = os.getenv("DEEPSEEK_API_URL")

client = OpenAI(
    api_key=api_key,
    base_url=api_url,
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": "我是一名前端开发工程师，现在准备转型做 AI 大模型应用开发，请给我一个学习建议。",
        }
    ],
)

print(response.choices[0].message.content)
