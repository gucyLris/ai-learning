from llm import chat

messages = [
    {
        "role": "system",
        "content": (
            "你是一名资深前端架构师。"
            "用户是一名前端开发工程师，正在转型 AI 应用开发。"
            "请用前端工程师容易理解的方式回答问题。"
        ),
    }
]


while True:
    user_input = input("\n\n你：")

    if user_input.lower() in ["exit", "quit"]:
        print("\nAI：再见！")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    print("\nAI：", end="")

    answer = chat(messages)

    messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
