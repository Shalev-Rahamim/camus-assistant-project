import time
import logging
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db, async_session_maker
from pydantic import BaseModel, Field, field_validator
from ai import process_campus_query
from core import sanitize_input, limiter
from db.repository import save_interaction_log

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", tags=["Landing"])
async def landing_page():
    """
    Landing page endpoint - returns available options for the main page.
    """
    return {
        "title": "Campus Elad Software",
        "description": "Welcome to Campus Elad Software",
        "options": [
            {
                "id": "chat",
                "title": "AI Chat",
                "description": "Ask questions about campus, schedules, exams, and more",
                "route": "/api/v1/ask",
            },
            {
                "id": "tables",
                "title": "Information Tables",
                "description": "View schedules, technical questions, and general questions",
                "route": "/api/v1/tables",
            },
        ],
    }


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
            raise ValueError(
                "The entered question is invalid or too short. Please rephrase."
            )
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
    except Exception as e:
        logger.error(f"Error processing question: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Error")
