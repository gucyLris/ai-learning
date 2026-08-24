from openai import OpenAI

from app.core.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)


def chat_stream(messages):

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        stream=True,
    )

    for chunk in response:

        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:

            yield content
