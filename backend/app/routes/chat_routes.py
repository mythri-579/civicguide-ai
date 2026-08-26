from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_service import ask_question

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def chat_ask(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = ask_question(question)
    return result