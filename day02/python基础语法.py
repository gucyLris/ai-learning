from pydantic import BaseModel


class User(BaseModel):
    name: str
    job: str


class ChatBot(BaseModel):
    answer: str


def chat(request: User) -> ChatBot:
    answer = f"AI 收到：{request.name, request.job}"

    return ChatBot(answer=answer)


request = User(name=12, job="前端开发")

response = chat(request)

print(response)
