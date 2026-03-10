"""Pydantic schemas for Course CRUD operations."""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CourseCreate(BaseModel):
    """Schema for creating a new course."""
    name: str = Field(..., max_length=100)
    lecturer_name: str = Field(..., max_length=100)
    lecturer_email: Optional[str] = None
    is_active: bool = True


class CourseUpdate(BaseModel):
    """Schema for updating a course (all fields optional)."""
    name: Optional[str] = Field(None, max_length=100)
    lecturer_name: Optional[str] = Field(None, max_length=100)
    lecturer_email: Optional[str] = None
    is_active: Optional[bool] = None


class CourseResponse(BaseModel):
    """Schema for course response."""
    id: int
    name: str
    lecturer_name: str
    lecturer_email: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
