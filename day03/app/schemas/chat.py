from pydantic import BaseModel


class ChatRequest(BaseModel):

    conversation_id: str

    message: str


class ConversationResponse(BaseModel):

    conversation_id: str
