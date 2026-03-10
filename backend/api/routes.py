import time
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db, async_session_maker
from pydantic import BaseModel, Field, field_validator
from ai import process_campus_query
from core.security import sanitize_input
from core.ratelimit import limiter
from db.repository import save_interaction_log

router = APIRouter()


async def _save_log_background(
    question: str, answer: str, category: str, process_time_ms: int
) -> None:
    """
    Background task wrapper that creates its own database session.
    This is necessary because the original session from the request will be closed.
    """
    async with async_session_maker() as db:
        await save_interaction_log(db, question, answer, category, process_time_ms)


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
    request: Request,
    data: QuestionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Handles student questions and returns AI-generated answers.
    Logs the interaction in the background without blocking the response.
    """
    start_time = time.perf_counter()

    try:
        result = await process_campus_query(data.question, db)

        # Calculate processing time in milliseconds
        process_time_ms = int((time.perf_counter() - start_time) * 1000)

        # Save log in background (non-blocking)
        # Note: We pass the data, not the session, because the session will be closed
        # The background task will create its own session
        background_tasks.add_task(
            _save_log_background,
            question=data.question,
            answer=result["answer"],
            category=result["category"],
            process_time_ms=process_time_ms,
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Error")
