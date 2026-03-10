"""CRUD operations for Course model."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Course


async def get_all_courses(
    session: AsyncSession, limit: int = 100, offset: int = 0
) -> List[Course]:
    """Get all courses with pagination."""
    result = await session.execute(
        select(Course).limit(limit).offset(offset)
    )
    return list(result.scalars().all())


async def get_course_by_id(session: AsyncSession, course_id: int) -> Optional[Course]:
    """Get a course by ID."""
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    return result.scalar_one_or_none()


async def create_course(session: AsyncSession, data: dict) -> Course:
    """Create a new course."""
    course = Course(**data)
    session.add(course)
    await session.flush()
    await session.refresh(course)
    return course


async def update_course(
    session: AsyncSession, course_id: int, data: dict
) -> Optional[Course]:
    """Update an existing course."""
    course = await get_course_by_id(session, course_id)
    if not course:
        return None
    
    for key, value in data.items():
        if value is not None:
            setattr(course, key, value)
    
    await session.flush()
    await session.refresh(course)
    return course


async def delete_course(session: AsyncSession, course_id: int) -> bool:
    """Delete a course by ID."""
    course = await get_course_by_id(session, course_id)
    if not course:
        return False
    
    await session.delete(course)
    await session.flush()
    return True
