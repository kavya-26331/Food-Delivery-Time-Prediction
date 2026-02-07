from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse

import requests

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"

@router.post("/rider", response_model=ChatResponse)
def rider_ai_chat(request: ChatRequest):
    payload = {
        "model": "llama3.1",
        "prompt": f"You are a rider AI assistant for food delivery. Answer: {request.query}",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        answer = data.get("response", "No response")
        return {"answer": answer}
    return {"answer": "Error in AI response"}
