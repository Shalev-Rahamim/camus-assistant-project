import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import time, date

from db.models import (
    Base,
    Room,
    Course,
    Schedule,
    Exam,
    KnowledgeBase,
    CategoryEnum,
    ExamTermEnum,
)


# In-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Creates a fresh database session for each test.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def test_data(db_session):
    """
    Creates comprehensive test data for testing.
    """
    # Create rooms
    rooms_data = [
        Room(name="Hall 101 - Engineering", capacity=150),
        Room(name="Hall 102 - Engineering", capacity=150),
        Room(name="Computer Lab A", capacity=35),
        Room(name="Main Auditorium", capacity=300),
        Room(name="Library - Study Room 1", capacity=10),
        Room(name="Social Sciences Building - Room 301", capacity=60),
    ]
    db_session.add_all(rooms_data)
    await db_session.flush()

    # Create courses
    courses_data = [
        Course(name="Data Structures and Algorithms", lecturer_name="Prof. David Levi"),
        Course(name="Artificial Intelligence", lecturer_name="Dr. Sarah Cohen"),
        Course(name="Operating Systems", lecturer_name="Prof. Haim Mizrahi"),
        Course(name="Web Systems Development", lecturer_name="Mr. Avi Israeli"),
    ]
    db_session.add_all(courses_data)
    await db_session.flush()

    # Create schedules
    schedules_data = [
        Schedule(
            course_id=courses_data[0].id,
            room_id=rooms_data[0].id,
            day_of_week="Sunday",
            start_time=time(10, 0),
            end_time=time(12, 0),
        ),
        Schedule(
            course_id=courses_data[1].id,
            room_id=rooms_data[3].id,
            day_of_week="Monday",
            start_time=time(14, 0),
            end_time=time(16, 0),
        ),
    ]
    db_session.add_all(schedules_data)
    await db_session.flush()

    # Create exams
    exams_data = [
        Exam(
            course_id=courses_data[0].id,
            room_id=rooms_data[0].id,
            exam_date=date(2025, 6, 20),
            start_time=time(10, 0),
            end_time=time(12, 0),
            term=ExamTermEnum.FIRST,
        ),
    ]
    db_session.add_all(exams_data)
    await db_session.flush()

    # Create knowledge base entries
    kb_items_data = [
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="Office Hours",
            content_or_answer="The office is open Sunday-Thursday between 09:00 and 14:00.",
        ),
        KnowledgeBase(
            category=CategoryEnum.TECHNICAL,
            topic_or_question="Moodle Password Reset",
            content_or_answer="Go to the main page and click on 'Forgot Password'.",
        ),
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="Cafeteria Location",
            content_or_answer="The main cafeteria is located on the ground floor of the Social Sciences Building.",
        ),
        KnowledgeBase(
            category=CategoryEnum.SCHEDULE,
            topic_or_question="Grade Publication",
            content_or_answer="Grades are published within 14 business days from the exam date.",
        ),
    ]
    db_session.add_all(kb_items_data)
    await db_session.commit()

    return {
        "rooms": rooms_data,
        "courses": courses_data,
        "schedules": schedules_data,
        "exams": exams_data,
        "knowledge_base": kb_items_data,
    }
