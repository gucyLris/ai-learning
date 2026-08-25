from uuid import uuid4

conversations = {}

# System Prompt
SYSTEM_PROMPT = "你是一名前端架构师，" "请用前端工程师能理解的方式回答。"


# 创建会话
def create_conversation():
    conversation_id = str(uuid4())
    conversations[conversation_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    return conversation_id


# 判断会话是否存在
def conversation_exists(conversation_id: str):
    return conversation_id in conversations


# 获取消息
def get_messages(conversation_id: str):
    return conversations[conversation_id]


# 添加用户消息
def add_user_message(conversation_id: str, content: str):
    messages = get_messages(conversation_id)
    messages.append({"role": "user", "content": content})


# 添加 AI 消息
def add_assistant_message(conversation_id: str, content: str):
    messages = get_messages(conversation_id)
    messages.append({"role": "assistant", "content": content})
