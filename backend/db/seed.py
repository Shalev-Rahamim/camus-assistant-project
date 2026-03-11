import asyncio
from datetime import time, date
from sqlalchemy import select
from db import (
    async_session_maker,
    init_db,
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
    Seeds the database with extensive campus data including rooms, courses,
    schedules, exams, and knowledge base entries in English for RAG compatibility.
    Deletes existing data before seeding to ensure clean state.
    """
    # Ensure tables are created before seeding
    await init_db()

    async with async_session_maker() as session:
        async with session.begin():
            print("Starting comprehensive data seeding (English Content)...")

            # Delete existing data to avoid conflicts
            print("Clearing existing data...")
            kb_result = await session.execute(select(KnowledgeBase))
            for kb in kb_result.scalars().all():
                await session.delete(kb)

            exam_result = await session.execute(select(Exam))
            for exam in exam_result.scalars().all():
                await session.delete(exam)

            schedule_result = await session.execute(select(Schedule))
            for schedule in schedule_result.scalars().all():
                await session.delete(schedule)

            course_result = await session.execute(select(Course))
            for course in course_result.scalars().all():
                await session.delete(course)

            room_result = await session.execute(select(Room))
            for room in room_result.scalars().all():
                await session.delete(room)

            await session.flush()
            print("Existing data cleared. Creating new data...")

            # ==========================================
            # 1. Create Campus Rooms (20 rooms)
            # ==========================================
            rooms_data = [
                Room(name="Hall 101 - Engineering", capacity=150),
                Room(name="Hall 102 - Engineering", capacity=150),
                Room(name="Hall 103 - Engineering", capacity=120),
                Room(name="Hall 201 - Sciences", capacity=200),
                Room(name="Hall 202 - Sciences", capacity=180),
                Room(name="Computer Lab A", capacity=35),
                Room(name="Computer Lab B", capacity=35),
                Room(name="Computer Lab C", capacity=40),
                Room(name="Seminar Room 201", capacity=25),
                Room(name="Seminar Room 202", capacity=25),
                Room(name="Seminar Room 301", capacity=30),
                Room(name="Main Auditorium", capacity=300),
                Room(name="Small Auditorium", capacity=150),
                Room(name="Library - Study Room 1", capacity=10),
                Room(name="Library - Study Room 2", capacity=12),
                Room(name="Library - Study Room 3", capacity=8),
                Room(name="Social Sciences Building - Room 301", capacity=60),
                Room(name="Social Sciences Building - Room 302", capacity=50),
                Room(name="Cybersecurity and Systems Lab", capacity=40),
                Room(name="Networking Lab", capacity=30),
            ]
            session.add_all(rooms_data)
            await session.flush()

            # ==========================================
            # 2. Create Academic Courses (20 courses)
            # ==========================================
            courses_data = [
                Course(
                    name="Data Structures and Algorithms",
                    lecturer_name="Prof. David Levi",
                ),
                Course(name="Artificial Intelligence", lecturer_name="Dr. Sarah Cohen"),
                Course(name="Web Systems Development", lecturer_name="Mr. Avi Israeli"),
                Course(
                    name="Introduction to Cybersecurity and Information Security",
                    lecturer_name="Dr. Ronit Avraham",
                ),
                Course(name="Operating Systems", lecturer_name="Prof. Haim Mizrahi"),
                Course(name="Relational Databases", lecturer_name="Dr. Yael Golan"),
                Course(
                    name="Object-Oriented Programming", lecturer_name="Mr. Tomer Gabai"
                ),
                Course(name="Communication Networks", lecturer_name="Dr. Ilan Rosen"),
                Course(
                    name="Discrete Mathematics", lecturer_name="Prof. Eliezer Stern"
                ),
                Course(
                    name="Professional Ethics in High-Tech",
                    lecturer_name="Dr. Michal Barak",
                ),
                Course(
                    name="Machine Learning Fundamentals",
                    lecturer_name="Dr. Rachel Cohen",
                ),
                Course(name="Software Engineering", lecturer_name="Prof. Yossi Katz"),
                Course(name="Computer Graphics", lecturer_name="Dr. Maya Schwartz"),
                Course(
                    name="Distributed Systems", lecturer_name="Prof. Amir Ben-David"
                ),
                Course(
                    name="Mobile Application Development",
                    lecturer_name="Dr. Tal Friedman",
                ),
                Course(name="Cloud Computing", lecturer_name="Prof. Noam Weiss"),
                Course(
                    name="Information Systems Analysis",
                    lecturer_name="Dr. Lior Shalom",
                ),
                Course(
                    name="Human-Computer Interaction",
                    lecturer_name="Dr. Dana Levy",
                ),
                Course(name="Advanced Algorithms", lecturer_name="Prof. Ron Keren"),
                Course(
                    name="Data Mining and Big Data",
                    lecturer_name="Dr. Orit Shapira",
                ),
            ]
            session.add_all(courses_data)
            await session.flush()

            # ==========================================
            # 3. Create Weekly Academic Schedules (30+ schedules)
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
                    room_id=rooms_data[11].id,
                    day_of_week="Sunday",
                    start_time=time(12, 0),
                    end_time=time(15, 0),
                ),
                Schedule(
                    course_id=courses_data[4].id,
                    room_id=rooms_data[5].id,
                    day_of_week="Sunday",
                    start_time=time(16, 0),
                    end_time=time(19, 0),
                ),
                Schedule(
                    course_id=courses_data[10].id,
                    room_id=rooms_data[1].id,
                    day_of_week="Sunday",
                    start_time=time(10, 0),
                    end_time=time(13, 0),
                ),
                # Monday
                Schedule(
                    course_id=courses_data[2].id,
                    room_id=rooms_data[6].id,
                    day_of_week="Monday",
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                ),
                Schedule(
                    course_id=courses_data[5].id,
                    room_id=rooms_data[16].id,
                    day_of_week="Monday",
                    start_time=time(13, 0),
                    end_time=time(16, 0),
                ),
                Schedule(
                    course_id=courses_data[11].id,
                    room_id=rooms_data[2].id,
                    day_of_week="Monday",
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                ),
                Schedule(
                    course_id=courses_data[14].id,
                    room_id=rooms_data[7].id,
                    day_of_week="Monday",
                    start_time=time(10, 0),
                    end_time=time(13, 0),
                ),
                # Tuesday
                Schedule(
                    course_id=courses_data[3].id,
                    room_id=rooms_data[18].id,
                    day_of_week="Tuesday",
                    start_time=time(10, 0),
                    end_time=time(13, 0),
                ),
                Schedule(
                    course_id=courses_data[6].id,
                    room_id=rooms_data[5].id,
                    day_of_week="Tuesday",
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                ),
                Schedule(
                    course_id=courses_data[12].id,
                    room_id=rooms_data[3].id,
                    day_of_week="Tuesday",
                    start_time=time(8, 30),
                    end_time=time(11, 30),
                ),
                Schedule(
                    course_id=courses_data[15].id,
                    room_id=rooms_data[19].id,
                    day_of_week="Tuesday",
                    start_time=time(16, 0),
                    end_time=time(19, 0),
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
                    room_id=rooms_data[11].id,
                    day_of_week="Wednesday",
                    start_time=time(12, 0),
                    end_time=time(15, 0),
                ),
                Schedule(
                    course_id=courses_data[13].id,
                    room_id=rooms_data[4].id,
                    day_of_week="Wednesday",
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                ),
                Schedule(
                    course_id=courses_data[16].id,
                    room_id=rooms_data[17].id,
                    day_of_week="Wednesday",
                    start_time=time(13, 0),
                    end_time=time(16, 0),
                ),
                # Thursday
                Schedule(
                    course_id=courses_data[9].id,
                    room_id=rooms_data[8].id,
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
                Schedule(
                    course_id=courses_data[5].id,
                    room_id=rooms_data[9].id,
                    day_of_week="Thursday",
                    start_time=time(14, 0),
                    end_time=time(16, 0),
                ),
                Schedule(
                    course_id=courses_data[17].id,
                    room_id=rooms_data[10].id,
                    day_of_week="Thursday",
                    start_time=time(8, 0),
                    end_time=time(11, 0),
                ),
                Schedule(
                    course_id=courses_data[18].id,
                    room_id=rooms_data[12].id,
                    day_of_week="Thursday",
                    start_time=time(12, 0),
                    end_time=time(15, 0),
                ),
                Schedule(
                    course_id=courses_data[19].id,
                    room_id=rooms_data[6].id,
                    day_of_week="Thursday",
                    start_time=time(16, 0),
                    end_time=time(19, 0),
                ),
            ]
            session.add_all(schedules_data)
            await session.flush()

            # ==========================================
            # 4. Create Exam Records (20 exams)
            # ==========================================
            exams_data = [
                Exam(
                    course_id=courses_data[0].id,
                    room_id=rooms_data[11].id,
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
                    room_id=rooms_data[5].id,
                    exam_date=date(2026, 6, 27),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[3].id,
                    room_id=rooms_data[18].id,
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
                    room_id=rooms_data[16].id,
                    exam_date=date(2026, 7, 9),
                    start_time=time(13, 0),
                    end_time=time(16, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[6].id,
                    room_id=rooms_data[6].id,
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
                    room_id=rooms_data[11].id,
                    exam_date=date(2026, 7, 21),
                    start_time=time(9, 0),
                    end_time=time(13, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[9].id,
                    room_id=rooms_data[8].id,
                    exam_date=date(2026, 7, 25),
                    start_time=time(16, 0),
                    end_time=time(18, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[10].id,
                    room_id=rooms_data[1].id,
                    exam_date=date(2026, 6, 22),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[11].id,
                    room_id=rooms_data[2].id,
                    exam_date=date(2026, 6, 26),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[12].id,
                    room_id=rooms_data[3].id,
                    exam_date=date(2026, 6, 30),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[13].id,
                    room_id=rooms_data[4].id,
                    exam_date=date(2026, 7, 4),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[14].id,
                    room_id=rooms_data[7].id,
                    exam_date=date(2026, 7, 8),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[15].id,
                    room_id=rooms_data[19].id,
                    exam_date=date(2026, 7, 12),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[16].id,
                    room_id=rooms_data[17].id,
                    exam_date=date(2026, 7, 16),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[17].id,
                    room_id=rooms_data[10].id,
                    exam_date=date(2026, 7, 20),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[18].id,
                    room_id=rooms_data[12].id,
                    exam_date=date(2026, 7, 24),
                    start_time=time(9, 0),
                    end_time=time(12, 0),
                    term=ExamTermEnum.FIRST,
                ),
                Exam(
                    course_id=courses_data[19].id,
                    room_id=rooms_data[6].id,
                    exam_date=date(2026, 7, 28),
                    start_time=time(14, 0),
                    end_time=time(17, 0),
                    term=ExamTermEnum.FIRST,
                ),
            ]
            session.add_all(exams_data)

            # ==========================================
            # 5. Populate Knowledge Base (20+ entries)
            # ==========================================
            kb_items_data = [
                # GENERAL Category
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Office Hours",
                    content_or_answer="The office is open Sunday-Thursday between 09:00 and 14:00. For urgent matters, contact the student services hotline at extension 1234.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Cafeteria Location",
                    content_or_answer="The main cafeteria is located on the ground floor of the Social Sciences Building. It serves hot meals, sandwiches, and beverages from 08:00 to 18:00.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Library Opening Hours",
                    content_or_answer="The library is open Sunday-Thursday between 08:00 and 20:00, and on Fridays between 09:00 and 13:00. Study rooms can be reserved online.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Excellence Scholarships",
                    content_or_answer="You can apply for an excellence scholarship until March 15th each year. Contact the student office for application forms and requirements. Minimum GPA of 85 required.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Campus Parking",
                    content_or_answer="Parking is available in the main parking lot. Cost: 10 NIS per day or 200 NIS per month. Student parking permits can be purchased at the security office.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Course Cancellation",
                    content_or_answer="You can cancel a course up to two weeks from the start of the semester without a fine. After that, there is a fine of 200 NIS. Cancellation forms are available online.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Student ID Card",
                    content_or_answer="Student ID cards can be obtained at the student services office. Bring a passport photo and your acceptance letter. Processing takes 3-5 business days.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Academic Calendar",
                    content_or_answer="The academic year runs from October to June. First semester: October-January, Second semester: February-June. Check the website for exact dates and holidays.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Dormitory Information",
                    content_or_answer="On-campus dormitories are available for first-year students. Applications open in August. Contact the housing office for availability and pricing.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.GENERAL,
                    topic_or_question="Printing on Campus",
                    content_or_answer="You can print at the library or computer labs. Cost: 0.5 NIS per page for black and white, 2 NIS per page for color. Payment via student card or cash.",
                ),
                # TECHNICAL Category
                KnowledgeBase(
                    category=CategoryEnum.TECHNICAL,
                    topic_or_question="Moodle Password Reset",
                    content_or_answer="Go to the main Moodle page and click on 'Forgot Password'. Enter your student ID and email. A reset link will be sent to your registered email address.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.TECHNICAL,
                    topic_or_question="WiFi Connection",
                    content_or_answer="Network name: Campus-WiFi, Password: Student2025. If you have connection issues, contact the IT department at extension 5678 or visit room 205 in the Engineering building.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.TECHNICAL,
                    topic_or_question="Projector Not Working",
                    content_or_answer="If the projector in the classroom is not working, report to the office or IT department at phone 1234. Include the room number and time of the issue.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.TECHNICAL,
                    topic_or_question="Lab Server Access",
                    content_or_answer="Access to lab servers via VPN. Download the VPN software from the department website and connect with your student credentials. Support available at lab@university.edu.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.TECHNICAL,
                    topic_or_question="Computer Lab Software",
                    content_or_answer="Computer labs have all required software installed including IDEs, databases, and development tools. If specific software is needed, request it through the IT department at least one week in advance.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.TECHNICAL,
                    topic_or_question="Email Account Setup",
                    content_or_answer="Student email accounts are created automatically upon enrollment. Format: firstname.lastname@student.university.edu. Access via webmail or configure in your email client using IMAP settings.",
                ),
                # SCHEDULE Category
                KnowledgeBase(
                    category=CategoryEnum.SCHEDULE,
                    topic_or_question="Grade Publication",
                    content_or_answer="Grades are published within 14 business days from the exam date. Check your student portal or Moodle. For grade disputes, contact the course lecturer within 7 days of publication.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.SCHEDULE,
                    topic_or_question="Exam Schedule Changes",
                    content_or_answer="Exam schedule changes are posted on the notice board and sent via email. Check your student email regularly. For conflicts, contact the academic office immediately.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.SCHEDULE,
                    topic_or_question="Course Registration",
                    content_or_answer="Course registration opens two weeks before the semester starts. Register online through the student portal. Late registration incurs a 100 NIS fee.",
                ),
                KnowledgeBase(
                    category=CategoryEnum.SCHEDULE,
                    topic_or_question="Make-up Exams",
                    content_or_answer="Make-up exams are available for students with valid excuses (medical, military, etc.). Submit documentation to the academic office within 48 hours of the original exam date.",
                ),
            ]
            session.add_all(kb_items_data)

        print(
            "Database successfully seeded with 20 rooms, 20 courses, 22 schedules, 20 exams, and 20 knowledge base entries!"
        )


if __name__ == "__main__":
    # Standard entry point to execute the seed script
    asyncio.run(seed_data())
