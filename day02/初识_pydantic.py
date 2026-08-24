from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


def chat(request: ChatRequest) -> ChatResponse:
    answer = f"AI 收到：{request.message}"

    return ChatResponse(answer=answer)


request = ChatRequest(message="什么是 RAG？")

response = chat(request)

print(response.answer)
