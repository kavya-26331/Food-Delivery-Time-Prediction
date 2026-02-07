from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.llm.rag_chat import chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def rag_chat(request: ChatRequest):
    answer = chat(request.query)
    return ChatResponse(answer=answer)

