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

messages = [
    {
        "role": "system",
        "content": "你是一名专业的 AI 编程助手，请用清晰、易懂的方式回答问题。",
    }
]


while True:
    user_input = input("\n你：")

    if user_input.lower() in ["exit", "quit"]:
        print("AI：再见！")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )

    answer = response.choices[0].message.content

    messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    print("\nAI：", answer)
