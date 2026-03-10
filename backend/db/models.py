import enum
from datetime import datetime, time, date, timezone
from typing import List, Optional
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    DateTime,
    Boolean,
    Enum,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""

    pass


# --- Enumerations ---


class CategoryEnum(str, enum.Enum):
    """AI classification categories for incoming queries"""

    SCHEDULE = "schedule"
    GENERAL = "general"
    TECHNICAL = "technical"
    OUT_OF_CONTEXT = "out_of_context"
    SCHEDULE_UPDATES = "schedule_updates"


class ExamTermEnum(str, enum.Enum):
    """Specific exam terms"""

    FIRST = "first"
    SECOND = "second"
    SPECIAL = "special"


# --- Database Tables ---


class Room(Base):
    """Physical campus locations"""

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    capacity: Mapped[Optional[int]] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Soft delete flag

    # Relationships
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="room")
    exams: Mapped[List["Exam"]] = relationship(back_populates="room")


class Course(Base):
    """Academic course information and faculty data"""

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    lecturer_name: Mapped[str] = mapped_column(String(100), index=True)
    lecturer_email: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="course")
    exams: Mapped[List["Exam"]] = relationship(back_populates="course")


class Schedule(Base):
    """Recurring weekly class schedule mapping courses to rooms"""

    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    day_of_week: Mapped[str] = mapped_column(String(20), index=True)
    start_time: Mapped[time] = mapped_column()
    end_time: Mapped[time] = mapped_column()

    __table_args__ = (
        UniqueConstraint("room_id", "day_of_week", "start_time", name="uix_room_time"),
    )
    # Relationships
    course: Mapped["Course"] = relationship(back_populates="schedules")
    room: Mapped["Room"] = relationship(back_populates="schedules")


class Exam(Base):
    """Final examination schedule with specific dates and terms"""

    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    exam_date: Mapped[date] = mapped_column(Date, index=True)
    start_time: Mapped[time] = mapped_column()
    end_time: Mapped[time] = mapped_column()
    term: Mapped[ExamTermEnum] = mapped_column(Enum(ExamTermEnum), nullable=False)

    # Relationships
    course: Mapped["Course"] = relationship(back_populates="exams")
    room: Mapped["Room"] = relationship(back_populates="exams")


class KnowledgeBase(Base):
    """Unstructured data for FAQ, technical support, and dynamic updates"""

    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum), index=True)
    topic_or_question: Mapped[str] = mapped_column(String(255), index=True)
    content_or_answer: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class InteractionLog(Base):
    """Audit log for AI performance monitoring and analytics"""

    __tablename__ = "interaction_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_question: Mapped[str] = mapped_column(Text)
    ai_classification: Mapped[Optional[CategoryEnum]] = mapped_column(
        Enum(CategoryEnum)
    )
    ai_answer: Mapped[Optional[str]] = mapped_column(Text)
    was_fallback: Mapped[bool] = mapped_column(Boolean, default=False)
    processing_time_ms: Mapped[Optional[int]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


# =======================================================
# Future Features Placeholder (Won't Have in Current MVP)
# =======================================================

# class Student(Base):
#     """Placeholder for future student personal area"""
#     __tablename__ = "students"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     student_number: Mapped[str] = mapped_column(String(20), unique=True)
#     full_name: Mapped[str] = mapped_column(String(100))

# class Enrollment(Base):
#     """Placeholder for course registrations and grades"""
#     __tablename__ = "enrollments"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
#     course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
#     final_grade: Mapped[Optional[int]] = mapped_column()
