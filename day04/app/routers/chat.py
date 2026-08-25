import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import (
    ChatRequest,
    ConversationResponse,
)
from app.services.llm_service import (
    chat_stream,
)
from app.services.memory_service import (
    create_conversation,
    conversation_exists,
    get_messages,
    add_user_message,
    add_assistant_message,
)

from app.services.context_service import (
    build_context,
)

# Router
router = APIRouter(prefix="/chat", tags=["Chat"])


# 创建 Conversation
@router.post("/conversation", response_model=ConversationResponse)
def create_chat_conversation():

    conversation_id = create_conversation()

    return {"conversation_id": conversation_id}


# Streaming Chat
@router.post("/stream")
def chat_stream_api(request: ChatRequest):

    conversation_id = request.conversation_id

    # 1. 检查 Conversation
    if not conversation_exists(conversation_id):

        def error_generator():

            error_data = json.dumps(
                {"error": "conversation not found"}, ensure_ascii=False
            )

            yield (f"data: {error_data}\n\n")

        return StreamingResponse(error_generator(), media_type="text/event-stream")

    # 2. 保存用户消息
    add_user_message(conversation_id, request.message)

    # 3. 获取完整 Memory
    messages = get_messages(conversation_id)

    # 4. 构建 Context
    context = build_context(messages)

    print("\n========== Context ==========")

    for message in context:

        print(message["role"], ":", message["content"])

    print("=============================\n")

    # 5. Streaming
    def generate():

        assistant_message = ""

        try:

            # LLM 使用 Context
            for content in chat_stream(context):

                assistant_message += content

                # SSE
                data = json.dumps({"content": content}, ensure_ascii=False)

                yield (f"data: {data}\n\n")

            # 6. 保存 AI 完整回答
            add_assistant_message(conversation_id, assistant_message)

            # 7. 完成
            done_data = json.dumps({"done": True}, ensure_ascii=False)

            yield (f"data: {done_data}\n\n")

        except Exception as error:

            print(f"LLM Error: {error}")

            error_data = json.dumps({"error": str(error)}, ensure_ascii=False)

            yield (f"data: {error_data}\n\n")

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
