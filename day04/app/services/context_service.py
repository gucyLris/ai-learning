from app.services.token_service import count_message_tokens

MAX_CONTEXT_TOKENS = 2000


def build_context(messages):

    if not messages:
        return []

    # System
    system_messages = [m for m in messages if m["role"] == "system"]

    normal_messages = [m for m in messages if m["role"] != "system"]

    context = []

    current_tokens = 0

    # 倒序
    for message in reversed(normal_messages):

        message_tokens = count_message_tokens(message)

        if current_tokens + message_tokens > MAX_CONTEXT_TOKENS:

            break

        context.insert(0, message)

        current_tokens += message_tokens

    return system_messages + context
