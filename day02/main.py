import json
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm import chat, chat_stream

# ========================================
# 1. 创建 FastAPI
# ========================================

app = FastAPI(
    title="AI Chat API",
    description="Day 3 - Streaming + SSE + Memory",
    version="1.0.0",
)


# ========================================
# 2. CORS
# ========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# 3. 后端 Memory
# ========================================
#
# 结构：
#
# {
#     "conversation_id": [
#         {
#             "role": "system",
#             "content": "..."
#         },
#         {
#             "role": "user",
#             "content": "..."
#         },
#         {
#             "role": "assistant",
#             "content": "..."
#         }
#     ]
# }
#
# ========================================

conversations = {}


# ========================================
# 4. 请求数据模型
# ========================================


class ChatRequest(BaseModel):

    conversation_id: str

    message: str


# ========================================
# 5. 首页
# ========================================


@app.get("/")
def root():

    return {"message": "AI Chat API is running"}


# ========================================
# 6. 创建 Conversation
# ========================================


@app.post("/conversation")
def create_conversation():

    # 创建唯一 ID
    conversation_id = str(uuid4())

    # 初始化 Memory
    conversations[conversation_id] = [
        {
            "role": "system",
            "content": "你是一名前端架构师，请用前端工程师能理解的方式回答。",
        }
    ]

    return {"conversation_id": conversation_id}


# ========================================
# 7. 普通聊天
# ========================================


@app.post("/chat")
def chat_api(request: ChatRequest):

    conversation_id = request.conversation_id

    # ====================================
    # 检查会话是否存在
    # ====================================

    if conversation_id not in conversations:

        return {"error": "conversation not found"}

    # ====================================
    # 获取历史消息
    # ====================================

    messages = conversations[conversation_id]

    # ====================================
    # 添加用户消息
    # ====================================

    messages.append({"role": "user", "content": request.message})

    # ====================================
    # 调用 AI
    # ====================================

    answer = chat(messages)

    # ====================================
    # 保存 AI 回复
    # ====================================

    messages.append({"role": "assistant", "content": answer})

    return {"answer": answer}


# ========================================
# 8. SSE Streaming
# ========================================


@app.post("/chat/stream")
def chat_stream_api(request: ChatRequest):

    conversation_id = request.conversation_id

    # ====================================
    # 检查 Conversation
    # ====================================

    if conversation_id not in conversations:

        def error_generator():

            error_data = json.dumps(
                {"error": "conversation not found"},
                ensure_ascii=False,
            )

            yield (f"data: {error_data}\n\n")

        return StreamingResponse(
            error_generator(),
            media_type="text/event-stream",
        )

    # ====================================
    # 获取历史消息
    # ====================================

    messages = conversations[conversation_id]

    # ====================================
    # 添加用户消息
    # ====================================

    messages.append({"role": "user", "content": request.message})

    # ====================================
    # SSE Generator
    # ====================================

    def generate():

        assistant_message = ""

        try:

            # =================================
            # 调用 Streaming LLM
            # =================================

            for content in chat_stream(messages):

                # 保存完整 AI 回复
                assistant_message += content

                # =================================
                # SSE JSON
                # =================================

                data = json.dumps(
                    {"content": content},
                    ensure_ascii=False,
                )

                # =================================
                # SSE 格式
                # =================================

                yield (f"data: {data}\n\n")

            # =================================
            # AI 完整回答
            # =================================

            messages.append({"role": "assistant", "content": assistant_message})

            # =================================
            # 发送 done
            # =================================

            done_data = json.dumps(
                {"done": True},
                ensure_ascii=False,
            )

            yield (f"data: {done_data}\n\n")

        except Exception as error:

            print(f"Streaming Error: {error}")

            # =================================
            # 错误 SSE
            # =================================

            error_data = json.dumps(
                {"error": str(error)},
                ensure_ascii=False,
            )

            yield (f"data: {error_data}\n\n")

    # ====================================
    # 返回 SSE
    # ====================================

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
