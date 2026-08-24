import json

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
    description="Day 3 AI Streaming + SSE",
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
# 3. 数据模型
# ========================================


class ChatMessage(BaseModel):

    role: str

    content: str


class ChatRequest(BaseModel):

    messages: list[ChatMessage]


# ========================================
# 4. 首页
# ========================================


@app.get("/")
def root():

    return {"message": "AI API is running"}


# ========================================
# 5. 普通聊天接口
# ========================================


@app.post("/chat")
def chat_api(request: ChatRequest):

    # ====================================
    # Pydantic Model
    # ↓
    # Python dict
    # ====================================

    messages = [message.model_dump() for message in request.messages]

    # ====================================
    # 调用 AI
    # ====================================

    answer = chat(messages)

    return {"answer": answer}


# ========================================
# 6. SSE Streaming
# ========================================


@app.post("/chat/stream")
def chat_stream_api(request: ChatRequest):

    # ====================================
    # Pydantic
    # ↓
    # dict
    # ====================================

    messages = [message.model_dump() for message in request.messages]

    # ====================================
    # SSE Generator
    # ====================================

    def generate():

        try:

            # =================================
            # 从 LLM 一点一点获取内容
            # =================================

            for content in chat_stream(messages):

                # =============================
                # 转成 JSON
                # =============================

                data = json.dumps(
                    {"content": content},
                    ensure_ascii=False,
                )

                # =============================
                # SSE 格式
                # =============================

                yield (f"data: {data}\n\n")

            # =================================
            # AI 完成
            # =================================

            done_data = json.dumps(
                {"done": True},
                ensure_ascii=False,
            )

            yield (f"data: {done_data}\n\n")

        except Exception as error:

            # =================================
            # SSE 错误
            # =================================

            error_data = json.dumps(
                {"error": str(error)},
                ensure_ascii=False,
            )

            yield (f"data: {error_data}\n\n")

    # ====================================
    # 返回 StreamingResponse
    # ====================================

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
