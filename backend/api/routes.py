from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from pydantic import BaseModel, Field, field_validator
from ai.service import process_campus_query
from core.security import sanitize_input
from core.ratelimit import limiter

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str = Field(
        ..., max_length=150, min_length=2, description="The student's question"
    )

    @field_validator("question")
    @classmethod
    def validate_and_sanitize(cls, value: str) -> str:
        sanitized = sanitize_input(value)
        if len(sanitized) < 2:
            raise ValueError("השאלה מכילה תוכן לא תקין או קצרה מדי לאחר ניקוי.")
        return sanitized


@router.post("/ask")
@limiter.limit("5/minute")
async def ask_question(
    request: Request, data: QuestionRequest, db: AsyncSession = Depends(get_db)
):
    try:
        # Sanitize user input to prevent prompt injection
        sanitized_question = sanitize_input(data.question)

        # Check if sanitization removed too much (empty or too short)
        if len(sanitized_question) < 2:
            raise HTTPException(
                status_code=400, detail="השאלה מכילה תוכן לא תקין. אנא נסה שוב."
            )

        result = await process_campus_query(sanitized_question, db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Error")
