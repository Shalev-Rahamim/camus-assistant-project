import asyncio
from datetime import time, date
from sqlalchemy import select
from db.database import async_session_maker, init_db
from db.models import (
    Room,
    Course,
    Schedule,
    Exam,
    KnowledgeBase,
    CategoryEnum,
    ExamTermEnum,
)


async def seed_data():
    """
    Seeds the database with initial campus data including rooms, courses,
    schedules, exams, and knowledge base entries in Hebrew for RAG compatibility.
    """
    # Ensure tables are created before seeding
    await init_db()

    async with async_session_maker() as session:
        async with session.begin():
            # Check for existing data to prevent duplicate seeding
            existing_data = await session.execute(select(Course).limit(1))
            if existing_data.scalar_one_or_none():
                print("⚠️ Data already exists. Skipping seed.")
                return

            print("🌱 Starting extended data seeding (Hebrew Content)...")

            # ==========================================
            # 1. Create Campus Rooms
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
            session.add_all(rooms_data)
            # Flush to generate IDs for foreign key relationships
            await session.flush()

            # ==========================================
            # 2. Create Academic Courses
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
            session.add_all(courses_data)
            await session.flush()

            # ==========================================
            # 3. Create Weekly Academic Schedules
            # ==========================================
            schedules_data = [
                # Sunday
                Schedule(
                    course_id=courses_data[0].id,
                    room_id=rooms_data[0].id,
                    day_of_week="Sunday",
                    start_time=time(8, 0),
                    end_time=time(11, 0),
                ),
                Schedule(
                    course_id=courses_data[1].id,
                    room_id=rooms_data[6].id,
                    day_of_week="Sunday",
                    start_time=time(12, 0),
                    end_time=time(15, 0),
                ),
                Schedule(
                    course_id=courses_data[4].id,
                    room_id=rooms_data[2].id,
                    day_of_week="Sunday",
                    start_time=time(16, 0),
                    end_time=time(19, 0),
                ),
                # Monday
                Schedule(
                    course_id=courses_data[2].id,
                    room_id=rooms_data[3].id,
                    day_of_week="Monday",
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                ),
                Schedule(
                    course_id=courses_data[5].id,
                    room_id=rooms_data[8].id,
                    day_of_week="Monday",
                    start_time=time(13, 0),
                    end_time=time(16, 0),
                ),
                # Tuesday
                Schedule(
                    course_id=courses_data[3].id,
                    room_id=rooms_data[9].id,
                    day_of_week="Tuesday",
                    start_time=time(10, 0),
                    end_time=time(13, 0),
                ),
                Schedule(
                    course_id=courses_data[6].id,
                    room_id=rooms_data[2].id,
                    day_of_week="Tuesday",
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                ),
                # Wednesday
                Schedule(
                    course_id=courses_data[7].id,
                    room_id=rooms_data[1].id,
                    day_of_week="Wednesday",
                    start_time=time(8, 30),
                    end_time=time(11, 30),
                ),
                Schedule(
                    course_id=courses_data[8].id,
                    room_id=rooms_data[6].id,
                    day_of_week="Wednesday",
                    start_time=time(12, 0),
                    end_time=time(15, 0),
                ),
                # Thursday
                Schedule(
                    course_id=courses_data[9].id,
                    room_id=rooms_data[4].id,
                    day_of_week="Thursday",
                    start_time=time(16, 0),
                    end_time=time(18, 0),
                ),
                Schedule(
                    course_id=courses_data[0].id,
                    room_id=rooms_data[0].id,
                    day_of_week="Thursday",
                    start_time=time(10, 0),
                    end_time=time(12, 0),
                ),
            ]
            session.add_all(schedules_data)

            # ==========================================
            # 4. Create Exam Records
            # ==========================================
            exams_data = [
                Exam(
                    course_id=courses_data[0].id,
                    room_id=rooms_data[6].id,
                    exam_date=date(2026, 6, 20),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[1].id,
                    room_id=rooms_data[0].id,
                    exam_date=date(2026, 6, 23),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[2].id,
                    room_id=rooms_data[2].id,
                    exam_date=date(2026, 6, 27),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[3].id,
                    room_id=rooms_data[9].id,
                    exam_date=date(2026, 7, 1),
                    start_time=time(10, 0),
                    end_time=time(13, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[4].id,
                    room_id=rooms_data[1].id,
                    exam_date=date(2026, 7, 5),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[5].id,
                    room_id=rooms_data[8].id,
                    exam_date=date(2026, 7, 9),
                    start_time=time(13, 0),
                    end_time=time(16, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[6].id,
                    room_id=rooms_data[3].id,
                    exam_date=date(2026, 7, 13),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[7].id,
                    room_id=rooms_data[0].id,
                    exam_date=date(2026, 7, 17),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[8].id,
                    room_id=rooms_data[6].id,
                    exam_date=date(2026, 7, 21),
                    start_time=time(9, 0),
                    end_time=time(13, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[9].id,
                    room_id=rooms_data[4].id,
                    exam_date=date(2026, 7, 25),
                    start_time=time(16, 0),
                    end_time=time(18, 0),
                    term=ExamTermEnum.FIRST,
                ),
            ]
            session.add_all(exams_data)

            # ==========================================
            # 5. Populate Knowledge Base (Hebrew Content)
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
                    category=CategoryEnum.SCHEDULE,
                    topic_or_question="פרסום ציונים",
                    content_or_answer="ציונים מפורסמים תוך 14 ימי עסקים ממועד הבחינה.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="מיקום הקפיטריה",
                    content_or_answer="הקפיטריה המרכזית נמצאת בקומת הקרקע של בניין מדעי החברה.",
                ),
            ]
            session.add_all(kb_items_data)

        print(
            "✅ Database successfully seeded with rooms, courses, schedules, and exams!"
        )


if __name__ == "__main__":
    # Standard entry point to execute the seed script
    asyncio.run(seed_data())
