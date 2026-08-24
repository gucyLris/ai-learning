import os

from dotenv import load_dotenv
from openai import OpenAI

# ========================================
# 1. 加载 .env
# ========================================

load_dotenv()


# ========================================
# 2. 获取 API Key
# ========================================

API_KEY = os.getenv("DEEPSEEK_API_KEY")


if not API_KEY:
    raise ValueError("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件")


# ========================================
# 3. 创建 OpenAI Client
# ========================================

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com",
)


# ========================================
# 4. 普通聊天
# ========================================


def chat(messages):
    """
    普通模式：
    等 AI 完整生成以后，一次性返回。
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False,
    )

    return response.choices[0].message.content


# ========================================
# 5. Streaming 聊天
# ========================================


def chat_stream(messages):
    """
    Streaming 模式：

    AI 生成一点
        ↓
    yield 一点
        ↓
    FastAPI
        ↓
    SSE
        ↓
    浏览器
    """

    try:

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=True,
        )

        # ====================================
        # 不断获取 AI 返回的数据
        # ====================================

        for chunk in response:

            # 有些 chunk 没有 choices
            if not chunk.choices:
                continue

            # 获取本次生成的内容
            content = chunk.choices[0].delta.content

            # 有内容才返回
            if content:
                yield content

    except Exception as error:

        print(f"调用 AI 失败：{error}")

        raise
