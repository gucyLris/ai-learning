import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
)

load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_API_URL"),
)


def chat(messages):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=True,
        )

        answer = ""

        for chunk in response:
            content = chunk.choices[0].delta.content

            if content:
                print(content, end="", flush=True)
                answer += content

        return answer

    except APITimeoutError:
        print("\n请求 AI 超时，请稍后重试。")

    except APIConnectionError:
        print("\n无法连接 AI 服务，请检查网络。")

    except APIStatusError as error:
        print(f"\nAI 服务返回错误：{error.status_code}")

    except Exception as error:
        print(f"\n未知错误：{error}")

    return None
