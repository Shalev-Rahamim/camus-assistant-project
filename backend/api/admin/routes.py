"""Admin CRUD endpoints for Courses."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.admin.auth import verify_admin
from api.admin import schemas
from api.admin import crud

router = APIRouter(prefix="/admin/courses", tags=["Admin - Courses"])


@router.get("", response_model=List[schemas.CourseResponse])
async def get_courses(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin),
):
    """Get all courses."""
    return await crud.get_all_courses(db, limit=limit, offset=offset)


@router.get("/{course_id}", response_model=schemas.CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin),
):
    """Get a course by ID."""
    course = await crud.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("", response_model=schemas.CourseResponse, status_code=201)
async def create_course(
    course_data: schemas.CourseCreate,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin),
):
    """Create a new course."""
    course = await crud.create_course(db, course_data.model_dump())
    await db.commit()
    return course


@router.put("/{course_id}", response_model=schemas.CourseResponse)
async def update_course(
    course_id: int,
    course_data: schemas.CourseUpdate,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin),
):
    """Update a course."""
    update_data = course_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    course = await crud.update_course(db, course_id, update_data)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.commit()
    return course


@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin),
):
    """Delete a course."""
    deleted = await crud.delete_course(db, course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    await db.commit()
