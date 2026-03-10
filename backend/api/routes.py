from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from pydantic import BaseModel, Field, field_validator, Request
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
            raise ValueError("השאלה שהוזנה אינה חוקית או קצרה מדי. אנא נסח שוב.")
        return sanitized


@router.post("/ask")
@limiter.limit("5/minute")
async def ask_question(
    request: Request, data: QuestionRequest, db: AsyncSession = Depends(get_db)
):
    try:
        result = await process_campus_query(data.question, db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Error")
