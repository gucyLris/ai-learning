import json
from uuid import uuid4
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import (
    ChatRequest,
    ConversationResponse,
)

from app.services.llm_service import (
    chat_stream,
)

router = APIRouter(prefix="/chat", tags=["Chat"])


conversations = {}

SYSTEM_PROMPT = "你是一名前端架构师，" "请用前端工程师能理解的方式回答。"


@router.post("/conversation", response_model=ConversationResponse)
def create_conversation():

    conversation_id = str(uuid4())

    conversations[conversation_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    return {"conversation_id": conversation_id}


@router.post("/stream")
def chat_stream_api(request: ChatRequest):
    conversation_id = request.conversation_id

    if conversation_id not in conversations:
        return {"error": "conversation not found"}

    messages = conversations[conversation_id]
    messages.append({"role": "user", "content": request.message})

    def generate():
        assistant_message = ""
        try:
            for content in chat_stream(messages):
                assistant_message += content
                data = json.dumps({"content": content}, ensure_ascii=False)
                yield (f"data: {data}\n\n")

            messages.append({"role": "assistant", "content": assistant_message})
            done = json.dumps({"done": True})

            yield (f"data: {done}\n\n")

        except Exception as error:
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
