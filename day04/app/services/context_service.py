from app.services.token_service import count_message_tokens

# 模型 Context Window
MAX_CONTEXT_WINDOW = 8000

# 给模型输出预留 Token
MAX_OUTPUT_TOKENS = 1000


# 构建 Context
def build_context(messages: list):
    if not messages:

        return []

    # 1. System
    system_messages = [m for m in messages if m["role"] == "system"]

    # 2. 普通消息
    normal_messages = [m for m in messages if m["role"] != "system"]

    if not normal_messages:
        return system_messages

    # 3. 当前 User Message
    current_user_message = normal_messages[-1]

    # 4. 历史消息
    history_messages = normal_messages[:-1]

    # 5. System Token
    system_tokens = sum(count_message_tokens(message) for message in system_messages)

    # 6. 当前用户 Token
    current_user_tokens = count_message_tokens(current_user_message)

    # 7. Output 预留
    input_budget = MAX_CONTEXT_WINDOW - MAX_OUTPUT_TOKENS

    # 8. History Budget
    history_budget = input_budget - system_tokens - current_user_tokens

    # 9. 没有空间放历史
    if history_budget <= 0:

        return system_messages + [current_user_message]

    # 10. 从最新历史开始
    selected_history = []

    current_tokens = 0

    # 倒序
    for message in reversed(history_messages):

        message_tokens = count_message_tokens(message)

        # 超过预算
        if current_tokens + message_tokens > history_budget:

            break

        selected_history.insert(0, message)

        current_tokens += message_tokens

    # 11. 最终 Context
    return system_messages + selected_history + [current_user_message]
