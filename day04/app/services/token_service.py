import tiktoken

# GPT / DeepSeek 兼容编码
encoding = tiktoken.get_encoding("cl100k_base")


def count_text_tokens(text: str) -> int:
    tokens = encoding.encode(text)
    return len(tokens)


def count_message_tokens(message: dict) -> int:
    content = message.get("content", "")
    return count_text_tokens(content)


def count_messages_tokens(messages: list) -> int:
    total = 0
    for message in messages:
        total += count_message_tokens(message)
    return total
