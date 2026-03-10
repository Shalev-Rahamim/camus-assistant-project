import logging
from db.models import CategoryEnum
from ai.classifier import classify_question
from ai.prompt_manager import build_generation_prompt, BASE_SYSTEM_INSTRUCTION
from ai.llm_client import ask_llm
from db.repository import get_campus_context
from sqlalchemy.ext.asyncio import AsyncSession

# Initialize logger for tracking the RAG pipeline flow
logger = logging.getLogger(__name__)


async def process_campus_query(question: str, db: AsyncSession) -> dict:
    """
    Orchestrates the RAG (Retrieval-Augmented Generation) pipeline.
    Steps: Classification -> Retrieval -> Prompt Construction -> LLM Generation.
    """

    # 1. Classification: Identify the user's intent using the AI Classifier
    category = await classify_question(question)

    # Guardrail: Handle queries that are outside the defined campus scope
    if category == CategoryEnum.OUT_OF_CONTEXT:
        return {
            "answer": "אני עוזר קמפוס בלבד. במה אוכל לעזור בנושאי לימודים?",
            "category": category.name,
        }

    # 2. Retrieval: Fetch relevant organizational data based on the identified category
    context = await get_campus_context(db, category)

    # 3. Prompt Engineering: Combine question and context into a structured prompt
    prompt = build_generation_prompt(question, category, context)

    # Handle cases where no relevant information was found in the database (Fallback)
    if prompt == "FALLBACK_NO_INFO":
        answer = "מצטער, המידע לא קיים במאגר שלי."
    else:
        # 4. Generation: Request the final answer from the LLM client
        answer = await ask_llm(
            prompt=prompt, system_instruction=BASE_SYSTEM_INSTRUCTION
        )

        # Handle technical API failures or timeouts
        if answer == "FALLBACK_ERROR":
            answer = "שירות ה-AI אינו זמין כרגע, נסה שוב מאוחר יותר."
        elif "FALLBACK_NO_INFO" in answer:
            answer = "מצטער, המידע שחיפשת לא נמצא במערכת השעות או בנהלי הקמפוס."

    return {"answer": answer, "category": category.name}
