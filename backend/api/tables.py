"""Public endpoints for viewing tables (schedules, knowledge base)."""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from pydantic import BaseModel

from db import get_db, Schedule, KnowledgeBase, CategoryEnum, Course, Room

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tables", tags=["Tables"])


# Response schemas
class ScheduleResponse(BaseModel):
    id: int
    course_name: str
    lecturer_name: str
    day_of_week: str
    start_time: str
    end_time: str
    room_name: str

    class Config:
        from_attributes = True


class KnowledgeBaseResponse(BaseModel):
    id: int
    category: str
    topic_or_question: str
    content_or_answer: str

    class Config:
        from_attributes = True


@router.get("/schedules", response_model=List[ScheduleResponse])
async def get_schedules(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all schedules (לוז) for public viewing.
    Returns course schedules with room and course information.
    """
    try:
        query = (
            select(Schedule)
            .options(joinedload(Schedule.course), joinedload(Schedule.room))
            .limit(limit)
            .offset(offset)
            .order_by(Schedule.day_of_week, Schedule.start_time)
        )
        result = await db.execute(query)
        schedules = result.scalars().unique().all()

        return [
            ScheduleResponse(
                id=s.id,
                course_name=s.course.name,
                lecturer_name=s.course.lecturer_name,
                day_of_week=s.day_of_week,
                start_time=str(s.start_time),
                end_time=str(s.end_time),
                room_name=s.room.name,
            )
            for s in schedules
        ]
    except Exception as e:
        logger.error(f"Error fetching schedules: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch schedules")


@router.get("/knowledge-base", response_model=List[KnowledgeBaseResponse])
async def get_knowledge_base(
    category: Optional[str] = Query(None, description="Filter by category: technical, general"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    Get knowledge base items (שאלות טכניות או כלליות).
    Can filter by category: 'technical' or 'general'.
    """
    try:
        query = select(KnowledgeBase).where(KnowledgeBase.is_active == True)

        if category:
            try:
                category_enum = CategoryEnum(category.lower())
                query = query.where(KnowledgeBase.category == category_enum)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category. Must be one of: technical, general"
                )

        query = query.limit(limit).offset(offset).order_by(KnowledgeBase.topic_or_question)
        result = await db.execute(query)
        items = result.scalars().all()

        return [
            KnowledgeBaseResponse(
                id=item.id,
                category=item.category.value,
                topic_or_question=item.topic_or_question,
                content_or_answer=item.content_or_answer,
            )
            for item in items
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching knowledge base: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch knowledge base")
