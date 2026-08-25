import tiktoken

# GPT / DeepSeek 兼容编码
encoding = tiktoken.get_encoding("cl100k_base")


def count_text_tokens(text: str):

    tokens = encoding.encode(text)

    return len(tokens)
