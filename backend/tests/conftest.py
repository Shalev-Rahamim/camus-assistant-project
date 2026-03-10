"""
Pytest fixtures for database testing.
Provides test database session and test data setup.
"""

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
    Creates minimal test data for basic tests (kept for backward compatibility).
    """
    # Create rooms
    room1 = Room(name="אולם 101 - הנדסה", capacity=150)
    room2 = Room(name="אולם 102 - הנדסה", capacity=150)
    room3 = Room(name="מעבדת מחשבים A", capacity=35)
    db_session.add_all([room1, room2, room3])
    await db_session.flush()

    # Create courses
    course1 = Course(name="מבני נתונים ואלגוריתמים", lecturer_name="פרופ' דוד לוי")
    course2 = Course(name="בינה מלאכותית", lecturer_name='ד"ר שרה כהן')
    course3 = Course(name="מערכות הפעלה", lecturer_name="פרופ' חיים מזרחי")
    db_session.add_all([course1, course2, course3])
    await db_session.flush()

    # Create schedules
    schedule1 = Schedule(
        course_id=course1.id,
        room_id=room1.id,
        day_of_week="ראשון",
        start_time=time(10, 0),
        end_time=time(12, 0),
    )
    schedule2 = Schedule(
        course_id=course2.id,
        room_id=room2.id,
        day_of_week="שני",
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    db_session.add_all([schedule1, schedule2])
    await db_session.flush()

    # Create exams
    exam1 = Exam(
        course_id=course1.id,
        room_id=room1.id,
        exam_date=date(2025, 1, 20),
        start_time=time(10, 0),
        end_time=time(12, 0),
        term=ExamTermEnum.FIRST,
    )
    exam2 = Exam(
        course_id=course2.id,
        room_id=room2.id,
        exam_date=date(2025, 2, 15),
        start_time=time(14, 0),
        end_time=time(16, 0),
        term=ExamTermEnum.FIRST,
    )
    db_session.add_all([exam1, exam2])
    await db_session.flush()

    # Create knowledge base entries
    kb1 = KnowledgeBase(
        category=CategoryEnum.GENERAL,
        topic_or_question="שעות קבלת קהל",
        content_or_answer="המזכירות פתוחה בימים א'-ה' בין 09:00 ל-14:00.",
    )
    kb2 = KnowledgeBase(
        category=CategoryEnum.TECHNICAL,
        topic_or_question="איפוס סיסמה למודל",
        content_or_answer="יש להיכנס לעמוד הראשי וללחוץ על 'שכחתי סיסמה'.",
    )
    kb3 = KnowledgeBase(
        category=CategoryEnum.GENERAL,
        topic_or_question="מיקום הקפיטריה",
        content_or_answer="הקפיטריה המרכזית נמצאת בקומת הקרקע של בניין מדעי החברה.",
    )
    db_session.add_all([kb1, kb2, kb3])
    await db_session.commit()

    return {
        "rooms": [room1, room2, room3],
        "courses": [course1, course2, course3],
        "schedules": [schedule1, schedule2],
        "exams": [exam1, exam2],
        "knowledge_base": [kb1, kb2, kb3],
    }


@pytest_asyncio.fixture(scope="function")
async def large_test_data(db_session):
    """
    Creates extensive test data for comprehensive accuracy testing.
    This fixture provides a realistic dataset similar to production.
    """
    # ==========================================
    # 1. Create 10 Campus Rooms
    # ==========================================
    rooms_data = [
        Room(name="אולם 101 - הנדסה", capacity=150),
        Room(name="אולם 102 - הנדסה", capacity=150),
        Room(name="מעבדת מחשבים A", capacity=35),
        Room(name="מעבדת מחשבים B", capacity=35),
        Room(name="כיתת סמינר 201", capacity=25),
        Room(name="כיתת סמינר 202", capacity=25),
        Room(name="אודיטוריום מרכזי", capacity=300),
        Room(name="ספרייה - חדר למידה 1", capacity=10),
        Room(name="בניין מדעי החברה - כיתה 301", capacity=60),
        Room(name="מעבדת סייבר ומערכות", capacity=40),
    ]
    db_session.add_all(rooms_data)
    await db_session.flush()

    # ==========================================
    # 2. Create 10 Academic Courses
    # ==========================================
    courses_data = [
        Course(name="מבני נתונים ואלגוריתמים", lecturer_name="פרופ' דוד לוי"),
        Course(name="בינה מלאכותית", lecturer_name='ד"ר שרה כהן'),
        Course(name="פיתוח מערכות Web", lecturer_name="מר אבי ישראלי"),
        Course(name="מבוא לסייבר ואבטחת מידע", lecturer_name='ד"ר רונית אברהם'),
        Course(name="מערכות הפעלה", lecturer_name="פרופ' חיים מזרחי"),
        Course(name="מסדי נתונים רלציוניים", lecturer_name='ד"ר יעל גולן'),
        Course(name="תכנות מונחה עצמים", lecturer_name="מר תומר גבאי"),
        Course(name="רשתות תקשורת", lecturer_name='ד"ר אילן רוזן'),
        Course(name="מתמטיקה בדידה", lecturer_name="פרופ' אליעזר שטרן"),
        Course(name="אתיקה מקצועית בהייטק", lecturer_name='ד"ר מיכל ברק'),
    ]
    db_session.add_all(courses_data)
    await db_session.flush()

    # ==========================================
    # 3. Create 12 Weekly Academic Schedules
    # ==========================================
    schedules_data = [
        # ראשון
        Schedule(
            course_id=courses_data[0].id,
            room_id=rooms_data[0].id,
            day_of_week="ראשון",
            start_time=time(8, 0),
            end_time=time(11, 0),
        ),
        Schedule(
            course_id=courses_data[1].id,
            room_id=rooms_data[6].id,
            day_of_week="ראשון",
            start_time=time(12, 0),
            end_time=time(15, 0),
        ),
        Schedule(
            course_id=courses_data[4].id,
            room_id=rooms_data[2].id,
            day_of_week="ראשון",
            start_time=time(16, 0),
            end_time=time(19, 0),
        ),
        # שני
        Schedule(
            course_id=courses_data[2].id,
            room_id=rooms_data[3].id,
            day_of_week="שני",
            start_time=time(9, 0),
            end_time=time(12, 0),
        ),
        Schedule(
            course_id=courses_data[5].id,
            room_id=rooms_data[8].id,
            day_of_week="שני",
            start_time=time(13, 0),
            end_time=time(16, 0),
        ),
        # שלישי
        Schedule(
            course_id=courses_data[3].id,
            room_id=rooms_data[9].id,
            day_of_week="שלישי",
            start_time=time(10, 0),
            end_time=time(13, 0),
        ),
        Schedule(
            course_id=courses_data[6].id,
            room_id=rooms_data[2].id,
            day_of_week="שלישי",
            start_time=time(14, 0),
            end_time=time(17, 0),
        ),
        # רביעי
        Schedule(
            course_id=courses_data[7].id,
            room_id=rooms_data[1].id,
            day_of_week="רביעי",
            start_time=time(8, 30),
            end_time=time(11, 30),
        ),
        Schedule(
            course_id=courses_data[8].id,
            room_id=rooms_data[6].id,
            day_of_week="רביעי",
            start_time=time(12, 0),
            end_time=time(15, 0),
        ),
        # חמישי
        Schedule(
            course_id=courses_data[9].id,
            room_id=rooms_data[4].id,
            day_of_week="חמישי",
            start_time=time(16, 0),
            end_time=time(18, 0),
        ),
        Schedule(
            course_id=courses_data[0].id,
            room_id=rooms_data[0].id,
            day_of_week="חמישי",
            start_time=time(10, 0),
            end_time=time(12, 0),
        ),
        Schedule(
            course_id=courses_data[5].id,
            room_id=rooms_data[5].id,
            day_of_week="חמישי",
            start_time=time(14, 0),
            end_time=time(16, 0),
        ),
    ]
    db_session.add_all(schedules_data)
    await db_session.flush()

    # ==========================================
    # 4. Create 10 Exam Records
    # ==========================================
    exams_data = [
        Exam(
            course_id=courses_data[0].id,
            room_id=rooms_data[6].id,
            exam_date=date(2025, 6, 20),
            start_time=time(9, 0),
            end_time=time(12, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[1].id,
            room_id=rooms_data[0].id,
            exam_date=date(2025, 6, 23),
            start_time=time(9, 0),
            end_time=time(12, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[2].id,
            room_id=rooms_data[2].id,
            exam_date=date(2025, 6, 27),
            start_time=time(14, 0),
            end_time=time(17, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[3].id,
            room_id=rooms_data[9].id,
            exam_date=date(2025, 7, 1),
            start_time=time(9, 0),
            end_time=time(12, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[4].id,
            room_id=rooms_data[3].id,
            exam_date=date(2025, 7, 5),
            start_time=time(14, 0),
            end_time=time(17, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[5].id,
            room_id=rooms_data[8].id,
            exam_date=date(2025, 7, 9),
            start_time=time(13, 0),
            end_time=time(16, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[6].id,
            room_id=rooms_data[3].id,
            exam_date=date(2025, 7, 13),
            start_time=time(9, 0),
            end_time=time(12, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[7].id,
            room_id=rooms_data[0].id,
            exam_date=date(2025, 7, 17),
            start_time=time(14, 0),
            end_time=time(17, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[8].id,
            room_id=rooms_data[6].id,
            exam_date=date(2025, 7, 21),
            start_time=time(9, 0),
            end_time=time(13, 0),
            term=ExamTermEnum.FIRST,
        ),
        Exam(
            course_id=courses_data[9].id,
            room_id=rooms_data[4].id,
            exam_date=date(2025, 7, 25),
            start_time=time(16, 0),
            end_time=time(18, 0),
            term=ExamTermEnum.FIRST,
        ),
    ]
    db_session.add_all(exams_data)
    await db_session.flush()

    # ==========================================
    # 5. Create 12 Knowledge Base Entries
    # ==========================================
    kb_items_data = [
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="שעות קבלת קהל",
            content_or_answer="המזכירות פתוחה בימים א'-ה' בין 09:00 ל-14:00.",
        ),
        KnowledgeBase(
            category=CategoryEnum.TECHNICAL,
            topic_or_question="איפוס סיסמה למודל",
            content_or_answer="יש להיכנס לעמוד הראשי וללחוץ על 'שכחתי סיסמה'.",
        ),
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="מיקום הקפיטריה",
            content_or_answer="הקפיטריה המרכזית נמצאת בקומת הקרקע של בניין מדעי החברה.",
        ),
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="שעות פתיחת הספרייה",
            content_or_answer="הספרייה פתוחה בימים א'-ה' בין 08:00 ל-20:00, ובימי ו' בין 09:00 ל-13:00.",
        ),
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="מלגות הצטיינות",
            content_or_answer="ניתן להגיש בקשה למלגת הצטיינות עד 15.3 בכל שנה. יש לפנות למזכירות הסטודנטים.",
        ),
        KnowledgeBase(
            category=CategoryEnum.TECHNICAL,
            topic_or_question="חיבור ל-WiFi",
            content_or_answer="שם הרשת: Campus-WiFi, סיסמה: Student2025. אם יש בעיה, פנה למחלקת IT.",
        ),
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="חניה בקמפוס",
            content_or_answer='חניה זמינה בחניון המרכזי. עלות: 10 ש"ח ליום או 200 ש"ח לחודש.',
        ),
        KnowledgeBase(
            category=CategoryEnum.TECHNICAL,
            topic_or_question="מקרן לא עובד",
            content_or_answer="אם המקרן בכיתה לא עובד, יש לדווח למזכירות או למחלקת IT בטלפון 1234.",
        ),
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="הדפסה בקמפוס",
            content_or_answer='ניתן להדפיס בספרייה או במעבדת המחשבים. עלות: 0.5 ש"ח לעמוד.',
        ),
        KnowledgeBase(
            category=CategoryEnum.SCHEDULE,
            topic_or_question="פרסום ציונים",
            content_or_answer="ציונים מפורסמים תוך 14 ימי עסקים ממועד הבחינה.",
        ),
        KnowledgeBase(
            category=CategoryEnum.GENERAL,
            topic_or_question="ביטול קורס",
            content_or_answer='ניתן לבטל קורס עד שבועיים מתחילת הסמסטר ללא קנס. לאחר מכן יש קנס של 200 ש"ח.',
        ),
        KnowledgeBase(
            category=CategoryEnum.TECHNICAL,
            topic_or_question="גישה לשרתי המעבדה",
            content_or_answer="גישה לשרתי המעבדה דרך VPN. הורד את התוכנה מאתר המחלקה והתחבר עם פרטי הסטודנט.",
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
