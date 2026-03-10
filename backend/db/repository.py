import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from db.models import CategoryEnum, Exam, KnowledgeBase, Schedule, InteractionLog

logger = logging.getLogger(__name__)


async def get_campus_context(session: AsyncSession, category: CategoryEnum) -> str:
    """
    Retrieves and formats context from the database based on the AI's classification.
    """
    try:
        if category == CategoryEnum.SCHEDULE:
            combined_context = []
            # 1. Fetch Dynamic Updates (High Priority)
            updates_query = select(KnowledgeBase).where(
                KnowledgeBase.category == CategoryEnum.SCHEDULE_UPDATES,
                KnowledgeBase.is_active == True,
            )
            updates_result = await session.execute(updates_query)
            updates = updates_result.scalars().all()

            if updates:
                updates_text = "\n".join(
                    [
                        f"IMPORTANT UPDATE - {u.topic_or_question}: {u.content_or_answer}"
                        for u in updates
                    ]
                )
                combined_context.append(f"--- ACTIVE UPDATES ---\n{updates_text}")

            # 2. Fetch Regular Weekly Schedule
            schedule_query = (
                select(Schedule)
                .options(joinedload(Schedule.course), joinedload(Schedule.room))
                .limit(10)
            )
            schedule_result = await session.execute(schedule_query)
            schedules = schedule_result.scalars().all()

            if schedules:
                schedule_text = "\n".join(
                    [
                        f"Class: {s.course.name}, Lecturer: {s.course.lecturer_name}, "
                        f"Day: {s.day_of_week}, Time: {s.start_time}-{s.end_time}, Room: {s.room.name}"
                        for s in schedules
                    ]
                )
                combined_context.append(f"--- REGULAR SCHEDULE ---\n{schedule_text}")

            # 3. Fetch Exams
            exam_query = (
                select(Exam)
                .options(joinedload(Exam.course), joinedload(Exam.room))
                .limit(10)
            )
            exam_result = await session.execute(exam_query)
            exams = exam_result.scalars().all()

            if exams:
                exam_text = "\n".join(
                    [
                        f"Exam: {e.course.name}, Date: {e.exam_date}, "
                        f"Time: {e.start_time}-{e.end_time}, Room: {e.room.name}, Term: {e.term.value}"
                        for e in exams
                    ]
                )
                combined_context.append(f"--- EXAMS ---\n{exam_text}")
            return "\n\n".join(combined_context) if combined_context else ""

        elif category in (CategoryEnum.GENERAL, CategoryEnum.TECHNICAL):
            kb_query = (
                select(KnowledgeBase)
                .where(
                    KnowledgeBase.category == category, KnowledgeBase.is_active == True
                )
                .limit(10)
            )
            kb_result = await session.execute(kb_query)
            kb_items = kb_result.scalars().all()

            if not kb_items:
                return ""

            lines = [
                f"{item.topic_or_question}: {item.content_or_answer}"
                for item in kb_items
            ]
            return "\n".join(lines)

        return ""

    except Exception as e:
        logger.error(f"❌ DB Query Error for category {category.name}: {str(e)}")
        # Return empty string to trigger the LLM Fallback safely
        return ""


async def save_interaction_log(
    db: AsyncSession, question: str, answer: str, category: str, process_time_ms: int
) -> None:
    """
    Saves interaction log to the database in the background.
    This function should be called asynchronously to avoid blocking the user response.
    """
    try:
        # Convert category string to CategoryEnum if needed
        if isinstance(category, str):
            try:
                category_enum = CategoryEnum(category.lower())
            except ValueError:
                logger.warning(f"Invalid category '{category}', defaulting to GENERAL")
                category_enum = CategoryEnum.GENERAL
        else:
            category_enum = category

        # Detect fallback responses (Hebrew keywords)
        is_fallback = any(
            keyword in answer
            for keyword in ["מצטער", "שגיאה", "לא קיים", "לא נמצא", "אינו זמין"]
        )

        log_entry = InteractionLog(
            student_question=question,
            ai_classification=category_enum,
            ai_answer=answer,
            was_fallback=is_fallback,
            processing_time_ms=process_time_ms,
        )

        db.add(log_entry)
        await db.commit()
        logger.debug(
            f"✅ Interaction log saved: {category_enum.name} ({process_time_ms}ms)"
        )

    except Exception as e:
        logger.error(f"❌ Failed to save interaction log: {e}")
        await db.rollback()
        # Don't raise - logging failures shouldn't break the API
