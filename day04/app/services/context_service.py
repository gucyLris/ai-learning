from typing import List, Dict

# 最大保留消息数量
MAX_RECENT_MESSAGES = 4


# 构建 Context
def build_context(messages: List[Dict[str, str]]):
    """
    从完整历史中构建发送给 LLM 的 Context。

    保留：
    1. system message
    2. 最近 N 条消息
    """

    if not messages:
        return []

    # 找 System Prompt
    system_messages = [message for message in messages if message["role"] == "system"]

    # 非 System 消息
    normal_messages = [message for message in messages if message["role"] != "system"]

    # 最近 N 条
    recent_messages = normal_messages[-MAX_RECENT_MESSAGES:]

    # 最终 Context
    context = system_messages + recent_messages

    return context
